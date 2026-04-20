"""Tutor chat API — structured knowledge-point-by-knowledge-point teaching."""

import json
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
from app.i18n import effective_teaching_language, get_request_locale
from app.models.book import KnowledgePoint
from app.models.user import User
from app.models.tutor import TutorConversation, TutorMessage
from app.services.ai_context import ai_user_context
from app.services.billing import check_credits_or_raise
from app.services.teaching.agent import (
    get_chapter_knowledge_points,
    plan_next_step,
    parse_comprehension_verdict,
    parse_profile_notes,
    VerdictStreamFilter,
)
from app.services.teaching.context import (
    kp_highlight_data,
    load_chapter_context,
    load_kp_list_text,
    load_student_block,
    recent_api_messages,
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
from app.services.teaching.streaming import (
    iter_llm_chunks,
    save_assistant_turn,
    wrap_sse_errors,
)

router = APIRouter()

# Reasoning models (gpt-5-class) spend most of their budget on internal
# thought that never becomes output content. Tight ceilings (1024/2048)
# regularly yielded zero-token streams — the UI would show the header and
# immediately move on. 8192 gives the reasoner room to think and still
# emit a full conversational turn.
TUTOR_MAX_TOKENS = 8192


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
    load_messages: bool = False,
) -> TutorConversation:
    """Load a conversation owned by current_user or raise 404/403.

    Messages are NOT loaded by default — hot-path endpoints use
    ``recent_api_messages`` to fetch a bounded tail instead.
    """
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


def _build_system_blocks(
    book_title: str,
    chapter_title: str,
    chapter_content: str,
    kp_list_text: str,
    student_block: str,
    current_task: str,
    language: str,
) -> list[dict]:
    # Four blocks with two cache breakpoints:
    #   0. static rules (global cache prefix, cached with block 1)
    #   1. chapter context — expensive; cached per-conversation (1h TTL —
    #      a study session typically spans 15–45 min, exceeding the 5-min default)
    #   2. student block  — cached per-student; invalidated on profile update
    #   3. per-turn task  — uncached
    #
    # Two cache_control markers let block 1's cache survive even when
    # block 2 changes (the prefix up to block 1 still matches).
    # Markers are no-ops for non-Anthropic providers.
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
            "cache_control": {"type": "ephemeral", "ttl": "1h"},
        },
        {
            "type": "text",
            "text": student_block,
            "cache_control": {"type": "ephemeral"},
        },
        {"type": "text", "text": task_text},
    ]


