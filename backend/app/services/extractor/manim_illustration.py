"""Experimental Manim-based animation generator.

Ask the LLM for a self-contained Manim `Scene` subclass, write it to a
temp .py file, and invoke the `manim` CLI to render MP4. Returns the
output path on success.

This is a proof-of-concept alongside the JSON-spec + Framer Motion
pipeline in `illustration.py`. It is intentionally not wired into the
KP extraction flow yet — callers are explicit (e.g. the
`scripts/manim_demo.py` CLI).
"""

from __future__ import annotations

import asyncio
import logging
import re
import shutil
import tempfile
import time
import uuid
from dataclasses import dataclass
from pathlib import Path

from app.config import settings
from app.services.ai_client import chat_completion
from app.services.extractor.manim_prompt import (
    build_system_blocks,
    build_user_message,
)

logger = logging.getLogger(__name__)


FailureKind = str  # "ok" | "declined" | "llm_error" | "no_code" | "unsafe"
                   #   | "render_timeout" | "render_error"


@dataclass
class ManimOutcome:
    code: str | None
    output_path: Path | None
    failure_kind: FailureKind
    failure_detail: str | None
    decline_reason: str | None
    latency_ms: int
    render_stderr_tail: str | None = None

    @property
    def accepted(self) -> bool:
        return self.output_path is not None


# ── Constants ─────────────────────────────────────────────────

_SCENE_CLASS_NAME = "Illustration"
_RENDER_TIMEOUT_SEC = 180
_MAX_CODE_BYTES = 32_000

# Simple static safety check — veto obvious escapes. Generated code
# runs in a subprocess with the project's venv, so a malicious prompt
# output could do anything Python can. These substrings are banned.
_FORBIDDEN_SUBSTRINGS = (
    "subprocess",
    "os.system",
    "os.popen",
    "pty.",
    "socket.",
    "http.client",
    "urllib",
    "requests.",
    "shutil.rmtree",
    "open(",  # No file I/O in generated scenes.
    "__import__",
    "eval(",
    "exec(",
    "compile(",
    "importlib",
    "sys.modules",
)

_ALLOWED_IMPORT_LINES_RE = re.compile(
    r"^\s*(from\s+manim\s+import\s+\*|import\s+numpy(\s+as\s+\w+)?|from\s+numpy\s+import\s+[\w\s,]+)\s*$"
)


# ── Output parsing ────────────────────────────────────────────

_FENCE_RE = re.compile(r"^\s*```(?:python|py)?\s*\n(.*?)\n```\s*$", re.DOTALL)
_DECLINE_RE = re.compile(r"^\s*#\s*DECLINE\s*:\s*(.+?)\s*$", re.MULTILINE)


def _strip_fences(text: str) -> str:
    m = _FENCE_RE.match(text.strip())
    return m.group(1) if m else text


def _detect_decline(text: str) -> str | None:
    """Return the reason if the response is a structured decline, else None."""
    m = _DECLINE_RE.search(text)
    if not m:
        return None
    # Must be *the* response, not a stray comment in code. Reject if any
    # `class Illustration` appears.
    if "class Illustration" in text:
        return None
    return m.group(1).strip()


def _static_safety_check(code: str) -> str | None:
    """Return None if code passes, else a short reason string."""
    if len(code.encode("utf-8")) > _MAX_CODE_BYTES:
        return f"code too large (> {_MAX_CODE_BYTES} bytes)"
    for bad in _FORBIDDEN_SUBSTRINGS:
        if bad in code:
            return f"forbidden token: {bad!r}"
    # Every `import` / `from` line must be whitelisted.
    for line in code.splitlines():
        s = line.strip()
        if s.startswith("import ") or s.startswith("from "):
            if not _ALLOWED_IMPORT_LINES_RE.match(line):
                return f"disallowed import: {s!r}"
    if f"class {_SCENE_CLASS_NAME}" not in code:
        return f"missing `class {_SCENE_CLASS_NAME}(Scene)`"
    return None


# ── LLM call ──────────────────────────────────────────────────

