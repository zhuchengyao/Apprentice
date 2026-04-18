"""Tutor chat API — structured knowledge-point-by-knowledge-point teaching."""

import json
import logging
import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sse_starlette.sse import EventSourceResponse

from app.config import settings
from app.database import get_db
from app.dependencies import get_current_user
from app.i18n import get_request_locale
from app.models.book import Book, Chapter, Section, BookPage, KnowledgePoint
from app.models.user import User
from app.models.tutor import TutorConversation, TutorMessage
from app.services.ai_client import chat_completion_stream
from app.services.ai_context import ai_user_context
from app.services.billing import check_credits_or_raise
from app.services.teaching.agent import (
    get_chapter_knowledge_points,
    plan_next_step,
    format_kp_list,
    parse_comprehension_verdict,
    VerdictStreamFilter,
)
from app.services.teaching.prompts import (
    TUTOR_STATIC_RULES,
    TASK_OPENING,
    build_tutor_context,
    build_task_block,
    build_teach_task,
    build_batch_task,
    build_answer_task,
)

logger = logging.getLogger(__name__)

router = APIRouter()


# ── Request / Response schemas ────────────────────────────────

class StartConversationRequest(BaseModel):
    book_id: str
    chapter_id: str


class ConversationResponse(BaseModel):
    id: str
    book_id: str
    chapter_id: str
    current_kp_index: int
    total_kps: int
    messages: list[dict]


class SendMessageRequest(BaseModel):
    content: str


# ── Helpers ───────────────────────────────────────────────────

async def _get_user_conversation(
    conversation_id: str,
    current_user: User,
    db: AsyncSession,
    *,
    load_messages: bool = True,
) -> TutorConversation:
    """Load a conversation owned by current_user or raise 404/403."""
    conv_id = uuid.UUID(conversation_id)
    stmt = select(TutorConversation).where(TutorConversation.id == conv_id)
    if load_messages:
        stmt = stmt.options(selectinload(TutorConversation.messages))
    result = await db.execute(stmt)
    conversation = result.scalar_one_or_none()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    if conversation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return conversation


