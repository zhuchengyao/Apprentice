"""Scope planner — decides how to carve a chapter's knowledge points into
ordered 3–5-KP "scopes" for a guided study session.

One LLM call per session, at session start. The plan is persisted onto
`StudySession.scope_plan` as JSONB and never re-called unless KP IDs
drift (chapter re-parsed).
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass

from app.config import settings
from app.models.book import Chapter, KnowledgePoint
from app.services.ai_client import chat_completion
from app.services.teaching.prompts import (
    TUTOR_STATIC_RULES,
    build_tutor_context,
    build_task_block,
    build_plan_scopes_task,
)

logger = logging.getLogger(__name__)


SCOPE_MIN_KPS = 3
SCOPE_MAX_KPS = 5


@dataclass
class ScopePlan:
    title: str
    kp_ids: list[str]
    anchor_hint: str

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "kp_ids": list(self.kp_ids),
            "anchor_hint": self.anchor_hint,
        }


def _kp_list_text(kps: list[KnowledgePoint]) -> str:
    lines = []
    for kp in kps:
        diff = "easy" if kp.difficulty <= 1 else "medium" if kp.difficulty <= 2 else "hard"
        lines.append(
            f"- id={kp.id} [{diff}] {kp.concept}: {(kp.explanation or '')[:160]}"
        )
    return "\n".join(lines) if lines else "(none)"


def _strip_json_fence(text: str) -> str:
    text = text.strip()
    fence = re.match(r"^```(?:json)?\s*\n(.*?)\n```$", text, re.DOTALL)
    return fence.group(1).strip() if fence else text


def _fallback_plan(kps: list[KnowledgePoint]) -> list[ScopePlan]:
    """Chunk KPs into groups of 3-5 in their natural order — never leaves
    the student without a plan if the LLM response is unusable."""
    plans: list[ScopePlan] = []
    i = 0
    n = len(kps)
    while i < n:
        remaining = n - i
        if remaining <= SCOPE_MAX_KPS:
            take = remaining
        elif remaining <= SCOPE_MAX_KPS + SCOPE_MIN_KPS:
            # Avoid leaving a tiny tail scope by pulling one fewer now.
            take = remaining - SCOPE_MIN_KPS
        else:
            take = SCOPE_MAX_KPS
        group = kps[i : i + take]
        title = group[0].concept if group else "Scope"
        plans.append(
            ScopePlan(
                title=title[:80],
                kp_ids=[str(kp.id) for kp in group],
                anchor_hint=(group[0].source_anchor or "")[:120] if group else "",
            )
        )
        i += take
    return plans


def _validate_plan(
    raw_plans: list[dict], kps: list[KnowledgePoint]
) -> list[ScopePlan] | None:
    """Ensure the LLM output covers every KP exactly once and nothing extra.

    Returns None if the plan is unusable (we fall back to the heuristic chunker).
    """
    valid_kp_ids = {str(kp.id) for kp in kps}
    seen: set[str] = set()
    validated: list[ScopePlan] = []
    for entry in raw_plans:
        if not isinstance(entry, dict):
            return None
        title = str(entry.get("title", "")).strip() or "Untitled scope"
        kp_ids = entry.get("kp_ids", [])
        if not isinstance(kp_ids, list) or not kp_ids:
            return None
        kp_ids = [str(k).strip() for k in kp_ids]
        for kp_id in kp_ids:
            if kp_id not in valid_kp_ids or kp_id in seen:
                return None
            seen.add(kp_id)
        anchor_hint = str(entry.get("anchor_hint", "")).strip()
        validated.append(ScopePlan(title=title[:120], kp_ids=kp_ids, anchor_hint=anchor_hint[:200]))
    if seen != valid_kp_ids:
        return None
    return validated


async def plan_scopes(
    chapter: Chapter,
    book_title: str,
    chapter_content: str,
    kps: list[KnowledgePoint],
    student_block: str,
    *,
    language: str,
) -> list[ScopePlan]:
    """Return an ordered list of ScopePlans covering every KP exactly once.

    Falls back to a deterministic chunker if the LLM output is malformed or
    fails to cover the KP set.
    """
    if not kps:
        return []

    context_text = build_tutor_context(
        book_title,
        chapter.title,
        chapter_content,
        knowledge_points_text=_kp_list_text(kps),
        language=language,
    )
    task_text = build_task_block(build_plan_scopes_task())
    system_blocks = [
        {"type": "text", "text": TUTOR_STATIC_RULES},
        {
            "type": "text",
            "text": context_text,
            "cache_control": {"type": "ephemeral", "ttl": "1h"},
        },
        {
            "type": "text",
            "text": student_block,
            "cache_control": {"type": "ephemeral"},
        },
        {"type": "text", "text": task_text},
    ]

    try:
        raw = await chat_completion(
            messages=[{"role": "user", "content": "Plan the scopes now."}],
            # Reasoning models eat most of the budget on internal thought;
            # with 2048 the JSON output is routinely truncated or empty and
            # we silently fall back to the heuristic chunker.
            max_tokens=8192,
            model=settings.tutor_model,
            caller="study_plan_scopes",
            system=system_blocks,
        )
    except Exception as e:
        logger.warning("plan_scopes LLM call failed, using fallback: %s", e)
        return _fallback_plan(kps)

    try:
        parsed = json.loads(_strip_json_fence(raw))
    except json.JSONDecodeError:
        logger.warning("plan_scopes: invalid JSON, using fallback. Raw: %s", raw[:400])
        return _fallback_plan(kps)

    if not isinstance(parsed, list):
        return _fallback_plan(kps)

    validated = _validate_plan(parsed, kps)
    if validated is None:
        logger.warning("plan_scopes: plan did not cover KP set, using fallback.")
        return _fallback_plan(kps)

    return validated
