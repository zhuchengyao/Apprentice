from manim import *
import numpy as np


class BatchNormalizationExample(Scene):
    """
    Batch normalization: for a mini-batch {x_1, ..., x_m}, compute
    mean μ and variance σ², then y_i = (x_i - μ) / √(σ² + ε).
    Normalizes activations to mean 0, variance 1.

    TWO_COLUMN:
      LEFT  — scatter of raw batch samples (2D) before BN.
      RIGHT — after BN: zero-centered, unit-scale samples.
      ValueTracker s_tr morphs the left samples into the normalized
      right samples.
    """

    def construct(self):
        title = Tex(r"BatchNorm: $y = (x - \mu) / \sqrt{\sigma^2 + \varepsilon}$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 4, 1], y_range=[-3, 3, 1],
                             x_length=9, y_length=6,
                             background_line_style={"stroke_opacity": 0.25}
                             ).move_to([0, -0.3, 0])
        self.play(Create(plane))

        # Generate batch with non-zero mean and non-unit variance
        rng = np.random.default_rng(8)
        N = 40
        raw = rng.normal(loc=[1.5, -1.0], scale=[1.3, 0.8], size=(N, 2))
        mu_x = raw.mean(axis=0)
        sigma_x = raw.std(axis=0) + 1e-6
        normalized = (raw - mu_x) / sigma_x

        s_tr = ValueTracker(0.0)

        def sample_dots():
            s = s_tr.get_value()
            grp = VGroup()
            for i in range(N):
                p = (1 - s) * raw[i] + s * normalized[i]
                grp.add(Dot(plane.c2p(p[0], p[1]),
                              color=BLUE, radius=0.06))
            return grp

        def mean_dot():
            s = s_tr.get_value()
            cur_mu = (1 - s) * mu_x + s * np.array([0, 0])
            return Dot(plane.c2p(cur_mu[0], cur_mu[1]),
                        color=RED, radius=0.15)

        def std_ellipse():
            s = s_tr.get_value()
            cur_mu = (1 - s) * mu_x + s * np.array([0, 0])
            cur_sigma = (1 - s) * sigma_x + s * np.array([1, 1])
            w = plane.c2p(cur_sigma[0], 0)[0] - plane.c2p(0, 0)[0]
            h = plane.c2p(0, cur_sigma[1])[1] - plane.c2p(0, 0)[1]
            return Ellipse(width=2 * w, height=2 * h,
                             color=RED, stroke_width=3,
                             fill_opacity=0.15
                             ).move_to(plane.c2p(cur_mu[0], cur_mu[1]))

        self.add(always_redraw(std_ellipse),
                  always_redraw(sample_dots),
                  always_redraw(mean_dot))

        def info():
            s = s_tr.get_value()
            cur_mu = (1 - s) * mu_x + s * np.array([0, 0])
            cur_sigma = (1 - s) * sigma_x + s * np.array([1, 1])
            return VGroup(
                MathTex(rf"s = {s:.2f}", color=YELLOW, font_size=22),
                MathTex(rf"\mu = ({cur_mu[0]:+.2f}, {cur_mu[1]:+.2f})",
                         color=RED, font_size=20),
                MathTex(rf"\sigma = ({cur_sigma[0]:.2f}, {cur_sigma[1]:.2f})",
                         color=RED, font_size=20),
                Tex(r"target: $\mu = 0$, $\sigma = 1$",
                     color=GREEN, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        self.play(s_tr.animate.set_value(1.0),
                   run_time=4, rate_func=smooth)
        self.wait(0.4)
        self.play(s_tr.animate.set_value(0.0),
                   run_time=3, rate_func=smooth)
        self.wait(0.4)