def _resolve_model(model: str | None) -> str:
    return model or settings.illustration_model or settings.ai_model


async def _request_code(
    concept: str,
    explanation: str,
    *,
    chapter_title: str | None,
    section_title: str | None,
    model: str,
    caller: str,
) -> str:
    user_msg = build_user_message(
        concept,
        explanation,
        chapter_title=chapter_title,
        section_title=section_title,
    )
    messages = [{"role": "user", "content": user_msg}]
    return await chat_completion(
        messages=messages,
        system=build_system_blocks(),
        model=model,
        caller=caller,
        max_tokens=4096,
    )


# ── Render ────────────────────────────────────────────────────

def _resolve_manim_python() -> str:
    """Pick the Python interpreter used to run manim.

    Preference: settings.manim_python → backend/.venv/bin/python → sys.executable.
    The backend may be started under Anaconda while manim lives only in the
    project .venv, so we must not assume sys.executable has manim installed.
    """
    import sys

    if settings.manim_python:
        return settings.manim_python
    # backend/ = parents[3] relative to this file
    # ( .../backend/app/services/extractor/manim_illustration.py )
    backend_root = Path(__file__).resolve().parents[3]
    venv_py = backend_root / ".venv" / "bin" / "python"
    if venv_py.exists():
        return str(venv_py)
    return sys.executable


def _render_sync(code: str, work_dir: Path, quality_flag: str) -> tuple[Path | None, str, str]:
    """Run `manim` on `code` inside `work_dir`. Return (mp4_path, failure_kind, stderr_tail).

    failure_kind is "" on success.
    """
    import subprocess

    work_dir.mkdir(parents=True, exist_ok=True)
    scene_file = work_dir / "scene.py"
    scene_file.write_text(code, encoding="utf-8")

    python = _resolve_manim_python()
    cmd = [
        python, "-m", "manim",
        quality_flag,                    # e.g. -ql  (low-quality, fast)
        "--disable_caching",             # fresh render each time
        "--format=mp4",
        "--output_file", "scene.mp4",
        "--media_dir", str(work_dir / "media"),
        str(scene_file),
        _SCENE_CLASS_NAME,
    ]
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(work_dir),
            capture_output=True,
            text=True,
            timeout=_RENDER_TIMEOUT_SEC,
        )
    except subprocess.TimeoutExpired as e:
        tail = (e.stderr or "")[-1000:] if isinstance(e.stderr, str) else ""
        return None, "render_timeout", tail

    if proc.returncode != 0:
        return None, "render_error", (proc.stderr or "")[-2000:]

    # Manim writes to media/videos/scene/<quality>/scene.mp4
    media = work_dir / "media" / "videos" / "scene"
    candidates = list(media.rglob("scene.mp4"))
    if not candidates:
        return None, "render_error", (proc.stderr or "")[-2000:]
    return candidates[0], "", ""


async def _render(code: str, work_dir: Path, quality_flag: str):
    return await asyncio.to_thread(_render_sync, code, work_dir, quality_flag)


# ── Public API ────────────────────────────────────────────────

