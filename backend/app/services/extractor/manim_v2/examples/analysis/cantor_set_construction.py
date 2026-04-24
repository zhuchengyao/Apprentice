from manim import *
import numpy as np


class CantorSetConstructionExample(Scene):
    """
    Cantor set: start with [0, 1]; at each step, remove the middle
    third of each remaining interval. Result is uncountable, has
    Lebesgue measure 0, and Hausdorff dimension log 2 / log 3.

    SINGLE_FOCUS:
      Stack of bars representing the Cantor set at depths 0..7.
      ValueTracker depth_tr grows; always_redraw rebuilds bars.
    """

    def construct(self):
        title = Tex(r"Cantor set: remove middle thirds",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Each row is at a certain y, representing the set at depth k
        depth_tr = ValueTracker(0)

        def cantor_intervals(depth):
            intervals = [(0.0, 1.0)]
            for _ in range(depth):
                new_ints = []
                for (l, r) in intervals:
                    third = (r - l) / 3
                    new_ints.append((l, l + third))
                    new_ints.append((r - third, r))
                intervals = new_ints
            return intervals

        def stacked_bars():
            d_cur = int(round(depth_tr.get_value()))
            d_cur = max(0, min(d_cur, 7))
            grp = VGroup()
            for d in range(d_cur + 1):
                ints = cantor_intervals(d)
                y = 2.5 - d * 0.55
                for (l, r) in ints:
                    x_lo = -5.5 + 11 * l
                    x_hi = -5.5 + 11 * r
                    w = x_hi - x_lo
                    if w < 0.005:
                        continue
                    bar = Rectangle(width=w, height=0.3,
                                     color=YELLOW, fill_opacity=0.7,
                                     stroke_width=0)
                    bar.move_to([(x_lo + x_hi) / 2, y, 0])
                    grp.add(bar)
                # Depth label
                grp.add(MathTex(rf"d={d}", font_size=18, color=BLUE
                                  ).move_to([-6.3, y, 0]))
            return grp

        self.add(always_redraw(stacked_bars))

        def info():
            d = int(round(depth_tr.get_value()))
            d = max(0, min(d, 7))
            # Number of intervals = 2^d; total length = (2/3)^d
            return VGroup(
                MathTex(rf"d = {d}", color=YELLOW, font_size=24),
                MathTex(rf"\text{{intervals}} = 2^d = {2**d}",
                         color=GREEN, font_size=22),
                MathTex(rf"\text{{total length}} = (2/3)^d = {(2/3)**d:.5f}",
                         color=ORANGE, font_size=20),
                MathTex(r"\dim_H = \log 2 / \log 3 \approx 0.6309",
                         color=RED, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        for d in range(1, 8):
            self.play(depth_tr.animate.set_value(d),
                       run_time=0.8, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
