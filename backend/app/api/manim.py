"""Experimental Manim animation endpoints.

POST /api/manim/generate       → render an MP4 for a concept label.
GET  /api/manim/video/{name}   → stream a previously-rendered MP4.

Used by the `/manim-lab` frontend page — not part of the KP flow yet.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app.config import settings
from app.dependencies import get_current_user
from app.models.user import User
from app.services.extractor.manim_v2 import generate_manim_animation

logger = logging.getLogger(__name__)

router = APIRouter()

_MANIM_DIR = (Path(settings.upload_dir).resolve() / "manim")
_SAFE_NAME_RE = re.compile(r"^manim_[a-f0-9]{32}\.mp4$")


class ManimGenerateRequest(BaseModel):
    concept: str = Field(min_length=1, max_length=300)
    quality: str = Field(default="low", pattern=r"^(low|medium|high)$")
    model: str | None = None


class ManimGenerateResponse(BaseModel):
    accepted: bool
    failure_kind: str
    failure_detail: str | None = None
    decline_reason: str | None = None
    latency_ms: int
    filename: str | None = None
    render_stderr_tail: str | None = None
    code: str | None = None


@router.post("/generate", response_model=ManimGenerateResponse)
async def generate(
    body: ManimGenerateRequest,
    user: User = Depends(get_current_user),
) -> ManimGenerateResponse:
    outcome = await generate_manim_animation(
        body.concept,
        model=body.model,
        quality=body.quality,
        caller="manim_lab",
        output_dir=_MANIM_DIR,
    )

    filename = outcome.output_path.name if outcome.output_path else None
    logger.info(
        "manim_lab user=%s accepted=%s kind=%s latency_ms=%d",
        user.id, outcome.accepted, outcome.failure_kind, outcome.latency_ms,
    )
    return ManimGenerateResponse(
        accepted=outcome.accepted,
        failure_kind=outcome.failure_kind,
        failure_detail=outcome.failure_detail,
        decline_reason=outcome.decline_reason,
        latency_ms=outcome.latency_ms,
        filename=filename,
        render_stderr_tail=outcome.render_stderr_tail,
        code=outcome.code if not outcome.accepted else None,
    )


@router.get("/video/{filename}")
async def get_video(filename: str, user: User = Depends(get_current_user)):
    if not _SAFE_NAME_RE.match(filename):
        raise HTTPException(status_code=400, detail="Invalid filename")
    path = (_MANIM_DIR / filename).resolve()
    if not path.is_relative_to(_MANIM_DIR):
        raise HTTPException(status_code=400, detail="Invalid path")
    if not path.is_file():
        raise HTTPException(status_code=404, detail="Video not found")
    return FileResponse(path, media_type="video/mp4")
