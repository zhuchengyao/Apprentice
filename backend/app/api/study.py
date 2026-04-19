"""Study session API — guided four-phase flow (READ → EXPLAIN → PRACTICE → FEEDBACK).

A StudySession is scoped to (user, chapter). Its `scope_plan` is an ordered
JSONB array of KP clusters produced by `plan_scopes` at session creation. The
client drives the phase machine via `/advance`, `/questions`, `/answer`, and
`/next-scope` endpoints.

The EXPLAIN phase streams via SSE using the same cached 4-block system prompt
the tutor chat uses; a TutorConversation is created lazily and linked via
`study_session_id` so the explanation turn participates in prompt cache reuse.
"""

from __future__ import annotations

import json
import logging
import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, func, text, update
from sqlalchemy.ext.asyncio import AsyncSession
from sse_starlette.sse import EventSourceResponse

from app.config import settings
from app.database import get_db
from app.dependencies import get_current_user
from app.i18n import get_request_locale
from app.models.book import Book, Chapter, KnowledgePoint
from app.models.study import (
    QuizAttempt,
    QuizQuestion,
    StudyPhase,
    StudySession,
)
from app.models.tutor import TutorConversation
from app.models.user import User
from app.services.ai_client import chat_completion_stream
from app.services.ai_context import ai_user_context
from app.services.billing import check_credits_or_raise
from app.services.learning.mastery import (
    QUALITY_CLARIFY,
    QUALITY_UNDERSTOOD,
    record_kp_exposure,
    update_mastery,
)
from app.services.teaching.agent import get_chapter_knowledge_points
from app.services.teaching.context import (
    load_chapter_context,
    load_chapter_context_for,
    load_kp_list_text,
    load_student_block,
)
from app.services.teaching.errors import (
    TutorLLMError,
    TutorPersistError,
    log_stream_failure,
    stream_error_payload,
)
from app.services.teaching.prompts import (
    TUTOR_STATIC_RULES,
    build_explain_scope_task,
    build_task_block,
    build_tutor_context,
)
from app.services.learning.adaptive import choose_quiz_plan
from app.services.teaching.quiz import generate_quiz_for_scope
from app.services.teaching.study_planner import plan_scopes

logger = logging.getLogger(__name__)

router = APIRouter()

# Cap on the explanation text echoed back in the SSE `done` event. The full
# text already streamed token-by-token; this just bounds the final summary
# payload so an unexpectedly long response doesn't pin large strings.
EXPLAIN_DONE_PAYLOAD_CAP = 20_000

# Upper bound on how many cached questions per scope_signature we need to
# inspect when deciding scope-complete. plan.count is 2-5; this is generous.
SCOPE_QUESTION_FETCH_CAP = 50

# Generous token budgets for reasoning models (gpt-5-class) where a large
# fraction of `max_completion_tokens` is spent on internal reasoning that
# never becomes output content. A tight budget causes zero-content streams.
EXPLAIN_MAX_TOKENS = 8192
QUIZ_MAX_TOKENS = 8192


# ── Schemas ───────────────────────────────────────────────────

class StartSessionRequest(BaseModel):
    book_id: str
    chapter_id: str


class ScopeView(BaseModel):
    index: int
    title: str
    anchor_hint: str
    kp_ids: list[str]
    source_anchors: list[str]


class AttemptView(BaseModel):
    question_id: str
    chosen_option: str
    correct: bool


class SessionResponse(BaseModel):
    id: str
    book_id: str
    chapter_id: str
    phase: str
    current_scope_index: int
    total_scopes: int
    current_question_index: int
    scope: ScopeView | None
    attempts: list[AttemptView]
    completed_at: str | None


class QuestionView(BaseModel):
    id: str
    stem: str
    options: list[dict]
    difficulty: int


class QuestionsResponse(BaseModel):
    scope_index: int
    total: int
    questions: list[QuestionView]
    answered: list[AttemptView]


class AnswerRequest(BaseModel):
    question_id: str
    chosen_option: str
    time_spent_ms: int = 0


