"""Stage 3 prompt — Plan + Spec + retrieved examples → Manim Python code.

Keeps the *rules* block byte-stable (and cached). The retrieved example
code is included in the user message so the cache survives across KPs
even when the examples selected change. The spec JSON is also in the
user message — it's the concrete target for this render.
"""

from __future__ import annotations

import json

from app.services.extractor.manim_v2.spec_model import SceneSpec


CODEGEN_RULES = """\
You generate a single self-contained Python script using the Manim \
Community library (v0.19.0) that renders the provided SceneSpec.

Output contract:
- Output ONLY Python code. No prose, no markdown fences.
- The code must faithfully realize the SceneSpec — honor object ids, \
timeline ordering, parallel actions inside each beat, durations, and \
the chosen camera scene_type.

Hard requirements on the code:
1. Start with:  from manim import *
2. If numeric work is needed, additionally: import numpy as np
3. Define EXACTLY ONE class that subclasses the spec's camera.scene_type \
(Scene / MovingCameraScene / ZoomedScene / ThreeDScene). Name it `Illustration`.
4. The `construct(self)` method must run end to end within 4–18 s of \
animation time, matching `duration_s` in the spec.
5. No other top-level classes, no main-guard, no custom config, no \
__file__ usage, no file I/O, no network calls, no imports beyond \
`from manim import *` and (optionally) `import numpy as np`.
6. Valid LaTeX in every MathTex / Tex. Use raw strings and no `$` \
delimiters — e.g. `MathTex(r"F = m a")`.
7. Keep everything on screen. Camera frame is 14.22 × 8.0 units at \
origin for 2D scenes; avoid x outside [-7, 7] and y outside [-4, 4]. \
Prefer `.next_to()`, `.to_edge()`, `.shift()` over raw coordinates.
8. Use built-in color constants (BLUE, RED, GREEN, YELLOW, WHITE, GRAY, \
TEAL, ORANGE, PURPLE) or the color strings in the spec's style blocks.
9. Use `self.play(...)` for every animation and `self.wait(t)` for holds. \
Actions listed together inside a Beat go into one `self.play(...)` call.
10. Do NOT set random seeds or use time/date — output must be deterministic.

Implementation guidance:
- Treat the retrieved examples as idiom references. Copy their patterns \
for updaters, 3D cameras, Riemann rects, ValueTracker flows, etc. Do \
not literally paste an unrelated example into the output.
- For each `ValueTrackerSpec`, instantiate `ValueTracker(start)` before \
the beat whose tracker-driven updaters fire, and animate it via \
`self.play(tracker.animate.set_value(end), run_time=duration)`.
- For `AddUpdater` actions, compile the `updater` Python expression \
into a closure over the named trackers; remove it with `remove_updater` \
if a later `RemoveUpdater` references the same id.
- For `Brace`/`SurroundingRectangle`, resolve `target_id` / `line1_id` \
/ `line2_id` by id to the Python variable.
- End with `self.wait(0.6)` if the spec's last beat doesn't already hold.

Forbidden:
- No `from manim_*` plugin imports.
- No `config.*` assignment.
- No `subprocess`, `os.system`, `open(`, `requests`, `urllib`, \
`__import__`, `eval(`, `exec(`, `compile(`, `importlib`.

If rendering a prior attempt failed, you will also receive the tail of \
the manim stderr. Diagnose the error (KeyError, NameError, LaTeX \
compile failure, AttributeError on a Manim class, etc.) and emit a \
fixed version. Do not repeat the same mistake."""


def build_system_blocks() -> list[dict]:
    return [{"type": "text", "text": CODEGEN_RULES, "cache_control": {"type": "ephemeral"}}]


def _format_example(ex: dict) -> str:
    """`ex` = {'id', 'summary', 'tags', 'apis', 'code'} — dict as produced by retrieval."""
    tags = ", ".join(ex.get("tags") or [])
    apis = ", ".join(ex.get("apis") or [])
    return (
        f"--- example: {ex['id']} ---\n"
        f"summary: {ex.get('summary', '').strip()}\n"
        f"tags: {tags}\n"
        f"apis: {apis}\n"
        f"code:\n{ex['code']}\n"
    )


def build_user_message(
    concept: str,
    plan_markdown: str,
    spec: SceneSpec,
    examples: list[dict],
    *,
    prior_code: str | None = None,
    stderr_tail: str | None = None,
) -> str:
    parts: list[str] = []
    parts.append(f"Concept: {concept.strip()}")
    parts.append("")
    parts.append("Scene plan:")
    parts.append(plan_markdown.strip())
    parts.append("")
    parts.append("SceneSpec JSON:")
    parts.append(json.dumps(spec.model_dump(exclude_none=True), indent=2))
    parts.append("")
    if examples:
        parts.append("Retrieved Manim example references (for idioms; do not copy wholesale):")
        parts.append("")
        parts.extend(_format_example(ex) for ex in examples)
    if prior_code and stderr_tail:
        parts.append("Previous attempt failed to render. Fix the error.")
        parts.append("Previous code:")
        parts.append(prior_code)
        parts.append("")
        parts.append("Manim stderr (tail):")
        parts.append(stderr_tail[-1500:])
        parts.append("")
    parts.append("Emit the final Python code now. Only code.")
    return "\n".join(parts)
