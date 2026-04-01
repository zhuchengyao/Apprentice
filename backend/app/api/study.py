import logging
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sse_starlette.sse import EventSourceResponse

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
            kp = KnowledgePoint(
                section_id=section.id,
                concept=kp_data["concept"],
                explanation=kp_data["explanation"],
                difficulty=kp_data.get("difficulty", 2),
                order_index=kp_data.get("order_index", 0),
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


@router.post("/sessions", response_model=StudySessionResponse)
async def create_session(
    body: CreateSessionRequest,
    db: AsyncSession = Depends(get_db),
):
    section_id = uuid.UUID(body.section_id)
    book_id = uuid.UUID(body.book_id)

    # Load section with its knowledge points
    result = await db.execute(
        select(Section)
        .where(Section.id == section_id)
        .options(selectinload(Section.knowledge_points))
    )
    section = result.scalar_one_or_none()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    # Get section title and chapter for context
    chapter_result = await db.execute(
        select(Chapter).where(Chapter.id == section.chapter_id)
    )
    chapter = chapter_result.scalar_one_or_none()
    section_title = f"{chapter.title} - {section.title}" if chapter else section.title

    # Extract KPs on demand if not yet done
    kps = await _ensure_knowledge_points(section, db)
    if not kps:
        raise HTTPException(status_code=400, detail="Section has no knowledge points")

    # Create DB session
    study_session = StudySession(
        user_id=DEFAULT_USER_ID,
        book_id=book_id,
        section_id=section_id,
        started_at=datetime.utcnow(),
    )
    db.add(study_session)
    await db.commit()
    await db.refresh(study_session)

    session_id = str(study_session.id)

    # Build KP data for the agent
    kp_data = [
        {
            "id": str(kp.id),
            "concept": kp.concept,
            "explanation": kp.explanation,
            "difficulty": kp.difficulty,
        }
        for kp in kps
    ]

    # Create and register the teaching agent
    agent = TeachingAgent(
        session_id=session_id,
        section_id=body.section_id,
        knowledge_points=kp_data,
        section_title=section_title,
    )
    register_agent(session_id, agent)

    return StudySessionResponse(
        id=session_id,
        book_id=body.book_id,
        section_id=body.section_id,
        current_kp_index=0,
        state="explain",
        messages=[],
        knowledge_points=[
            KnowledgePointBrief(
                id=kp["id"],
                concept=kp["concept"],
                explanation=kp["explanation"],
                difficulty=kp["difficulty"],
            )
            for kp in kp_data
        ],
    )


@router.get("/sessions/{session_id}/stream")
async def stream_session(session_id: str):
    agent = get_agent(session_id)
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
async def send_message(session_id: str, body: UserMessageRequest):
    agent = get_agent(session_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Session not found or expired")

    agent.receive_message(body.content)
    return {"status": "ok"}
