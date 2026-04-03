"""
Unified AI client that supports both Anthropic (Claude) and OpenAI providers.
"""

import base64
import logging
import os
from collections.abc import AsyncGenerator
from enum import Enum

from app.config import settings

logger = logging.getLogger(__name__)


class AIProvider(str, Enum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"


# ── Model Registry ──────────────────────────────────────────────
# Maps each provider to its available models.
# First model in the list is the default for that provider.
# To add a new model, just append it to the appropriate list.
MODEL_REGISTRY: dict[AIProvider, list[str]] = {
    AIProvider.ANTHROPIC: [
        "claude-sonnet-4-6",
        "claude-opus-4-6",
        "claude-haiku-4-5-20251001",
    ],
    AIProvider.OPENAI: [
        "gpt-5.4",
        "gpt-5.4-mini",
        "gpt-5.4-nano",
    ],
}

# Reverse lookup: model name → provider
_MODEL_TO_PROVIDER: dict[str, AIProvider] = {
    model: provider
    for provider, models in MODEL_REGISTRY.items()
    for model in models
}


def get_available_models() -> dict[str, list[str]]:
    """Return the full registry for display / API use."""
    return {p.value: models for p, models in MODEL_REGISTRY.items()}


def _resolve_provider_model(
    provider: AIProvider | None = None, model: str | None = None
) -> tuple[AIProvider, str]:
    model = model or settings.ai_model
    if model not in _MODEL_TO_PROVIDER:
        available = ", ".join(_MODEL_TO_PROVIDER.keys())
        raise ValueError(
            f"Unknown model '{model}'. Available models: {available}"
        )
    provider = provider or _MODEL_TO_PROVIDER[model]
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


def build_image_content_blocks(image_paths: list[str]) -> list[dict]:
    """Build multimodal content blocks from image file paths.

    Returns a list of dicts suitable for both Anthropic and OpenAI vision APIs.
    Format returned is Anthropic-style; callers convert for OpenAI if needed.
    """
    blocks = []
    for path in image_paths:
        if not os.path.isfile(path):
            continue
        ext = os.path.splitext(path)[1].lstrip(".").lower()
        media_type_map = {
            "png": "image/png",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "gif": "image/gif",
            "webp": "image/webp",
        }
        media_type = media_type_map.get(ext, "image/png")
        with open(path, "rb") as f:
            data = base64.standard_b64encode(f.read()).decode("utf-8")
        blocks.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": media_type,
                "data": data,
            },
        })
    return blocks


def _to_openai_content(content) -> list[dict]:
    """Convert Anthropic-style content blocks to OpenAI format."""
    if isinstance(content, str):
        return [{"type": "text", "text": content}]
    parts = []
    for block in content:
        if block.get("type") == "text":
            parts.append({"type": "text", "text": block["text"]})
        elif block.get("type") == "image":
            source = block["source"]
            parts.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:{source['media_type']};base64,{source['data']}",
                },
            })
    return parts


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
    # Convert multimodal content blocks for OpenAI
    oai_messages = []
    for msg in messages:
        if isinstance(msg.get("content"), list):
            oai_messages.append({"role": msg["role"], "content": _to_openai_content(msg["content"])})
        else:
            oai_messages.append(msg)
    response = await client.chat.completions.create(
        model=model,
        max_completion_tokens=max_tokens,
        messages=oai_messages,
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
    # Convert multimodal content blocks for OpenAI
    oai_messages = []
    for msg in messages:
        if isinstance(msg.get("content"), list):
            oai_messages.append({"role": msg["role"], "content": _to_openai_content(msg["content"])})
        else:
            oai_messages.append(msg)
    response = await client.chat.completions.create(
        model=model,
        max_completion_tokens=max_tokens,
        messages=oai_messages,
        stream=True,
    )
    async for chunk in response:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
