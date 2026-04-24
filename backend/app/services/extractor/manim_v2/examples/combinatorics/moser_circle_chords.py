from manim import *
import numpy as np
from math import comb


class MoserCircleChordsExample(Scene):
    """
    Moser's circle regions: n points on a circle in general position,
    all C(n, 2) chords drawn, divide interior into at most
    1 + C(n, 2) + C(n, 4) regions.

    SINGLE_FOCUS:
      Circle with n dots; ValueTracker n_tr sweeps 1..6 via
      always_redraw rebuilding points + chords + intersection dots;
      live region count = 1 + C(n,2) + C(n,4) showing 1, 2, 4, 8,
      16, 31 (not 32!).
    """

    def construct(self):
        title = Tex(r"Moser's circle regions: $R_n = 1 + \binom{n}{2} + \binom{n}{4}$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        R = 2.3
        center = np.array([-2.0, -0.3, 0])
        circ = Circle(radius=R, color=BLUE_D, stroke_width=3
                       ).move_to(center)
        self.play(Create(circ))

        n_tr = ValueTracker(1)

        def pts_of(n):
            return [center + R * np.array([np.cos(2 * PI * k / n + PI / 2),
                                              np.sin(2 * PI * k / n + PI / 2), 0])
                    for k in range(n)]

        def points():
            n = int(round(n_tr.get_value()))
            grp = VGroup()
            for p in pts_of(n):
                grp.add(Dot(p, color=YELLOW, radius=0.11))
            return grp

        def chords():
            n = int(round(n_tr.get_value()))
            pts = pts_of(n)
            grp = VGroup()
            for i in range(n):
                for j in range(i + 1, n):
                    grp.add(Line(pts[i], pts[j], color=BLUE,
                                   stroke_width=1.5))
            return grp

        self.add(always_redraw(chords), always_redraw(points))

        def info():
            n = int(round(n_tr.get_value()))
            R_n = 1 + comb(n, 2) + comb(n, 4)
            return VGroup(
                MathTex(rf"n = {n}", color=YELLOW, font_size=26),
                MathTex(rf"\binom{{n}}{{2}} = {comb(n, 2)}",
                         color=BLUE, font_size=22),
                MathTex(rf"\binom{{n}}{{4}} = {comb(n, 4)}",
                         color=RED, font_size=22),
                MathTex(rf"R_n = {R_n}", color=GREEN, font_size=28),
                Tex(r"(not powers of 2!)", color=GREY_B, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.2, 0.5, 0])

        self.add(always_redraw(info))

        for target in [2, 3, 4, 5, 6]:
            self.play(n_tr.animate.set_value(target),
                       run_time=1.4, rate_func=smooth)
            self.wait(0.5)

        sequence = MathTex(r"R_1,\,R_2,\ldots,R_6 = 1, 2, 4, 8, 16, 31",
                            color=YELLOW, font_size=26
                            ).to_edge(DOWN, buff=0.3)
        self.play(Write(sequence))
        self.wait(0.5)
