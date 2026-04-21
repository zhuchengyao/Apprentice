"""Stage 2 — Scene Plan → SceneSpec (validated JSON)."""

from __future__ import annotations

import json
import re

from pydantic import ValidationError

from app.services.ai_client import chat_completion
from app.services.extractor.manim_v2.prompts import spec_prompt
from app.services.extractor.manim_v2.spec_model import SceneSpec


# Occasionally the model wraps its JSON in a fence or adds stray text —
# tolerate that by extracting the outermost { ... } block if direct
# parsing fails.
_FENCE_RE = re.compile(r"```(?:json|JSON)?\s*\n(.*?)\n```", re.DOTALL)


class SpecDeclined(Exception):
    """Upstream plan marked this concept as a decline; the LLM echoed it
    into the spec via scene_id == 'declined'."""

    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


def _extract_json_blob(text: str) -> str:
    text = text.strip()
    m = _FENCE_RE.search(text)
    if m:
        return m.group(1).strip()
    # Best-effort: find the first '{' and last matching '}' scan.
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end > start:
        return text[start : end + 1]
    return text


async def generate_spec(
    concept: str,
    plan_markdown: str,
    *,
    model: str,
    caller: str,
    max_attempts: int = 2,
) -> SceneSpec:
    """Call the LLM with the plan; parse and validate into a SceneSpec.

    Retries up to `max_attempts` times, feeding the prior error message
    back into the user prompt so the model can self-correct.
    """
    last_error: str | None = None
    last_raw: str | None = None
    for attempt in range(max_attempts):
        user = spec_prompt.build_user_message(
            concept, plan_markdown, prior_spec_error=last_error,
        )
        raw = await chat_completion(
            messages=[{"role": "user", "content": user}],
            system=spec_prompt.build_system_blocks(),
            model=model,
            caller=caller,
            max_tokens=4096,
        )
        last_raw = raw
        blob = _extract_json_blob(raw)
        try:
            data = json.loads(blob)
        except json.JSONDecodeError as e:
            last_error = f"JSON decode error: {e}; first 200 chars: {blob[:200]!r}"
            continue
        try:
            spec = SceneSpec.model_validate(data)
        except ValidationError as e:
            last_error = f"Pydantic validation error: {e}"
            continue
        if spec.scene_id == "declined":
            reason = spec.learning_objective.removeprefix("DECLINE:").strip() or "unspecified"
            raise SpecDeclined(reason)
        return spec
    raise ValueError(
        f"spec_generator failed after {max_attempts} attempts: {last_error}; "
        f"last raw (first 400): {(last_raw or '')[:400]!r}"
    )
