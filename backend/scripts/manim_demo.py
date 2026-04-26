"""Manually drive the Manim animation pipeline from the shell.

Usage (from backend/):
    python -m scripts.manim_demo "Newton's second law"

    # Optional flags:
    #   --model claude-opus-4-7
    #   --quality medium   # low | medium | high
    #   --out /tmp/my.mp4  # write MP4 here (default: backend/uploads/manim/)

Writes the MP4 to disk and prints the path. Nothing is persisted to the DB.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import sys
from pathlib import Path

from app.services.extractor.manim_v2 import generate_manim_animation


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Render a Manim animation for a concept.")
    p.add_argument("concept", help="Short concept label (e.g. 'Newton's second law')")
    p.add_argument("--model", default=None,
                   help="Override model (defaults to illustration_model or ai_model)")
    p.add_argument("--quality", default="low", choices=["low", "medium", "high"])
    p.add_argument("--out", default=None, help="Path for the output MP4")
    p.add_argument("--verbose", "-v", action="store_true")
    return p.parse_args()


async def _main() -> int:
    args = _parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    out_dir: Path | None = None
    if args.out:
        out_path = Path(args.out).expanduser().resolve()
        out_dir = out_path.parent

    outcome = await generate_manim_animation(
        args.concept,
        model=args.model,
        quality=args.quality,
        output_dir=out_dir,
        caller="manim_demo",
    )

    print()
    print(f"result         : {'OK' if outcome.accepted else 'FAIL'}")
    print(f"failure_kind   : {outcome.failure_kind}")
    if outcome.failure_detail:
        print(f"failure_detail : {outcome.failure_detail}")
    if outcome.decline_reason:
        print(f"decline_reason : {outcome.decline_reason}")
    print(f"latency_ms     : {outcome.latency_ms}")

    if outcome.output_path:
        final = outcome.output_path
        if args.out:
            final_dest = Path(args.out).expanduser().resolve()
            if final != final_dest:
                final_dest.parent.mkdir(parents=True, exist_ok=True)
                final.replace(final_dest)
                final = final_dest
        print(f"output         : {final}")
        return 0

    if outcome.render_stderr_tail:
        print("--- render stderr (tail) ---")
        print(outcome.render_stderr_tail[-1500:])

    if outcome.code:
        code_dump = Path("/tmp") / f"manim_failed_{outcome.failure_kind}.py"
        code_dump.write_text(outcome.code, encoding="utf-8")
        print(f"generated_code : {code_dump}")

    return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(_main()))
