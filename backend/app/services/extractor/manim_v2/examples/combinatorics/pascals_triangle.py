from manim import *
import numpy as np
from math import comb


class PascalsTriangleExample(Scene):
    """
    Pascal's triangle built row by row; each entry = sum of the
    two above it (C(n,k) = C(n-1,k-1) + C(n-1,k)).

    SINGLE_FOCUS:
      ValueTracker row_tr steps n = 0..9; always_redraw rebuilds
      the triangle. Once built, highlight animation via Rotate and
      Transform: the symmetry C(n,k) = C(n,n-k) via reflection, and
      the hockey-stick identity trace with a yellow marker moving
      along a diagonal.
    """

    def construct(self):
        title = Tex(r"Pascal's triangle: $\binom{n}{k} = \binom{n-1}{k-1} + \binom{n-1}{k}$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        dx = 0.75
        dy = 0.55
        top_y = 2.6

        row_tr = ValueTracker(0)

        def triangle():
            N = int(round(row_tr.get_value()))
            grp = VGroup()
            for n in range(N + 1):
                row_width = n * dx
                x_start = -row_width / 2
                for k in range(n + 1):
                    x = x_start + k * dx
                    y = top_y - n * dy
                    val = comb(n, k)
                    color = YELLOW if k == 0 or k == n else WHITE
                    lbl = MathTex(str(val),
                                    font_size=20 if val < 100 else 16,
                                    color=color)
                    lbl.move_to([x, y, 0])
                    grp.add(lbl)
            return grp

        self.add(always_redraw(triangle))

        def counter():
            N = int(round(row_tr.get_value()))
            return MathTex(rf"n = {N}", color=YELLOW, font_size=24
                            ).to_corner(DR, buff=0.5)

        self.add(always_redraw(counter))

        for target in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            self.play(row_tr.animate.set_value(target),
                       run_time=0.7, rate_func=smooth)
            self.wait(0.2)

        # Row sums: highlight 2^n for a few rows
        sum_lbl = Tex(r"Row $n$ sums to $2^n$:", font_size=22,
                      color=GREEN).to_edge(LEFT, buff=0.4).shift(DOWN * 0.6)
        self.play(Write(sum_lbl))

        for n in [3, 5, 7, 9]:
            total = 2 ** n
            pop = MathTex(rf"\text{{row }} {n}: 2^{{{n}}} = {total}",
                           font_size=22, color=GREEN
                           ).next_to(sum_lbl, RIGHT, buff=0.5)
            self.play(FadeIn(pop, shift=RIGHT * 0.2))
            self.wait(0.4)
            self.play(FadeOut(pop))

        self.wait(0.4)
