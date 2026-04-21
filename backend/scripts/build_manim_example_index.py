"""Build `_index.json` for the manim_v2 retrieval layer.

Walks
    backend/app/services/extractor/manim_v2/examples/**/*.py
pairs each file with its sidecar `.meta.json`, embeds
(summary + tags + apis + category), and writes the index to
    backend/app/services/extractor/manim_v2/examples/_index.json

Usage (from backend/):
    python -m scripts.build_manim_example_index
"""

from __future__ import annotations

import asyncio
import json
import logging
import sys
from pathlib import Path

from app.services.embedding import generate_embeddings

logger = logging.getLogger(__name__)


_EXAMPLES_DIR = (
    Path(__file__).resolve().parents[1]
    / "app" / "services" / "extractor" / "manim_v2" / "examples"
)
_OUT_PATH = _EXAMPLES_DIR / "_index.json"


def _discover() -> list[dict]:
    """Scan the examples directory for (.py, .meta.json) pairs."""
    entries: list[dict] = []
    for py_path in sorted(_EXAMPLES_DIR.rglob("*.py")):
        if py_path.name.startswith("_"):
            continue
        meta_path = py_path.with_suffix(".meta.json")
        if not meta_path.exists():
            logger.warning("Skip %s: no .meta.json sidecar", py_path)
            continue
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        relative = py_path.relative_to(_EXAMPLES_DIR).as_posix()
        entries.append(
            {
                "id": meta["id"],
                "summary": meta.get("summary", ""),
                "tags": meta.get("tags", []),
                "apis": meta.get("apis", []),
                "difficulty": meta.get("difficulty", 1),
                "category": meta.get("category", ""),
                "code_path": relative,
            }
        )
    return entries


def _embed_text(entry: dict) -> str:
    tags = ", ".join(entry.get("tags", []) or [])
    apis = ", ".join(entry.get("apis", []) or [])
    return (
        f"category: {entry.get('category', '')}\n"
        f"summary: {entry.get('summary', '')}\n"
        f"tags: {tags}\n"
        f"apis: {apis}"
    )


async def _main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    entries = _discover()
    if not entries:
        logger.error("No examples found under %s", _EXAMPLES_DIR)
        return 1

    logger.info("Embedding %d examples…", len(entries))
    texts = [_embed_text(e) for e in entries]
    vectors = await generate_embeddings(texts)
    if len(vectors) != len(entries):
        logger.error("Embedding count mismatch: %d vs %d", len(vectors), len(entries))
        return 2
    for e, v in zip(entries, vectors):
        e["embedding"] = v

    payload = {
        "version": 1,
        "count": len(entries),
        "dim": len(vectors[0]) if vectors else 0,
        "entries": entries,
    }
    _OUT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    logger.info("Wrote %s (%d entries, dim=%d)", _OUT_PATH, len(entries), payload["dim"])
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(_main()))