async def generate_manim_animation(
    concept: str,
    explanation: str,
    *,
    chapter_title: str | None = None,
    section_title: str | None = None,
    model: str | None = None,
    caller: str = "kp_manim",
    output_dir: Path | None = None,
    quality: str = "low",  # "low" | "medium" | "high"
) -> ManimOutcome:
    """Generate a Manim animation MP4 for a single knowledge point.

    On success `output_path` is a path to the rendered MP4 under
    `output_dir` (copied there so the temp work dir can be cleaned up by
    the caller). On failure `output_path` is None and `failure_kind`
    indicates why.
    """
    quality_flag = {"low": "-ql", "medium": "-qm", "high": "-qh"}.get(quality, "-ql")
    model_name = _resolve_model(model)
    started = time.perf_counter()

    try:
        raw = await _request_code(
            concept, explanation,
            chapter_title=chapter_title, section_title=section_title,
            model=model_name, caller=caller,
        )
    except Exception as e:
        return ManimOutcome(
            code=None, output_path=None,
            failure_kind="llm_error", failure_detail=repr(e)[:200],
            decline_reason=None,
            latency_ms=int((time.perf_counter() - started) * 1000),
        )

    reason = _detect_decline(raw)
    if reason is not None:
        return ManimOutcome(
            code=raw, output_path=None,
            failure_kind="declined", failure_detail=None,
            decline_reason=reason,
            latency_ms=int((time.perf_counter() - started) * 1000),
        )

    code = _strip_fences(raw).strip()
    if not code or "class " not in code:
        return ManimOutcome(
            code=raw, output_path=None,
            failure_kind="no_code", failure_detail="no class in response",
            decline_reason=None,
            latency_ms=int((time.perf_counter() - started) * 1000),
        )

    safety = _static_safety_check(code)
    if safety is not None:
        return ManimOutcome(
            code=code, output_path=None,
            failure_kind="unsafe", failure_detail=safety,
            decline_reason=None,
            latency_ms=int((time.perf_counter() - started) * 1000),
        )

    # Render in a scratch dir, then copy MP4 to `output_dir` if provided.
    with tempfile.TemporaryDirectory(prefix="manim_gen_") as tmp:
        work = Path(tmp)
        mp4, fail, stderr_tail = await _render(code, work, quality_flag)

        if mp4 is None:
            logger.warning(
                "manim render failed (%s): %s",
                fail, (stderr_tail or "")[-400:],
            )
            return ManimOutcome(
                code=code, output_path=None,
                failure_kind=fail or "render_error",
                failure_detail=(stderr_tail or "")[-200:] or None,
                decline_reason=None,
                latency_ms=int((time.perf_counter() - started) * 1000),
                render_stderr_tail=stderr_tail,
            )

        dest_dir = output_dir or (Path(settings.upload_dir) / "manim")
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / f"manim_{uuid.uuid4().hex}.mp4"
        shutil.copy2(mp4, dest)

    return ManimOutcome(
        code=code, output_path=dest,
        failure_kind="ok", failure_detail=None,
        decline_reason=None,
        latency_ms=int((time.perf_counter() - started) * 1000),
    )


@dataclass(frozen=True)
class ManimInput:
    """Single KP input for the batch pipeline."""
    concept: str
    explanation: str
    chapter_title: str | None = None
    section_title: str | None = None
    kp_index: int | None = None


async def generate_manim_batch(
    inputs: list[ManimInput],
    *,
    concurrency: int = 2,
    model: str | None = None,
    caller: str = "kp_manim",
    output_dir: Path | None = None,
    quality: str = "high",
) -> list[ManimOutcome]:
    """Render MP4s for a batch of KPs with bounded concurrency.

    Manim rendering is CPU-bound (runs a full subprocess with FFmpeg),
    so `concurrency` defaults to 2 — raising this saturates all cores
    and slows overall throughput.
    """
    sem = asyncio.Semaphore(max(1, concurrency))

    async def _one(inp: ManimInput) -> ManimOutcome:
        async with sem:
            return await generate_manim_animation(
                inp.concept,
                inp.explanation,
                chapter_title=inp.chapter_title,
                section_title=inp.section_title,
                model=model,
                caller=caller,
                output_dir=output_dir,
                quality=quality,
            )

    return await asyncio.gather(*(_one(i) for i in inputs))


def log_manim_outcome(
    outcome: ManimOutcome,
    *,
    book_id: str,
    chapter_id: str,
    kp_id: str,
    concept: str,
) -> None:
    """One structured log record per KP (success or failure)."""
    logger.info(
        "manim_generation",
        extra={
            "event": "manim_generation",
            "book_id": book_id,
            "chapter_id": chapter_id,
            "kp_id": kp_id,
            "concept_prefix": (concept or "")[:60],
            "accepted": outcome.accepted,
            "failure_kind": outcome.failure_kind,
            "failure_detail": outcome.failure_detail,
            "decline_reason": outcome.decline_reason,
            "latency_ms": outcome.latency_ms,
            "filename": outcome.output_path.name if outcome.output_path else None,
        },
    )
