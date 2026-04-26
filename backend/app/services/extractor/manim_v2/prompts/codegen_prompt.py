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
4. The `construct(self)` method must run end to end within 2–30 s of \
animation time, matching `duration_s` in the spec.
5. No other top-level classes, no main-guard, no custom config, no \
__file__ usage, no file I/O, no network calls, no imports beyond \
`from manim import *` and (optionally) `import numpy as np`.
6. Valid LaTeX in every MathTex / Tex. Use raw strings and no `$` \
delimiters — e.g. `MathTex(r"F = m a")`.
7. Keep everything on screen and non-overlapping. The 2D camera frame \
is 14.22 × 8.0 at origin; the hard edges are x ∈ [-7, 7], y ∈ [-4, 4]. \
Treat x ∈ [-6, 6] and y ∈ [-3.3, 3.3] as the *safe inner frame* — keep \
labels and text inside it; text near the edges clips. Prefer relative \
positioning (`.next_to()`, `.to_edge()`, `VGroup.arrange()`) over \
raw `.shift(RIGHT * 3 + UP * 2)` style coordinates; absolute \
coordinates are fine only for the root anchor of a diagram.
8. Use built-in color constants (BLUE, RED, GREEN, YELLOW, WHITE, GRAY, \
TEAL, ORANGE, PURPLE) or the color strings in the spec's style blocks.
9. Use `self.play(...)` for every animation and `self.wait(t)` for holds. \
Actions listed together inside a Beat go into one `self.play(...)` call.
10. Do NOT set random seeds or use time/date — output must be deterministic.

Spatial planning (do this BEFORE writing any code):

Layout failure is the #1 cause of unusable renders. The trap is to \
place objects one at a time and only discover the overlap after. Avoid \
it by partitioning the frame into named regions FIRST, then committing \
each persistent mobject to exactly one region.

Pick one of four canonical layouts. One will fit.

  A. SINGLE_FOCUS — one central visualization. No persistent side text.
     Regions:  title   y ∈ [+3.4, +3.8]
               viz     x ∈ [-6, +6],  y ∈ [-2.8, +3.0]
               summary y ∈ [-3.6, -3.2]
     Use when: one object being transformed, no live readouts or legends.

  B. TWO_COLUMN — viz one side, commentary stacked on the other.
     Regions:  title        y ∈ [+3.4, +3.8]
               viz_column   x ∈ [-6, -1]     (or [+1, +6])
               text_column  x ∈ [+0.5, +6]   (or [-6, -0.5])
                            stacked top-down from y=+2.2,
                            each block ≥0.3 units below the previous
     Use when: the viz is bounded to half the frame AND you need any \
persistent labels, legends, live readouts, or a final formula alongside \
it. This is the DEFAULT when you would otherwise stack text below the \
viz — stacking below almost always collides with a to_edge(DOWN) \
summary formula.

  C. THREE_ROW — stacked panels sharing a vertical axis.
     Regions:  title      y ∈ [+3.4, +3.8]
               top_panel  y ∈ [+1.6, +2.8]
               mid_panel  y ∈ [-0.4, +0.8]
               bot_panel  y ∈ [-2.4, -1.2]
               summary    y ∈ [-3.6, -3.0]
     Use when: function composition chains, input→transform→output, \
side-by-side evolving curves, PDF/CDF pairs.

  D. COMPARISON — two or three side-by-side subpanels.
     Two:   x ∈ [-6, -0.5] and [+0.5, +6]
     Three: x ∈ [-6, -2], [-1.5, +1.5], [+2, +6]
     Title top, summary bottom; each subpanel stays in its x-slice.
     Use when: the teaching point is direct contrast.

After picking a layout, commit each persistent mobject to a named \
region with an absolute anchor, e.g.:

    # TEXT COLUMN (right): anchored at x=+2.2, stacked top-down
    info_panel = always_redraw(...).move_to([+2.2, +1.8, 0])
    legend     = VGroup(...).arrange(DOWN, buff=0.3).move_to([+2.2, +0.5, 0])
    formula    = MathTex(...).move_to([+2.2, -1.8, 0])

Absolute `.move_to([x, y, 0])` is PREFERRED for multi-block regions — \
it prevents the chained-next_to drift that pushes later blocks into \
adjacent regions. Use `.to_edge(...)` only for a SINGLE mobject per \
edge (title alone, or summary alone — never both competing for the \
bottom strip).