class AnswerResponse(BaseModel):
    correct: bool
    correct_option: str
    explanation: str
    scope_score: dict  # {"correct": int, "total": int}
    next_question_id: str | None
    scope_complete: bool


class NextScopeResponse(BaseModel):
    session: SessionResponse
    done: bool


# ── Helpers ───────────────────────────────────────────────────

def _now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


async def _load_session(
    session_id: str, user: User, db: AsyncSession
) -> StudySession:
    try:
        sid = uuid.UUID(session_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid session id")
    session = await db.get(StudySession, sid)
    if session is None:
        raise HTTPException(status_code=404, detail="Study session not found")
    if session.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return session


def _current_scope(session: StudySession) -> dict | None:
    plan = session.scope_plan or []
    idx = session.current_scope_index
    if 0 <= idx < len(plan):
        return plan[idx]
    return None


def _anchors_for_scope(
    scope: dict, kps_by_id: dict[str, KnowledgePoint]
) -> list[str]:
    anchors: list[str] = []
    for kp_id in scope.get("kp_ids", []):
        kp = kps_by_id.get(str(kp_id))
        if kp and kp.source_anchor:
            anchors.append(kp.source_anchor)
    return anchors


def _scope_view(
    session: StudySession, kps_by_id: dict[str, KnowledgePoint]
) -> ScopeView | None:
    scope = _current_scope(session)
    if not scope:
        return None
    return ScopeView(
        index=session.current_scope_index,
        title=scope.get("title", ""),
        anchor_hint=scope.get("anchor_hint", ""),
        kp_ids=[str(k) for k in scope.get("kp_ids", [])],
        source_anchors=_anchors_for_scope(scope, kps_by_id),
    )


async def _attempts_for_scope(
    db: AsyncSession, session_id: uuid.UUID, scope_index: int
) -> list[QuizAttempt]:
    result = await db.execute(
        select(QuizAttempt)
        .where(
            QuizAttempt.session_id == session_id,
            QuizAttempt.scope_index == scope_index,
        )
        .order_by(QuizAttempt.answered_at)
    )
    return list(result.scalars().all())


def _attempt_views(attempts: list[QuizAttempt]) -> list[AttemptView]:
    return [
        AttemptView(
            question_id=str(a.question_id),
            chosen_option=a.chosen_option,
            correct=a.correct,
        )
        for a in attempts
    ]


async def _session_response(
    session: StudySession,
    db: AsyncSession,
    kps_by_id: dict[str, KnowledgePoint],
) -> SessionResponse:
    attempts = await _attempts_for_scope(db, session.id, session.current_scope_index)
    plan = session.scope_plan or []
    return SessionResponse(
        id=str(session.id),
        book_id=str(session.book_id),
        chapter_id=str(session.chapter_id),
        phase=session.phase.value,
        current_scope_index=session.current_scope_index,
        total_scopes=len(plan),
        current_question_index=session.current_question_index,
        scope=_scope_view(session, kps_by_id),
        attempts=_attempt_views(attempts),
        completed_at=session.completed_at.isoformat() if session.completed_at else None,
    )


async def _ensure_tutor_conversation(
    session: StudySession, db: AsyncSession
) -> TutorConversation:
    if session.tutor_conversation_id:
        conv = await db.get(TutorConversation, session.tutor_conversation_id)
        if conv is not None:
            return conv
    conv = TutorConversation(
        user_id=session.user_id,
        book_id=session.book_id,
        chapter_id=session.chapter_id,
        study_session_id=session.id,
        current_kp_index=0,
    )
    db.add(conv)
    await db.flush()
    session.tutor_conversation_id = conv.id
    await db.commit()
    await db.refresh(conv)
    return conv


def _kp_index_by_id(kps: list[KnowledgePoint]) -> dict[str, KnowledgePoint]:
    return {str(kp.id): kp for kp in kps}


def _scope_kp_triples(
    scope: dict, kps_by_id: dict[str, KnowledgePoint]
) -> list[tuple[str, str, str]]:
    triples: list[tuple[str, str, str]] = []
    for kp_id in scope.get("kp_ids", []):
        kp = kps_by_id.get(str(kp_id))
        if kp:
            triples.append((str(kp.id), kp.concept, (kp.explanation or "")[:500]))
    return triples


# ── Endpoints ─────────────────────────────────────────────────

@router.post("/sessions", response_model=SessionResponse)
async def start_or_resume_session(
    body: StartSessionRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    request_locale: str = Depends(get_request_locale),
):
    """Start a new session or resume an existing one for (user, chapter).

    On creation: plan scopes via LLM, persist. On resume: return current state.
    """
    try:
        book_id = uuid.UUID(body.book_id)
        chapter_id = uuid.UUID(body.chapter_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid book_id or chapter_id")

    chapter = await db.get(Chapter, chapter_id)
    if chapter is None or chapter.book_id != book_id:
        raise HTTPException(status_code=404, detail="Chapter not found")
    book = await db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    # Serialize concurrent create-or-resume calls for the same (user,
    # chapter) pair. Without this, two near-simultaneous requests (React
    # StrictMode dev double-mount, fast double-click, multiple tabs) both
    # see "no session" → both call plan_scopes (LLM, expensive) → both
    # try to INSERT and the loser crashes on uq_study_sessions_user_chapter.
    # The xact lock auto-releases on commit/rollback.
    await db.execute(
        text("SELECT pg_advisory_xact_lock(hashtextextended(:key, 0))"),
        {"key": f"study_session:{current_user.id}:{chapter_id}"},
    )

    all_kps = await get_chapter_knowledge_points(chapter_id, db)
    kps_by_id = _kp_index_by_id(all_kps)

    result = await db.execute(
        select(StudySession).where(
            StudySession.user_id == current_user.id,
            StudySession.chapter_id == chapter_id,
        )
    )
    session = result.scalar_one_or_none()

    if session is not None:
        # Resume — but if the chapter's KP set has drifted, re-plan.
        planned_ids = {
            str(kp_id)
            for scope in (session.scope_plan or [])
            for kp_id in scope.get("kp_ids", [])
        }
        current_ids = {str(kp.id) for kp in all_kps}
        if planned_ids != current_ids and all_kps:
            logger.info(
                "Re-planning study session %s due to KP drift", session.id
            )
            session = await _replan_session(
                session, chapter, all_kps, current_user, db, request_locale
            )
        return await _session_response(session, db, kps_by_id)

    if not all_kps:
        raise HTTPException(
            status_code=409,
            detail="Chapter has no knowledge points yet; try again after processing.",
        )

    _, _, chapter_content = await load_chapter_context_for(book_id, chapter_id, db)
    student_block = _render_student_block(current_user)

    scope_plans = await plan_scopes(
        chapter=chapter,
        book_title=book.title,
        chapter_content=chapter_content,
        kps=all_kps,
        student_block=student_block,
        language=request_locale,
    )

    session = StudySession(
        user_id=current_user.id,
        book_id=book_id,
        chapter_id=chapter_id,
        phase=StudyPhase.read,
        scope_plan=[p.to_dict() for p in scope_plans],
        current_scope_index=0,
        current_question_index=0,
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)

    return await _session_response(session, db, kps_by_id)


async def _replan_session(
    session: StudySession,
    chapter: Chapter,
    kps: list[KnowledgePoint],
    current_user: User,
    db: AsyncSession,
    language: str,
) -> StudySession:
    book = await db.get(Book, session.book_id)
    _, _, chapter_content = await load_chapter_context_for(
        session.book_id, session.chapter_id, db
    )
    student_block = _render_student_block(current_user)
    scope_plans = await plan_scopes(
        chapter=chapter,
        book_title=book.title if book else "",
        chapter_content=chapter_content,
        kps=kps,
        student_block=student_block,
        language=language,
    )
    session.scope_plan = [p.to_dict() for p in scope_plans]
    session.phase = StudyPhase.read
    session.current_scope_index = 0
    session.current_question_index = 0
    session.completed_at = None
    await db.commit()
    await db.refresh(session)
    return session


def _render_student_block(user: User) -> str:
    """Compact student block for scope planning / quiz generation.

    Uses the learner profile directly; `recent_kp_signals` is reserved for
    tutor-conversation turns where we also cache the block on the conversation.
    """
    from app.services.teaching.prompts import build_student_block

    return build_student_block(user.learner_profile, [], [])


@router.get("/sessions/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = await _load_session(session_id, current_user, db)
    all_kps = await get_chapter_knowledge_points(session.chapter_id, db)
    return await _session_response(session, db, _kp_index_by_id(all_kps))


@router.post("/sessions/{session_id}/advance")
async def advance_to_explain(
    session_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    request_locale: str = Depends(get_request_locale),
):
    """READ → EXPLAIN: streams the scope explanation via SSE.

    Idempotent by phase: if the session is already past READ we re-stream
    an explanation for the current scope (useful if the client dropped the
    previous stream).
    """
    session = await _load_session(session_id, current_user, db)
    scope = _current_scope(session)
    if scope is None:
        raise HTTPException(status_code=409, detail="No active scope")

    all_kps = await get_chapter_knowledge_points(session.chapter_id, db)
    kps_by_id = _kp_index_by_id(all_kps)
    scope_kps = [kps_by_id[str(k)] for k in scope.get("kp_ids", []) if str(k) in kps_by_id]

    conversation = await _ensure_tutor_conversation(session, db)
    book_title, chapter_title, chapter_content = await load_chapter_context(conversation, db)
    kp_list_text = await load_kp_list_text(conversation, all_kps, db)
    student_block = await load_student_block(conversation, current_user, db)

    task_text = build_task_block(
        build_explain_scope_task(
            scope.get("title", ""),
            [(str(kp.id), kp.concept, (kp.explanation or "")[:500]) for kp in scope_kps],
        )
    )
    context_text = build_tutor_context(
        book_title, chapter_title, chapter_content,
        knowledge_points_text=kp_list_text,
        language=request_locale,
    )
    system_blocks = [
        {"type": "text", "text": TUTOR_STATIC_RULES},
        {"type": "text", "text": context_text, "cache_control": {"type": "ephemeral"}},
        {"type": "text", "text": student_block, "cache_control": {"type": "ephemeral"}},
        {"type": "text", "text": task_text},
    ]

    # gpt-5-class reasoning models spend a significant slice of
    # `max_completion_tokens` on internal reasoning that never surfaces as
    # output content. With 2048 and a big system prompt (chapter + KPs +
    # student block) the model frequently burned the entire budget on
    # reasoning and emitted zero content — the stream ended with only a
    # usage chunk, the backend yielded `done` with empty content, and the
    # UI flashed the Explain header then jumped to Practice.
    await check_credits_or_raise(
        db, current_user.id, model=settings.tutor_model, max_tokens=EXPLAIN_MAX_TOKENS
    )

    user_id_str = str(current_user.id)
    user_uuid = current_user.id
    session_id_uuid = session.id
    exposed_kp_ids = [kp.id for kp in scope_kps]

    # Immediately advance phase to EXPLAIN so clients that drop the stream
    # can resume by calling /advance again without reverting state.
    if session.phase == StudyPhase.read:
        session.phase = StudyPhase.explain
        await db.commit()

    async def event_stream():
        with ai_user_context(user_id_str):
            collected: list[str] = []
            collected_size = 0
            try:
                try:
                    async for chunk in chat_completion_stream(
                        messages=[{"role": "user", "content": "请开始。"}],
                        max_tokens=EXPLAIN_MAX_TOKENS,
                        model=settings.tutor_model,
                        caller="study_explain",
                        system=system_blocks,
                    ):
                        # Stream every token to the client; cap what we keep
                        # in memory for the final `done` payload so a runaway
                        # response doesn't pin a large string per request.
                        if collected_size < EXPLAIN_DONE_PAYLOAD_CAP:
                            collected.append(chunk)
                            collected_size += len(chunk)
                        yield {"event": "token", "data": chunk}
                except Exception as e:
                    raise TutorLLMError() from e

                full_text = "".join(collected)
                if collected_size >= EXPLAIN_DONE_PAYLOAD_CAP:
                    full_text = full_text[:EXPLAIN_DONE_PAYLOAD_CAP] + "\n\n[…]"

                try:
                    from app.database import async_session
                    async with async_session() as save_db:
                        # Atomic phase transition: only one concurrent stream
                        # for this session "wins" the EXPLAIN→PRACTICE flip,
                        # avoiding double-advance if the user opened the
                        # session in two tabs.
                        result = await save_db.execute(
                            update(StudySession)
                            .where(
                                StudySession.id == session_id_uuid,
                                StudySession.phase == StudyPhase.explain,
                            )
                            .values(phase=StudyPhase.practice)
                        )
                        if result.rowcount:
                            for kp_id in exposed_kp_ids:
                                await record_kp_exposure(save_db, user_uuid, kp_id)
                        await save_db.commit()
                except Exception as e:
                    raise TutorPersistError() from e

                yield {
                    "event": "done",
                    "data": json.dumps({
                        "content": full_text,
                        "next_phase": StudyPhase.practice.value,
                    }),
                }
            except Exception as e:
                log_stream_failure(logger, "study_explain", e)
                yield {"event": "error", "data": stream_error_payload(e)}

    return EventSourceResponse(event_stream())


@router.get("/sessions/{session_id}/questions", response_model=QuestionsResponse)
async def get_scope_questions(
    session_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    request_locale: str = Depends(get_request_locale),
):
    """Return questions for the current scope. Lazily generates on first hit."""
    session = await _load_session(session_id, current_user, db)
    scope = _current_scope(session)
    if scope is None:
        raise HTTPException(status_code=409, detail="No active scope")

    all_kps = await get_chapter_knowledge_points(session.chapter_id, db)
    kps_by_id = _kp_index_by_id(all_kps)
    scope_kps = [kps_by_id[str(k)] for k in scope.get("kp_ids", []) if str(k) in kps_by_id]
    if not scope_kps:
        raise HTTPException(status_code=409, detail="Scope has no resolvable KPs")

    plan = await choose_quiz_plan(db, current_user.id, scope_kps)

    conversation = await _ensure_tutor_conversation(session, db)
    book_title, chapter_title, chapter_content = await load_chapter_context(conversation, db)
    kp_list_text = await load_kp_list_text(conversation, all_kps, db)
    student_block = await load_student_block(conversation, current_user, db)

    await check_credits_or_raise(
        db, current_user.id, model=settings.tutor_model, max_tokens=QUIZ_MAX_TOKENS
    )

    with ai_user_context(str(current_user.id)):
        questions = await generate_quiz_for_scope(
            kps=scope_kps,
            plan=plan,
            db=db,
            book_title=book_title,
            chapter_title=chapter_title,
            chapter_content=chapter_content,
            kp_list_text=kp_list_text,
            student_block=student_block,
            language=request_locale,
        )

    if not questions:
        raise HTTPException(status_code=502, detail="Failed to generate questions")

    if session.phase == StudyPhase.explain:
        session.phase = StudyPhase.practice

    attempts = await _attempts_for_scope(db, session.id, session.current_scope_index)
    answered_ids = {str(a.question_id) for a in attempts}
    unanswered = [q for q in questions if str(q.id) not in answered_ids]

    # Session might have an index beyond what we just sliced — normalize.
    if not unanswered:
        session.current_question_index = len(questions)
    else:
        session.current_question_index = questions.index(unanswered[0])
    await db.commit()

    return QuestionsResponse(
        scope_index=session.current_scope_index,
        total=len(questions),
        questions=[
            QuestionView(
                id=str(q.id),
                stem=q.stem,
                options=q.options,
                difficulty=q.difficulty,
            )
            for q in questions
        ],
        answered=_attempt_views(attempts),
    )


@router.post("/sessions/{session_id}/answer", response_model=AnswerResponse)
async def answer_question(
    session_id: str,
    body: AnswerRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = await _load_session(session_id, current_user, db)
    try:
        qid = uuid.UUID(body.question_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid question_id")

    question = await db.get(QuizQuestion, qid)
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    chosen = body.chosen_option.strip().upper()
    if chosen not in ("A", "B", "C", "D"):
        raise HTTPException(status_code=400, detail="chosen_option must be A/B/C/D")

    # Idempotency: if this question was already answered in this scope,
    # return the original attempt's verdict rather than double-counting.
    existing_result = await db.execute(
        select(QuizAttempt).where(
            QuizAttempt.session_id == session.id,
            QuizAttempt.question_id == qid,
            QuizAttempt.scope_index == session.current_scope_index,
        )
    )
    existing = existing_result.scalar_one_or_none()
    if existing is None:
        correct = chosen == question.correct_option
        attempt = QuizAttempt(
            session_id=session.id,
            question_id=qid,
            scope_index=session.current_scope_index,
            chosen_option=chosen,
            correct=correct,
            time_spent_ms=max(0, int(body.time_spent_ms)),
        )
        db.add(attempt)

        primary_kp_id: uuid.UUID | None = None
        for kp_id in question.kp_ids or []:
            try:
                primary_kp_id = uuid.UUID(str(kp_id))
                break
            except ValueError:
                continue
        if primary_kp_id is not None:
            quality = QUALITY_UNDERSTOOD if correct else QUALITY_CLARIFY
            await update_mastery(db, current_user.id, primary_kp_id, quality)
    else:
        correct = existing.correct

    # Refresh attempts + decide whether the scope is complete.
    attempts = await _attempts_for_scope(db, session.id, session.current_scope_index)
    # We only need the ordered id list to compare against attempts; the full
    # row payloads aren't used. Cap the cache fetch — even popular scopes
    # never serve more than MAX_QUESTIONS in a single session.
    signature_result = await db.execute(
        select(QuizQuestion.id)
        .where(QuizQuestion.scope_signature == question.scope_signature)
        .order_by(QuizQuestion.generated_at)
        .limit(SCOPE_QUESTION_FETCH_CAP)
    )
    scope_question_ids = list(signature_result.scalars().all())
    answered_ids = {a.question_id for a in attempts}
    remaining_ids = [qid for qid in scope_question_ids if qid not in answered_ids]
    scope_complete = len(remaining_ids) == 0

    if scope_complete:
        session.phase = StudyPhase.feedback
        session.current_question_index = len(scope_question_ids)
    else:
        session.current_question_index = scope_question_ids.index(remaining_ids[0])
    await db.commit()

    return AnswerResponse(
        correct=correct,
        correct_option=question.correct_option,
        explanation=question.explanation,
        scope_score={
            "correct": sum(1 for a in attempts if a.correct),
            "total": len(attempts),
        },
        next_question_id=str(remaining_ids[0]) if remaining_ids else None,
        scope_complete=scope_complete,
    )


@router.post("/sessions/{session_id}/next-scope", response_model=NextScopeResponse)
async def advance_to_next_scope(
    session_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = await _load_session(session_id, current_user, db)
    plan = session.scope_plan or []
    next_index = session.current_scope_index + 1
    done = next_index >= len(plan)
    if done:
        session.phase = StudyPhase.done
        if session.completed_at is None:
            session.completed_at = _now()
    else:
        session.current_scope_index = next_index
        session.current_question_index = 0
        session.phase = StudyPhase.read
    await db.commit()
    await db.refresh(session)

    all_kps = await get_chapter_knowledge_points(session.chapter_id, db)
    return NextScopeResponse(
        session=await _session_response(session, db, _kp_index_by_id(all_kps)),
        done=done,
    )
