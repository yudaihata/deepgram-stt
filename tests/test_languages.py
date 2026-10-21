"""Regression tests for selectable Nova-3 languages and integration options."""

import asyncio
from contextlib import asynccontextmanager
from dataclasses import replace
import json
from unittest.mock import AsyncMock, MagicMock, patch
from urllib.parse import parse_qs, urlparse

from deepgram.core.events import EventType
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry
import voluptuous as vol

from custom_components.deepgram_stt.config_flow import STEP_USER_DATA_SCHEMA, ConfigFlow
from custom_components.deepgram_stt.const import (
    CONF_API_KEY,
    CONF_LANGUAGE,
    CONF_MODEL,
    DEFAULT_LANGUAGE,
    DEFAULT_MODEL,
    DOMAIN,
    MULTILINGUAL_LANGUAGES,
    NOVA_3_LANGUAGES,
)
from custom_components.deepgram_stt.stt import DeepgramSTTEntity
from homeassistant import config_entries
from homeassistant.components.stt import (
    AudioBitRates,
    AudioChannels,
    AudioCodecs,
    AudioFormats,
    AudioSampleRates,
    SpeechMetadata,
    SpeechResultState,
)
from homeassistant.data_entry_flow import FlowResultType


@pytest.mark.parametrize("language", NOVA_3_LANGUAGES)
async def test_every_language_is_selectable_and_reaches_deepgram(language):
    """Exercise the actual schema, metadata check and SDK call for every option."""
    data = STEP_USER_DATA_SCHEMA({CONF_API_KEY: "test_api_key_12345", CONF_LANGUAGE: language})
    entry = MockConfigEntry(domain=DOMAIN, data=data)
    entity = DeepgramSTTEntity(entry)
    metadata = SpeechMetadata(
        language="ja" if language == "multi" else language,
        format=AudioFormats.WAV,
        codec=AudioCodecs.PCM,
        bit_rate=AudioBitRates.BITRATE_16,
        sample_rate=AudioSampleRates.SAMPLERATE_16000,
        channel=AudioChannels.CHANNEL_MONO,
    )
    assert entity.check_metadata(metadata)
    if language == "multi":
        assert entity.supported_languages == list(MULTILINGUAL_LANGUAGES)
        assert "multi" not in entity.supported_languages
    else:
        assert entity.supported_languages == [language]
        assert not entity.check_metadata(replace(metadata, language="unsupported"))

    handlers = {}
    connection = AsyncMock()
    connection.__aenter__.return_value = connection
    connection.on = MagicMock(side_effect=lambda event, handler: handlers.update({event: handler}))

    async def finalize():
        await handlers[EventType.MESSAGE](
            MagicMock(channel=MagicMock(alternatives=[MagicMock(transcript="認識結果")]), is_final=True)
        )

    connection.send_close_stream.side_effect = finalize
    client = MagicMock()
    client.listen.v1.connect.return_value = connection

    async def audio():
        yield b"pcm audio"

    with patch("custom_components.deepgram_stt.stt.AsyncDeepgramClient", return_value=client):
        result = await entity.async_process_audio_stream(metadata, audio())

    assert result.result == SpeechResultState.SUCCESS
    assert result.text == "認識結果"
    assert client.listen.v1.connect.call_args.kwargs["language"] == language
    assert client.listen.v1.connect.call_args.kwargs["model"] == "nova-3"
    connection.send_media.assert_awaited_once_with(b"pcm audio")


def test_dropdown_rejects_arbitrary_language():
    with pytest.raises(vol.Invalid):
        STEP_USER_DATA_SCHEMA({CONF_API_KEY: "test_api_key_12345", CONF_LANGUAGE: "not-a-language"})
    selector = STEP_USER_DATA_SCHEMA.schema[
        next(key for key in STEP_USER_DATA_SCHEMA.schema if key.schema == CONF_LANGUAGE)
    ]
    config = selector.config
    assert config["mode"] == "dropdown"
    assert config["custom_value"] is False
    assert {option["value"] for option in config["options"]} == set(NOVA_3_LANGUAGES)
    assert any(option["label"] == "Japanese (ja)" for option in config["options"])


