"""Generate an illustration spec for a single knowledge point.

The model returns a JSON object conforming to `IllustrationSpec`. We parse
+ Pydantic-validate before returning — any schema error yields None so
the pipeline moves on without an illustration rather than failing.
"""

import asyncio
import json
import logging
import re

from pydantic import ValidationError

from app.config import settings
from app.schemas.illustration import IllustrationSpec, validate_spec
from app.services.ai_client import chat_completion

logger = logging.getLogger(__name__)


# A compact schema description the model can follow. We lean on a few short
# canonical examples rather than a formal JSON-Schema dump — examples
# generalize better and cost fewer output tokens at inference.
_ILLUSTRATION_PROMPT = """\
You produce a small animated SVG scene that illustrates a single knowledge \
point for a student. Output STRICT JSON only — no prose, no markdown fences.

If the concept is not well-suited to a visual illustration (e.g. purely \
linguistic, historical trivia, or already obvious from words), return the \
exact string:  null

Otherwise return an object matching this shape. Units are SVG pixels in a \
viewBox from (0,0) to (w,h). Keep w ≤ 400 and h ≤ 260 — this renders inside \
a narrow tutor panel.

{
  "v": 1,
  "w": 400,
  "h": 220,
  "title": "short label",
  "elements": [ /* 2–20 items */ ],
  "steps":    [ /* 2–6 items  */ ]
}

Allowed element types and their required keys:

  { "id":"c1", "type":"circle", "cx":200, "cy":110, "r":40,
    "fill":"primary", "stroke":{"color":"fg","width":1.5}, "opacity":0 }
  { "id":"r1", "type":"rect", "x":40, "y":60, "w":120, "h":70, "rx":8,
    "fill":"accent", "opacity":0 }
  { "id":"l1", "type":"line", "x1":20, "y1":180, "x2":380, "y2":180,
    "stroke":{"color":"muted","width":1,"dash":"4 4"} }
  { "id":"a1", "type":"arrow", "x1":100, "y1":100, "x2":250, "y2":100,
    "stroke":{"color":"primary","width":2}, "head":"end" }
  { "id":"p1", "type":"polyline",
    "points":[[20,200],[80,140],[160,170],[240,90]],
    "stroke":{"color":"primary","width":2} }
  { "id":"pa1","type":"path", "d":"M20 200 C80 60 260 60 380 200",
    "stroke":{"color":"primary","width":2} }
  { "id":"t1", "type":"text", "x":200, "y":30, "content":"Newton's 2nd law",
    "size":13, "weight":"medium", "anchor":"middle", "color":"fg" }
  { "id":"x1", "type":"latex", "x":200, "y":200, "content":"F = ma",
    "size":16, "anchor":"middle", "color":"fg" }
  { "id":"ax", "type":"axes", "ox":40, "oy":180, "xLen":320, "yLen":140,
    "xLabel":"t", "yLabel":"v", "stroke":{"color":"fg","width":1.2} }

Color values MUST be one of these palette tokens (NOT hex, NOT names):
  "primary", "accent", "muted", "fg", "fg-soft", "bg", "bg-soft",
  "success", "warning", "danger", "none".

Each step advances the scene in time. A step looks like:

  {
    "duration": 700,
    "caption": "One short sentence (≤120 chars).",
    "animations": [
      { "target":"c1", "set": {"opacity":1}, "easing":"easeOut" },
      { "target":"t1", "set": {"opacity":1}, "delay":200 }
    ]
  }

Animatable keys on `set`: opacity (0..1), x, y, scale (0..10), rotate (deg),
cx, cy, r, w, h, draw (0..1 — for paths/lines/arrows/polylines, animates
stroke-dashoffset to draw in), color (palette token).

Rules:
- First step should typically fade elements in from opacity 0 to 1.
- Build complexity gradually: introduce shapes, then labels, then motion.
- Captions narrate WHAT the viewer is seeing — not meta commentary.
- Every animation's `target` MUST match an element id you declared.
- All numeric coords must fit inside the canvas (0..w, 0..h).
- Keep element count ≤ 20. Keep step count between 2 and 6.
- NEVER include external URLs, script tags, HTML, or inline styles.

Concept: __CONCEPT__

Author's explanation:
__EXPLANATION__
"""


def _strip_fences(text: str) -> str:
    t = text.strip()
    if t.startswith("```"):
        lines = [l for l in t.splitlines() if not l.strip().startswith("```")]
        t = "\n".join(lines).strip()
    return t


def _extract_first_json(text: str) -> str | None:
    """Return the outermost JSON object or the literal 'null' in `text`."""
    s = text.strip()
    if s == "null":
        return "null"
    # Find the first balanced {...}. Good enough for our model's outputs —
    # we don't need to handle nested strings containing unescaped braces
    # because Claude reliably escapes them.
    start = s.find("{")
    if start < 0:
        return None
    depth = 0
    in_str = False
    esc = False
    for i in range(start, len(s)):
        ch = s[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return s[start : i + 1]
    return None


async def generate_illustration(
    concept: str,
    explanation: str,
    *,
    model: str | None = None,
    caller: str = "kp_illustration",
) -> dict | None:
    """Generate and validate an illustration spec for a KP.

    Returns a dict (IllustrationSpec.model_dump) ready to store in JSONB,
    or None if the model declined / output was unparseable / invalid.
    """
    prompt = (
        _ILLUSTRATION_PROMPT
        .replace("__CONCEPT__", concept[:300])
        .replace("__EXPLANATION__", (explanation or "")[:2000])
    )

    try:
        raw = await chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2048,
            caller=caller,
            model=model or settings.ai_model,
        )
    except Exception as e:
        logger.warning("Illustration LLM call failed for %s: %s", concept[:40], e)
        return None

    candidate = _extract_first_json(_strip_fences(raw))
    if candidate is None:
        return None
    if candidate == "null":
        return None

    try:
        data = json.loads(candidate)
    except json.JSONDecodeError as e:
        logger.info("Illustration JSON parse failed for %s: %s", concept[:40], e)
        return None

    try:
        spec: IllustrationSpec = validate_spec(data)
    except ValidationError as e:
        logger.info(
            "Illustration schema validation failed for %s: %s",
            concept[:40], _first_error(e),
        )
        return None

    return spec.model_dump(mode="json", exclude_none=True)


def _first_error(e: ValidationError) -> str:
    errs = e.errors()
    if not errs:
        return str(e)
    first = errs[0]
    loc = ".".join(str(p) for p in first.get("loc", []))
    return f"{loc}: {first.get('msg', '')}"


async def generate_illustrations_batch(
    kps: list[tuple[str, str]],
    *,
    concurrency: int = 4,
    model: str | None = None,
) -> list[dict | None]:
    """Generate illustrations for many KPs with bounded concurrency.

    `kps` is a list of (concept, explanation). Returns a list parallel to
    the input, with None for KPs where generation failed or was declined.
    """
    sem = asyncio.Semaphore(max(1, concurrency))

    async def _one(concept: str, explanation: str) -> dict | None:
        async with sem:
            return await generate_illustration(concept, explanation, model=model)

    return await asyncio.gather(*(_one(c, e) for c, e in kps))
