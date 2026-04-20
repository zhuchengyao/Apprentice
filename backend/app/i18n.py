"""Request locale helpers.

Frontend sends `Accept-Language: en` or `Accept-Language: zh`. We map that
to the canonical codes already used by the teaching prompts
(`LANGUAGE_DISPLAY_NAMES` in services/teaching/prompts.py). The user's
stored `preferred_language` is the fallback when no header is present.
"""

from __future__ import annotations

from fastapi import Header

DEFAULT_LOCALE = "en"

# Maps short locale tags the frontend sends to the canonical code the
# teaching prompts and user model use. Kept in sync with
# app.models.user.SUPPORTED_LANGUAGES.
_SHORT_TO_CANONICAL: dict[str, str] = {
    "en": "en",
    "zh": "zh-CN",
    "zh-cn": "zh-CN",
    "zh-hans": "zh-CN",
    "ja": "ja",
    "ko": "ko",
    "es": "es",
    "fr": "fr",
    "de": "de",
}


def normalize_locale(raw: str | None, fallback: str = DEFAULT_LOCALE) -> str:
    """Turn an Accept-Language header into a canonical locale code.

    Accepts either a simple tag (`en`, `zh`) or a full Accept-Language
    string with priorities. Returns the first supported match, else
    `fallback`.
    """
    if not raw:
        return fallback
    tags = [part.split(";")[0].strip().lower() for part in raw.split(",")]
    for tag in tags:
        if not tag:
            continue
        canonical = _SHORT_TO_CANONICAL.get(tag)
        if canonical:
            return canonical
        base = tag.split("-")[0]
        canonical = _SHORT_TO_CANONICAL.get(base)
        if canonical:
            return canonical
    return fallback


async def get_request_locale(
    accept_language: str | None = Header(default=None, alias="Accept-Language"),
) -> str:
    """FastAPI dependency: returns a canonical locale (e.g. `en` / `zh-CN`).

    Falls back to `DEFAULT_LOCALE` when no header is present.
    """
    return normalize_locale(accept_language, fallback=DEFAULT_LOCALE)


def effective_teaching_language(user_pref: str | None, request_locale: str) -> str:
    """Pick the language for a tutor/study prompt.

    The UI locale (``Accept-Language``) and the tutor language are two
    separate settings — a learner can read a Chinese interface while
    asking the tutor to teach in English, or vice-versa. The Settings
    page writes the learner's choice to ``User.preferred_language``; we
    honor that over the request header. Falls back to ``request_locale``
    only when the user has no stored preference.
    """
    return user_pref or request_locale


# Minimal error-message catalog. Expand lazily as endpoints need it.
_ERRORS: dict[str, dict[str, str]] = {
    "en": {
        "generic": "Something went wrong.",
        "not_found": "Not found.",
        "unauthorized": "Unauthorized.",
        "insufficient_credits": "Not enough credits.",
    },
    "zh-CN": {
        "generic": "出错了。",
        "not_found": "未找到。",
        "unauthorized": "未授权。",
        "insufficient_credits": "点数不足。",
    },
}


def error_message(key: str, locale: str = DEFAULT_LOCALE) -> str:
    catalog = _ERRORS.get(locale) or _ERRORS[DEFAULT_LOCALE]
    return catalog.get(key) or _ERRORS[DEFAULT_LOCALE].get(key, key)
