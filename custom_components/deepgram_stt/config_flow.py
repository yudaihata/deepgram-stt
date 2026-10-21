"""Config flow for Deepgram STT integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.selector import SelectSelector, SelectSelectorConfig, SelectSelectorMode

from .const import CONF_API_KEY, CONF_LANGUAGE, CONF_MODEL, DEFAULT_LANGUAGE, DEFAULT_MODEL, DOMAIN, NOVA_3_LANGUAGES

_LOGGER = logging.getLogger(__name__)


def language_selector() -> SelectSelector:
    """Build the shared English-language dropdown for setup and options."""
    return SelectSelector(
        SelectSelectorConfig(
            options=[{"value": code, "label": label} for code, label in NOVA_3_LANGUAGES.items()],
            mode=SelectSelectorMode.DROPDOWN,
            custom_value=False,
            sort=True,
        )
    )


STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_KEY): str,
        vol.Optional(CONF_MODEL, default=DEFAULT_MODEL): str,
        vol.Optional(CONF_LANGUAGE, default=DEFAULT_LANGUAGE): language_selector(),
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    # Basic validation - ensure API key is not empty
    data[CONF_API_KEY] = data[CONF_API_KEY].strip()
    if not data[CONF_API_KEY] or len(data[CONF_API_KEY]) < 10:
        raise InvalidAPIKey

    # Return info to be stored in config entry
    return {"title": "Deepgram STT"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Deepgram STT."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> OptionsFlow:
        """Allow changing language without removing the integration."""
        return OptionsFlow()

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except InvalidAPIKey:
                errors["base"] = "invalid_api_key"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                # Prevent multiple instances
                await self.async_set_unique_id(DOMAIN)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors)

    async def async_step_import(self, import_data: dict[str, Any]) -> FlowResult:
        """Handle import from async_setup (auto-configuration from sops secret)."""
        # Prevent multiple instances
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        return self.async_create_entry(title="Deepgram STT", data=import_data)


class InvalidAPIKey(HomeAssistantError):
    """Error to indicate API key is invalid."""


class OptionsFlow(config_entries.OptionsFlow):
    """Handle Deepgram STT options."""

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Manage the transcription language."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        language = self.config_entry.options.get(
            CONF_LANGUAGE, self.config_entry.data.get(CONF_LANGUAGE, DEFAULT_LANGUAGE)
        )
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({vol.Required(CONF_LANGUAGE, default=language): language_selector()}),
        )
