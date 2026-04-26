"""Scope planner — decides how to carve a chapter's knowledge points into
thematic "scopes" for a guided study session.

The plan is computed once at chapter parse time (see
`plan_and_persist_scopes_for_chapter`) and stored in the `scopes` table,
then hydrated into `StudySession.scope_plan` at session creation. The
LLM is allowed to drop KPs it judges as trivia/redundant; any KP not
assigned to a scope is implicitly skipped.
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
from dataclasses import dataclass

import sqlalchemy as sa
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.book import Chapter, KnowledgePoint, Scope
from app.services.ai_client import chat_completion
from app.services.teaching.anchor_validator import validate_anchors
from app.services.teaching.prompts import (
    TUTOR_STATIC_RULES,
    build_tutor_context,
    build_task_block,
    build_plan_scopes_task,
)

logger = logging.getLogger(__name__)


# Fallback chunker bands (used only when the LLM plan fails to validate).
SCOPE_MIN_KPS = 3
SCOPE_MAX_KPS = 5

# Neutral student block used when planning is done offline (parse stage).
# The base plan is shared across all learners; personalized re-planning
# is a session-time overlay that can be layered later.
_NEUTRAL_STUDENT_BLOCK = (
    "<student>\nThis is the base scope plan, computed before any single "
    "learner opens the chapter. Treat the student as a motivated beginner "
    "with no prior signal.\n</student>"
)


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
) -> tuple[list[ScopePlan], set[str]] | None:
    """Validate the LLM plan and return (scopes, dropped_kp_ids).

    The LLM is explicitly allowed to drop KPs it judges as trivia, redundant,
    or tangential — any KP not assigned to a scope ends up in `dropped`.
    Returns None only when the plan is structurally unusable (not a list of
    non-empty scope dicts, references to unknown KP ids, duplicate KP
    assignments, or zero scopes), in which case the caller falls back to
    the heuristic chunker that covers every KP.
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
    if not validated:
        return None
    dropped = valid_kp_ids - seen
    return validated, dropped


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

    result = _validate_plan(parsed, kps)
    if result is None:
        logger.warning("plan_scopes: plan structurally invalid, using fallback.")
        return _fallback_plan(kps)

    validated, dropped = result
    total = len(kps)
    logger.info(
        "plan_scopes: chapter=%s kps_total=%d kps_kept=%d kps_dropped=%d scopes=%d drop_rate=%.2f dropped_ids=%s",
        getattr(chapter, "id", "?"), total, total - len(dropped), len(dropped),
        len(validated), (len(dropped) / total) if total else 0.0,
        sorted(dropped)[:10],
    )
    return validated


# ── Parse-stage persistence ───────────────────────────────────

def _kp_set_hash(kps: list[KnowledgePoint]) -> str:
    """Deterministic hash of the KP id set. Used to flag stale Scope rows
    when the chapter's KPs drift (e.g. after a re-parse)."""
    joined = "|".join(sorted(str(k.id) for k in kps))
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()[:40]


async def plan_and_persist_scopes_for_chapter(
    db: AsyncSession,
    chapter: Chapter,
    book_title: str,
    chapter_content: str,
    kps: list[KnowledgePoint],
    *,
    language: str = "en",
) -> list[Scope]:
    """Parse-stage: run the LLM scope plan once, validate anchors against
    the chapter HTML, and persist the result as `scopes` rows.

    Idempotent per (chapter_id, kp-set-hash): if the existing Scope rows'
    stored `plan_hash` already matches the current KP set, we skip.
    Otherwise the chapter's old scopes are deleted and replaced.
    """
    if not kps:
        return []

    kp_hash = _kp_set_hash(kps)

    existing = (await db.execute(
        select(Scope).where(Scope.chapter_id == chapter.id).order_by(Scope.index)
    )).scalars().all()
    if existing and all((s.plan_hash or "") == kp_hash for s in existing):
        logger.info(
            "plan_and_persist_scopes_for_chapter: chapter=%s already planned (hash=%s, %d scopes), skipping",
            chapter.id, kp_hash, len(existing),
        )
        return existing

    # KP set changed — replan. Remove the old rows first so the upsert is clean.
    if existing:
        await db.execute(sa.delete(Scope).where(Scope.chapter_id == chapter.id))
        await db.flush()

    scope_plans = await plan_scopes(
        chapter=chapter,
        book_title=book_title,
        chapter_content=chapter_content,
        kps=kps,
        student_block=_NEUTRAL_STUDENT_BLOCK,
        language=language,
    )

    kp_by_id: dict[str, KnowledgePoint] = {str(k.id): k for k in kps}
    rows: list[Scope] = []
    for idx, plan in enumerate(scope_plans):
        raw_anchors: list[str] = []
        for kp_id in plan.kp_ids:
            kp = kp_by_id.get(str(kp_id))
            if kp is not None and (kp.source_anchor or "").strip():
                raw_anchors.append(kp.source_anchor.strip())

        final_anchors, repaired, unmatched = validate_anchors(raw_anchors, chapter_content)
        scope = Scope(
            chapter_id=chapter.id,
            index=idx,
            title=(plan.title or "Scope")[:200],
            anchor_hint=(plan.anchor_hint or None),
            kp_ids=list(plan.kp_ids),
            source_anchors=final_anchors,
            anchors_repaired=repaired,
            anchors_unmatched=unmatched,
            plan_model=settings.tutor_model,
            plan_hash=kp_hash,
        )
        db.add(scope)
        rows.append(scope)

    await db.flush()

    logger.info(
        "plan_and_persist_scopes_for_chapter: chapter=%s scopes=%d anchors_repaired=%d anchors_unmatched=%d hash=%s",
        chapter.id, len(rows),
        sum(r.anchors_repaired for r in rows),
        sum(r.anchors_unmatched for r in rows),
        kp_hash,
    )
    return rows


