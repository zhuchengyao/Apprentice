"""Stage 1 prompt — Text → Scene Plan (free-form pedagogical markdown).

The plan is deliberately not machine-readable: we want the LLM to think
about *how to teach* the concept visually before committing to concrete
mobjects and timing. Stage 2 translates the plan to structured JSON.
"""

from __future__ import annotations


PLANNER_RULES = """\
You design a short educational Manim animation (6–14 seconds) for one \
knowledge point. Your job is to plan it, not to write code yet.

Return a concise markdown plan with exactly these sections:

## Learning objective
One sentence stating what the viewer should understand after watching.

## Visual metaphor
One or two sentences describing the central visual representation \
(e.g. "a mass on a frictionless table pushed by a horizontal arrow", \
"a unit circle traced by a rotating radius").

## Beats
A numbered list of 3–6 beats. For each beat:
- **t**: approximate start second (0, 2.0, 4.5, …)
- **show**: what appears on screen this beat
- **why**: one phrase explaining its pedagogical purpose

## Diagram inventory
Bullet list of the mobjects needed: names + kind (Text, MathTex, Axes, \
Arrow, Circle, …) + one-line purpose each.

## Duration
A single number in seconds (4–18).

## Decline
Write ONLY "no" — unless the concept is a poor fit for visual animation \
(e.g. purely etymological, a list of names, trivia), in which case write \
"yes: <short reason>".

Rules:
- Keep it minimal. A clear three-beat plan beats a crowded six-beat plan.
- Prefer progressive disclosure: show one idea per beat, don't dump \
everything at once.
- If math is central, name specific equations you'll display with MathTex.
- Output plain markdown. No code fences, no preamble."""


def build_system_blocks() -> list[dict]:
    return [{"type": "text", "text": PLANNER_RULES, "cache_control": {"type": "ephemeral"}}]


def build_user_message(
    concept: str,
    explanation: str,
    *,
    chapter_title: str | None = None,
    section_title: str | None = None,
) -> str:
    ctx = ""
    if chapter_title:
        ctx += f"Chapter: {chapter_title}\n"
    if section_title:
        ctx += f"Section: {section_title}\n"
    exp = explanation.strip()
    if len(exp) > 2000:
        exp = exp[:2000] + "…"
    return (
        f"{ctx}"
        f"Concept: {concept.strip()}\n\n"
        f"Explanation:\n{exp}\n\n"
        f"Produce the scene plan now."
    )