async def _get_chapter_context(
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

    result = await db.execute(
        select(Section)
        .where(Section.chapter_id == conversation.chapter_id)
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
                BookPage.book_id == conversation.book_id,
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

    conversation.chapter_context = chapter_content
    await db.commit()
    return book.title, chapter.title, chapter_content


def _build_system_blocks(
    book_title: str,
    chapter_title: str,
    chapter_content: str,
    kp_list_text: str,
    current_task: str,
    language: str,
) -> list[dict]:
    # Three blocks. The cache_control marker caches blocks 0+1 together;
    # the per-turn task lives in block 2 so task changes never bust the
    # chapter-level cache.
    context_text = build_tutor_context(
        book_title, chapter_title, chapter_content,
        knowledge_points_text=kp_list_text,
        language=language,
    )
    task_text = build_task_block(current_task)
    return [
        {"type": "text", "text": TUTOR_STATIC_RULES},
        {
            "type": "text",
            "text": context_text,
            "cache_control": {"type": "ephemeral"},
        },
        {"type": "text", "text": task_text},
    ]


# Sliding-window history. The chapter content + KP list live in the cached
# system prefix, so the model already "knows" the material. The message
# history only provides conversational continuity — a short tail is enough.
HISTORY_WINDOW = 6


def _history_to_api_messages(messages: list[TutorMessage]) -> list[dict]:
    """Return the last HISTORY_WINDOW messages, clamped to start on a
    user turn so the sequence is a valid alternating chat.

    The chapter content + KP list live in the cached system prefix, so the
    model already has full context for the material. History only provides
    conversational continuity — a short tail is enough.
    """
    recent = list(messages[-HISTORY_WINDOW:])
    while recent and recent[0].role != "user":
        recent.pop(0)
    return [{"role": m.role, "content": m.content} for m in recent]


async def _get_kp_list_text(
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


def _kp_highlight_data(kps: list[KnowledgePoint]) -> dict:
    return {
        "knowledge_points": [
            {
                "id": str(kp.id),
                "concept": kp.concept,
                "section_id": str(kp.section_id),
                "explanation": kp.explanation[:200],
                "source_anchor": kp.source_anchor,
                "illustration": kp.illustration,
            }
            for kp in kps
        ]
    }


# ── Endpoints ─────────────────────────────────────────────────

@router.post("/conversations", response_model=ConversationResponse)
async def start_conversation(
    body: StartConversationRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get or create a conversation for a book+chapter."""
    book_id = uuid.UUID(body.book_id)
    chapter_id = uuid.UUID(body.chapter_id)

    result = await db.execute(
        select(TutorConversation)
        .where(
            TutorConversation.book_id == book_id,
            TutorConversation.chapter_id == chapter_id,
            TutorConversation.user_id == current_user.id,
        )
        .options(selectinload(TutorConversation.messages))
        .order_by(TutorConversation.created_at.desc())
        .limit(1)
    )
    conversation = result.scalar_one_or_none()

    all_kps = await get_chapter_knowledge_points(chapter_id, db)

    if not conversation:
        conversation = TutorConversation(
            user_id=current_user.id,
            book_id=book_id,
            chapter_id=chapter_id,
            current_kp_index=0,
        )
        db.add(conversation)
        await db.commit()
        await db.refresh(conversation)
        existing_messages: list[TutorMessage] = []
    else:
        existing_messages = list(conversation.messages)

    return ConversationResponse(
        id=str(conversation.id),
        book_id=body.book_id,
        chapter_id=body.chapter_id,
        current_kp_index=conversation.current_kp_index,
        total_kps=len(all_kps),
        messages=[
            {
                "id": str(m.id),
                "role": m.role,
                "content": m.content,
                "metadata": m.metadata_,
            }
            for m in existing_messages
        ],
    )


@router.get("/conversations/{conversation_id}/messages")
async def get_messages(
    conversation_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    conversation = await _get_user_conversation(conversation_id, current_user, db)

    return [
        {
            "id": str(m.id),
            "role": m.role,
            "content": m.content,
            "metadata": m.metadata_,
        }
        for m in conversation.messages
    ]


@router.post("/conversations/{conversation_id}/open")
async def open_chapter(
    conversation_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    request_locale: str = Depends(get_request_locale),
):
    """Generate an AI opening message when the student first opens a chapter."""
    conversation = await _get_user_conversation(conversation_id, current_user, db)
    conv_id = conversation.id

    if conversation.messages:
        raise HTTPException(status_code=409, detail="Conversation already has messages")

    book_title, chapter_title, chapter_content = await _get_chapter_context(
        conversation, db
    )
    all_kps = await get_chapter_knowledge_points(conversation.chapter_id, db)
    kp_list_text = await _get_kp_list_text(conversation, all_kps, db)

    system_blocks = _build_system_blocks(
        book_title, chapter_title, chapter_content,
        kp_list_text, TASK_OPENING,
        language=request_locale,
    )
    api_messages = [{"role": "user", "content": "请开始"}]

    await check_credits_or_raise(
        db, conversation.user_id, model=settings.tutor_model, max_tokens=1024
    )

    user_id = str(conversation.user_id)

    async def event_stream():
        with ai_user_context(user_id):
            collected = []
            try:
                async for chunk in chat_completion_stream(
                    messages=api_messages,
                    max_tokens=1024,
                    model=settings.tutor_model,
                    caller="tutor_opening",
                    system=system_blocks,
                ):
                    collected.append(chunk)
                    yield {"event": "token", "data": chunk}

                full_text = "".join(collected)
                opening_metadata = {"type": "opening", "action": "continue"}

                from app.database import async_session
                async with async_session() as save_db:
                    assistant_msg = TutorMessage(
                        conversation_id=conv_id,
                        role="assistant",
                        content=full_text,
                        metadata_=opening_metadata,
                    )
                    save_db.add(assistant_msg)
                    await save_db.commit()
                    msg_id = str(assistant_msg.id)

                yield {
                    "event": "done",
                    "data": json.dumps({
                        "id": msg_id,
                        "content": full_text,
                        "action": "continue",
                        "metadata": opening_metadata,
                    }),
                }
            except Exception as e:
                logger.error("Tutor opening error: %s", e)
                yield {"event": "error", "data": str(e)}

    return EventSourceResponse(event_stream())


@router.post("/conversations/{conversation_id}/teach")
async def teach_next(
    conversation_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    request_locale: str = Depends(get_request_locale),
):
    """Teach the next knowledge point(s). Called automatically or by student."""
    conversation = await _get_user_conversation(conversation_id, current_user, db)
    conv_id = conversation.id

    all_kps = await get_chapter_knowledge_points(conversation.chapter_id, db)

    step = plan_next_step(all_kps, conversation.current_kp_index)
    if not step:
        async def done_stream():
            yield {
                "event": "done",
                "data": json.dumps({
                    "id": None,
                    "content": "",
                    "action": "finished",
                    "metadata": {"type": "chapter_complete"},
                }),
            }
        return EventSourceResponse(done_stream())

    book_title, chapter_title, chapter_content = await _get_chapter_context(
        conversation, db
    )
    kp_list_text = await _get_kp_list_text(conversation, all_kps, db)

    if len(step.knowledge_points) == 1:
        kp = step.knowledge_points[0]
        kp_global_idx = conversation.current_kp_index
        task_text = build_teach_task(kp_global_idx, kp.concept, kp.explanation)
    else:
        batch_data = []
        for i, kp in enumerate(step.knowledge_points):
            batch_data.append((conversation.current_kp_index + i, kp.concept, kp.explanation))
        task_text = build_batch_task(batch_data)

    system_blocks = _build_system_blocks(
        book_title, chapter_title, chapter_content,
        kp_list_text, task_text,
        language=request_locale,
    )

    history = _history_to_api_messages(list(conversation.messages))
    api_messages = history + [{"role": "user", "content": "请讲解下一个知识点。"}]

    highlight_data = _kp_highlight_data(step.knowledge_points)

    await check_credits_or_raise(
        db, conversation.user_id, model=settings.tutor_model, max_tokens=2048
    )

    new_kp_index = step.kp_end_index
    action = step.action
    user_id = str(conversation.user_id)

    async def event_stream():
        yield {
            "event": "highlight",
            "data": json.dumps(highlight_data),
        }

        with ai_user_context(user_id):
            collected = []
            try:
                async for chunk in chat_completion_stream(
                    messages=api_messages,
                    max_tokens=2048,
                    model=settings.tutor_model,
                    caller="tutor_teach",
                    system=system_blocks,
                ):
                    collected.append(chunk)
                    yield {"event": "token", "data": chunk}

                full_text = "".join(collected)

                kp_ids = [str(kp.id) for kp in step.knowledge_points]
                msg_metadata = {
                    "type": "teach",
                    "knowledge_point_ids": kp_ids,
                    "action": action,
                }

                from app.database import async_session
                async with async_session() as save_db:
                    assistant_msg = TutorMessage(
                        conversation_id=conv_id,
                        role="assistant",
                        content=full_text,
                        metadata_=msg_metadata,
                    )
                    save_db.add(assistant_msg)

                    conv = await save_db.get(TutorConversation, conv_id)
                    conv.current_kp_index = new_kp_index
                    await save_db.commit()
                    msg_id = str(assistant_msg.id)

                yield {
                    "event": "done",
                    "data": json.dumps({
                        "id": msg_id,
                        "content": full_text,
                        "action": action,
                        "kp_index": new_kp_index,
                        "total_kps": len(all_kps),
                        "metadata": msg_metadata,
                    }),
                }
            except Exception as e:
                logger.error("Tutor teach error: %s", e)
                yield {"event": "error", "data": str(e)}

    return EventSourceResponse(event_stream())


@router.post("/conversations/{conversation_id}/message")
async def send_message(
    conversation_id: str,
    body: SendMessageRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    request_locale: str = Depends(get_request_locale),
):
    """Student sends a question during a lesson. AI answers in context."""
    conversation = await _get_user_conversation(conversation_id, current_user, db)
    conv_id = conversation.id

    user_msg = TutorMessage(
        conversation=conversation,
        role="user",
        content=body.content,
    )
    db.add(user_msg)
    await db.commit()

    book_title, chapter_title, chapter_content = await _get_chapter_context(
        conversation, db
    )
    all_kps = await get_chapter_knowledge_points(conversation.chapter_id, db)
    kp_list_text = await _get_kp_list_text(conversation, all_kps, db)

    kp_index = max(0, conversation.current_kp_index - 1)
    if kp_index < len(all_kps):
        current_kp = all_kps[kp_index]
        task_text = build_answer_task(kp_index, current_kp.concept)
    else:
        task_text = "Answer the student's question about this chapter."

    system_blocks = _build_system_blocks(
        book_title, chapter_title, chapter_content,
        kp_list_text, task_text,
        language=request_locale,
    )

    api_messages = _history_to_api_messages(conversation.messages)

    await check_credits_or_raise(
        db, conversation.user_id, model=settings.tutor_model, max_tokens=2048
    )

    user_id = str(conversation.user_id)

    async def event_stream():
        with ai_user_context(user_id):
            collected = []
            vfilter = VerdictStreamFilter()
            try:
                async for chunk in chat_completion_stream(
                    messages=api_messages,
                    max_tokens=2048,
                    model=settings.tutor_model,
                    caller="tutor_chat",
                    system=system_blocks,
                ):
                    collected.append(chunk)
                    safe = vfilter.push(chunk)
                    if safe:
                        yield {"event": "token", "data": safe}

                tail = vfilter.flush()
                if tail:
                    yield {"event": "token", "data": tail}

                full_text = "".join(collected)
                cleaned_text, action = parse_comprehension_verdict(full_text)
                msg_metadata = {"type": "answer", "action": action}

                from app.database import async_session
                async with async_session() as save_db:
                    assistant_msg = TutorMessage(
                        conversation_id=conv_id,
                        role="assistant",
                        content=cleaned_text,
                        metadata_=msg_metadata,
                    )
                    save_db.add(assistant_msg)
                    await save_db.commit()
                    msg_id = str(assistant_msg.id)

                yield {
                    "event": "done",
                    "data": json.dumps({
                        "id": msg_id,
                        "content": cleaned_text,
                        "action": action,
                        "metadata": msg_metadata,
                    }),
                }
            except Exception as e:
                logger.error("Tutor chat error: %s", e)
                yield {"event": "error", "data": str(e)}

    return EventSourceResponse(event_stream())
