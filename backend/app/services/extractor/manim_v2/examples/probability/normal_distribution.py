from manim import *
import numpy as np


class NormalDistributionExample(Scene):
    """
    Parameter-swept normal density.

    Two ValueTrackers μ and σ drive an always_redraw curve of the
    normal pdf. Vertical dashed lines at μ−σ, μ, μ+σ move with the
    distribution, plus a live readout of μ, σ, and the shaded
    probability P(|X − μ| < σ) ≈ 0.682. First the mean slides, then
    the spread widens and narrows so the 1-σ band visibly scales.
    """

    def construct(self):
        title = Text("Normal density: moving mean, changing spread", font_size=26).to_edge(UP)
        self.play(Write(title))

        axes = Axes(
            x_range=[-5, 5, 1], y_range=[0, 0.8, 0.2],
            x_length=10, y_length=4,
            axis_config={"include_tip": True, "include_numbers": True, "font_size": 22},
        ).shift(0.3 * DOWN)
        self.play(Create(axes))

        mu = ValueTracker(0.0)
        sigma = ValueTracker(1.0)

        def pdf(x, m, s):
            return np.exp(-((x - m) ** 2) / (2 * s * s)) / (s * np.sqrt(2 * PI))

        def curve():
            m = mu.get_value()
            s = sigma.get_value()
            return axes.plot(lambda x: pdf(x, m, s), x_range=[-4.9, 4.9], color=BLUE)

        def shaded_band():
            m = mu.get_value()
            s = sigma.get_value()
            return axes.get_area(axes.plot(lambda x: pdf(x, m, s), x_range=[m - s, m + s]),
                                 x_range=[m - s, m + s], color=YELLOW, opacity=0.4)

        def mean_line():
            m = mu.get_value()
            s = sigma.get_value()
            top = axes.c2p(m, pdf(m, m, s))
            bot = axes.c2p(m, 0)
            return DashedLine(bot, top, color=RED, stroke_width=3)

        def sigma_left():
            m = mu.get_value()
            s = sigma.get_value()
            y = pdf(m - s, m, s)
            return DashedLine(axes.c2p(m - s, 0), axes.c2p(m - s, y),
                              color=ORANGE, stroke_width=2)

        def sigma_right():
            m = mu.get_value()
            s = sigma.get_value()
            y = pdf(m + s, m, s)
            return DashedLine(axes.c2p(m + s, 0), axes.c2p(m + s, y),
                              color=ORANGE, stroke_width=2)

        self.add(
            always_redraw(shaded_band),
            always_redraw(curve),
            always_redraw(mean_line),
            always_redraw(sigma_left),
            always_redraw(sigma_right),
        )

        # Live readout panel
        def info_panel():
            m = mu.get_value()
            s = sigma.get_value()
            return VGroup(
                MathTex(rf"\mu = {m:+.2f}", color=RED, font_size=28),
                MathTex(rf"\sigma = {s:.2f}", color=ORANGE, font_size=28),
                MathTex(r"P(|X - \mu| < \sigma) \approx 0.682",
                        color=YELLOW, font_size=24),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR).shift(LEFT * 0.3 + DOWN * 0.5)

        self.add(always_redraw(info_panel))
        self.wait(0.5)

        # First: slide the mean
        self.play(mu.animate.set_value(2.0), run_time=2.5, rate_func=smooth)
        self.play(mu.animate.set_value(-2.0), run_time=3, rate_func=smooth)
        self.play(mu.animate.set_value(0.0), run_time=2, rate_func=smooth)

        # Then: widen and narrow
        self.play(sigma.animate.set_value(2.0), run_time=2.5, rate_func=smooth)
        self.play(sigma.animate.set_value(0.5), run_time=2.5, rate_func=smooth)
        self.play(sigma.animate.set_value(1.0), run_time=1.5, rate_func=smooth)

        formula = MathTex(
            r"f(x) = \frac{1}{\sigma\sqrt{2\pi}} \exp\!\left(-\tfrac{(x-\mu)^2}{2\sigma^2}\right)",
            font_size=30, color=YELLOW,
        ).to_edge(DOWN)
        self.play(Write(formula))
        self.wait(1.0)
