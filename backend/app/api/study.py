import json
import logging
import os
import re
import uuid
from datetime import UTC, datetime
from typing import Callable, Awaitable

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sse_starlette.sse import EventSourceResponse

from app.config import settings

from app.constants import DEFAULT_USER_ID
from app.database import get_db
from app.models.book import Section, KnowledgePoint, Chapter
from app.models.study import StudySession
from app.schemas.study import (
    CreateSessionRequest,
    StudySessionResponse,
    KnowledgePointBrief,
    UserMessageRequest,
)
from app.services.extractor.knowledge import extract_knowledge_points
from app.services.teaching.agent import (
    TeachingAgent,
    get_agent,
    register_agent,
)

logger = logging.getLogger(__name__)

router = APIRouter()


async def _ensure_knowledge_points(section: Section, db: AsyncSession) -> list[KnowledgePoint]:
    """Extract KPs on demand if the section doesn't have any yet."""
    if section.knowledge_points:
        return sorted(section.knowledge_points, key=lambda k: k.order_index)

    logger.info("Extracting knowledge points on demand for section '%s'", section.title)

    try:
        kp_result = await extract_knowledge_points(
            section.title,
            section.content_raw or "",
        )
        section.summary = kp_result.get("section_summary", "")

        kps = []
        for kp_data in kp_result.get("knowledge_points", []):
            image_refs = kp_data.get("image_refs", [])
            kp = KnowledgePoint(
                section_id=section.id,
                concept=kp_data["concept"],
                explanation=kp_data["explanation"],
                difficulty=kp_data.get("difficulty", 2),
                order_index=kp_data.get("order_index", 0),
                image_urls=json.dumps(image_refs) if image_refs else None,
            )
            db.add(kp)
            kps.append(kp)

    except Exception as e:
        logger.warning("KP extraction failed for section '%s': %s", section.title, e)
        kp = KnowledgePoint(
            section_id=section.id,
            concept=section.title,
            explanation=f"Key concepts from: {section.title}",
            difficulty=2,
            order_index=0,
        )
        db.add(kp)
        kps = [kp]

    await db.flush()
    return sorted(kps, key=lambda k: k.order_index)


def _build_kp_data(kps: list[KnowledgePoint]) -> list[dict]:
    """Build KP data dicts for the agent from ORM objects."""
    return [
        {
            "id": str(kp.id),
            "concept": kp.concept,
            "explanation": kp.explanation,
            "difficulty": kp.difficulty,
            "illustration": kp.illustration,
            "question": kp.question,
            "mastered": kp.mastered_at is not None,
            "image_urls": json.loads(kp.image_urls) if kp.image_urls else [],
        }
        for kp in kps
    ]


def _make_save_callbacks(
    session_id: str,
) -> tuple[
    Callable[[str, str], Awaitable[None]],
    Callable[[str, str], Awaitable[None]],
    Callable[[str], Awaitable[None]],
    Callable[[str, int], Awaitable[None]],
]:
    """Create the four DB persistence callbacks for a teaching agent."""
    from app.database import async_session

    async def _save_kp_field(kp_id: str, field: str, value) -> None:
        async with async_session() as session:
            result = await session.execute(
                select(KnowledgePoint).where(KnowledgePoint.id == uuid.UUID(kp_id))
            )
            kp_obj = result.scalar_one_or_none()
            if kp_obj:
                setattr(kp_obj, field, value)
                await session.commit()

    async def save_illustration(kp_id: str, text: str) -> None:
        await _save_kp_field(kp_id, "illustration", text)

    async def save_question(kp_id: str, text: str) -> None:
        await _save_kp_field(kp_id, "question", text)

    async def save_mastery(kp_id: str) -> None:
        await _save_kp_field(kp_id, "mastered_at", datetime.now(UTC).replace(tzinfo=None))

    async def save_state(sid: str, current_kp_index: int) -> None:
        async with async_session() as session:
            result = await session.execute(
                select(StudySession).where(StudySession.id == uuid.UUID(sid))
            )
            ss = result.scalar_one_or_none()
            if ss:
                ss.interactions = {"current_kp_index": current_kp_index}
                await session.commit()

    return save_illustration, save_question, save_mastery, save_state


def _extract_image_paths(section: Section) -> list[str]:
    """Extract local image file paths from section content."""
    image_paths = []
    raw_content = section.content_raw or ""
    for match in re.finditer(r'!\[[^\]]*\]\(/api/images/([^/]+)/([^)]+)\)', raw_content):
        bid, fname = match.group(1), match.group(2)
        img_path = os.path.join(settings.upload_dir, "images", bid, fname)
        if os.path.isfile(img_path):
            image_paths.append(img_path)
    return image_paths


async def _load_section_with_context(
    section_id: uuid.UUID, db: AsyncSession
) -> tuple[Section, str, list[KnowledgePoint]] | None:
    """Load a section with its KPs and chapter title. Returns None if not found."""
    result = await db.execute(
        select(Section)
        .where(Section.id == section_id)
        .options(selectinload(Section.knowledge_points))
    )
    section = result.scalar_one_or_none()
    if not section:
        return None

    chapter_result = await db.execute(
        select(Chapter).where(Chapter.id == section.chapter_id)
    )
    chapter = chapter_result.scalar_one_or_none()
    section_title = f"{chapter.title} - {section.title}" if chapter else section.title

    kps = await _ensure_knowledge_points(section, db)
    return section, section_title, kps