Layout audit (mandatory, in your head, before emitting code):
  - List every persistent mobject's approximate (x, y) bounds.
  - Title Text at font_size=26 occupies ≈0.45 tall; MathTex at \
font_size=28 with a fraction ≈0.7 tall; plain MathTex ≈0.5 tall.
  - Verify no two mobjects share the same (x-range ∩ y-range).
  - If two do, move one to another region, shrink font_size, or split \
a long LaTeX across two shorter MathTex lines.

Worked pitfall (lower-strip collision):
  A scene grows a rectangle in the lower-left quadrant. After the \
growth it adds (a) a 'df·dg → 0 faster' note below the rectangle via \
`next_to(rect, DOWN, buff=0.8)` and (b) a final summary formula via \
`to_edge(DOWN)`. Both resolve to the lower strip of the frame — note \
bottom ≈ y=-3.15 collides with formula top ≈ y=-2.90. Fix: recognize \
this as TWO_COLUMN. Rectangle stays in x ∈ [-6, -2]; BOTH the note \
AND the formula go in the right column at x=+2.2 — note at y=-0.8, \
formula at y=-1.8 and y=-2.7 (split across two lines). All gaps ≥ 0.3.

Layout discipline (detail rules that follow from the spatial plan):
- Default `buff=0.3` on every `.next_to(...)`. The Manim default 0.1 is \
almost always too tight for text or MathTex and produces overlap.
- For 2+ related labels/equations, stack them with \
`VGroup(label1, label2, ...).arrange(DOWN, buff=0.35)` then place the \
group once — don't chain `.next_to()` calls, which compounds spacing \
errors.
- Estimate MathTex/Text width as ~0.35 units per character. If a label \
is longer than ~12 characters, do NOT place it next to another object \
on the same row — stack vertically, use a column anchor, or shrink \
`font_size` to 30 or lower.
- A single MathTex over ~11 units wide (≈30 chars at font_size=28) \
MUST be split across two shorter MathTex lines placed \
`.arrange(DOWN, buff=0.3)` — do not let a formula trail off the \
right edge.
- Titles go at `.to_edge(UP, buff=0.4)`; a single summary equation may \
use `.to_edge(DOWN, buff=0.5)`. Never hand-pick `UP * 3.5` style coords.
- Before introducing new content in a region where earlier content \
still lives, `self.play(FadeOut(earlier_group))` first. Do not animate \
new mobjects on top of old ones.
- When a mobject needs to move to make room, animate the shift via \
`self.play(existing.animate.shift(UP * 1.2))` — don't rely on z-order \
to hide overlap.
- Group related mobjects (labels + the thing they label) into a single \
`VGroup` before any shift/scale so they move together.

Text vs LaTeX (the #2 source of bad-looking renders):

`Text(...)` uses Pango with the system font and CANNOT render math glyphs \
correctly. Characters like z², α, β, π, θ, ε, δ, ξ, ∫, ∑, ∞, →, ↦, ∈, ∂ \
either come out as a different font, a tofu box, or spacing-broken text. \
Use `Text` ONLY for plain prose with no mathematical symbols.

For ANY string containing math notation (Greek letters, subscripts, \
superscripts, integrals, fractions, set/relation symbols), use one of:
  - `MathTex(r"\\theta_r = \\theta_i")` — pure math
  - `Tex(r"Reflection law: $\\theta_r = \\theta_i$")` — prose + inline math
  - `VGroup(Text("Prose part"), MathTex(r"\\theta = ..."))` — separate mobjects

Concretely:
  ✗ `Text("Compute I = ∫e⁻ˣ²dx by squaring")`
  ✓ `Tex(r"Compute $I = \\int e^{-x^2}\\,dx$ by squaring")`

  ✗ `Text("z ↦ z² doubles the angle")`
  ✓ `Tex(r"$z \\mapsto z^2$ doubles the angle")`

  ✗ `Text("Beta(α, β): density on [0, 1]")`
  ✓ `Tex(r"Beta$(\\alpha, \\beta)$: density on $[0, 1]$")`

  ✗ `Text("ε–δ limit window")`
  ✓ `Tex(r"$\\varepsilon$–$\\delta$ limit window")`

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
