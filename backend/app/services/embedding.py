"""OpenAI embeddings — used by the Manim v2 example-retrieval pipeline.

Anthropic doesn't expose an embeddings endpoint, so every embedding call
goes through OpenAI regardless of which chat provider generates the code.
Reuses the shared AsyncOpenAI singleton from `ai_client` so we don't burn
a TLS handshake per call.
"""

from __future__ import annotations

import logging

from app.config import settings
from app.services.ai_client import _get_openai_client

logger = logging.getLogger(__name__)


async def generate_embedding(
    text: str,
    *,
    model: str | None = None,
) -> list[float]:
    """Embed a single string. Returns a float vector (1536-dim for 3-small)."""
    client = await _get_openai_client()
    mdl = model or settings.illustration_embedding_model
    resp = await client.embeddings.create(model=mdl, input=text)
    return resp.data[0].embedding


async def generate_embeddings(
    texts: list[str],
    *,
    model: str | None = None,
) -> list[list[float]]:
    """Embed a batch in a single request. Order preserved."""
    if not texts:
        return []
    client = await _get_openai_client()
    mdl = model or settings.illustration_embedding_model
    resp = await client.embeddings.create(model=mdl, input=texts)
    # `data` is ordered by `index` on each element — re-sort defensively.
    ordered = sorted(resp.data, key=lambda d: d.index)
    return [d.embedding for d in ordered]
