"""Manim v2 pipeline: Text → Scene Plan → Structured Spec → Manim Code
→ Render → Feedback Loop.

Replaces the single-shot `manim_illustration` module. Public API
(`ManimInput`, `ManimOutcome`, `generate_manim_animation`,
`generate_manim_batch`, `log_manim_outcome`) is kept shape-compatible so
callers in `tasks/processing.py` and `scripts/manim_demo.py` only need
an import swap.
"""

from app.services.extractor.manim_v2.pipeline import (
    ManimInput,
    ManimOutcome,
    generate_manim_animation,
    generate_manim_batch,
    log_manim_outcome,
)

__all__ = [
    "ManimInput",
    "ManimOutcome",
    "generate_manim_animation",
    "generate_manim_batch",
    "log_manim_outcome",
]
