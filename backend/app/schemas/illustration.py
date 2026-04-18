"""Illustration DSL — a constrained JSON spec that the AI emits to illustrate
a knowledge point, and the frontend IllustrationPlayer renders as an animated
SVG scene.

Design tenets:
  - Finite set of element types (no raw SVG/HTML) — prevents injection and
    keeps visual style consistent under theming.
  - Palette tokens (not free-form hex) so dark/light themes work out of the
    box and the brand palette can be swapped later.
  - Bounded dimensions, element counts, step counts — caps keep one bad
    spec from locking up the renderer.
  - Step-based timeline with explicit target ids; no implicit magic.

The Pydantic models here are the authoritative schema. The AI generator
validates every returned spec before persisting; the frontend trusts the
shape and reuses an equivalent TypeScript type.
"""

from __future__ import annotations

import re
from typing import Annotated, Literal, Union

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator


# ── Limits ────────────────────────────────────────────────────

MAX_ELEMENTS = 24
MAX_STEPS = 12
MAX_ANIMATIONS_PER_STEP = 8
MAX_CAPTION_LEN = 140
MAX_TEXT_LEN = 200
MAX_LATEX_LEN = 240
MAX_POLYLINE_POINTS = 64
MAX_PATH_LEN = 600  # characters of `d`
MIN_STEP_MS = 120
MAX_STEP_MS = 4000

# Scene canvas is normalized to a fixed viewBox so the renderer can scale
# fluidly to the popover width. We allow a modest range to let Claude pick
# a sensible aspect ratio per illustration.
MIN_CANVAS = 120
MAX_CANVAS = 800


# ── Palette & easing tokens ────────────────────────────────────

Palette = Literal[
    "primary", "accent", "muted", "fg", "bg",
    "success", "warning", "danger",
    "fg-soft", "bg-soft",
    "none",
]

Easing = Literal["linear", "easeIn", "easeOut", "easeInOut"]

TextAnchor = Literal["start", "middle", "end"]


# ── Shared style fields ───────────────────────────────────────

class Stroke(BaseModel):
    model_config = ConfigDict(extra="forbid")

    color: Palette = "fg"
    width: Annotated[float, Field(ge=0, le=12)] = 1.5
    dash: Annotated[str, StringConstraints(max_length=40)] | None = None
    linecap: Literal["butt", "round", "square"] = "round"

    @field_validator("dash")
    @classmethod
    def _dash_shape(cls, v: str | None) -> str | None:
        if v is None:
            return v
        if not re.fullmatch(r"[0-9 ,.]+", v):
            raise ValueError("dash must contain only digits, spaces, commas, dots")
        return v


# ── Element variants ──────────────────────────────────────────

class _ElemBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: Annotated[str, StringConstraints(min_length=1, max_length=32, pattern=r"^[a-zA-Z0-9_\-]+$")]
    opacity: Annotated[float, Field(ge=0, le=1)] = 1.0
    fill: Palette = "none"
    stroke: Stroke | None = None


class Circle(_ElemBase):
    type: Literal["circle"]
    cx: Annotated[float, Field(ge=-MAX_CANVAS, le=MAX_CANVAS * 2)]
    cy: Annotated[float, Field(ge=-MAX_CANVAS, le=MAX_CANVAS * 2)]
    r: Annotated[float, Field(ge=0, le=MAX_CANVAS)]


class Rect(_ElemBase):
    type: Literal["rect"]
    x: Annotated[float, Field(ge=-MAX_CANVAS, le=MAX_CANVAS * 2)]
    y: Annotated[float, Field(ge=-MAX_CANVAS, le=MAX_CANVAS * 2)]
    w: Annotated[float, Field(ge=0, le=MAX_CANVAS * 2)]
    h: Annotated[float, Field(ge=0, le=MAX_CANVAS * 2)]
    rx: Annotated[float, Field(ge=0, le=MAX_CANVAS)] = 0


class Line(_ElemBase):
    type: Literal["line"]
    x1: Annotated[float, Field(ge=-MAX_CANVAS, le=MAX_CANVAS * 2)]
    y1: Annotated[float, Field(ge=-MAX_CANVAS, le=MAX_CANVAS * 2)]
    x2: Annotated[float, Field(ge=-MAX_CANVAS, le=MAX_CANVAS * 2)]
    y2: Annotated[float, Field(ge=-MAX_CANVAS, le=MAX_CANVAS * 2)]


class Arrow(_ElemBase):
    type: Literal["arrow"]
    x1: float
    y1: float
    x2: float
    y2: float
    head: Literal["end", "both", "none"] = "end"


class Polyline(_ElemBase):
    type: Literal["polyline"]
    points: Annotated[
        list[tuple[float, float]],
        Field(min_length=2, max_length=MAX_POLYLINE_POINTS),
    ]
    closed: bool = False


_PATH_D_ALLOWED = re.compile(r"^[MLHVCSQTAZmlhvcsqtaz0-9eE\s,+\-.]+$")


