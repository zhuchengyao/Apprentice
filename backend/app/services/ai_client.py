"""
Unified AI client that supports both Anthropic (Claude) and OpenAI providers.
Every call records token usage and cost to the api_usage table.
"""

import asyncio
import base64
import logging
import os
import uuid as _uuid
from collections.abc import AsyncGenerator
from dataclasses import dataclass
from enum import Enum

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool

from app.config import settings
from app.services.ai_context import get_user_id

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
# Cache rates follow each provider's public pricing:
#   Anthropic ephemeral:  read = 0.10 × input,  write = 1.25 × input
#   OpenAI auto cache:    read = 0.50 × input,  write = 1.00 × input (no surcharge)
MODEL_PRICING: dict[str, dict[str, float]] = {
    "claude-opus-4-6":           {"input": 15.0, "output": 75.0, "cache_read": 1.50,  "cache_write": 18.75},
    "claude-sonnet-4-6":         {"input": 3.0,  "output": 15.0, "cache_read": 0.30,  "cache_write": 3.75},
    "claude-haiku-4-5-20251001": {"input": 0.8,  "output": 4.0,  "cache_read": 0.08,  "cache_write": 1.00},
    "gpt-5.4":                   {"input": 2.5,  "output": 10.0, "cache_read": 1.25,  "cache_write": 2.5},
    "gpt-5.4-mini":              {"input": 0.4,  "output": 1.6,  "cache_read": 0.20,  "cache_write": 0.4},
    "gpt-5.4-nano":              {"input": 0.1,  "output": 0.4,  "cache_read": 0.05,  "cache_write": 0.1},
}


def compute_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
    cache_creation_input_tokens: int = 0,
    cache_read_input_tokens: int = 0,
) -> float:
    """Compute cost in USD for a single API call.

    `input_tokens` is the NON-cached prompt portion. Cached tokens are billed
    at the provider-specific `cache_read` / `cache_write` rates defined in
    MODEL_PRICING.
    """
    pricing = MODEL_PRICING.get(model)
    if not pricing:
        logger.warning("No pricing for model '%s', recording $0", model)
        return 0.0
    total = (
        input_tokens * pricing["input"]
        + cache_creation_input_tokens * pricing["cache_write"]
        + cache_read_input_tokens * pricing["cache_read"]
        + output_tokens * pricing["output"]
    )
    return total / 1_000_000


# ── Usage recording ────────────────────────────────────────────

# NullPool engine shared across all _record_usage calls. NullPool creates a
# fresh connection per session and holds none between calls, so it works
# correctly across different event loops (FastAPI vs background asyncio.run).
_usage_engine = create_async_engine(settings.database_url, poolclass=NullPool)
_usage_session_factory = async_sessionmaker(_usage_engine, class_=AsyncSession, expire_on_commit=False)


@dataclass
class TokenUsage:
    input_tokens: int
    output_tokens: int
    cache_creation_input_tokens: int = 0
    cache_read_input_tokens: int = 0


async def _record_usage(
    model: str, provider: AIProvider, caller: str, usage: TokenUsage,
) -> None:
    """Persist a usage record to the database (fire-and-forget).

    Reads the caller's user_id from the ai_user_context contextvar (copied
    into this task when it was spawned). Deducts credits if user_id is set.
    """
    try:
        from app.models.usage import ApiUsage

        cost = compute_cost(
            model,
            usage.input_tokens,
            usage.output_tokens,
            usage.cache_creation_input_tokens,
            usage.cache_read_input_tokens,
        )
        user_id = get_user_id()
        uid = _uuid.UUID(user_id) if user_id else None

        # Cache reads/creates are surcharged/discounted input tokens — bundle
        # into the single input_tokens column for dashboard totals.
        total_input = (
            usage.input_tokens
            + usage.cache_creation_input_tokens
            + usage.cache_read_input_tokens
        )

        async with _usage_session_factory() as db:
            record = ApiUsage(
                model=model,
                provider=provider.value,
                caller=caller,
                user_id=uid,
                input_tokens=total_input,
                output_tokens=usage.output_tokens,
                cost_usd=cost,
            )
            db.add(record)
            await db.flush()

            if uid:
                from app.services.billing import deduct_credits_for_usage
                await deduct_credits_for_usage(db, user_id, record.id, cost)

            await db.commit()

        logger.debug(
            "Usage: %s [%s] user=%s in=%d out=%d cache_r=%d cache_w=%d cost=$%.6f",
            model, caller, user_id or "system",
            usage.input_tokens, usage.output_tokens,
            usage.cache_read_input_tokens, usage.cache_creation_input_tokens,
            cost,
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

SystemParam = str | list[dict] | None


def _openai_messages_from_system(
    system: SystemParam, messages: list[dict]
) -> list[dict]:
    """OpenAI has no top-level system parameter — prepend it as a message."""
    if system is None:
        return messages
    if isinstance(system, str):
        system_text = system
    else:
        system_text = "\n\n".join(
            b.get("text", "") for b in system if b.get("type") == "text"
        )
    return [{"role": "system", "content": system_text}] + messages


async def chat_completion(
    messages: list[dict],
    max_tokens: int = 4096,
    provider: AIProvider | None = None,
    model: str | None = None,
    caller: str = "unknown",
    system: SystemParam = None,
) -> str:
    """Send a chat completion request. Returns the full response text.

    `system` may be a plain string or a list of Anthropic content blocks. For
    Anthropic it is passed as the top-level `system` parameter (and can carry
    `cache_control` markers). For OpenAI the blocks are flattened to text and
    prepended as a `role=system` message.
    """
    provider, model = _resolve_provider_model(provider, model)

    if provider == AIProvider.ANTHROPIC:
        text, usage = await _anthropic_chat(messages, max_tokens, model, system)
    elif provider == AIProvider.OPENAI:
        text, usage = await _openai_chat(messages, max_tokens, model, system)
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
    system: SystemParam = None,
) -> AsyncGenerator[str, None]:
    """Send a chat completion request. Yields text chunks as they arrive.
    Usage is recorded after the stream completes.
    """
    provider, model = _resolve_provider_model(provider, model)

    if provider == AIProvider.ANTHROPIC:
        async for chunk in _anthropic_stream(
            messages, max_tokens, model, provider, caller, system=system
        ):
            yield chunk
    elif provider == AIProvider.OPENAI:
        async for chunk in _openai_stream(
            messages, max_tokens, model, provider, caller, system=system
        ):
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


