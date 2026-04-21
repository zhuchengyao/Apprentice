"""Stage 2 prompt — Scene Plan → Structured Spec (JSON matching SceneSpec).

Pydantic's auto-generated JSON schema is embedded so both Anthropic and
OpenAI can constrain output. Most cache-friendly bytes (rules + schema)
live in the system block; the per-KP plan is the user message.
"""

from __future__ import annotations

import json

from app.services.extractor.manim_v2.spec_model import scene_spec_json_schema


SPEC_RULES = """\
Translate the scene plan you are given into a JSON object conforming \
EXACTLY to the SceneSpec schema below.

Output contract:
- Output ONE JSON object. No prose, no markdown fences, no leading text.
- All mobject ids are unique, lowercase snake_case, referenced in \
timeline.actions[].target and in Brace/Angle/SurroundingRectangle \
params (target_id) when applicable.
- `timeline` is ordered by `t` ascending. Times inside one beat play in \
parallel; the next beat's `t` should be ≥ prior beat's `t + max(duration)`.
- `duration_s` must be within 4–18 and roughly equal \
max(beat.t + max(action.duration)) across the timeline.
- Use built-in Manim color names (BLUE, RED, GREEN, YELLOW, WHITE, \
TEAL, ORANGE, PURPLE, GRAY) in `style.color` / `style.fill_color` \
rather than hex strings.
- MathTex payload is raw LaTeX without `$` delimiters \
(e.g. {"tex": "F = m a"} not {"tex": "$F = ma$"}).
- For 3D: set `camera.scene_type` to "ThreeDScene" and give \
`camera.phi` + `camera.theta` (radians). Otherwise leave camera default.
- If the plan declined the concept, return exactly: \
{"scene_id":"declined","learning_objective":"DECLINE: <reason>",\
"duration_s":4.0,"camera":{"scene_type":"Scene"},"objects":[\
{"id":"decline_text","kind":"Text","params":{"text":"<reason>"}}],\
"timeline":[{"t":0,"parallel":[{"kind":"FadeIn","target":"decline_text","duration":1.0}]}]} \
— callers detect declines by scene_id=="declined".

Kind-specific `params` documentation is in the `MObject` docstring of \
the Python Pydantic model. Common patterns:
- Text            params: {"text": "..."}
- MathTex         params: {"tex": "F = m a"}
- Circle          params: {"radius": 1.0}
- Arrow           params: {"start": [0,0,0], "end": [2,0,0]}
- Axes            params: {"x_range": [0,5,1], "y_range": [0,10,2], "x_length": 6, "y_length": 4}
- ParametricFunction params: {"function": "lambda t: [cos(t), sin(t), 0]", "t_range": [0, 6.283]}
- Surface         params: {"func": "lambda u,v: [u, v, sin(u)*cos(v)]", "u_range": [-3,3], "v_range": [-3,3]}
- ValueTracker-driven animation: declare the tracker in `trackers`, \
then AddUpdater actions with `params.updater` as a Python lambda-like \
string referencing the tracker by `name`.

Relative positioning via `anchor` is preferred over absolute `placement.position`.

SceneSpec JSON Schema:
"""


def _schema_text() -> str:
    return json.dumps(scene_spec_json_schema(), indent=2)


def build_system_blocks() -> list[dict]:
    # Schema is large — keep it in the cached system block so it is
    # billed once per prompt-cache window rather than per KP.
    text = SPEC_RULES + "\n" + _schema_text()
    return [{"type": "text", "text": text, "cache_control": {"type": "ephemeral"}}]


def build_user_message(
    concept: str,
    plan_markdown: str,
    *,
    prior_spec_error: str | None = None,
) -> str:
    lines = [
        f"Concept: {concept.strip()}",
        "",
        "Scene plan:",
        plan_markdown.strip(),
    ]
    if prior_spec_error:
        lines += [
            "",
            "Previous attempt failed schema validation:",
            prior_spec_error.strip(),
            "Return a corrected JSON object — same requirements, no wrapper keys.",
        ]
    lines += ["", "Output the JSON object now."]
    return "\n".join(lines)