def scope_rows_to_plan_dicts(rows: list[Scope]) -> list[dict]:
    """Hydrate prebuilt Scope rows into the JSONB shape StudySession
    expects on `scope_plan`. The session machinery is unchanged —
    `current_scope_index` still indexes this list."""
    return [
        {
            "title": r.title,
            "kp_ids": list(r.kp_ids or []),
            "anchor_hint": r.anchor_hint or "",
            "source_anchors": list(r.source_anchors or []),
            "explanation_text": r.explanation_text,
        }
        for r in rows
    ]


async def load_scope_plan_for_chapter(
    db: AsyncSession, chapter_id
) -> list[dict] | None:
    """Return the pre-built scope plan as wire dicts, or None if the
    chapter has no Scope rows yet (caller should fall back to an
    on-demand `plan_scopes` call)."""
    result = await db.execute(
        select(Scope).where(Scope.chapter_id == chapter_id).order_by(Scope.index)
    )
    rows = result.scalars().all()
    if not rows:
        return None
    return scope_rows_to_plan_dicts(rows)


# ── Pre-warmed EXPLAIN text ───────────────────────────────────
#
# The session's /advance endpoint already cache-short-circuits when a
# scope's `explanation_text` is populated. By pre-computing that text at
# parse time and loading it via `scope_rows_to_plan_dicts`, the very
# first learner to hit a chapter sees zero-latency explanations instead
# of waiting for a full stream. Opt in via `settings.prewarm_scope_explanations`
# (off by default — adds one tutor LLM call per scope to parse cost).


async def prewarm_scope_explanations(
    db: AsyncSession,
    chapter: Chapter,
    book_title: str,
    chapter_content: str,
    kps: list[KnowledgePoint],
    *,
    language: str = "en",
) -> int:
    """Generate and persist `Scope.explanation_text` for every scope in
    the chapter that doesn't have one yet. Returns the number written.
    """
    # Late imports: these pull in the full tutor prompt machinery which
    # we want to avoid at module import time (prompts module loads big
    # cached strings and touches models). Lazy keeps the planner import
    # cheap for callers that only need scope planning.
    from app.services.teaching.prompts import (
        TUTOR_STATIC_RULES,
        build_explain_scope_task,
        build_task_block,
        build_tutor_context,
    )

    rows = (await db.execute(
        select(Scope).where(Scope.chapter_id == chapter.id).order_by(Scope.index)
    )).scalars().all()
    if not rows:
        return 0

    kp_by_id: dict[str, KnowledgePoint] = {str(k.id): k for k in kps}
    kp_list_lines: list[str] = []
    for kp in kps:
        diff_label = "easy" if kp.difficulty <= 1 else "medium" if kp.difficulty <= 2 else "hard"
        kp_list_lines.append(
            f"- id={kp.id} [{diff_label}] {kp.concept}: {(kp.explanation or '')[:160]}"
        )
    kp_list_text = "\n".join(kp_list_lines) if kp_list_lines else "(none)"

    context_text = build_tutor_context(
        book_title, chapter.title, chapter_content,
        knowledge_points_text=kp_list_text,
        language=language,
    )

    written = 0
    for scope_row in rows:
        if scope_row.explanation_text:
            continue
        scope_kps = [
            kp_by_id[str(kp_id)] for kp_id in (scope_row.kp_ids or [])
            if str(kp_id) in kp_by_id
        ]
        if not scope_kps:
            continue

        task_text = build_task_block(
            build_explain_scope_task(
                scope_row.title,
                [(str(kp.id), kp.concept, (kp.explanation or "")[:500]) for kp in scope_kps],
            )
        )
        system_blocks = [
            {"type": "text", "text": TUTOR_STATIC_RULES},
            {"type": "text", "text": context_text,
             "cache_control": {"type": "ephemeral", "ttl": "1h"}},
            {"type": "text", "text": _NEUTRAL_STUDENT_BLOCK,
             "cache_control": {"type": "ephemeral"}},
            {"type": "text", "text": task_text},
        ]
        try:
            text = await chat_completion(
                messages=[{"role": "user", "content": "Deliver the explanation now."}],
                max_tokens=4096,
                model=settings.tutor_model,
                caller="prewarm_scope_explain",
                system=system_blocks,
            )
        except Exception as e:
            logger.warning(
                "prewarm_scope_explanations: chapter=%s scope=%d failed: %s",
                chapter.id, scope_row.index, e,
            )
            continue
        scope_row.explanation_text = text.strip() or None
        written += 1

    await db.flush()
    logger.info(
        "prewarm_scope_explanations: chapter=%s scopes=%d written=%d (existing cached=%d)",
        chapter.id, len(rows), written, len(rows) - written,
    )
    return written