@pytest.mark.parametrize("language", ["ja", "zh-HK", "multi"])
async def test_setup_flow_saves_selected_language(hass, enable_custom_integrations, language):
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_USER})
    assert result["type"] == FlowResultType.FORM
    with patch("custom_components.deepgram_stt.async_setup_entry", return_value=True):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_API_KEY: "test_api_key_12345", CONF_MODEL: DEFAULT_MODEL, CONF_LANGUAGE: language},
        )
        await hass.async_block_till_done()
    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["data"][CONF_LANGUAGE] == language


async def test_options_flow_saves_language_and_reloads(hass, enable_custom_integrations):
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_API_KEY: "test_api_key_12345", CONF_LANGUAGE: "pl"},
        unique_id=DOMAIN,
    )
    entry.add_to_hass(hass)
    with patch("custom_components.deepgram_stt.stt.async_setup_entry", return_value=True):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
    result = await hass.config_entries.options.async_init(entry.entry_id)
    assert result["type"] == FlowResultType.FORM
    assert result["data_schema"]({})[CONF_LANGUAGE] == "pl"
    with patch.object(hass.config_entries, "async_reload", return_value=True) as reload_entry:
        result = await hass.config_entries.options.async_configure(result["flow_id"], {CONF_LANGUAGE: "ja"})
        await hass.async_block_till_done()
    assert result["type"] == FlowResultType.CREATE_ENTRY
    reload_entry.assert_awaited_once_with(entry.entry_id)
    assert DeepgramSTTEntity(entry).language == "ja"
    assert entry.data[CONF_LANGUAGE] == "pl"
    result = await hass.config_entries.options.async_init(entry.entry_id)
    assert result["data_schema"]({})[CONF_LANGUAGE] == "ja"
    assert isinstance(ConfigFlow.async_get_options_flow(entry), config_entries.OptionsFlow)


def test_existing_entry_without_language_keeps_default():
    entity = DeepgramSTTEntity(MockConfigEntry(domain=DOMAIN, data={CONF_API_KEY: "test_api_key_12345"}))
    assert entity.language == DEFAULT_LANGUAGE


@pytest.mark.parametrize("language", ["ja", "ar-AE", "multi"])
async def test_real_sdk_serializes_language_and_transcript(language):
    """Run the installed SDK with only the network transport replaced."""
    entry = MockConfigEntry(domain=DOMAIN, data={CONF_API_KEY: "test_api_key_12345", CONF_LANGUAGE: language})
    entity = DeepgramSTTEntity(entry)
    metadata = SpeechMetadata(
        language="ja" if language == "multi" else language,
        format=AudioFormats.WAV,
        codec=AudioCodecs.PCM,
        bit_rate=AudioBitRates.BITRATE_16,
        sample_rate=AudioSampleRates.SAMPLERATE_16000,
        channel=AudioChannels.CHANNEL_MONO,
    )
    received = asyncio.Queue()
    sent = []

    async def send(message):
        sent.append(message)
        if isinstance(message, str) and json.loads(message).get("type") == "CloseStream":
            await received.put(
                json.dumps(
                    {
                        "type": "Results",
                        "channel_index": [0, 1],
                        "start": 0.0,
                        "duration": 0.1,
                        "is_final": True,
                        "speech_final": True,
                        "channel": {
                            "alternatives": [{"transcript": "日本語の文字起こし", "confidence": 0.99, "words": []}]
                        },
                    }
                )
            )

    async def messages():
        while True:
            yield await received.get()

    protocol = MagicMock()
    protocol.send = send
    protocol.__aiter__.side_effect = messages

    @asynccontextmanager
    async def connect(url, **kwargs):
        query = parse_qs(urlparse(url).query)
        assert query["language"] == [language]
        assert query["model"] == ["nova-3"]
        assert query["sample_rate"] == ["16000"]
        assert query["encoding"] == ["linear16"]
        assert "Authorization" in kwargs["extra_headers"]
        yield protocol

    async def audio():
        yield b"pcm audio"

    with patch("deepgram.listen.v1.client.websockets_client_connect", connect):
        result = await entity.async_process_audio_stream(metadata, audio())
    assert result.result == SpeechResultState.SUCCESS
    assert result.text == "日本語の文字起こし"
    assert sent[0] == b"pcm audio"
    assert json.loads(sent[-1]) == {"type": "CloseStream"}
