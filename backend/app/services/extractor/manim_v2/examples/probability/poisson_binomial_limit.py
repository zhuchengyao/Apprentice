from manim import *
import numpy as np
from math import comb, factorial


class PoissonBinomialLimitExample(Scene):
    """
    Poisson limit theorem: Binomial(n, p) → Poisson(λ) as n → ∞,
    p → 0, np = λ fixed. Visualize the bar shapes coinciding.

    TWO_COLUMN:
      LEFT  — bar chart of Binomial(n, λ/n) probabilities and
              Poisson(λ) overlay; ValueTracker n_tr grows n from
              10 → 200.
      RIGHT — live n, p = λ/n, KL divergence measurement.
    """

    def construct(self):
        title = Tex(r"Binomial$(n, \lambda/n) \to $Poisson$(\lambda)$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        lam = 4.0

        ax = Axes(x_range=[0, 12, 2], y_range=[0, 0.25, 0.05],
                   x_length=7, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-2.8, -0.3, 0])
        xlbl = MathTex(r"k", font_size=20).next_to(ax, DOWN, buff=0.1)
        ylbl = MathTex(r"P(X=k)", font_size=20).next_to(ax, LEFT, buff=0.1)
        self.play(Create(ax), Write(xlbl), Write(ylbl))

        n_tr = ValueTracker(10)

        def bin_pmf(n, p, k):
            if k > n or k < 0:
                return 0.0
            return comb(n, k) * p ** k * (1 - p) ** (n - k)

        def pois_pmf(lam, k):
            return np.exp(-lam) * lam ** k / factorial(k)

        def binomial_bars():
            n = int(round(n_tr.get_value()))
            n = max(1, min(n, 200))
            p = lam / n
            grp = VGroup()
            for k in range(13):
                pr = bin_pmf(n, p, k)
                h_scene = ax.c2p(0, pr)[1] - ax.c2p(0, 0)[1]
                if h_scene < 0.003:
                    continue
                bar = Rectangle(width=0.35, height=h_scene,
                                 color=BLUE, fill_opacity=0.5,
                                 stroke_width=1)
                bar.move_to([ax.c2p(k, 0)[0] - 0.2,
                             ax.c2p(0, 0)[1] + h_scene / 2, 0])
                grp.add(bar)
            return grp

        def poisson_bars():
            grp = VGroup()
            for k in range(13):
                pr = pois_pmf(lam, k)
                h_scene = ax.c2p(0, pr)[1] - ax.c2p(0, 0)[1]
                if h_scene < 0.003:
                    continue
                bar = Rectangle(width=0.35, height=h_scene,
                                 color=RED, fill_opacity=0.5,
                                 stroke_width=1)
                bar.move_to([ax.c2p(k, 0)[0] + 0.2,
                             ax.c2p(0, 0)[1] + h_scene / 2, 0])
                grp.add(bar)
            return grp

        self.add(always_redraw(binomial_bars))
        self.add(always_redraw(poisson_bars))

        def info():
            n = int(round(n_tr.get_value()))
            n = max(1, min(n, 200))
            p = lam / n
            kl = 0.0
            for k in range(max(0, int(lam - 5)), int(lam + 6)):
                pb = bin_pmf(n, p, k)
                pp = pois_pmf(lam, k)
                if pb > 1e-10 and pp > 1e-10:
                    kl += pb * np.log(pb / pp)
            return VGroup(
                MathTex(rf"n = {n}", color=BLUE, font_size=24),
                MathTex(rf"p = \lambda/n = {p:.4f}",
                         color=BLUE, font_size=22),
                MathTex(rf"\lambda = {lam}", color=RED, font_size=22),
                Tex(r"BLUE: Binomial", color=BLUE, font_size=20),
                Tex(r"RED: Poisson", color=RED, font_size=20),
                MathTex(rf"D_{{\text{{KL}}}}(B\|P) = {kl:.4f}",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(RIGHT, buff=0.3).shift(UP * 0.5)

        self.add(always_redraw(info))

        for nv in [20, 50, 100, 200]:
            self.play(n_tr.animate.set_value(nv),
                       run_time=1.7, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
