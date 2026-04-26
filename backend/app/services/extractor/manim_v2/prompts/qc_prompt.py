"""QC (visual review) prompt — stage 4.5.

Fed a rendered last-frame PNG plus the SceneSpec summary, the vision
LLM returns a small JSON verdict: severity + a list of concrete issues.
The caller uses the issues as feedback into a codegen retry when
severity exceeds the configured threshold.

Kept tight: the prompt is narrow ("is there overlap/clipping here"),
not an open-ended critique, so a small cheap vision model (Haiku 4.5
or GPT-5.4-mini) can handle it at ~$0.001-0.002 per call.
"""

from __future__ import annotations

import json

from app.services.extractor.manim_v2.spec_model import SceneSpec


QC_RULES = """\
You review rendered frames from educational Manim animations for layout \
issues that would confuse a student.

Look for:
- Overlapping text/equations — two pieces of text or MathTex occupying \
the same pixels.
- Clipping at screen edges — content cut off at the top, bottom, left, \
or right of the frame.
- Orphan labels — text floating in empty space, detached from the thing \
it labels.
- Illegible text — font so small it can't be read, or text placed on top \
of shapes without contrast.
- Missing content — the frame is nearly empty when the spec describes \
many objects (suggests a render or sizing failure).

Do NOT flag:
- Color choices, stylistic preferences, aesthetics.
- Deliberate size differences (one object intentionally larger than \
another).
- Minor gaps or slight asymmetry that a student wouldn't notice.
- Intended empty space around a focal element.

Output contract — ONE JSON object, no prose, no markdown, no fences:

{
  "severity": "none" | "minor" | "major",
  "issues": ["concrete observation 1", "concrete observation 2", ...]
}

Severity rules:
- "none" — no issues; the frame is clean.
- "minor" — cosmetic (small alignment drift, a whitespace gap). Does not \
harm comprehension.
- "major" — overlap, clipping, or illegibility that hurts learning. \
This is the signal that triggers a regeneration upstream.

Issues are concrete: "the label 'F = m a' overlaps the arrow tip at \
right center", not "looks crowded". Keep the list short (0-4 items).

If severity is "none", the issues list may be empty."""


def build_system_blocks() -> list[dict]:
    # Small prompt, unlikely to hit cache thresholds, but mark cacheable
    # anyway in case we later expand examples into this block.
    return [{"type": "text", "text": QC_RULES, "cache_control": {"type": "ephemeral"}}]


def _spec_summary(spec: SceneSpec) -> str:
    """Short human-readable summary of what the frame *should* show."""
    objects = ", ".join(f"{o.id}({o.kind})" for o in spec.objects[:12])
    if len(spec.objects) > 12:
        objects += f", … (+{len(spec.objects) - 12} more)"
    camera = spec.camera.scene_type
    last_beat_actions = (
        ", ".join(a.kind for a in spec.timeline[-1].parallel[:6])
        if spec.timeline else ""
    )
    return json.dumps(
        {
            "learning_objective": spec.learning_objective,
            "camera": camera,
            "duration_s": spec.duration_s,
            "objects": objects,
            "last_beat_actions": last_beat_actions,
        },
        ensure_ascii=False,
    )


def build_user_text(concept: str, spec: SceneSpec) -> str:
    return (
        f"Concept: {concept.strip()}\n\n"
        f"Scene summary: {_spec_summary(spec)}\n\n"
        "Review the attached final frame for the layout issues listed "
        "in the rules. Return the JSON verdict now."
    )
