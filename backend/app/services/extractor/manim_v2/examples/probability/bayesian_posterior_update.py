from manim import *
import numpy as np


class BayesianPosteriorUpdateExample(Scene):
    """
    Bayesian update: prior · likelihood → posterior ∝ p(θ) · p(D|θ).
    Use Beta-Binomial: prior Beta(2, 2), data = k heads in n flips,
    posterior = Beta(2+k, 2+n-k).

    TWO_COLUMN:
      LEFT  — prior + posterior curves; ValueTracker k_tr increases
              observed heads (with fixed n=20).
      RIGHT — Bayes formula; live (k, posterior mean).
    """

    def construct(self):
        title = Tex(r"Bayes update: $p(\theta|D) \propto p(\theta) \cdot p(D|\theta)$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        from scipy.special import beta as beta_fn

        def beta_pdf(x, a, b):
            if x <= 0 or x >= 1:
                return 0.0
            return x ** (a - 1) * (1 - x) ** (b - 1) / beta_fn(a, b)

        ax = Axes(x_range=[0, 1, 0.25], y_range=[0, 7, 2],
                   x_length=7, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-2.5, -0.3, 0])
        self.play(Create(ax))

        # Prior Beta(2, 2) static
        prior_a, prior_b = 2.0, 2.0
        prior_curve = ax.plot(lambda x: beta_pdf(x, prior_a, prior_b),
                                x_range=[0.005, 0.995, 0.005],
                                color=BLUE, stroke_width=3)
        prior_lbl = MathTex(r"\text{prior: Beta}(2, 2)",
                              color=BLUE, font_size=20
                              ).next_to(ax.c2p(0.5, 1.5), UR, buff=0.1)
        self.play(Create(prior_curve), Write(prior_lbl))

        n = 20
        k_tr = ValueTracker(0)

        def posterior():
            k = int(round(k_tr.get_value()))
            k = max(0, min(k, n))
            a = prior_a + k
            b = prior_b + n - k
            return ax.plot(lambda x: min(beta_pdf(x, a, b), 7),
                            x_range=[0.005, 0.995, 0.005],
                            color=RED, stroke_width=3)

        self.add(always_redraw(posterior))

        def info():
            k = int(round(k_tr.get_value()))
            k = max(0, min(k, n))
            a = prior_a + k
            b = prior_b + n - k
            mean = a / (a + b)
            var = a * b / ((a + b) ** 2 * (a + b + 1))
            return VGroup(
                MathTex(rf"n = {n},\ k = {k}",
                         color=WHITE, font_size=22),
                MathTex(rf"\text{{posterior: Beta}}({a:.0f}, {b:.0f})",
                         color=RED, font_size=20),
                MathTex(rf"\mu = {mean:.3f}",
                         color=YELLOW, font_size=22),
                MathTex(rf"\sigma = {np.sqrt(var):.3f}",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for kv in [5, 10, 15, 20, 8]:
            self.play(k_tr.animate.set_value(kv),
                       run_time=1.4, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
