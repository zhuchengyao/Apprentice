"""MCQ quiz generator for guided study sessions.

Generation is lazy and cached by `scope_signature` — a hash of the sorted
KP IDs in the scope. Once one user has completed PRACTICE for a scope, any
other user who reaches that scope reuses the same question pool.
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
import uuid
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.book import KnowledgePoint
from app.models.study import QuizQuestion
from app.services.ai_client import chat_completion
from app.services.teaching.prompts import (
    TUTOR_STATIC_RULES,
    build_tutor_context,
    build_task_block,
    build_generate_mcq_task,
)

logger = logging.getLogger(__name__)


MIN_QUESTIONS = 2
MAX_QUESTIONS = 5
VALID_OPTIONS = ("A", "B", "C", "D")


@dataclass
class QuizPlan:
    count: int
    target_difficulty: int


def scope_signature(kp_ids: list[str]) -> str:
    """Stable hash of a scope's KP set. Order-insensitive."""
    joined = "|".join(sorted(kp_ids))
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()[:48]


def _strip_json_fence(text: str) -> str:
    text = text.strip()
    fence = re.match(r"^```(?:json)?\s*\n(.*?)\n```$", text, re.DOTALL)
    return fence.group(1).strip() if fence else text


def _validate_question(
    raw: dict, valid_kp_ids: set[str]
) -> dict | None:
    """Return a normalized question dict, or None if the entry is malformed."""
    if not isinstance(raw, dict):
        return None
    stem = str(raw.get("stem", "")).strip()
    if not stem:
        return None
    options = raw.get("options", [])
    if not isinstance(options, list) or len(options) != 4:
        return None
    normalized_options: list[dict] = []
    keys_seen: set[str] = set()
    for opt in options:
        if not isinstance(opt, dict):
            return None
        key = str(opt.get("key", "")).strip().upper()
        text = str(opt.get("text", "")).strip()
        if key not in VALID_OPTIONS or key in keys_seen or not text:
            return None
        keys_seen.add(key)
        normalized_options.append({"key": key, "text": text})
    if keys_seen != set(VALID_OPTIONS):
        return None
    # Enforce stable A-D order regardless of what the model emitted.
    normalized_options.sort(key=lambda o: o["key"])
    correct_option = str(raw.get("correct_option", "")).strip().upper()
    if correct_option not in VALID_OPTIONS:
        return None
    explanation = str(raw.get("explanation", "")).strip()
    if not explanation:
        return None
    kp_id = str(raw.get("kp_id", "")).strip()
    if kp_id and kp_id not in valid_kp_ids:
        kp_id = ""
    try:
        difficulty = int(raw.get("difficulty", 1))
    except (TypeError, ValueError):
        difficulty = 1
    difficulty = max(1, min(5, difficulty))
    return {
        "stem": stem,
        "options": normalized_options,
        "correct_option": correct_option,
        "explanation": explanation,
        "kp_id": kp_id,
        "difficulty": difficulty,
    }


async def _existing_for_signature(
    db: AsyncSession, signature: str
) -> list[QuizQuestion]:
    result = await db.execute(
        select(QuizQuestion)
        .where(QuizQuestion.scope_signature == signature)
        .order_by(QuizQuestion.generated_at)
    )
    return list(result.scalars().all())


def _pick_from_cache(
    cached: list[QuizQuestion], plan: QuizPlan
) -> list[QuizQuestion]:
    """Pick up to plan.count questions from the cache, preferring ones near
    the target difficulty. No partial generation — either we have enough
    cached matches or we generate fresh.
    """
    matching = [q for q in cached if q.difficulty == plan.target_difficulty]
    if len(matching) >= plan.count:
        return matching[: plan.count]
    # Widen: include ±1 around target, sorted by distance then oldest first.
    ranked = sorted(
        cached,
        key=lambda q: (abs(q.difficulty - plan.target_difficulty), q.generated_at),
    )
    if len(ranked) >= plan.count:
        return ranked[: plan.count]
    return []


async def generate_quiz_for_scope(
    kps: list[KnowledgePoint],
    plan: QuizPlan,
    db: AsyncSession,
    *,
    book_title: str,
    chapter_title: str,
    chapter_content: str,
    kp_list_text: str,
    student_block: str,
    language: str,
) -> list[QuizQuestion]:
    """Return `plan.count` QuizQuestion rows for the given scope.

    Checks the cache first; generates & persists new questions if the cache
    can't satisfy the plan. Safe to call concurrently — duplicate-generation
    just produces extra cached rows for next time.
    """
    if not kps:
        return []

    kp_ids = [str(kp.id) for kp in kps]
    signature = scope_signature(kp_ids)
    valid_kp_ids = set(kp_ids)

    cached = await _existing_for_signature(db, signature)
    picked = _pick_from_cache(cached, plan)
    if picked:
        return picked

    count = max(MIN_QUESTIONS, min(MAX_QUESTIONS, plan.count))
    task_text = build_task_block(
        build_generate_mcq_task(
            [(str(kp.id), kp.concept, (kp.explanation or "")[:500]) for kp in kps],
            count=count,
            target_difficulty=plan.target_difficulty,
        )
    )
    context_text = build_tutor_context(
        book_title,
        chapter_title,
        chapter_content,
        knowledge_points_text=kp_list_text,
        language=language,
    )
    system_blocks = [
        {"type": "text", "text": TUTOR_STATIC_RULES},
        {
            "type": "text",
            "text": context_text,
            "cache_control": {"type": "ephemeral"},
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
            messages=[{"role": "user", "content": "Generate the questions now."}],
            # Reasoning models (gpt-5-class) can burn most of the budget on
            # internal reasoning; a tight ceiling leaves no room for the JSON
            # output and the caller receives an empty/invalid response.
            max_tokens=8192,
            model=settings.tutor_model,
            caller="study_generate_mcq",
            system=system_blocks,
        )
    except Exception as e:
        logger.warning("generate_quiz_for_scope LLM call failed: %s", e)
        return []

    try:
        parsed = json.loads(_strip_json_fence(raw))
    except json.JSONDecodeError:
        logger.warning(
            "generate_quiz_for_scope: invalid JSON. Raw: %s", raw[:400]
        )
        return []
    if not isinstance(parsed, list) or not parsed:
        return []

    # Validate everything before touching the session — if any row is bad,
    # we'd rather skip generation than half-persist and force the caller
    # into a rollback that wipes their other work in the same transaction.
    normalized_rows: list[dict] = []
    for entry in parsed:
        normalized = _validate_question(entry, valid_kp_ids)
        if normalized is None:
            continue
        normalized_rows.append(normalized)
        if len(normalized_rows) >= count:
            break

    if not normalized_rows:
        return []

    new_rows = [
        QuizQuestion(
            id=uuid.uuid4(),
            scope_signature=signature,
            kp_ids=kp_ids,
            difficulty=n["difficulty"],
            stem=n["stem"],
            options=n["options"],
            correct_option=n["correct_option"],
            explanation=n["explanation"],
            source="ai_generated",
        )
        for n in normalized_rows
    ]
    db.add_all(new_rows)
    await db.flush()
    return new_rows
