from manim import *
import numpy as np
from math import comb


class MoserPatternBreakExample(Scene):
    """
    The famous Moser trap: R_1 = 1, R_2 = 2, R_3 = 4, R_4 = 8,
    R_5 = 16 ... but R_6 = 31, NOT 32. Illustrates that a guessed
    pattern from a handful of data points can be wrong.

    SINGLE_FOCUS:
      ValueTracker n_tr steps n = 1..6. For each n, always_redraw
      rebuilds the circle/chords/intersections; right column shows
      a table of R_n predicted (2^(n-1)) vs actual. At n = 6 the
      table highlights the mismatch in RED.
    """

    def construct(self):
        title = Tex(r"The pattern $1, 2, 4, 8, 16, \ldots$ — and how it breaks",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        R = 1.8
        center = np.array([-3.2, -0.4, 0])
        circ = Circle(radius=R, color=BLUE_D, stroke_width=2).move_to(center)
        self.play(Create(circ))

        n_tr = ValueTracker(1)

        def pts_of(n):
            return [center + R * np.array([np.cos(2 * PI * k / n + PI / 2),
                                              np.sin(2 * PI * k / n + PI / 2), 0])
                    for k in range(n)]

        def points():
            n = int(round(n_tr.get_value()))
            return VGroup(*[Dot(p, color=YELLOW, radius=0.1)
                             for p in pts_of(n)])

        def chords():
            n = int(round(n_tr.get_value()))
            pts = pts_of(n)
            g = VGroup()
            for i in range(n):
                for j in range(i + 1, n):
                    g.add(Line(pts[i], pts[j], color=BLUE, stroke_width=1.5))
            return g

        self.add(always_redraw(chords), always_redraw(points))

        # Right: table
        def table():
            n_val = int(round(n_tr.get_value()))
            rows = [MathTex(r"n\quad 2^{n-1}\quad R_n",
                             font_size=22, color=WHITE)]
            for k in range(1, 7):
                guess = 2 ** (k - 1)
                actual = 1 + comb(k, 2) + comb(k, 4)
                color = GREEN if guess == actual else RED
                mark = r"\checkmark" if guess == actual else r"\times"
                show_color = color if k <= n_val else GREY_B
                rows.append(MathTex(rf"{k}\quad {guess}\quad {actual}\,{mark}",
                                      font_size=22, color=show_color))
            return VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.16
                                          ).move_to([3.5, 0.3, 0])

        self.add(always_redraw(table))

        for target in [2, 3, 4, 5, 6]:
            self.play(n_tr.animate.set_value(target),
                       run_time=1.3, rate_func=smooth)
            self.wait(0.7)

        punchline = Tex(r"``Look at enough examples before conjecturing'' --- $R_6 = 31$, not $32$",
                        color=YELLOW, font_size=24
                        ).to_edge(DOWN, buff=0.3)
        self.play(Write(punchline))
        self.wait(0.4)
