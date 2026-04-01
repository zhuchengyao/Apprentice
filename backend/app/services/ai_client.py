"""
Unified AI client that supports both Anthropic (Claude) and OpenAI providers.
"""

import logging
from collections.abc import AsyncGenerator
from enum import Enum

from app.config import settings

logger = logging.getLogger(__name__)


class AIProvider(str, Enum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"


# Default models per provider
DEFAULT_MODELS = {
    AIProvider.ANTHROPIC: "claude-sonnet-4-20250514",
    AIProvider.OPENAI: "gpt-4o",
}


def _resolve_provider_model(
    provider: AIProvider | None, model: str | None
) -> tuple[AIProvider, str]:
    provider = provider or AIProvider(settings.ai_provider)
    model = model or settings.ai_model or DEFAULT_MODELS[provider]
    return provider, model


async def chat_completion(
    messages: list[dict],
    max_tokens: int = 4096,
    provider: AIProvider | None = None,
    model: str | None = None,
) -> str:
    """Send a chat completion request. Returns the full response text."""
    provider, model = _resolve_provider_model(provider, model)

    if provider == AIProvider.ANTHROPIC:
        return await _anthropic_chat(messages, max_tokens, model)
    elif provider == AIProvider.OPENAI:
        return await _openai_chat(messages, max_tokens, model)
    else:
        raise ValueError(f"Unsupported AI provider: {provider}")


async def chat_completion_stream(
    messages: list[dict],
    max_tokens: int = 4096,
    provider: AIProvider | None = None,
    model: str | None = None,
) -> AsyncGenerator[str, None]:
    """Send a chat completion request. Yields text chunks as they arrive."""
    provider, model = _resolve_provider_model(provider, model)

    if provider == AIProvider.ANTHROPIC:
        async for chunk in _anthropic_stream(messages, max_tokens, model):
            yield chunk
    elif provider == AIProvider.OPENAI:
        async for chunk in _openai_stream(messages, max_tokens, model):
            yield chunk
    else:
        raise ValueError(f"Unsupported AI provider: {provider}")


# --- Non-streaming implementations ---


async def _anthropic_chat(messages: list[dict], max_tokens: int, model: str) -> str:
    import anthropic

    client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
    message = await client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=messages,
    )
    return message.content[0].text.strip()


async def _openai_chat(messages: list[dict], max_tokens: int, model: str) -> str:
    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=settings.openai_api_key)
    response = await client.chat.completions.create(
        model=model,
        max_completion_tokens=max_tokens,
        messages=messages,
    )
    return response.choices[0].message.content.strip()


# --- Streaming implementations ---


async def _anthropic_stream(
    messages: list[dict], max_tokens: int, model: str
) -> AsyncGenerator[str, None]:
    import anthropic

    client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
    async with client.messages.stream(
        model=model,
        max_tokens=max_tokens,
        messages=messages,
    ) as stream:
        async for text in stream.text_stream:
            yield text


async def _openai_stream(
    messages: list[dict], max_tokens: int, model: str
) -> AsyncGenerator[str, None]:
    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=settings.openai_api_key)
    response = await client.chat.completions.create(
        model=model,
        max_completion_tokens=max_tokens,
        messages=messages,
        stream=True,
    )
    async for chunk in response:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
