"""Example-library retrieval: embed the scene spec, cosine top-K.

The index is a single `_index.json` file produced offline by
`scripts/build_manim_example_index.py`. It contains per-example metadata
and the pre-computed embedding vector so retrieval is a single OpenAI
call (for the query) plus an in-process NumPy cosine sweep.

The index is loaded lazily and cached in-process.
"""

from __future__ import annotations

import json
import logging
import math
from pathlib import Path

from app.services.embedding import generate_embedding
from app.services.extractor.manim_v2.spec_model import SceneSpec

logger = logging.getLogger(__name__)


_EXAMPLES_DIR = Path(__file__).parent / "examples"
_INDEX_PATH = _EXAMPLES_DIR / "_index.json"


# mtime-aware cache: reload the index if _index.json is rebuilt while the
# process is running. An lru_cache locks the first result forever, which
# causes "no RAG" in a server that was started before the index existed.
_cache_entries: list[dict] = []
_cache_mtime_ns: int = -1


def _load_index() -> list[dict]:
    global _cache_entries, _cache_mtime_ns
    if not _INDEX_PATH.exists():
        if _cache_mtime_ns != -2:
            logger.warning(
                "manim_v2 example index not found at %s; retrieval will return [] — "
                "run `python -m scripts.build_manim_example_index` to build it.",
                _INDEX_PATH,
            )
            _cache_mtime_ns = -2  # "warned once" sentinel
        _cache_entries = []
        return _cache_entries
    mtime_ns = _INDEX_PATH.stat().st_mtime_ns
    if mtime_ns == _cache_mtime_ns and _cache_entries:
        return _cache_entries
    with _INDEX_PATH.open("r", encoding="utf-8") as f:
        payload = json.load(f)
    entries = payload.get("entries") or []
    for e in entries:
        e["_code_path"] = str(_EXAMPLES_DIR / e["code_path"])
    _cache_entries = entries
    _cache_mtime_ns = mtime_ns
    logger.info(
        "manim_v2 retrieval: loaded index from %s (%d entries, mtime_ns=%d)",
        _INDEX_PATH, len(entries), mtime_ns,
    )
    return _cache_entries


def _read_code(entry: dict) -> str:
    p = Path(entry["_code_path"])
    try:
        return p.read_text(encoding="utf-8")
    except OSError as exc:
        logger.warning("Could not read example code %s: %s", p, exc)
        return ""


def _cosine(a: list[float], b: list[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)


def _spec_query_text(concept: str, plan_markdown: str, spec: SceneSpec) -> str:
    """Distill the spec into a short string we can embed.

    Includes concept, learning objective, camera type, object kinds, and
    action kinds — the surface area most predictive of which example
    idioms will help.
    """
    kinds = sorted({o.kind for o in spec.objects})
    actions = sorted({a.kind for b in spec.timeline for a in b.parallel})
    has_3d = spec.camera.scene_type == "ThreeDScene"
    parts = [
        f"concept: {concept}",
        f"objective: {spec.learning_objective}",
        f"camera: {spec.camera.scene_type}",
        f"object_kinds: {', '.join(kinds)}",
        f"action_kinds: {', '.join(actions)}",
    ]
    if has_3d:
        parts.append("category: 3d")
    return "\n".join(parts)


async def retrieve_examples(
    concept: str,
    plan_markdown: str,
    spec: SceneSpec,
    *,
    k: int = 4,
) -> list[dict]:
    """Return up to `k` examples ranked by cosine similarity to the spec."""
    entries = _load_index()
    if not entries:
        logger.warning(
            "retrieve_examples: index empty — no RAG context will be injected "
            "(concept=%r). Rebuild with `python -m scripts.build_manim_example_index`.",
            concept[:80],
        )
        return []
    query = _spec_query_text(concept, plan_markdown, spec)
    try:
        q_vec = await generate_embedding(query)
    except Exception as exc:
        logger.warning("retrieve_examples: embedding failed (%s) — skipping retrieval", exc)
        return []

    scored = [
        (_cosine(q_vec, e.get("embedding") or []), e)
        for e in entries
    ]
    scored.sort(key=lambda p: p[0], reverse=True)
    top = scored[: max(1, k)]

    results: list[dict] = []
    for score, entry in top:
        results.append(
            {
                "id": entry["id"],
                "summary": entry.get("summary", ""),
                "tags": entry.get("tags", []),
                "apis": entry.get("apis", []),
                "score": round(float(score), 4),
                "code": _read_code(entry),
            }
        )
    logger.info(
        "retrieve_examples: concept=%r k=%d index=%d picked=%s",
        concept[:60], k, len(entries),
        [(r["id"], r["score"]) for r in results],
    )
    return results


def retrieved_ids(examples: list[dict]) -> list[str]:
    """Used for structured logging."""
    return [e.get("id", "?") for e in examples]
