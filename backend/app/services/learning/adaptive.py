"""Adaptive difficulty for the guided study quiz.

`choose_quiz_plan` picks a question count and target difficulty based on the
user's rolling accuracy across their most recent completed scopes. The idea
is to keep the quiz in a productive struggle zone: too many right answers
means push harder, too many misses means dial it back.
"""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.book import KnowledgePoint
from app.models.study import QuizAttempt
from app.services.teaching.quiz import QuizPlan

# Accuracy band → (question_count, difficulty_delta_from_avg)
LOW_BAND = 0.5
HIGH_BAND = 0.8

ROLLING_ATTEMPT_LIMIT = 30  # ~last 3 scopes at 5 questions + slack


async def rolling_accuracy(
    db: AsyncSession, user_id: uuid.UUID, limit: int = ROLLING_ATTEMPT_LIMIT
) -> float | None:
    """Accuracy over the user's most recent attempts across all sessions.

    Returns None if the user has no attempts yet — the caller should fall
    back to a neutral plan in that case.
    """
    from app.models.study import StudySession

    result = await db.execute(
        select(QuizAttempt.correct)
        .join(StudySession, QuizAttempt.session_id == StudySession.id)
        .where(StudySession.user_id == user_id)
        .order_by(QuizAttempt.answered_at.desc())
        .limit(limit)
    )
    rows = list(result.scalars().all())
    if not rows:
        return None
    return sum(1 for r in rows if r) / len(rows)


def _avg_kp_difficulty(kps: list[KnowledgePoint]) -> int:
    if not kps:
        return 2
    vals = [int(getattr(kp, "difficulty", 2) or 2) for kp in kps]
    return max(1, min(5, round(sum(vals) / len(vals))))


def _kp_difficulty_range(kps: list[KnowledgePoint]) -> tuple[int, int]:
    if not kps:
        return 1, 5
    vals = [int(getattr(kp, "difficulty", 2) or 2) for kp in kps]
    return max(1, min(vals)), min(5, max(vals))


async def choose_quiz_plan(
    db: AsyncSession,
    user_id: uuid.UUID,
    kps: list[KnowledgePoint],
) -> QuizPlan:
    """Return a QuizPlan calibrated to the user's rolling accuracy.

    - <50% accuracy → 2 questions at one step easier than the scope's avg KP
      difficulty (floor 1).
    - >80% accuracy → 5 questions at one step harder (ceil 5).
    - Otherwise → 3 questions at the scope's avg KP difficulty.

    The target is clamped to the actual difficulty range of the scope's KPs
    so a request for difficulty 5 against a scope of difficulty-1 KPs falls
    back to the highest available — otherwise the cache lookup misses
    silently and the user sees an empty quiz.

    New users (no attempts yet) get the neutral plan.
    """
    avg_diff = _avg_kp_difficulty(kps)
    min_diff, max_diff = _kp_difficulty_range(kps)
    acc = await rolling_accuracy(db, user_id)
    if acc is None:
        target = avg_diff
        count = 3
    elif acc < LOW_BAND:
        target = max(1, avg_diff - 1)
        count = 2
    elif acc > HIGH_BAND:
        target = min(5, avg_diff + 1)
        count = 5
    else:
        target = avg_diff
        count = 3
    target = max(min_diff, min(max_diff, target))
    return QuizPlan(count=count, target_difficulty=target)
