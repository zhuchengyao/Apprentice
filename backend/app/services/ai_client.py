"""
Unified AI client that supports both Anthropic (Claude) and OpenAI providers.
Every call records token usage and cost to the api_usage table.
"""

import asyncio
import base64
import logging
import os
from collections.abc import AsyncGenerator
from dataclasses import dataclass
from enum import Enum

from app.config import settings

logger = logging.getLogger(__name__)


class AIProvider(str, Enum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"


# ── Model Registry ──────────────────────────────────────────────
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

_MODEL_TO_PROVIDER: dict[str, AIProvider] = {
    model: provider
    for provider, models in MODEL_REGISTRY.items()
    for model in models
}


def get_available_models() -> dict[str, list[str]]:
    return {p.value: models for p, models in MODEL_REGISTRY.items()}


# ── Pricing (USD per 1M tokens) ───────────────────────────────
MODEL_PRICING: dict[str, dict[str, float]] = {
    "claude-opus-4-6":           {"input": 15.0,  "output": 75.0},
    "claude-sonnet-4-6":         {"input": 3.0,   "output": 15.0},
    "claude-haiku-4-5-20251001": {"input": 0.8,   "output": 4.0},
    "gpt-5.4":                   {"input": 2.5,   "output": 10.0},
    "gpt-5.4-mini":              {"input": 0.4,   "output": 1.6},
    "gpt-5.4-nano":              {"input": 0.1,   "output": 0.4},
}


def compute_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Compute cost in USD for a single API call."""
    pricing = MODEL_PRICING.get(model)
    if not pricing:
        logger.warning("No pricing for model '%s', recording $0", model)
        return 0.0
    return (input_tokens * pricing["input"] + output_tokens * pricing["output"]) / 1_000_000


# ── Usage recording ────────────────────────────────────────────

@dataclass
class TokenUsage:
    input_tokens: int
    output_tokens: int


async def _record_usage(
    model: str, provider: AIProvider, caller: str, usage: TokenUsage,
) -> None:
    """Persist a usage record to the database (fire-and-forget).

    Uses its own engine+session to avoid event-loop mismatch when called
    from background tasks that run in a different loop (asyncio.run).
    """
    try:
        from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
        from sqlalchemy.pool import NullPool
        from app.models.usage import ApiUsage

        cost = compute_cost(model, usage.input_tokens, usage.output_tokens)

        engine = create_async_engine(settings.database_url, poolclass=NullPool)
        session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        try:
            async with session_factory() as db:
                db.add(ApiUsage(
                    model=model,
                    provider=provider.value,
                    caller=caller,
                    input_tokens=usage.input_tokens,
                    output_tokens=usage.output_tokens,
                    cost_usd=cost,
                ))
                await db.commit()
        finally:
            await engine.dispose()

        logger.debug(
            "Usage: %s [%s] in=%d out=%d cost=$%.6f",
            model, caller, usage.input_tokens, usage.output_tokens, cost,
        )
    except Exception as e:
        logger.warning("Failed to record usage: %s", e)


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


# ── Public API ─────────────────────────────────────────────────

async def chat_completion(
    messages: list[dict],
    max_tokens: int = 4096,
    provider: AIProvider | None = None,
    model: str | None = None,
    caller: str = "unknown",
) -> str:
    """Send a chat completion request. Returns the full response text."""
    provider, model = _resolve_provider_model(provider, model)

    if provider == AIProvider.ANTHROPIC:
        text, usage = await _anthropic_chat(messages, max_tokens, model)
    elif provider == AIProvider.OPENAI:
        text, usage = await _openai_chat(messages, max_tokens, model)
    else:
        raise ValueError(f"Unsupported AI provider: {provider}")

    asyncio.create_task(_record_usage(model, provider, caller, usage))
    return text


async def chat_completion_stream(
    messages: list[dict],
    max_tokens: int = 4096,
    provider: AIProvider | None = None,
    model: str | None = None,
    caller: str = "unknown",
) -> AsyncGenerator[str, None]:
    """Send a chat completion request. Yields text chunks as they arrive.
    Usage is recorded after the stream completes.
    """
    provider, model = _resolve_provider_model(provider, model)

    if provider == AIProvider.ANTHROPIC:
        async for chunk in _anthropic_stream(messages, max_tokens, model, provider, caller):
            yield chunk
    elif provider == AIProvider.OPENAI:
        async for chunk in _openai_stream(messages, max_tokens, model, provider, caller):
            yield chunk
    else:
        raise ValueError(f"Unsupported AI provider: {provider}")


# ── Helpers ────────────────────────────────────────────────────

def build_image_content_blocks(image_paths: list[str]) -> list[dict]:
    """Build multimodal content blocks from image file paths."""
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


# ── Non-streaming implementations ──────────────────────────────


async def _anthropic_chat(
    messages: list[dict], max_tokens: int, model: str,
) -> tuple[str, TokenUsage]:
    import anthropic

    client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
    message = await client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=messages,
    )
    usage = TokenUsage(
        input_tokens=message.usage.input_tokens,
        output_tokens=message.usage.output_tokens,
    )
    return message.content[0].text.strip(), usage


async def _openai_chat(
    messages: list[dict], max_tokens: int, model: str,
) -> tuple[str, TokenUsage]:
    from openai import AsyncOpenAI
    import httpx

    client = AsyncOpenAI(
        api_key=settings.openai_api_key,
        timeout=httpx.Timeout(120.0, connect=10.0),
    )
    try:
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
        text = response.choices[0].message.content.strip()
        usage = TokenUsage(
            input_tokens=response.usage.prompt_tokens if response.usage else 0,
            output_tokens=response.usage.completion_tokens if response.usage else 0,
        )
        return text, usage
    finally:
        await client.close()


# ── Streaming implementations ──────────────────────────────────


async def _anthropic_stream(
    messages: list[dict], max_tokens: int, model: str,
    provider: AIProvider, caller: str,
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

    # After stream ends, get_final_message() has usage
    final = await stream.get_final_message()
    usage = TokenUsage(
        input_tokens=final.usage.input_tokens,
        output_tokens=final.usage.output_tokens,
    )
    asyncio.create_task(_record_usage(model, provider, caller, usage))


async def _openai_stream(
    messages: list[dict], max_tokens: int, model: str,
    provider: AIProvider, caller: str,
) -> AsyncGenerator[str, None]:
    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=settings.openai_api_key)
    try:
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
            stream_options={"include_usage": True},
        )
        usage = TokenUsage(input_tokens=0, output_tokens=0)
        async for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
            # The final chunk with usage has empty choices
            if chunk.usage:
                usage = TokenUsage(
                    input_tokens=chunk.usage.prompt_tokens,
                    output_tokens=chunk.usage.completion_tokens,
                )

        asyncio.create_task(_record_usage(model, provider, caller, usage))
    finally:
        await client.close()
