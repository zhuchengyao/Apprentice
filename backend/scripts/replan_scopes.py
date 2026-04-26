"""Rebuild Scope rows for existing chapters.

Use this after the prompt or tutor model changes, or to backfill chapters
parsed before the parse-stage scope pipeline existed.

Usage (from backend/):
    # One chapter by id
    python -m scripts.replan_scopes --chapter-id <uuid>

    # Every chapter of a book
    python -m scripts.replan_scopes --book-id <uuid>

    # Every chapter in the DB that already has KPs
    python -m scripts.replan_scopes --all

    # Only chapters whose existing Scope rows are older than a date
    # (and chapters with no Scope rows at all)
    python -m scripts.replan_scopes --all --since 2026-04-20

    # Add EXPLAIN pre-warm after re-planning (tutor LLM call per scope)
    python -m scripts.replan_scopes --all --prewarm

The new Scope rows replace any existing ones for each replanned chapter
(plan_and_persist_scopes_for_chapter is idempotent). StudySession rows
are left as-is; on the next resume, the stale-scope check will hydrate
from the fresh Scope rows.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import sys
import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.config import settings
from app.models.book import Book, Chapter, KnowledgePoint, Scope, Section
from app.services.teaching.context import load_chapter_context_for
from app.services.teaching.study_planner import (
    plan_and_persist_scopes_for_chapter,
    prewarm_scope_explanations,
)

logger = logging.getLogger(__name__)


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Rebuild chapter scope plans.")
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--chapter-id", help="Single chapter uuid")
    group.add_argument("--book-id", help="Replan every chapter of a book")
    group.add_argument("--all", action="store_true", help="Replan every chapter with KPs")
    p.add_argument(
        "--since",
        help="Only replan if any existing Scope row is older than this date (YYYY-MM-DD). "
             "Chapters with no Scope rows are always replanned when in scope.",
    )
    p.add_argument("--prewarm", action="store_true",
                   help="Run pre-warm EXPLAIN after planning.")
    p.add_argument("--language", default=None,
                   help="Teaching language (defaults to settings.prewarm_language).")
    p.add_argument("-v", "--verbose", action="store_true")
    return p.parse_args()


async def _chapter_ids(args: argparse.Namespace, session) -> list[uuid.UUID]:
    if args.chapter_id:
        return [uuid.UUID(args.chapter_id)]
    if args.book_id:
        q = select(Chapter.id).where(Chapter.book_id == uuid.UUID(args.book_id))
    else:
        q = select(Chapter.id)

    # Only chapters that actually have KPs (via Section → KnowledgePoint).
    q = q.join(Section, Section.chapter_id == Chapter.id).join(
        KnowledgePoint, KnowledgePoint.section_id == Section.id
    ).distinct()

    rows = (await session.execute(q)).scalars().all()
    return list(rows)


async def _should_replan(
    session, chapter_id: uuid.UUID, since: datetime | None
) -> bool:
    """When --since is set, skip chapters whose every Scope row is newer
    than the cutoff. No Scope rows → always replan."""
    if since is None:
        return True
    rows = (await session.execute(
        select(Scope.created_at).where(Scope.chapter_id == chapter_id)
    )).scalars().all()
    if not rows:
        return True
    return any(ts < since for ts in rows)


async def _replan_one(
    session_factory,
    chapter_id: uuid.UUID,
    *,
    prewarm: bool,
    language: str,
) -> tuple[bool, str]:
    async with session_factory() as db:
        chapter = await db.get(Chapter, chapter_id)
        if chapter is None:
            return False, "chapter not found"
        book = await db.get(Book, chapter.book_id)

        kps = (await db.execute(
            select(KnowledgePoint)
            .join(Section, KnowledgePoint.section_id == Section.id)
            .where(Section.chapter_id == chapter_id)
            .order_by(KnowledgePoint.order_index)
        )).scalars().all()
        if not kps:
            return False, "no KPs"

        _, _, chapter_content = await load_chapter_context_for(
            chapter.book_id, chapter.id, db
        )

        rows = await plan_and_persist_scopes_for_chapter(
            db,
            chapter,
            book_title=(book.title if book else "") or "",
            chapter_content=chapter_content,
            kps=kps,
            language=language,
        )

        if prewarm:
            await prewarm_scope_explanations(
                db,
                chapter,
                book_title=(book.title if book else "") or "",
                chapter_content=chapter_content,
                kps=kps,
                language=language,
            )

        await db.commit()
        return True, f"{len(rows)} scopes"


async def _main() -> int:
    args = _parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    since: datetime | None = None
    if args.since:
        try:
            since = datetime.fromisoformat(args.since)
        except ValueError:
            print(f"--since must be ISO date (YYYY-MM-DD); got {args.since!r}", file=sys.stderr)
            return 2

    language = args.language or settings.prewarm_language

    engine = create_async_engine(settings.database_url, poolclass=NullPool)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    try:
        async with session_factory() as db:
            chapter_ids = await _chapter_ids(args, db)
            filtered: list[uuid.UUID] = []
            for cid in chapter_ids:
                if await _should_replan(db, cid, since):
                    filtered.append(cid)

        logger.info("Replanning %d chapter(s) (prewarm=%s, language=%s)",
                    len(filtered), args.prewarm, language)

        ok = 0
        skipped = 0
        for cid in filtered:
            try:
                success, note = await _replan_one(
                    session_factory, cid,
                    prewarm=args.prewarm, language=language,
                )
            except Exception as e:
                logger.error("chapter %s failed: %s", cid, e)
                continue
            if success:
                ok += 1
                logger.info("chapter %s → %s", cid, note)
            else:
                skipped += 1
                logger.info("chapter %s skipped (%s)", cid, note)
        logger.info("Done: %d replanned, %d skipped", ok, skipped)
        return 0
    finally:
        await engine.dispose()


if __name__ == "__main__":
    sys.exit(asyncio.run(_main()))
