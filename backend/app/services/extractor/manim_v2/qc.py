"""Stage 4.5 — visual QC of a rendered frame.

Renders the last frame as a PNG (fast, ~3-8 s), sends it to a vision-
capable LLM with a narrow "does this have overlap/clipping?" prompt,
and returns a structured verdict. The pipeline uses the verdict to
decide whether to regenerate codegen with the issues as feedback.
"""

from __future__ import annotations

import json
import logging
import re
import shutil
import time
from dataclasses import dataclass, field
from pathlib import Path

from app.services.ai_client import build_image_content_blocks, chat_completion
from app.services.extractor.manim_v2.prompts import qc_prompt
from app.services.extractor.manim_v2.renderer import render_last_frame
from app.services.extractor.manim_v2.spec_model import SceneSpec

logger = logging.getLogger(__name__)


_SEVERITY_ORDER = {"none": 0, "minor": 1, "major": 2}


@dataclass
class QcOutcome:
    ran: bool                          # False when QC was skipped (frame render failed, etc.)
    severity: str                      # "none" | "minor" | "major" | "unknown"
    issues: list[str] = field(default_factory=list)
    frame_path: Path | None = None     # caller cleans this up
    latency_ms: int = 0
    raw_response: str | None = None    # kept for debugging when parsing fails

    def exceeds(self, threshold: str) -> bool:
        """True iff this outcome's severity is >= threshold."""
        return _SEVERITY_ORDER.get(self.severity, 0) >= _SEVERITY_ORDER.get(threshold, 2)

    def feedback_text(self) -> str:
        """Concatenated issues, ready to paste into a codegen retry."""
        if not self.issues:
            return "Visual QC flagged the last frame but provided no specific issues."
        bullets = "\n".join(f"- {i}" for i in self.issues[:6])
        return (
            "Visual QC on the rendered last frame flagged these layout problems:\n"
            f"{bullets}\n\n"
            "Fix them. Common fixes:\n"
            "- Move overlapping labels to a VGroup(...).arrange(DOWN, buff=0.35).\n"
            "- Pull content closer to ORIGIN (safe inner frame x ∈ [-6, 6], y ∈ [-3.3, 3.3]).\n"
            "- Shrink MathTex font_size or split a long equation across two lines.\n"
            "- Fade out stale content before dropping new content in the same region."
        )


_JSON_FENCE_RE = re.compile(r"```(?:json)?\s*\n(.*?)\n```", re.DOTALL)


def _extract_json_blob(text: str) -> str:
    text = text.strip()
    m = _JSON_FENCE_RE.search(text)
    if m:
        return m.group(1).strip()
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end > start:
        return text[start : end + 1]
    return text


async def run_qc(
    code: str,
    concept: str,
    spec: SceneSpec,
    *,
    model: str,
    caller: str,
) -> QcOutcome:
    """Render last frame, ask a vision model for a verdict. Always
    returns a QcOutcome — never raises; on infrastructure failure
    returns `ran=False` so the caller can skip the retry path cleanly.
    """
    started = time.perf_counter()

    png = await render_last_frame(code)
    if png is None:
        return QcOutcome(
            ran=False, severity="unknown",
            issues=["QC frame render failed"],
            latency_ms=int((time.perf_counter() - started) * 1000),
        )

    try:
        image_blocks = await build_image_content_blocks([str(png)])
        if not image_blocks:
            return QcOutcome(
                ran=False, severity="unknown",
                issues=["QC image encode failed"],
                frame_path=png,
                latency_ms=int((time.perf_counter() - started) * 1000),
            )

        user_blocks = image_blocks + [
            {"type": "text", "text": qc_prompt.build_user_text(concept, spec)}
        ]
        raw = await chat_completion(
            messages=[{"role": "user", "content": user_blocks}],
            system=qc_prompt.build_system_blocks(),
            model=model,
            caller=caller,
            max_tokens=512,
        )
    except Exception as e:
        logger.warning("qc.run_qc: LLM call failed: %s", e)
        return QcOutcome(
            ran=False, severity="unknown",
            issues=[f"QC LLM call failed: {e!r}"[:200]],
            frame_path=png,
            latency_ms=int((time.perf_counter() - started) * 1000),
        )

    blob = _extract_json_blob(raw)
    try:
        data = json.loads(blob)
    except json.JSONDecodeError:
        logger.warning("qc.run_qc: non-JSON response: %s", raw[:300])
        return QcOutcome(
            ran=True, severity="unknown",
            issues=["QC response was not valid JSON"],
            frame_path=png,
            raw_response=raw[:500],
            latency_ms=int((time.perf_counter() - started) * 1000),
        )

    severity = str(data.get("severity") or "unknown").lower().strip()
    if severity not in _SEVERITY_ORDER and severity != "unknown":
        severity = "unknown"
    issues_raw = data.get("issues") or []
    issues = [str(i).strip() for i in issues_raw if str(i).strip()][:6]

    return QcOutcome(
        ran=True,
        severity=severity,
        issues=issues,
        frame_path=png,
        raw_response=raw[:500],
        latency_ms=int((time.perf_counter() - started) * 1000),
    )


def cleanup_frame(outcome: QcOutcome) -> None:
    """Best-effort cleanup of the QC PNG + its temp parent directory."""
    if outcome.frame_path is None:
        return
    try:
        parent = outcome.frame_path.parent
        # Walk up to the manim_qc_frame_* directory we created.
        while parent.name and not parent.name.startswith("manim_qc_frame_"):
            if parent == parent.parent:
                break
            parent = parent.parent
        if parent.name.startswith("manim_qc_frame_"):
            shutil.rmtree(parent, ignore_errors=True)
    except Exception:
        pass
