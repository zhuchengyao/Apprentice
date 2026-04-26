"""Manim v2 orchestrator.

Stage 1 (planner) → Stage 2 (spec_generator) → retrieval → Stage 3 (codegen)
→ Stage 4 (renderer). On render failure, one retry: feed `prior_code` +
`stderr_tail` back into the codegen stage and try to render again.

Public API mirrors the retired `manim_illustration` module so callers in
`tasks/processing.py` and `scripts/manim_demo.py` only update imports.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path

from app.config import settings
from app.services.extractor.manim_v2 import codegen, planner, qc, retrieval, spec_generator
from app.services.extractor.manim_v2.renderer import render

logger = logging.getLogger(__name__)


# FailureKind values: "ok" | "declined" | "plan_error" | "spec_error"
#                   | "llm_error" | "no_code" | "unsafe"
#                   | "render_timeout" | "render_error"
FailureKind = str


@dataclass
class ManimOutcome:
    code: str | None
    output_path: Path | None
    failure_kind: FailureKind
    failure_detail: str | None
    decline_reason: str | None
    latency_ms: int
    render_stderr_tail: str | None = None
    # v2 observability — filled by the orchestrator.
    stage_reached: str = "start"             # "plan" | "spec" | "retrieve" | "code" | "render_1" | "render_2" | "qc"
    attempt: int = 1                         # 1 or 2 (2 = post-retry)
    plan_hash: str | None = None
    spec_hash: str | None = None
    examples_retrieved: list[str] = field(default_factory=list)
    # QC observability.
    qc_ran: bool = False
    qc_severity: str | None = None           # "none" | "minor" | "major" | "unknown"
    qc_issues: list[str] = field(default_factory=list)
    qc_retry_fired: bool = False
    # Persistable artifacts for AnimationJob. These are intentionally
    # optional so direct callers can keep using the old shape.
    plan_markdown: str | None = None
    scene_spec: dict | None = None
    code_attempts: list[dict] = field(default_factory=list)
    render_attempts: list[dict] = field(default_factory=list)
    qc_reports: list[dict] = field(default_factory=list)

    @property
    def accepted(self) -> bool:
        return self.output_path is not None


@dataclass(frozen=True)
class ManimInput:
    """Single KP input for the batch pipeline."""
    concept: str
    kp_index: int | None = None


def _fallback_model() -> str:
    return settings.illustration_model or settings.ai_model


def _stage_models(override: str | None) -> tuple[str, str, str]:
    """Return (planner, spec, codegen) models. An explicit `override` wins
    for all three stages so callers (CLI, API) can still pin one model."""
    if override:
        return override, override, override
    fb = _fallback_model()
    return (
        settings.illustration_planner_model or fb,
        settings.illustration_spec_model or fb,
        settings.illustration_codegen_model or fb,
    )


def _hash(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]


def _render_attempt_payload(attempt: int, result) -> dict:
    return {
        "attempt": attempt,
        "failure_kind": result.failure_kind,
        "failure_detail": result.failure_detail,
        "stderr_tail": result.stderr_tail,
        "output_filename": result.output_path.name if result.output_path else None,
    }


async def generate_manim_animation(
    concept: str,
    *,
    model: str | None = None,
    caller: str = "kp_manim",
    output_dir: Path | None = None,
    quality: str = "high",
) -> ManimOutcome:
    planner_model, spec_model, codegen_model = _stage_models(model)
    started = time.perf_counter()
    plan_markdown_out: str | None = None
    scene_spec_out: dict | None = None
    code_attempts: list[dict] = []
    render_attempts: list[dict] = []
    qc_reports: list[dict] = []

    def _elapsed_ms() -> int:
        return int((time.perf_counter() - started) * 1000)

    def _artifact_kwargs() -> dict:
        return {
            "plan_markdown": plan_markdown_out,
            "scene_spec": scene_spec_out,
            "code_attempts": list(code_attempts),
            "render_attempts": list(render_attempts),
            "qc_reports": list(qc_reports),
        }

    # ── Stage 1: plan ───────────────────────────────────────
    try:
        plan_markdown = await planner.generate_plan(
            concept,
            model=planner_model, caller=f"{caller}_plan",
        )
    except planner.PlannerDecline as d:
        return ManimOutcome(
            code=None, output_path=None,
            failure_kind="declined", failure_detail=None,
            decline_reason=d.reason,
            latency_ms=_elapsed_ms(),
            stage_reached="plan",
            **_artifact_kwargs(),
        )
    except Exception as e:
        return ManimOutcome(
            code=None, output_path=None,
            failure_kind="llm_error", failure_detail=f"planner: {e!r}"[:200],
            decline_reason=None,
            latency_ms=_elapsed_ms(),
            stage_reached="plan",
            **_artifact_kwargs(),
        )

    plan_markdown_out = plan_markdown
    plan_hash = _hash(plan_markdown)

    # ── Stage 2: spec ───────────────────────────────────────
    try:
        spec = await spec_generator.generate_spec(
            concept, plan_markdown,
            model=spec_model, caller=f"{caller}_spec",
        )
    except spec_generator.SpecDeclined as d:
        return ManimOutcome(
            code=None, output_path=None,
            failure_kind="declined", failure_detail=None,
            decline_reason=d.reason,
            latency_ms=_elapsed_ms(),
            stage_reached="spec",
            plan_hash=plan_hash,
            **_artifact_kwargs(),
        )
    except Exception as e:
        return ManimOutcome(
            code=None, output_path=None,
            failure_kind="spec_error", failure_detail=str(e)[:300],
            decline_reason=None,
            latency_ms=_elapsed_ms(),
            stage_reached="spec",
            plan_hash=plan_hash,
            **_artifact_kwargs(),
        )

    scene_spec_out = spec.model_dump(mode="json")
    spec_hash = _hash(json.dumps(scene_spec_out, sort_keys=True))

    # ── Retrieval (non-fatal on failure) ────────────────────
    examples = await retrieval.retrieve_examples(concept, plan_markdown, spec, k=4)
    retrieved_ids = retrieval.retrieved_ids(examples)

    # ── Stage 3: code ───────────────────────────────────────
    try:
        code = await codegen.generate_code(
            concept, plan_markdown, spec, examples,
            model=codegen_model, caller=f"{caller}_code",
        )
    except Exception as e:
        return ManimOutcome(
            code=None, output_path=None,
            failure_kind="llm_error", failure_detail=f"codegen: {e!r}"[:200],
            decline_reason=None,
            latency_ms=_elapsed_ms(),
            stage_reached="code",
            plan_hash=plan_hash, spec_hash=spec_hash,
            examples_retrieved=retrieved_ids,
            **_artifact_kwargs(),
        )
    code_attempts.append({
        "attempt": 1,
        "reason": "initial",
        "code": code,
        "has_class": bool(code and "class " in code),
    })

    if not code or "class " not in code:
        return ManimOutcome(
            code=code or None, output_path=None,
            failure_kind="no_code", failure_detail="no class in response",
            decline_reason=None,
            latency_ms=_elapsed_ms(),
            stage_reached="code",
            plan_hash=plan_hash, spec_hash=spec_hash,
            examples_retrieved=retrieved_ids,
            **_artifact_kwargs(),
        )

    # ── Stage 4: render (attempt 1) ────────────────────────
    result = await render(code, quality=quality, output_dir=output_dir)
    render_attempts.append(_render_attempt_payload(1, result))
    if result.output_path is not None:
        # Optional QC pass — render last frame, vision-LLM review, retry
        # codegen once if severity ≥ threshold. Never blocks success:
        # worst case we return the v1 render unchanged.
        final_code = code
        final_path = result.output_path
        qc_ran = False
        qc_severity: str | None = None
        qc_issues: list[str] = []
        qc_retry_fired = False
        final_attempt = 1
        final_stage = "render_1"

        if settings.illustration_qc_enabled:
            qc_model = (
                settings.illustration_qc_model
                or settings.illustration_model
                or settings.ai_model
            )
            qc_outcome = await qc.run_qc(
                code, concept, spec,
                model=qc_model, caller=f"{caller}_qc",
            )
            qc_ran = qc_outcome.ran
            qc_severity = qc_outcome.severity
            qc_issues = list(qc_outcome.issues)
            qc_reports.append({
                "attempt": 1,
                "ran": qc_outcome.ran,
                "severity": qc_outcome.severity,
                "issues": list(qc_outcome.issues),
                "latency_ms": qc_outcome.latency_ms,
                "raw_response": qc_outcome.raw_response,
            })
            threshold = settings.illustration_qc_severity_threshold
            if (
                qc_outcome.ran
                and qc_outcome.exceeds(threshold)
                and settings.illustration_qc_retries > 0
            ):
                qc_retry_fired = True
                logger.info(
                    "manim_v2 QC severity=%s, retrying codegen (issues: %s)",
                    qc_outcome.severity, qc_outcome.issues[:3],
                )
                try:
                    code2 = await codegen.generate_code(
                        concept, plan_markdown, spec, examples,
                        model=codegen_model, caller=f"{caller}_code_qc_retry",
                        prior_code=code,
                        stderr_tail=qc_outcome.feedback_text(),
                    )
                except Exception as e:
                    logger.warning("codegen QC-retry failed: %s", e)
                    code2 = ""
                code_attempts.append({
                    "attempt": 2,
                    "reason": "qc_retry",
                    "code": code2,
                    "has_class": bool(code2 and "class " in code2),
                    "feedback": qc_outcome.feedback_text(),
                })
                if code2 and "class " in code2:
                    result2 = await render(code2, quality=quality, output_dir=output_dir)
                    render_attempts.append(_render_attempt_payload(2, result2))
                    if result2.output_path is not None:
                        final_code = code2
                        final_path = result2.output_path
                        final_attempt = 2
                        final_stage = "render_2"
                    else:
                        logger.info(
                            "QC-retry render failed (%s); keeping v1",
                            result2.failure_kind,
                        )
            qc.cleanup_frame(qc_outcome)

        return ManimOutcome(
            code=final_code, output_path=final_path,
            failure_kind="ok", failure_detail=None,
            decline_reason=None,
            latency_ms=_elapsed_ms(),
            stage_reached=final_stage, attempt=final_attempt,
            plan_hash=plan_hash, spec_hash=spec_hash,
            examples_retrieved=retrieved_ids,
            qc_ran=qc_ran,
            qc_severity=qc_severity,
            qc_issues=qc_issues,
            qc_retry_fired=qc_retry_fired,
            **_artifact_kwargs(),
        )

    # `unsafe` is deterministic — retrying won't help.
    if result.failure_kind == "unsafe":
        return ManimOutcome(
            code=code, output_path=None,
            failure_kind="unsafe", failure_detail=result.failure_detail,
            decline_reason=None,
            latency_ms=_elapsed_ms(),
            stage_reached="render_1", attempt=1,
            plan_hash=plan_hash, spec_hash=spec_hash,
            examples_retrieved=retrieved_ids,
            **_artifact_kwargs(),
        )

    # ── Feedback loop (v1): ONE retry on render_error / render_timeout ──
    logger.info(
        "manim_v2 render failed (%s), retrying with stderr feedback",
        result.failure_kind,
    )
    try:
        code2 = await codegen.generate_code(
            concept, plan_markdown, spec, examples,
            model=codegen_model, caller=f"{caller}_code_retry",
            prior_code=code, stderr_tail=result.stderr_tail,
        )
    except Exception as e:
        return ManimOutcome(
            code=code, output_path=None,
            failure_kind="llm_error", failure_detail=f"codegen_retry: {e!r}"[:200],
            decline_reason=None,
            latency_ms=_elapsed_ms(),
            render_stderr_tail=result.stderr_tail,
            stage_reached="code", attempt=2,
            plan_hash=plan_hash, spec_hash=spec_hash,
            examples_retrieved=retrieved_ids,
            **_artifact_kwargs(),
        )
    code_attempts.append({
        "attempt": 2,
        "reason": "render_retry",
        "code": code2,
        "has_class": bool(code2 and "class " in code2),
        "feedback": result.stderr_tail,
    })

    if not code2 or "class " not in code2:
        return ManimOutcome(
            code=code2 or code, output_path=None,
            failure_kind="no_code", failure_detail="no class in retry response",
            decline_reason=None,
            latency_ms=_elapsed_ms(),
            render_stderr_tail=result.stderr_tail,
            stage_reached="code", attempt=2,
            plan_hash=plan_hash, spec_hash=spec_hash,
            examples_retrieved=retrieved_ids,
            **_artifact_kwargs(),
        )

    result2 = await render(code2, quality=quality, output_dir=output_dir)
    render_attempts.append(_render_attempt_payload(2, result2))
    if result2.output_path is not None:
        return ManimOutcome(
            code=code2, output_path=result2.output_path,
            failure_kind="ok", failure_detail=None,
            decline_reason=None,
            latency_ms=_elapsed_ms(),
            stage_reached="render_2", attempt=2,
            plan_hash=plan_hash, spec_hash=spec_hash,
            examples_retrieved=retrieved_ids,
            **_artifact_kwargs(),
        )

    return ManimOutcome(
        code=code2, output_path=None,
        failure_kind=result2.failure_kind, failure_detail=result2.failure_detail,
        decline_reason=None,
        latency_ms=_elapsed_ms(),
        render_stderr_tail=result2.stderr_tail,
        stage_reached="render_2", attempt=2,
        plan_hash=plan_hash, spec_hash=spec_hash,
        examples_retrieved=retrieved_ids,
        **_artifact_kwargs(),
    )


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

    Manim rendering is CPU-bound (subprocess + FFmpeg), so `concurrency`
    defaults to 2 — raising this saturates cores and slows throughput.
    """
    sem = asyncio.Semaphore(max(1, concurrency))

    async def _one(inp: ManimInput) -> ManimOutcome:
        async with sem:
            return await generate_manim_animation(
                inp.concept,
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
            "pipeline": "v2",
            "book_id": book_id,
            "chapter_id": chapter_id,
            "kp_id": kp_id,
            "concept_prefix": (concept or "")[:60],
            "accepted": outcome.accepted,
            "failure_kind": outcome.failure_kind,
            "failure_detail": outcome.failure_detail,
            "decline_reason": outcome.decline_reason,
            "latency_ms": outcome.latency_ms,
            "stage_reached": outcome.stage_reached,
            "attempt": outcome.attempt,
            "plan_hash": outcome.plan_hash,
            "spec_hash": outcome.spec_hash,
            "examples_retrieved": outcome.examples_retrieved,
            "qc_ran": outcome.qc_ran,
            "qc_severity": outcome.qc_severity,
            "qc_issues": outcome.qc_issues,
            "qc_retry_fired": outcome.qc_retry_fired,
            "mp4_filename": outcome.output_path.name if outcome.output_path else None,
        },
    )
