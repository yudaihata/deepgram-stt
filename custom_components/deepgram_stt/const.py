"""Constants for Deepgram STT integration."""

DOMAIN = "deepgram_stt"

# API Configuration
DEFAULT_MODEL = "nova-3"
DEFAULT_LANGUAGE = "pl"
DEFAULT_ENCODING = "linear16"
DEFAULT_SAMPLE_RATE = 16000

# Streaming Configuration
STREAM_DELAY = 0.01
TRANSCRIPT_TIMEOUT = 5

# Config Keys
CONF_API_KEY = "api_key"
CONF_MODEL = "model"
CONF_LANGUAGE = "language"

# Nova-3 / nova-3-general language codes, including regional aliases.
# Source: https://developers.deepgram.com/docs/models-languages-overview
# Last checked: 2026-10-21. Keep this shared by the UI and STT entity.
NOVA_3_LANGUAGES: dict[str, str] = {
    "multi": "Multilingual (10 languages)",
    "af": "Afrikaans (af)",
    "af-ZA": "Afrikaans (af-ZA)",
    "ar": "Arabic (ar)",
    "ar-AE": "Arabic (ar-AE)",
    "ar-SA": "Arabic (ar-SA)",
    "ar-QA": "Arabic (ar-QA)",
    "ar-KW": "Arabic (ar-KW)",
    "ar-SY": "Arabic (ar-SY)",
    "ar-LB": "Arabic (ar-LB)",
    "ar-PS": "Arabic (ar-PS)",
    "ar-JO": "Arabic (ar-JO)",
    "ar-EG": "Arabic (ar-EG)",
    "ar-SD": "Arabic (ar-SD)",
    "ar-TD": "Arabic (ar-TD)",
    "ar-MA": "Arabic (ar-MA)",
    "ar-DZ": "Arabic (ar-DZ)",
    "ar-TN": "Arabic (ar-TN)",
    "ar-IQ": "Arabic (ar-IQ)",
    "ar-IR": "Arabic (ar-IR)",
    "hy": "Armenian (hy)",
    "as": "Assamese (as)",
    "as-IN": "Assamese (as-IN)",
    "be": "Belarusian (be)",
    "bn": "Bengali (bn)",
    "bs": "Bosnian (bs)",
    "bg": "Bulgarian (bg)",
    "ca": "Catalan (ca)",
    "zh-HK": "Chinese (Cantonese, Traditional) (zh-HK)",
    "zh": "Chinese (Mandarin, Simplified) (zh)",
    "zh-CN": "Chinese (Mandarin, Simplified) (zh-CN)",
    "zh-Hans": "Chinese (Mandarin, Simplified) (zh-Hans)",
    "zh-TW": "Chinese (Mandarin, Traditional) (zh-TW)",
    "zh-Hant": "Chinese (Mandarin, Traditional) (zh-Hant)",
    "hr": "Croatian (hr)",
    "cs": "Czech (cs)",
    "cs-CZ": "Czech (cs-CZ)",
    "da": "Danish (da)",
    "da-DK": "Danish (da-DK)",
    "nl": "Dutch (nl)",
    "en": "English (en)",
    "en-US": "English (en-US)",
    "en-AU": "English (en-AU)",
    "en-GB": "English (en-GB)",
    "en-IN": "English (en-IN)",
    "en-NZ": "English (en-NZ)",
    "et": "Estonian (et)",
    "fi": "Finnish (fi)",
    "nl-BE": "Flemish (nl-BE)",
    "fr": "French (fr)",
    "fr-CA": "French (fr-CA)",
    "ka": "Georgian (ka)",
    "ka-GE": "Georgian (ka-GE)",
    "de": "German (de)",
    "de-CH": "German (Switzerland) (de-CH)",
    "el": "Greek (el)",
    "gu": "Gujarati (gu)",
    "gu-IN": "Gujarati (gu-IN)",
    "he": "Hebrew (he)",
    "hi": "Hindi (hi)",
    "hu": "Hungarian (hu)",
    "id": "Indonesian (id)",
    "it": "Italian (it)",
    "ja": "Japanese (ja)",
    "kn": "Kannada (kn)",
    "kk": "Kazakh (kk)",
    "kk-KZ": "Kazakh (kk-KZ)",
    "ko": "Korean (ko)",
    "ko-KR": "Korean (ko-KR)",
    "lv": "Latvian (lv)",
    "lt": "Lithuanian (lt)",
    "mk": "Macedonian (mk)",
    "ms": "Malay (ms)",
    "mr": "Marathi (mr)",
    "mn": "Mongolian (mn)",
    "ne": "Nepali (ne)",
    "no": "Norwegian (no)",
    "ps": "Pashto (ps)",
    "ps-AF": "Pashto (ps-AF)",
    "fa": "Persian (fa)",
    "pl": "Polish (pl)",
    "pt": "Portuguese (pt)",
    "pt-BR": "Portuguese (pt-BR)",
    "pt-PT": "Portuguese (pt-PT)",
    "pa": "Punjabi (pa)",
    "pa-IN": "Punjabi (pa-IN)",
    "ro": "Romanian (ro)",
    "ru": "Russian (ru)",
    "sr": "Serbian (sr)",
    "sk": "Slovak (sk)",
    "sl": "Slovenian (sl)",
    "es": "Spanish (es)",
    "es-419": "Spanish (es-419)",
    "sv": "Swedish (sv)",
    "sv-SE": "Swedish (sv-SE)",
    "tl": "Tagalog (tl)",
    "ta": "Tamil (ta)",
    "te": "Telugu (te)",
    "th": "Thai (th)",
    "th-TH": "Thai (th-TH)",
    "tr": "Turkish (tr)",
    "tr-TR": "Turkish (tr-TR)",
    "uk": "Ukrainian (uk)",
    "ur": "Urdu (ur)",
    "vi": "Vietnamese (vi)",
}

# `multi` is a Deepgram mode, not a BCP 47 language tag for Assist.
MULTILINGUAL_LANGUAGES = ("en", "es", "fr", "de", "hi", "ru", "pt", "ja", "it", "nl")
