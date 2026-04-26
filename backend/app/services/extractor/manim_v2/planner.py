"""Stage 1 — free-form pedagogical plan from the concept label."""

from __future__ import annotations

import re

from app.services.ai_client import chat_completion
from app.services.extractor.manim_v2.prompts import planner_prompt


_DECLINE_RE = re.compile(r"^\s*##\s*Decline\s*\n+\s*yes\s*:\s*(.+?)\s*$", re.IGNORECASE | re.MULTILINE)


class PlannerDecline(Exception):
    """The planner marked this concept unsuitable for animation."""

    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


async def generate_plan(
    concept: str,
    *,
    model: str,
    caller: str,
) -> str:
    """Return the plan markdown. Raise `PlannerDecline` if the plan says no."""
    user = planner_prompt.build_user_message(concept)
    text = await chat_completion(
        messages=[{"role": "user", "content": user}],
        system=planner_prompt.build_system_blocks(),
        model=model,
        caller=caller,
        max_tokens=1200,
    )
    m = _DECLINE_RE.search(text)
    if m:
        raise PlannerDecline(m.group(1).strip())
    return text.strip()
