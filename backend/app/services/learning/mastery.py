"""Per-KP mastery tracking via SM-2 spaced repetition.

The tutor emits ``<<UNDERSTOOD>>`` / ``<<CLARIFY>>`` verdict markers after
a student answers a Socratic question. Those map to SM-2 quality scores:

  UNDERSTOOD → 5 (perfect recall)
  CLARIFY    → 2 (incorrect, but could reconstruct with hint)

``teach_next`` first-touch on a KP is recorded as ``last_studied_at``
without a quality score.
"""
import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.book import KnowledgePoint, Section
from app.models.user import UserProgress
from app.services.spaced_repetition import sm2_algorithm


QUALITY_UNDERSTOOD = 5
QUALITY_CLARIFY = 2

# Thresholds for sorting KPs into struggled / mastered buckets when building
# the per-student context block. Chosen so a single CLARIFY leaves a KP in
# "struggled" until it's answered correctly at least twice.
STRUGGLED_MASTERY_MAX = 0.35
MASTERED_MASTERY_MIN = 0.8


async def _get_or_create_progress(
    db: AsyncSession, user_id: uuid.UUID, kp_id: uuid.UUID
) -> UserProgress:
    result = await db.execute(
        select(UserProgress).where(
            UserProgress.user_id == user_id,
            UserProgress.knowledge_point_id == kp_id,
        )
    )
    progress = result.scalar_one_or_none()
    if progress is None:
        progress = UserProgress(
            user_id=user_id,
            knowledge_point_id=kp_id,
        )
        db.add(progress)
    return progress


async def record_kp_exposure(
    db: AsyncSession, user_id: uuid.UUID, kp_id: uuid.UUID
) -> None:
    """Record that the student saw this KP (teach turn). No quality change."""
    progress = await _get_or_create_progress(db, user_id, kp_id)
    progress.last_studied_at = datetime.now(UTC).replace(tzinfo=None)


async def update_mastery(
    db: AsyncSession, user_id: uuid.UUID, kp_id: uuid.UUID, quality: int
) -> None:
    """Apply an SM-2 update for a student answering a Socratic question."""
    progress = await _get_or_create_progress(db, user_id, kp_id)
    result = sm2_algorithm(
        quality=quality,
        repetitions=progress.repetitions,
        ease_factor=progress.ease_factor,
        interval_days=progress.interval_days,
    )
    progress.ease_factor = result.ease_factor
    progress.interval_days = result.interval_days
    progress.repetitions = result.repetitions
    progress.next_review_at = result.next_review_at
    progress.last_studied_at = datetime.now(UTC).replace(tzinfo=None)

    # Mastery level is an exponential moving average weighted toward recent
    # outcomes — quality 5 pulls it up by 0.4, quality 2 pulls it down.
    signal = 1.0 if quality >= 4 else 0.0 if quality <= 2 else 0.5
    progress.mastery_level = round(
        0.6 * progress.mastery_level + 0.4 * signal, 3
    )


async def recent_kp_signals(
    db: AsyncSession,
    user_id: uuid.UUID,
    *,
    exclude_chapter_id: uuid.UUID | None = None,
    limit_each: int = 5,
) -> tuple[list[str], list[str]]:
    """Return (struggled_concepts, mastered_concepts) from this user's history.

    Excludes the current chapter so the tutor isn't reminded about the KPs
    it's actively teaching.
    """
    stmt = (
        select(UserProgress, KnowledgePoint)
        .join(KnowledgePoint, UserProgress.knowledge_point_id == KnowledgePoint.id)
        .where(UserProgress.user_id == user_id)
        .options(selectinload(KnowledgePoint.section))
        .order_by(UserProgress.last_studied_at.desc().nullslast())
        .limit(50)
    )
    result = await db.execute(stmt)
    rows = result.all()

    struggled: list[str] = []
    mastered: list[str] = []
    for progress, kp in rows:
        if exclude_chapter_id is not None:
            section = kp.section
            if section and section.chapter_id == exclude_chapter_id:
                continue
        if progress.mastery_level <= STRUGGLED_MASTERY_MAX and progress.repetitions == 0:
            if len(struggled) < limit_each:
                struggled.append(kp.concept)
        elif progress.mastery_level >= MASTERED_MASTERY_MIN:
            if len(mastered) < limit_each:
                mastered.append(kp.concept)
        if len(struggled) >= limit_each and len(mastered) >= limit_each:
            break
    return struggled, mastered
