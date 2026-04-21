"""Stage 4 — render Manim code to MP4.

Ported from the retired `manim_illustration` module. Responsibilities:
  - static safety veto on the generated code
  - write it to a temp dir and invoke `python -m manim` in a subprocess
  - copy the resulting MP4 to `uploads/manim/` with a UUID filename

The class base class is no longer asserted here: the new pipeline emits
scenes that may subclass `Scene`, `MovingCameraScene`, `ZoomedScene`, or
`ThreeDScene` depending on `SceneSpec.camera.scene_type`. We only assert
the class *name* is `Illustration` so the CLI command targets it.
"""

from __future__ import annotations

import asyncio
import logging
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
from dataclasses import dataclass
from pathlib import Path

from app.config import settings

logger = logging.getLogger(__name__)


SCENE_CLASS_NAME = "Illustration"
RENDER_TIMEOUT_SEC = 180
MAX_CODE_BYTES = 32_000


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
    "open(",
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

_CLASS_DECL_RE = re.compile(rf"^\s*class\s+{SCENE_CLASS_NAME}\s*\(", re.MULTILINE)


@dataclass
class RenderResult:
    output_path: Path | None
    failure_kind: str            # "ok" | "unsafe" | "render_timeout" | "render_error"
    failure_detail: str | None   # veto reason OR stderr tail
    stderr_tail: str | None


def static_safety_check(code: str) -> str | None:
    """Return None if code passes, else a short reason string."""
    if len(code.encode("utf-8")) > MAX_CODE_BYTES:
        return f"code too large (> {MAX_CODE_BYTES} bytes)"
    for bad in _FORBIDDEN_SUBSTRINGS:
        if bad in code:
            return f"forbidden token: {bad!r}"
    for line in code.splitlines():
        s = line.strip()
        if s.startswith("import ") or s.startswith("from "):
            if not _ALLOWED_IMPORT_LINES_RE.match(line):
                return f"disallowed import: {s!r}"
    if not _CLASS_DECL_RE.search(code):
        return f"missing `class {SCENE_CLASS_NAME}(...)`"
    return None


def _resolve_manim_python() -> str:
    """Pick the Python interpreter used to run manim.

    Preference: settings.manim_python → backend/.venv/bin/python → sys.executable.
    The backend may be started under Anaconda while manim lives only in
    the project .venv, so sys.executable may not have manim installed.
    """
    if settings.manim_python:
        return settings.manim_python
    # backend/ = parents[4] relative to this file:
    #   backend/app/services/extractor/manim_v2/renderer.py
    backend_root = Path(__file__).resolve().parents[4]
    venv_py = backend_root / ".venv" / "bin" / "python"
    if venv_py.exists():
        return str(venv_py)
    return sys.executable


def _render_sync(code: str, work_dir: Path, quality_flag: str) -> RenderResult:
    work_dir.mkdir(parents=True, exist_ok=True)
    scene_file = work_dir / "scene.py"
    scene_file.write_text(code, encoding="utf-8")

    cmd = [
        _resolve_manim_python(), "-m", "manim",
        quality_flag,
        "--disable_caching",
        "--format=mp4",
        "--output_file", "scene.mp4",
        "--media_dir", str(work_dir / "media"),
        str(scene_file),
        SCENE_CLASS_NAME,
    ]
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(work_dir),
            capture_output=True,
            text=True,
            timeout=RENDER_TIMEOUT_SEC,
        )
    except subprocess.TimeoutExpired as e:
        tail = (e.stderr or "")[-2000:] if isinstance(e.stderr, str) else ""
        return RenderResult(None, "render_timeout", tail[-200:] or None, tail)

    if proc.returncode != 0:
        tail = (proc.stderr or "")[-2000:]
        return RenderResult(None, "render_error", tail[-200:] or None, tail)

    media = work_dir / "media" / "videos" / "scene"
    candidates = list(media.rglob("scene.mp4"))
    if not candidates:
        tail = (proc.stderr or "")[-2000:]
        return RenderResult(None, "render_error", "no MP4 produced", tail)
    return RenderResult(candidates[0], "ok", None, None)


async def render(
    code: str,
    *,
    quality: str = "high",
    output_dir: Path | None = None,
) -> RenderResult:
    """Run the static check, render, and copy the MP4 to `output_dir`.

    `output_dir` defaults to `<settings.upload_dir>/manim/`.
    """
    safety = static_safety_check(code)
    if safety is not None:
        return RenderResult(None, "unsafe", safety, None)

    quality_flag = {"low": "-ql", "medium": "-qm", "high": "-qh"}.get(quality, "-qh")

    with tempfile.TemporaryDirectory(prefix="manim_v2_") as tmp:
        work = Path(tmp)
        result = await asyncio.to_thread(_render_sync, code, work, quality_flag)
        if result.output_path is None:
            return result
        dest_dir = output_dir or (Path(settings.upload_dir) / "manim")
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / f"manim_{uuid.uuid4().hex}.mp4"
        shutil.copy2(result.output_path, dest)
        return RenderResult(dest, "ok", None, None)
