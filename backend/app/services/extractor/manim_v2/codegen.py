"""Stage 3 — Plan + Spec + retrieved examples → Manim code."""

from __future__ import annotations

import logging
import re

from app.services.ai_client import chat_completion
from app.services.extractor.manim_v2.prompts import codegen_prompt
from app.services.extractor.manim_v2.spec_model import SceneSpec

logger = logging.getLogger(__name__)


_FENCE_RE = re.compile(r"^\s*```(?:python|py)?\s*\n(.*?)\n```\s*$", re.DOTALL)


def _strip_fences(text: str) -> str:
    m = _FENCE_RE.match(text.strip())
    return m.group(1) if m else text


async def generate_code(
    concept: str,
    plan_markdown: str,
    spec: SceneSpec,
    examples: list[dict],
    *,
    model: str,
    caller: str,
    prior_code: str | None = None,
    stderr_tail: str | None = None,
) -> str:
    """Return Manim Python source (no fences, no prose)."""
    user = codegen_prompt.build_user_message(
        concept, plan_markdown, spec, examples,
        prior_code=prior_code, stderr_tail=stderr_tail,
    )
    prompt_chars = sum(len(ex.get("code") or "") for ex in examples)
    logger.info(
        "codegen: caller=%s examples_in_prompt=%d ids=%s example_code_chars=%d retry=%s",
        caller, len(examples),
        [ex.get("id") for ex in examples],
        prompt_chars,
        bool(prior_code),
    )
    raw = await chat_completion(
        messages=[{"role": "user", "content": user}],
        system=codegen_prompt.build_system_blocks(),
        model=model,
        caller=caller,
        max_tokens=4096,
    )
    return _strip_fences(raw).strip()
