"""Stage 1 prompt — Text → Scene Plan (free-form pedagogical markdown).

The plan is deliberately not machine-readable: we want the LLM to think
about *how to teach* the concept visually before committing to concrete
mobjects and timing. Stage 2 translates the plan to structured JSON.
"""

from __future__ import annotations


PLANNER_RULES = """\
You design a short educational Manim animation plan for exactly one \
knowledge point. Plan only — do not write code.

Output contract:
- Plain markdown with the exact section headings below, in order.
- No code fences, no preamble, no extra sections or commentary.

## Learning objective
Exactly one sentence: what the viewer should understand after watching.

## Visual metaphor
1–2 sentences describing the central visual representation. Concrete \
and drawable (e.g. "a right triangle with squares built on each leg", \
"a unit circle with a rotating radius tracing a sine wave").

## Beats
A numbered list of 3–6 beats. One beat looks like:

1. **t**: [0-4]
   **show**: a right triangle with legs labeled a, b and hypotenuse c
   **why**: establish the geometric setting

Rules:
- Ranges are contiguous: first beat starts at 0; each beat's end equals \
the next beat's start; the last beat's end equals the Duration.
- Ranges are inclusive on both ends — time [0-4] means seconds 0 through 4.
- Describe WHAT is visible, not HOW it animates. No Write/FadeIn/\
Transform, no coordinates, no colors, no camera moves, no style.
- One idea per beat. Short, concrete phrases.

## Diagram inventory
A bullet list of every mobject the scene needs. One item looks like:

- **id**: triangle_abc
  **kind**: Polygon
  **purpose**: the central right triangle
  **first_beat**: 1

Allowed kinds: Text, MathTex, Axes, NumberPlane, NumberLine, Arrow, \
Line, Circle, Dot, Rectangle, Square, Polygon, Brace, VGroup, Surface, \
ThreeDAxes.

Rules:
- id is unique and lowercase snake_case — only letters, digits, and \
underscores.
- first_beat is the beat number (1–6) where this object first appears.
- Include only objects that actually appear in some beat.
- If math is central, give the exact LaTeX for each MathTex (no `$` \
delimiters), e.g. `F = m a`, `a^2 + b^2 = c^2`.

## Duration
Exactly one number in seconds between 2 and 30. Shortest duration that \
comfortably fits the beats — no padding waits, no crowding.

## Decline
Write exactly one of:
- no
- yes: <short reason>

Only decline if the concept is genuinely not visually teachable — pure \
trivia, a list of names, or something with no visual structure.

## Rules
- Keep the plan minimal. A clear 3-beat plan beats a crowded 6-beat plan.
- Prefer progressive disclosure — introduce ideas one at a time.
- Favor diagrams, equations, geometric relations, motion, comparison, \
transformation, and cause-effect visuals.
- No code, no numeric coordinates, no style prose, no camera \
instructions, no narration-like wording ("now we will see…")."""


def build_system_blocks() -> list[dict]:
    return [{"type": "text", "text": PLANNER_RULES, "cache_control": {"type": "ephemeral"}}]


def build_user_message(concept: str) -> str:
    return (
        f"Concept: {concept.strip()}\n\n"
        f"Produce the scene plan now."
    )
