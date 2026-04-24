from manim import *
import numpy as np
from math import comb


class NormalApproximationBinomialExample(Scene):
    """
    De Moivre-Laplace: Binomial(n, p) ≈ N(np, np(1-p)) for large n.

    TWO_COLUMN:
      LEFT  — axes with BLUE Binomial(n, p=0.5) bars + RED Normal pdf
              overlay; ValueTracker n_tr grows 4 → 80.
      RIGHT — live n, np, np(1-p), continuity-corrected P(X ≤ n/2).
    """

    def construct(self):
        title = Tex(r"de Moivre-Laplace: Bin$(n, 1/2) \to \mathcal N(n/2, n/4)$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        p = 0.5

        ax = Axes(x_range=[-0.5, 1.1, 0.25], y_range=[0, 0.35, 0.1],
                   x_length=7, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-2.5, -0.3, 0])
        xlbl = MathTex(r"x = k/n", font_size=18).next_to(ax, DOWN, buff=0.1)
        ylbl = MathTex(r"\mathrm{density}", font_size=18).next_to(ax, LEFT, buff=0.1)
        self.play(Create(ax), Write(xlbl), Write(ylbl))

        n_tr = ValueTracker(4)

        def bars():
            n = int(round(n_tr.get_value()))
            n = max(1, min(n, 80))
            grp = VGroup()
            bar_w = 0.9 / n
            for k in range(n + 1):
                pr = comb(n, k) * p ** k * (1 - p) ** (n - k)
                density = pr * n  # convert to pmf-density scale
                h_scene = ax.c2p(0, density)[1] - ax.c2p(0, 0)[1]
                if h_scene < 0.003:
                    continue
                bar = Rectangle(width=(ax.c2p(bar_w, 0)[0] - ax.c2p(0, 0)[0]) * 0.9,
                                 height=h_scene,
                                 color=BLUE, fill_opacity=0.65,
                                 stroke_width=0.5)
                bar.move_to([ax.c2p(k / n, 0)[0],
                             ax.c2p(0, 0)[1] + h_scene / 2, 0])
                grp.add(bar)
            return grp

        def normal_overlay():
            n = int(round(n_tr.get_value()))
            n = max(1, min(n, 80))
            mu = 0.5
            sigma = np.sqrt(p * (1 - p) / n)
            return ax.plot(
                lambda x: np.exp(-(x - mu) ** 2 / (2 * sigma ** 2)) / (sigma * np.sqrt(2 * PI)),
                x_range=[mu - 4 * sigma, mu + 4 * sigma, 0.005],
                color=RED, stroke_width=3)

        self.add(always_redraw(bars), always_redraw(normal_overlay))

        def info():
            n = int(round(n_tr.get_value()))
            n = max(1, min(n, 80))
            np_val = n * p
            var = n * p * (1 - p)
            return VGroup(
                MathTex(rf"n = {n}", color=BLUE, font_size=26),
                MathTex(rf"np = {np_val:.1f}", color=RED, font_size=22),
                MathTex(rf"np(1-p) = {var:.2f}", color=RED, font_size=22),
                MathTex(rf"\sigma/\mu = {np.sqrt(var)/np_val:.3f}",
                         color=GREEN, font_size=20),
                Tex(r"Normal overlay sharpens",
                     color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for nv in [8, 16, 32, 64, 80]:
            self.play(n_tr.animate.set_value(nv),
                       run_time=1.6, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
