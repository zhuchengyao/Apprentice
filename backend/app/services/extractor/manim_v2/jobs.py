"""Persistent animation jobs for the Manim pipeline.

This module keeps chapter parsing fast by separating KP extraction from
slow LLM/render work. Parsing creates queued AnimationJob rows after KPs
exist; the runner processes those rows and writes all intermediate
artifacts back for later inspection or re-run tooling.
"""

from __future__ import annotations

import asyncio
import logging
import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.config import settings
from app.constants import (
    ILLUSTRATION_CONCURRENCY,
    ILLUSTRATION_MIN_DIFFICULTY,
    ILLUSTRATION_QUALITY,
)
from app.models.animation import AnimationJob, AnimationJobStatus
from app.models.book import Book, Chapter, KnowledgePoint
from app.services.ai_context import ai_user_context
from app.services.extractor.manim_v2.pipeline import (
    ManimOutcome,
    generate_manim_animation,
    log_manim_outcome,
)

logger = logging.getLogger(__name__)


def _now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


def should_animate_kp(kp: KnowledgePoint) -> bool:
    return (
        int(kp.difficulty or 1) >= ILLUSTRATION_MIN_DIFFICULTY
        and bool((kp.concept or "").strip())
    )


def _input_snapshot(book: Book, chapter: Chapter, kp: KnowledgePoint) -> dict:
    """Stable job input. Excludes KP explanation because it is generated text."""
    return {
        "book_id": str(book.id),
        "book_title": book.title,
        "chapter_id": str(chapter.id),
        "chapter_title": chapter.title,
        "knowledge_point_id": str(kp.id),
        "concept": kp.concept,
        "source_anchor": kp.source_anchor,
        "difficulty": kp.difficulty,
        "order_index": kp.order_index,
    }


async def enqueue_animation_jobs_for_kps(
    db: AsyncSession,
    *,
    book: Book,
    chapter: Chapter,
    kps: list[KnowledgePoint],
) -> list[AnimationJob]:
    """Create queued jobs for eligible KPs, idempotent per KP."""
    jobs: list[AnimationJob] = []
    for kp in kps:
        if not should_animate_kp(kp):
            continue
        existing = await db.execute(
            select(AnimationJob.id).where(AnimationJob.knowledge_point_id == kp.id)
        )
        if existing.scalar_one_or_none() is not None:
            continue
        job = AnimationJob(
            knowledge_point_id=kp.id,
            book_id=book.id,
            chapter_id=chapter.id,
            status=AnimationJobStatus.queued,
            concept=(kp.concept or "")[:500],
            source_anchor=kp.source_anchor,
            input_snapshot=_input_snapshot(book, chapter, kp),
        )
        db.add(job)
        jobs.append(job)
    if jobs:
        await db.flush()
    return jobs


def _apply_outcome(job: AnimationJob, kp: KnowledgePoint, outcome: ManimOutcome) -> None:
    job.plan_markdown = outcome.plan_markdown
    job.scene_spec = outcome.scene_spec
    job.retrieved_example_ids = list(outcome.examples_retrieved)
    job.code_attempts = list(outcome.code_attempts)
    job.render_attempts = list(outcome.render_attempts)
    job.qc_reports = list(outcome.qc_reports)
    job.output_filename = outcome.output_path.name if outcome.output_path else None
    job.failure_kind = outcome.failure_kind
    job.failure_detail = outcome.failure_detail
    job.decline_reason = outcome.decline_reason
    job.stage_reached = outcome.stage_reached
    job.attempt = outcome.attempt
    job.latency_ms = outcome.latency_ms
    job.completed_at = _now()

    if outcome.accepted:
        job.status = AnimationJobStatus.succeeded
        kp.illustration_video = job.output_filename
    elif outcome.failure_kind == "declined":
        job.status = AnimationJobStatus.declined
    else:
        job.status = AnimationJobStatus.failed


async def _process_one_job(
    session_factory: async_sessionmaker[AsyncSession],
    job_id: uuid.UUID,
    *,
    user_id: str | None,
    quality: str,
) -> None:
    async with session_factory() as db:
        job = await db.get(AnimationJob, job_id)
        if job is None or job.status != AnimationJobStatus.queued:
            return
        job.status = AnimationJobStatus.running
        job.started_at = _now()
        await db.commit()
        concept = job.concept

    with ai_user_context(user_id):
        outcome = await generate_manim_animation(
            concept,
            quality=quality,
            caller="kp_manim",
        )

    async with session_factory() as db:
        job = await db.get(AnimationJob, job_id)
        if job is None:
            return
        kp = await db.get(KnowledgePoint, job.knowledge_point_id)
        if kp is None:
            job.status = AnimationJobStatus.failed
            job.failure_kind = "missing_kp"
            job.failure_detail = "Knowledge point was deleted before animation completed"
            job.completed_at = _now()
            await db.commit()
            return

        _apply_outcome(job, kp, outcome)
        await db.commit()
        log_manim_outcome(
            outcome,
            book_id=str(job.book_id),
            chapter_id=str(job.chapter_id),
            kp_id=str(kp.id),
            concept=kp.concept,
        )


async def process_queued_animation_jobs_for_chapter(
    chapter_id: uuid.UUID,
    *,
    user_id: str | None = None,
    concurrency: int = ILLUSTRATION_CONCURRENCY,
    quality: str = ILLUSTRATION_QUALITY,
) -> int:
    """Run queued animation jobs for a chapter. Returns the number claimed."""
    engine = create_async_engine(settings.database_url, poolclass=NullPool)
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    try:
        async with session_factory() as db:
            result = await db.execute(
                select(AnimationJob.id)
                .where(
                    AnimationJob.chapter_id == chapter_id,
                    AnimationJob.status == AnimationJobStatus.queued,
                )
                .order_by(AnimationJob.queued_at)
            )
            job_ids = list(result.scalars().all())

        if not job_ids:
            return 0

        sem = asyncio.Semaphore(max(1, concurrency))

        async def _guarded(job_id: uuid.UUID) -> None:
            async with sem:
                try:
                    await _process_one_job(
                        session_factory,
                        job_id,
                        user_id=user_id,
                        quality=quality,
                    )
                except Exception as e:
                    logger.exception("animation job %s failed unexpectedly: %s", job_id, e)
                    async with session_factory() as db:
                        job = await db.get(AnimationJob, job_id)
                        if job is not None:
                            job.status = AnimationJobStatus.failed
                            job.failure_kind = "job_error"
                            job.failure_detail = repr(e)[:500]
                            job.completed_at = _now()
                            await db.commit()

        await asyncio.gather(*(_guarded(job_id) for job_id in job_ids))
        return len(job_ids)
    finally:
        await engine.dispose()
