from manim import *
import numpy as np
from scipy.special import beta as beta_fn


class BetaPosteriorUpdateExample(Scene):
    """
    Bayesian coin-flip updating with Beta prior (from _2020/beta/):
    Beta(α, β) prior + h heads + t tails → Beta(α + h, β + t)
    posterior. As flips accumulate, the distribution tightens around
    the true bias p.

    TWO_COLUMN:
      LEFT  — axes with Beta PDF evolving via always_redraw; prior
              Beta(2, 2) stays dashed for reference.
      RIGHT — ValueTracker n_flips_tr grows 0 → 60; posterior
              refines. Precomputed deterministic heads/tails from
              true bias p=0.7.
    """

    def construct(self):
        title = Tex(r"Beta-Binomial update: $\text{Beta}(\alpha + h, \beta + t)$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        rng = np.random.default_rng(7)
        true_p = 0.7
        N_MAX = 60
        flips = rng.random(N_MAX) < true_p  # True = heads
        cum_h = np.cumsum(flips.astype(int))
        cum_t = np.cumsum((~flips).astype(int))

        alpha0, beta0 = 2.0, 2.0

        def beta_pdf(x, a, b):
            if x <= 0 or x >= 1:
                return 0.0
            return (x ** (a - 1) * (1 - x) ** (b - 1) / beta_fn(a, b))

        ax = Axes(x_range=[0, 1, 0.25], y_range=[0, 10, 2],
                   x_length=7, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-2.8, -0.3, 0])
        self.play(Create(ax))

        # Prior (dashed reference)
        prior_curve = ax.plot(lambda x: beta_pdf(x, alpha0, beta0),
                                x_range=[0.005, 0.995, 0.005],
                                color=GREY_B, stroke_width=2,
                                stroke_opacity=0.6)
        prior_curve.set_stroke(dash_array=[0.1, 0.1])

        true_line = DashedLine(ax.c2p(true_p, 0), ax.c2p(true_p, 10),
                                color=YELLOW, stroke_width=2)
        self.play(Create(prior_curve), Create(true_line))

        n_flips_tr = ValueTracker(0)

        def posterior():
            n = int(round(n_flips_tr.get_value()))
            n = max(0, min(n, N_MAX))
            h = int(cum_h[n - 1]) if n > 0 else 0
            t = int(cum_t[n - 1]) if n > 0 else 0
            a = alpha0 + h
            b = beta0 + t
            return ax.plot(lambda x: min(beta_pdf(x, a, b), 10),
                            x_range=[0.005, 0.995, 0.005],
                            color=RED, stroke_width=4)

        self.add(always_redraw(posterior))

        def info():
            n = int(round(n_flips_tr.get_value()))
            n = max(0, min(n, N_MAX))
            h = int(cum_h[n - 1]) if n > 0 else 0
            t = int(cum_t[n - 1]) if n > 0 else 0
            a = alpha0 + h
            b = beta0 + t
            mean = a / (a + b)
            var = a * b / ((a + b) ** 2 * (a + b + 1))
            return VGroup(
                MathTex(rf"n = {n}", color=WHITE, font_size=22),
                MathTex(rf"h = {h},\ t = {t}",
                         color=BLUE, font_size=22),
                MathTex(rf"\alpha = {a:.1f},\ \beta = {b:.1f}",
                         color=RED, font_size=22),
                MathTex(rf"\mu = \alpha/(\alpha+\beta) = {mean:.3f}",
                         color=YELLOW, font_size=22),
                MathTex(rf"\sigma = {np.sqrt(var):.3f}",
                         color=GREEN, font_size=22),
                Tex(rf"true $p = {true_p}$", color=YELLOW, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([4.0, 0.2, 0])

        self.add(always_redraw(info))

        self.play(n_flips_tr.animate.set_value(N_MAX),
                   run_time=8, rate_func=linear)
        self.wait(0.5)