async def _recover_agent(session_id: str, db: AsyncSession) -> TeachingAgent | None:
    """Attempt to reconstruct a TeachingAgent from DB state."""
    result = await db.execute(
        select(StudySession).where(StudySession.id == uuid.UUID(session_id))
    )
    study_session = result.scalar_one_or_none()
    if not study_session or study_session.ended_at:
        return None

    loaded = await _load_section_with_context(study_session.section_id, db)
    if not loaded:
        return None
    section, section_title, kps = loaded

    if not kps:
        return None

    # Extract persisted state
    interactions = study_session.interactions or {}
    current_kp_index = interactions.get("current_kp_index", 0)

    kp_data = _build_kp_data(kps)
    save_illustration, save_question, save_mastery, save_state = _make_save_callbacks(session_id)
    section_image_paths = _extract_image_paths(section)

    agent = TeachingAgent.reconstruct(
        session_id=session_id,
        section_id=str(study_session.section_id),
        knowledge_points=kp_data,
        section_title=section_title,
        current_kp_index=current_kp_index,
        save_illustration_cb=save_illustration,
        save_question_cb=save_question,
        save_mastery_cb=save_mastery,
        save_state_cb=save_state,
        section_image_paths=section_image_paths,
    )
    register_agent(session_id, agent)
    logger.info("Reconstructed agent for session %s at KP index %d", session_id, current_kp_index)
    return agent


@router.post("/sessions", response_model=StudySessionResponse)
async def create_session(
    body: CreateSessionRequest,
    db: AsyncSession = Depends(get_db),
):
    section_id = uuid.UUID(body.section_id)
    book_id = uuid.UUID(body.book_id)

    loaded = await _load_section_with_context(section_id, db)
    if not loaded:
        raise HTTPException(status_code=404, detail="Section not found")
    section, section_title, kps = loaded

    if not kps:
        raise HTTPException(status_code=400, detail="Section has no knowledge points")

    # Reuse existing active session for this section if one exists
    existing_result = await db.execute(
        select(StudySession)
        .where(
            StudySession.section_id == section_id,
            StudySession.book_id == book_id,
            StudySession.ended_at.is_(None),
        )
        .order_by(StudySession.started_at.desc())
        .limit(1)
    )
    study_session = existing_result.scalar_one_or_none()

    if not study_session:
        study_session = StudySession(
            user_id=DEFAULT_USER_ID,
            book_id=book_id,
            section_id=section_id,
            started_at=datetime.now(UTC).replace(tzinfo=None),
        )
        db.add(study_session)
        await db.commit()
        await db.refresh(study_session)

    session_id = str(study_session.id)

    kp_data = _build_kp_data(kps)
    save_illustration, save_question, save_mastery, save_state = _make_save_callbacks(session_id)
    section_image_paths = _extract_image_paths(section)

    # Create and register the teaching agent
    agent = TeachingAgent(
        session_id=session_id,
        section_id=body.section_id,
        knowledge_points=kp_data,
        section_title=section_title,
        save_illustration_cb=save_illustration,
        save_question_cb=save_question,
        save_mastery_cb=save_mastery,
        save_state_cb=save_state,
        section_image_paths=section_image_paths,
    )
    register_agent(session_id, agent)

    # Find first non-mastered for initial state
    first_pending = next((i for i, kp in enumerate(kp_data) if not kp["mastered"]), len(kp_data))

    return StudySessionResponse(
        id=session_id,
        book_id=body.book_id,
        section_id=body.section_id,
        current_kp_index=first_pending,
        state="explain" if first_pending < len(kp_data) else "done",
        messages=[],
        knowledge_points=[
            KnowledgePointBrief(
                id=kp["id"],
                concept=kp["concept"],
                explanation=kp["explanation"],
                difficulty=kp["difficulty"],
                mastered=kp["mastered"],
                illustration=kp.get("illustration") or "",
                question=kp.get("question") or "",
                image_urls=kp.get("image_urls", []),
            )
            for kp in kp_data
        ],
    )


@router.get("/sessions/{session_id}/stream")
async def stream_session(session_id: str, db: AsyncSession = Depends(get_db)):
    agent = get_agent(session_id)

    if agent and agent.active:
        raise HTTPException(status_code=409, detail="Stream already connected for this session")

    if not agent:
        agent = await _recover_agent(session_id, db)

    if not agent:
        raise HTTPException(status_code=404, detail="Session not found or expired")

    async def event_stream():
        async for event in agent.event_generator():
            yield {
                "event": event["event"],
                "data": event["data"],
            }

    return EventSourceResponse(event_stream())


@router.post("/sessions/{session_id}/message")
async def send_message(
    session_id: str, body: UserMessageRequest, db: AsyncSession = Depends(get_db),
):
    agent = get_agent(session_id)
    if not agent:
        # Check if session exists but agent is not in memory
        result = await db.execute(
            select(StudySession).where(StudySession.id == uuid.UUID(session_id))
        )
        ss = result.scalar_one_or_none()
        if ss and not ss.ended_at:
            raise HTTPException(
                status_code=409,
                detail="Session exists but stream not connected. Reconnect to stream first.",
            )
        raise HTTPException(status_code=404, detail="Session not found or expired")

    agent.receive_message(body.content)
    return {"status": "ok"}