async def _prepare_tutor_system(
    conversation: TutorConversation,
    current_user: User,
    db: AsyncSession,
    all_kps: list[KnowledgePoint],
    *,
    task_text: str,
    language: str,
) -> list[dict]:
    """Load cached per-conversation context and build the system prompt blocks.

    Callers pass in `all_kps` (they already need it for planning/highlighting)
    so we don't re-query.
    """
    book_title, chapter_title, chapter_content = await load_chapter_context(
        conversation, db
    )
    kp_list_text = await load_kp_list_text(conversation, all_kps, db)
    student_block = await load_student_block(conversation, current_user, db)
    return _build_system_blocks(
        book_title, chapter_title, chapter_content,
        kp_list_text, student_block, task_text,
        language=language,
    )


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
    conversation = await _get_user_conversation(
        conversation_id, current_user, db, load_messages=True
    )

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

    has_message = await db.scalar(
        select(TutorMessage.id)
        .where(TutorMessage.conversation_id == conv_id)
        .limit(1)
    )
    if has_message:
        raise HTTPException(status_code=409, detail="Conversation already has messages")

    all_kps = await get_chapter_knowledge_points(conversation.chapter_id, db)
    system_blocks = await _prepare_tutor_system(
        conversation, current_user, db, all_kps,
        task_text=TASK_OPENING,
        language=effective_teaching_language(
            current_user.preferred_language, request_locale
        ),
    )
    api_messages = [{"role": "user", "content": "请开始"}]

    await check_credits_or_raise(
        db, conversation.user_id, model=settings.tutor_model, max_tokens=TUTOR_MAX_TOKENS
    )

    user_id_str = str(conversation.user_id)
    user_uuid = conversation.user_id

    async def body():
        with ai_user_context(user_id_str):
            collected: list[str] = []
            async for chunk in iter_llm_chunks(
                messages=api_messages,
                max_tokens=TUTOR_MAX_TOKENS,
                model=settings.tutor_model,
                caller="tutor_opening",
                system=system_blocks,
            ):
                collected.append(chunk)
                yield {"event": "token", "data": chunk}

            full_text = "".join(collected)
            cleaned_text, profile_notes = parse_profile_notes(full_text)
            opening_metadata = {"type": "opening", "action": "continue"}

            msg_id = await save_assistant_turn(
                conv_id=conv_id,
                user_id=user_uuid,
                content=cleaned_text,
                metadata=opening_metadata,
                profile_notes=profile_notes,
            )

            yield {
                "event": "done",
                "data": json.dumps({
                    "id": msg_id,
                    "content": cleaned_text,
                    "action": "continue",
                    "metadata": opening_metadata,
                }),
            }

    return EventSourceResponse(wrap_sse_errors("tutor_opening", body()))


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

    if len(step.knowledge_points) == 1:
        kp = step.knowledge_points[0]
        kp_global_idx = conversation.current_kp_index
        task_text = build_teach_task(kp_global_idx, kp.concept, kp.explanation)
    else:
        batch_data = []
        for i, kp in enumerate(step.knowledge_points):
            batch_data.append((conversation.current_kp_index + i, kp.concept, kp.explanation))
        task_text = build_batch_task(batch_data)

    system_blocks = await _prepare_tutor_system(
        conversation, current_user, db, all_kps,
        task_text=task_text,
        language=effective_teaching_language(
            current_user.preferred_language, request_locale
        ),
    )

    history = await recent_api_messages(conv_id, db)
    api_messages = history + [{"role": "user", "content": "请讲解下一个知识点。"}]

    highlight_data = kp_highlight_data(step.knowledge_points)

    await check_credits_or_raise(
        db, conversation.user_id, model=settings.tutor_model, max_tokens=TUTOR_MAX_TOKENS
    )

    new_kp_index = step.kp_end_index
    action = step.action
    user_id_str = str(conversation.user_id)
    user_uuid = conversation.user_id
    taught_kp_ids = [kp.id for kp in step.knowledge_points]

    async def body():
        yield {
            "event": "highlight",
            "data": json.dumps(highlight_data),
        }

        with ai_user_context(user_id_str):
            collected: list[str] = []
            async for chunk in iter_llm_chunks(
                messages=api_messages,
                max_tokens=TUTOR_MAX_TOKENS,
                model=settings.tutor_model,
                caller="tutor_teach",
                system=system_blocks,
            ):
                collected.append(chunk)
                yield {"event": "token", "data": chunk}

            full_text = "".join(collected)
            cleaned_text, profile_notes = parse_profile_notes(full_text)

            kp_ids = [str(kp.id) for kp in step.knowledge_points]
            msg_metadata = {
                "type": "teach",
                "knowledge_point_ids": kp_ids,
                "action": action,
            }

            msg_id = await save_assistant_turn(
                conv_id=conv_id,
                user_id=user_uuid,
                content=cleaned_text,
                metadata=msg_metadata,
                profile_notes=profile_notes,
                exposed_kp_ids=taught_kp_ids,
                advance_kp_index=new_kp_index,
            )

            yield {
                "event": "done",
                "data": json.dumps({
                    "id": msg_id,
                    "content": cleaned_text,
                    "action": action,
                    "kp_index": new_kp_index,
                    "total_kps": len(all_kps),
                    "metadata": msg_metadata,
                }),
            }

    return EventSourceResponse(wrap_sse_errors("tutor_teach", body()))


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

    all_kps = await get_chapter_knowledge_points(conversation.chapter_id, db)

    kp_index = max(0, conversation.current_kp_index - 1)
    current_kp: KnowledgePoint | None = None
    if kp_index < len(all_kps):
        current_kp = all_kps[kp_index]
        task_text = build_answer_task(kp_index, current_kp.concept)
    else:
        task_text = "Answer the student's question about this chapter."

    system_blocks = await _prepare_tutor_system(
        conversation, current_user, db, all_kps,
        task_text=task_text,
        language=effective_teaching_language(
            current_user.preferred_language, request_locale
        ),
    )

    api_messages = await recent_api_messages(conv_id, db)

    await check_credits_or_raise(
        db, conversation.user_id, model=settings.tutor_model, max_tokens=TUTOR_MAX_TOKENS
    )

    user_id_str = str(conversation.user_id)
    user_uuid = conversation.user_id
    verdict_kp_id = current_kp.id if current_kp is not None else None

    async def body():
        with ai_user_context(user_id_str):
            collected: list[str] = []
            vfilter = VerdictStreamFilter()
            async for chunk in iter_llm_chunks(
                messages=api_messages,
                max_tokens=TUTOR_MAX_TOKENS,
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
            # Strip profile notes first, then verdict from the tail.
            text_after_notes, profile_notes = parse_profile_notes(full_text)
            cleaned_text, action, verdict = parse_comprehension_verdict(
                text_after_notes
            )
            msg_metadata = {"type": "answer", "action": action}

            msg_id = await save_assistant_turn(
                conv_id=conv_id,
                user_id=user_uuid,
                content=cleaned_text,
                metadata=msg_metadata,
                profile_notes=profile_notes,
                verdict_kp_id=verdict_kp_id,
                verdict=verdict,
            )

            yield {
                "event": "done",
                "data": json.dumps({
                    "id": msg_id,
                    "content": cleaned_text,
                    "action": action,
                    "metadata": msg_metadata,
                }),
            }

    return EventSourceResponse(wrap_sse_errors("tutor_chat", body()))
