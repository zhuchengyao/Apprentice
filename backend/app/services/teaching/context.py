"""Context loaders for tutor conversations.

These helpers fetch and cache the per-conversation data that the tutor
system prompt depends on — chapter content, KP list, and student block.
Each is idempotent and writes its cache back onto the TutorConversation
row so subsequent turns reuse the work.
"""

from __future__ import annotations

import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import HISTORY_WINDOW
from app.models.book import Book, BookPage, Chapter, KnowledgePoint, Section
from app.models.tutor import TutorConversation, TutorMessage
from app.models.user import User
from app.services.learning.mastery import recent_kp_signals
from app.services.teaching.agent import format_kp_list
from app.services.teaching.prompts import build_student_block


async def _fetch_chapter_content(
    book_id: uuid.UUID, chapter: Chapter, db: AsyncSession
) -> str:
    """Materialize the chapter body from sections (preferred) or raw pages.

    Truncates oversized chapters and normalizes any literal CHAPTER_BEGIN /
    CHAPTER_END markers so they don't collide with the prompt's own delimiters.
    """
    result = await db.execute(
        select(Section)
        .where(Section.chapter_id == chapter.id)
        .order_by(Section.order_index)
    )
    sections = result.scalars().all()

    if sections and any(s.content_raw for s in sections):
        chapter_content = "\n\n".join(
            f"## {s.title}\n{s.content_raw}" for s in sections if s.content_raw
        )
    else:
        page_result = await db.execute(
            select(BookPage)
            .where(
                BookPage.book_id == book_id,
                BookPage.page_number >= chapter.start_page,
                BookPage.page_number <= chapter.end_page,
            )
            .order_by(BookPage.page_number)
        )
        pages = page_result.scalars().all()
        chapter_content = "\n\n".join(p.html_content for p in pages) if pages else ""

    if len(chapter_content) > 50000:
        chapter_content = chapter_content[:50000] + "\n\n[... content truncated ...]"

    chapter_content = chapter_content.replace("<<<CHAPTER_END>>>", "<<<chapter_end>>>")
    chapter_content = chapter_content.replace("<<<CHAPTER_BEGIN>>>", "<<<chapter_begin>>>")
    return chapter_content


async def load_chapter_context_for(
    book_id: uuid.UUID, chapter_id: uuid.UUID, db: AsyncSession
) -> tuple[str, str, str]:
    """Return (book_title, chapter_title, chapter_content) without a conversation.

    Used by code paths (study session creation, re-planning) that need the
    chapter body before any TutorConversation row exists.
    """
    book = await db.get(Book, book_id)
    chapter = await db.get(Chapter, chapter_id)
    if not book or not chapter:
        raise HTTPException(status_code=404, detail="Book or chapter not found")
    chapter_content = await _fetch_chapter_content(book_id, chapter, db)
    return book.title, chapter.title, chapter_content


async def load_chapter_context(
    conversation: TutorConversation, db: AsyncSession
) -> tuple[str, str, str]:
    """Return (book_title, chapter_title, chapter_content) for the system prompt.

    chapter_content is cached on the conversation; backfilled on first access.
    """
    book = await db.get(Book, conversation.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    chapter = await db.get(Chapter, conversation.chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")

    if conversation.chapter_context is not None:
        return book.title, chapter.title, conversation.chapter_context

    chapter_content = await _fetch_chapter_content(conversation.book_id, chapter, db)
    conversation.chapter_context = chapter_content
    await db.commit()
    return book.title, chapter.title, chapter_content


async def load_student_block(
    conversation: TutorConversation,
    current_user: User,
    db: AsyncSession,
) -> str:
    """Return the per-student system block, cached on the conversation."""
    if conversation.student_block_cache is not None:
        return conversation.student_block_cache
    struggled, mastered = await recent_kp_signals(
        db, current_user.id, exclude_chapter_id=conversation.chapter_id
    )
    block = build_student_block(current_user.learner_profile, struggled, mastered)
    conversation.student_block_cache = block
    await db.commit()
    return block


async def load_kp_list_text(
    conversation: TutorConversation,
    all_kps: list[KnowledgePoint],
    db: AsyncSession,
) -> str:
    """Return the formatted KP list for the system prompt, cached on the
    conversation. Backfilled on first access, same pattern as chapter_context.
    """
    if conversation.kp_list_cache is not None:
        return conversation.kp_list_cache
    text = format_kp_list(all_kps)
    conversation.kp_list_cache = text
    await db.commit()
    return text


async def recent_api_messages(
    conv_id: uuid.UUID,
    db: AsyncSession,
    *,
    limit: int = HISTORY_WINDOW + 2,
) -> list[dict]:
    """Fetch just the last N messages for a conversation, clamped to start
    on a user turn. Used by hot endpoints so we never hydrate a full
    long-running conversation just to throw most of it away.
    """
    result = await db.execute(
        select(TutorMessage)
        .where(TutorMessage.conversation_id == conv_id)
        .order_by(TutorMessage.created_at.desc())
        .limit(limit)
    )
    recent = list(reversed(result.scalars().all()))
    while recent and recent[0].role != "user":
        recent.pop(0)
    return [{"role": m.role, "content": m.content} for m in recent]


def kp_highlight_data(kps: list[KnowledgePoint]) -> dict:
    return {
        "knowledge_points": [
            {
                "id": str(kp.id),
                "concept": kp.concept,
                "section_id": str(kp.section_id),
                "explanation": kp.explanation[:200],
                "source_anchor": kp.source_anchor,
                "illustration_video": kp.illustration_video,
            }
            for kp in kps
        ]
    }
