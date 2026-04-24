from manim import *
import numpy as np


class WheatAndChessboardExample(Scene):
    """
    Wheat and chessboard problem: 1 grain on square 1, 2 on square
    2, 4 on square 3, ..., total = 2^64 - 1 ≈ 1.8 × 10^19.

    SINGLE_FOCUS:
      Chessboard grid 8×8; ValueTracker k_tr steps k = 1..64;
      always_redraw colors each covered square YELLOW-brightness
      proportional to log(2^(k-1)) while a live counter shows the
      cumulative total 2^k - 1.
    """

    def construct(self):
        title = Tex(r"Wheat on chessboard: $\sum_{k=0}^{63} 2^k = 2^{64} - 1$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Build 8×8 grid
        grid_origin = np.array([-4.5, -2.8, 0])
        sq_size = 0.55
        squares = []
        for r in range(8):
            for c in range(8):
                color = GREY_B if (r + c) % 2 == 0 else GREY_D
                s = Square(side_length=sq_size, color=WHITE,
                             fill_opacity=0.85, fill_color=color,
                             stroke_width=1)
                s.move_to(grid_origin + np.array([c * sq_size, r * sq_size, 0]))
                squares.append(s)
        self.play(FadeIn(VGroup(*squares)), run_time=1.5)

        # Covered-squares indicator (a YELLOW dot placed on each with amount ∝ k)
        k_tr = ValueTracker(0)

        def covered():
            k = int(round(k_tr.get_value()))
            k = max(0, min(k, 64))
            grp = VGroup()
            import math
            for idx in range(k):
                sq = squares[idx]
                grains = 2 ** idx
                # Scale fill opacity by log-brightness
                intensity = min(1.0, 0.2 + 0.04 * math.log2(grains + 1))
                overlay = Square(side_length=sq_size,
                                   color=YELLOW, fill_opacity=intensity,
                                   stroke_width=0).move_to(sq.get_center())
                grp.add(overlay)
            return grp

        self.add(always_redraw(covered))

        def info():
            k = int(round(k_tr.get_value()))
            k = max(0, min(k, 64))
            total = 2 ** k - 1 if k > 0 else 0
            last = 2 ** (k - 1) if k > 0 else 0
            return VGroup(
                MathTex(rf"\text{{square}} = {k}",
                         color=WHITE, font_size=24),
                MathTex(rf"\text{{this square}} = 2^{{{max(k-1, 0)}}} = {last:,}".replace(",", r"\,"),
                         color=YELLOW, font_size=22),
                MathTex(rf"\text{{total}} = 2^{{{k}}} - 1",
                         color=GREEN, font_size=22),
                MathTex(rf"\approx {total:.3e}",
                         color=GREEN, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.4).shift(UP * 0.5)

        self.add(always_redraw(info))

        # Sweep all 64 squares
        self.play(k_tr.animate.set_value(64),
                   run_time=10, rate_func=linear)

        final = MathTex(r"2^{64} - 1 = 18,\!446,\!744,\!073,\!709,\!551,\!615",
                          color=YELLOW, font_size=22
                          ).to_edge(DOWN, buff=0.3)
        self.play(Write(final))
        self.wait(0.5)
