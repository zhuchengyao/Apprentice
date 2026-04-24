from manim import *
import numpy as np
from math import comb


class NegativeBinomialExample(Scene):
    """
    Negative binomial: time to r-th success in Bernoulli trials with
    success probability p. P(X = k) = C(k-1, r-1) p^r (1-p)^(k-r)
    for k >= r.

    TWO_COLUMN:
      LEFT  — bar chart of NB PMF; ValueTracker r_tr steps r = 1, 2,
              3, 5 with fixed p = 0.35.
      RIGHT — live r, E[X] = r/p, Var[X] = r(1-p)/p².
    """

    def construct(self):
        title = Tex(r"Negative binomial: trials until $r$-th success",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        p = 0.35

        ax = Axes(x_range=[0, 25, 5], y_range=[0, 0.4, 0.1],
                   x_length=7, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-2.8, -0.3, 0])
        xl = MathTex(r"k", font_size=20).next_to(ax, DOWN, buff=0.1)
        yl = MathTex(r"P(X=k)", font_size=18).next_to(ax, LEFT, buff=0.1)
        self.play(Create(ax), Write(xl), Write(yl))

        r_tr = ValueTracker(1)

        def nb_pmf(k, r):
            if k < r:
                return 0.0
            return comb(k - 1, r - 1) * p ** r * (1 - p) ** (k - r)

        def bars():
            r = int(round(r_tr.get_value()))
            r = max(1, min(r, 8))
            grp = VGroup()
            for k in range(r, 25):
                pr = nb_pmf(k, r)
                if pr < 0.002:
                    continue
                h_scene = ax.c2p(0, pr)[1] - ax.c2p(0, 0)[1]
                bar = Rectangle(width=0.3, height=h_scene,
                                 color=BLUE, fill_opacity=0.65,
                                 stroke_width=0.5)
                bar.move_to([ax.c2p(k, 0)[0],
                             ax.c2p(0, 0)[1] + h_scene / 2, 0])
                grp.add(bar)
            return grp

        self.add(always_redraw(bars))

        def info():
            r = int(round(r_tr.get_value()))
            r = max(1, min(r, 8))
            E = r / p
            Var = r * (1 - p) / (p ** 2)
            mode = int(np.ceil((r - 1) / p)) if r >= 2 else 1
            return VGroup(
                MathTex(rf"p = {p}", color=WHITE, font_size=22),
                MathTex(rf"r = {r}", color=BLUE, font_size=26),
                MathTex(rf"E[X] = r/p = {E:.3f}",
                         color=YELLOW, font_size=22),
                MathTex(rf"\mathrm{{Var}}[X] = r(1-p)/p^2 = {Var:.3f}",
                         color=GREEN, font_size=20),
                MathTex(rf"\mathrm{{mode}} = {mode}",
                         color=ORANGE, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for rv in [2, 3, 5, 8, 1]:
            self.play(r_tr.animate.set_value(rv),
                       run_time=1.5, rate_func=smooth)
            self.wait(0.6)
        self.wait(0.4)
