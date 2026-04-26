"""Structured Manim DSL — Stage 2 output, Stage 3 input.

Rationale: constraining the LLM to a validated JSON spec decouples
*what to show* from *how to code it*, so stage 3 can lean on a retrieved
example library without drifting into arbitrary Python. Kind-specific
payloads live in an untyped `params` dict — the prompt documents the
keys per kind, which keeps the schema compact for JSON-mode generation
without forcing a 20-way discriminated union over every Manim class.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


# ── Kind enums ────────────────────────────────────────────────

ObjectKind = Literal[
    # Text / math
    "Text", "MarkupText", "Tex", "MathTex",
    # Basic shapes
    "Dot", "Circle", "Square", "Rectangle", "RegularPolygon", "Polygon",
    "Ellipse", "Triangle", "Star",
    # Lines / arrows
    "Line", "DashedLine", "Arrow", "DoubleArrow", "Vector",
    # Plotting / axes
    "NumberLine", "Axes", "NumberPlane", "ComplexPlane", "PolarPlane",
    "ParametricFunction", "ImplicitFunction", "FunctionGraph",
    # 3D
    "ThreeDAxes", "Sphere", "Cube", "Torus", "Cylinder", "Cone",
    "Surface", "ParametricSurface",
    # Annotations / helpers
    "Brace", "BraceBetweenPoints", "Angle", "RightAngle",
    "SurroundingRectangle", "BackgroundRectangle",
    # Grouping (children must reference other ids)
    "VGroup", "Group",
]

ActionKind = Literal[
    # Creation / removal
    "Write", "Unwrite", "Create", "Uncreate",
    "FadeIn", "FadeOut", "DrawBorderThenFill",
    "GrowArrow", "GrowFromCenter", "SpinInFromNothing",
    # Transformations between mobjects
    "Transform", "ReplacementTransform",
    "TransformMatchingTex", "TransformMatchingShapes",
    # Emphasis
    "Indicate", "Flash", "Circumscribe", "Wiggle", "FocusOn", "ShowPassingFlash",
    # Motion
    "MoveAlongPath", "Rotate", "Rotating", "MoveTo", "Shift", "Scale",
    # Animate-method (applies to .animate syntax — param `method` e.g. "shift", args)
    "AnimateMethod",
    # Updaters
    "AddUpdater", "RemoveUpdater", "SuspendUpdating", "ResumeUpdating",
    # Camera moves
    "CameraMoveTo", "CameraSetOrientation", "CameraSetZoom",
    "AmbientCameraRotationStart", "AmbientCameraRotationStop",
    # Timing
    "Wait",
]

CameraKind = Literal["Scene", "MovingCameraScene", "ZoomedScene", "ThreeDScene"]

# Direction tokens understood by Manim (UP, DOWN, LEFT, RIGHT, UL, UR, DL, DR, ORIGIN)
DirectionKind = Literal["UP", "DOWN", "LEFT", "RIGHT", "UL", "UR", "DL", "DR", "ORIGIN", "IN", "OUT"]


# ── Leaf models ───────────────────────────────────────────────

class Style(BaseModel):
    """Visual styling — all keys optional, defaults come from Manim."""
    model_config = ConfigDict(extra="forbid")

    color: str | None = None        # e.g. "BLUE" (constant name) or "#3399FF"
    fill_color: str | None = None
    fill_opacity: float | None = None
    stroke_color: str | None = None
    stroke_width: float | None = None
    stroke_opacity: float | None = None
    opacity: float | None = None
    font_size: float | None = None
    z_index: int | None = None


class Placement(BaseModel):
    """Absolute or relative positioning. Prefer `anchor` for layout."""
    model_config = ConfigDict(extra="forbid")

    position: tuple[float, float, float] | None = None   # absolute [x,y,z]
    rotation: float | None = None                         # radians about z-axis (2D) or see `rotation_axis`
    rotation_axis: tuple[float, float, float] | None = None
    scale: float | None = None
    shift: tuple[float, float, float] | None = None       # applied after `position`/`anchor`


class Anchor(BaseModel):
    """Relative placement: `next_to(<relative_to>, <direction>, buff=...)`."""
    model_config = ConfigDict(extra="forbid")

    relative_to: str                     # id of another MObject
    direction: DirectionKind = "UP"
    buff: float = 0.2
    aligned_edge: DirectionKind | None = None


class MObject(BaseModel):
    """A scene element. `params` carries kind-specific values.

    Common `params` keys per kind (non-exhaustive):
      - Text / MarkupText:         {text, weight?, slant?, font?}
      - MathTex / Tex:             {tex: "F = ma"}  (raw LaTeX, no $ delimiters)
      - Circle:                    {radius?}
      - Square:                    {side_length?}
      - Rectangle:                 {width?, height?}
      - RegularPolygon:            {n, radius?}
      - Polygon:                   {vertices: [[x,y,z], ...]}
      - Line / DashedLine:         {start: [x,y,z], end: [x,y,z]}
      - Arrow / DoubleArrow:       {start, end, buff?, stroke_width?, max_tip_length_to_length_ratio?}
      - Vector:                    {direction: [x,y,z]}
      - NumberLine:                {x_range: [min,max,step]?, length?, include_numbers?}
      - Axes:                      {x_range, y_range, x_length?, y_length?, tips?, axis_config?}
      - NumberPlane:               {x_range?, y_range?, background_line_style?}
      - ParametricFunction:        {function: "lambda t: [cos(t), sin(t), 0]", t_range: [a,b]}
      - ImplicitFunction:          {func: "lambda x,y: x**2 + y**2 - 1"}
      - FunctionGraph:             {func: "lambda x: x**2", x_range?}
      - ThreeDAxes:                {x_range?, y_range?, z_range?}
      - Sphere / Cube / Torus / Cylinder / Cone:  {…}
      - Surface / ParametricSurface:
            {func: "lambda u,v: [u, v, sin(u)*cos(v)]", u_range, v_range, resolution?}
      - Brace:                     {target_id: "<mobject id>", direction?: DirectionKind}
      - BraceBetweenPoints:        {start, end}
      - Angle / RightAngle:        {line1_id, line2_id, radius?, quadrant?}
      - SurroundingRectangle:      {target_id, buff?, color?}
      - VGroup / Group:            {} (uses `children`)
    """
    model_config = ConfigDict(extra="forbid")

    id: str = Field(..., min_length=1, max_length=64,
                    description="Stable id used to reference this object in timeline actions")
    kind: ObjectKind
    params: dict[str, Any] = Field(default_factory=dict)
    style: Style | None = None
    placement: Placement | None = None
    anchor: Anchor | None = None
    children: list[str] = Field(default_factory=list,
                                description="Ids of child mobjects (only meaningful for VGroup/Group)")
    label: str | None = Field(None, description="Optional human note; ignored by codegen")

    @field_validator("id")
    @classmethod
    def _id_shape(cls, v: str) -> str:
        if not v.replace("_", "").isalnum():
            raise ValueError("id must be alphanumeric or underscore")
        return v


class ValueTrackerSpec(BaseModel):
    """A named ValueTracker that drives updaters over a time window."""
    model_config = ConfigDict(extra="forbid")

    name: str                        # python identifier
    start: float
    end: float
    duration: float                  # seconds the tracker animates for
    start_time: float = 0.0          # when within the scene it starts animating


class Action(BaseModel):
    """One animation, typically wrapped in `self.play(...)`.

    Common `params` keys per kind (non-exhaustive):
      - Write / FadeIn / Create / GrowArrow:    {}
      - Transform / ReplacementTransform:       {to_id: "<other mobject id>"}
      - TransformMatchingTex:                   {to_id}
      - Indicate:                               {scale_factor?, color?}
      - Flash:                                  {color?, line_length?}
      - Rotate / Rotating:                      {angle: 1.57, about_point?}
      - MoveAlongPath:                          {path_id: "<mobject id>"}
      - MoveTo:                                 {point: [x,y,z] | target_id: str}
      - Shift:                                  {vector: [x,y,z]}
      - Scale:                                  {factor: 1.5}
      - AnimateMethod:                          {method: "shift", args: [...], kwargs: {...}}
      - CameraMoveTo:                           {point: [x,y,z]}
      - CameraSetOrientation:                   {phi: 1.1, theta: -0.7}
      - CameraSetZoom:                          {zoom: 1.5}
      - AmbientCameraRotationStart:             {rate?: 0.1}
      - AmbientCameraRotationStop:              {}
      - AddUpdater:                             {updater: "<python expr referencing tracker names>"}
      - Wait:                                   {} (target is ignored)
    """
    model_config = ConfigDict(extra="forbid")

    kind: ActionKind
    target: str | None = None             # id of the mobject (None for Wait / pure camera moves)
    duration: float = Field(1.0, gt=0.0, le=10.0)
    params: dict[str, Any] = Field(default_factory=dict)
    rate_func: str | None = None          # e.g. "smooth", "linear", "there_and_back"


class Beat(BaseModel):
    """A moment in the timeline where ≥1 actions play together."""
    model_config = ConfigDict(extra="forbid")

    t: float = Field(0.0, ge=0.0, description="Start time in seconds")
    parallel: list[Action] = Field(..., min_length=1,
                                   description="Actions that run simultaneously inside one self.play(...)")


class Camera(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scene_type: CameraKind = "Scene"
    phi: float | None = None              # ThreeDScene initial polar
    theta: float | None = None            # ThreeDScene initial azimuth
    zoom: float | None = None             # MovingCameraScene / ZoomedScene initial
    frame_center: tuple[float, float, float] | None = None


# ── Top-level spec ────────────────────────────────────────────

class SceneSpec(BaseModel):
    """Structured plan for one Manim scene."""
    model_config = ConfigDict(extra="forbid")

    scene_id: str = Field(..., min_length=1, max_length=64)
    learning_objective: str = Field(..., max_length=400)
    duration_s: float = Field(..., ge=2.0, le=30.0,
                              description="Target wall-clock length; codegen should honor this")
    camera: Camera = Field(default_factory=Camera)
    trackers: list[ValueTrackerSpec] = Field(default_factory=list)
    objects: list[MObject] = Field(..., min_length=1)
    timeline: list[Beat] = Field(..., min_length=1)

    @field_validator("objects")
    @classmethod
    def _unique_ids(cls, v: list[MObject]) -> list[MObject]:
        seen: set[str] = set()
        for o in v:
            if o.id in seen:
                raise ValueError(f"duplicate object id: {o.id!r}")
            seen.add(o.id)
        return v


def scene_spec_json_schema() -> dict[str, Any]:
    """Return the JSON Schema for SceneSpec — fed to the LLM in stage 2."""
    return SceneSpec.model_json_schema()