def _extract_anthropic_usage(raw_usage) -> TokenUsage:
    """Pull usage + cache counters out of an Anthropic usage object safely."""
    return TokenUsage(
        input_tokens=getattr(raw_usage, "input_tokens", 0) or 0,
        output_tokens=getattr(raw_usage, "output_tokens", 0) or 0,
        cache_creation_input_tokens=getattr(raw_usage, "cache_creation_input_tokens", 0) or 0,
        cache_read_input_tokens=getattr(raw_usage, "cache_read_input_tokens", 0) or 0,
    )


async def _anthropic_chat(
    messages: list[dict], max_tokens: int, model: str, system: SystemParam = None,
) -> tuple[str, TokenUsage]:
    import anthropic

    client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
    kwargs: dict = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": messages,
    }
    if system is not None:
        kwargs["system"] = system
    message = await client.messages.create(**kwargs)
    usage = _extract_anthropic_usage(message.usage)
    return message.content[0].text.strip(), usage


def _extract_openai_usage(usage) -> TokenUsage:
    """Pull usage + cache counters out of an OpenAI usage object safely."""
    if not usage:
        return TokenUsage(input_tokens=0, output_tokens=0)
    cached = 0
    details = getattr(usage, "prompt_tokens_details", None)
    if details:
        cached = getattr(details, "cached_tokens", 0) or 0
    total_prompt = getattr(usage, "prompt_tokens", 0) or 0
    return TokenUsage(
        input_tokens=total_prompt - cached,
        output_tokens=getattr(usage, "completion_tokens", 0) or 0,
        cache_read_input_tokens=cached,
    )


async def _openai_chat(
    messages: list[dict], max_tokens: int, model: str, system: SystemParam = None,
) -> tuple[str, TokenUsage]:
    from openai import AsyncOpenAI
    import httpx

    client = AsyncOpenAI(
        api_key=settings.openai_api_key,
        timeout=httpx.Timeout(120.0, connect=10.0),
    )
    try:
        oai_messages = []
        for msg in _openai_messages_from_system(system, messages):
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
        usage = _extract_openai_usage(response.usage)
        return text, usage
    finally:
        await client.close()


# ── Streaming implementations ──────────────────────────────────


async def _anthropic_stream(
    messages: list[dict], max_tokens: int, model: str,
    provider: AIProvider, caller: str,
    system: SystemParam = None,
) -> AsyncGenerator[str, None]:
    import anthropic

    client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
    kwargs: dict = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": messages,
    }
    if system is not None:
        kwargs["system"] = system
    async with client.messages.stream(**kwargs) as stream:
        async for text in stream.text_stream:
            yield text

    # After stream ends, get_final_message() has usage
    final = await stream.get_final_message()
    usage = _extract_anthropic_usage(final.usage)
    asyncio.create_task(_record_usage(model, provider, caller, usage))


async def _openai_stream(
    messages: list[dict], max_tokens: int, model: str,
    provider: AIProvider, caller: str,
    system: SystemParam = None,
) -> AsyncGenerator[str, None]:
    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=settings.openai_api_key)
    try:
        oai_messages = []
        for msg in _openai_messages_from_system(system, messages):
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
            if chunk.usage:
                usage = _extract_openai_usage(chunk.usage)

        asyncio.create_task(_record_usage(model, provider, caller, usage))
    finally:
        await client.close()