class Path(_ElemBase):
    """Generic path. `d` is strictly validated: only M/L/H/V/C/S/Q/T/A/Z
    commands, numbers, signs, commas and spaces. No inline scripting or
    suspect characters reach the DOM."""
    type: Literal["path"]
    d: Annotated[str, StringConstraints(min_length=1, max_length=MAX_PATH_LEN)]

    @field_validator("d")
    @classmethod
    def _validate_d(cls, v: str) -> str:
        if not _PATH_D_ALLOWED.match(v):
            raise ValueError("path `d` contains disallowed characters")
        return v


class Text(_ElemBase):
    type: Literal["text"]
    x: float
    y: float
    content: Annotated[str, StringConstraints(min_length=1, max_length=MAX_TEXT_LEN)]
    size: Annotated[float, Field(ge=6, le=48)] = 13
    weight: Literal["regular", "medium", "bold"] = "regular"
    anchor: TextAnchor = "middle"
    color: Palette = "fg"


class Latex(_ElemBase):
    type: Literal["latex"]
    x: float
    y: float
    content: Annotated[str, StringConstraints(min_length=1, max_length=MAX_LATEX_LEN)]
    size: Annotated[float, Field(ge=8, le=36)] = 14
    anchor: TextAnchor = "middle"
    color: Palette = "fg"


class Axes(_ElemBase):
    """Convenience primitive: drawn as a pair of arrows from (ox, oy) to
    (ox + xLen, oy) and (ox, oy - yLen). Labels are optional."""
    type: Literal["axes"]
    ox: float
    oy: float
    xLen: Annotated[float, Field(ge=10, le=MAX_CANVAS * 2)]
    yLen: Annotated[float, Field(ge=10, le=MAX_CANVAS * 2)]
    xLabel: Annotated[str, StringConstraints(max_length=32)] | None = None
    yLabel: Annotated[str, StringConstraints(max_length=32)] | None = None


Element = Annotated[
    Union[Circle, Rect, Line, Arrow, Polyline, Path, Text, Latex, Axes],
    Field(discriminator="type"),
]


# ── Animation keyframes ───────────────────────────────────────

class AnimSet(BaseModel):
    """The values we can animate on an element. All optional; unset keys
    leave the existing attribute alone."""
    model_config = ConfigDict(extra="forbid")

    opacity: Annotated[float, Field(ge=0, le=1)] | None = None
    x: float | None = None
    y: float | None = None
    scale: Annotated[float, Field(ge=0, le=10)] | None = None
    rotate: Annotated[float, Field(ge=-720, le=720)] | None = None
    # For circle: cx, cy, r. For rect: x, y, w, h. The renderer picks
    # the ones that apply; extraneous keys are harmless.
    cx: float | None = None
    cy: float | None = None
    r: Annotated[float, Field(ge=0, le=MAX_CANVAS)] | None = None
    w: Annotated[float, Field(ge=0, le=MAX_CANVAS * 2)] | None = None
    h: Annotated[float, Field(ge=0, le=MAX_CANVAS * 2)] | None = None
    # For path/polyline/arrow/line: drawn-length fraction (0..1).
    draw: Annotated[float, Field(ge=0, le=1)] | None = None
    color: Palette | None = None


class Animation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    target: Annotated[str, StringConstraints(min_length=1, max_length=32)]
    set: AnimSet
    easing: Easing = "easeOut"
    delay: Annotated[int, Field(ge=0, le=3000)] = 0
    duration: Annotated[int, Field(ge=60, le=MAX_STEP_MS)] | None = None


class Step(BaseModel):
    model_config = ConfigDict(extra="forbid")

    duration: Annotated[int, Field(ge=MIN_STEP_MS, le=MAX_STEP_MS)] = 800
    caption: Annotated[str, StringConstraints(max_length=MAX_CAPTION_LEN)] | None = None
    animations: Annotated[list[Animation], Field(max_length=MAX_ANIMATIONS_PER_STEP)] = []


# ── Top-level spec ────────────────────────────────────────────

class IllustrationSpec(BaseModel):
    """The full scene. v=1 lets us version the shape without breaking
    stored rows later."""
    model_config = ConfigDict(extra="forbid")

    v: Literal[1] = 1
    w: Annotated[int, Field(ge=MIN_CANVAS, le=MAX_CANVAS)] = 400
    h: Annotated[int, Field(ge=MIN_CANVAS, le=MAX_CANVAS)] = 240
    title: Annotated[str, StringConstraints(max_length=120)] | None = None
    elements: Annotated[list[Element], Field(max_length=MAX_ELEMENTS)]
    steps: Annotated[list[Step], Field(min_length=1, max_length=MAX_STEPS)]

    @field_validator("steps")
    @classmethod
    def _targets_exist(cls, steps: list[Step], info):
        elements = info.data.get("elements") or []
        known = {e.id for e in elements}
        for i, step in enumerate(steps):
            for a in step.animations:
                if a.target not in known:
                    raise ValueError(
                        f"step {i}: animation target '{a.target}' not in elements"
                    )
        return steps

    @field_validator("elements")
    @classmethod
    def _unique_ids(cls, elements: list[Element]):
        seen: set[str] = set()
        for e in elements:
            if e.id in seen:
                raise ValueError(f"duplicate element id: {e.id}")
            seen.add(e.id)
        return elements


def validate_spec(raw: dict) -> IllustrationSpec:
    """Strictly parse+validate. Raises pydantic.ValidationError on failure."""
    return IllustrationSpec.model_validate(raw)
