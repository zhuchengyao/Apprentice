from manim import *
import numpy as np


class ExponentialGrowthLogVsLinear(Scene):
    """The same exponential data looks dramatically different on linear
    vs log y-axis.  On linear axes, exponential growth looks 'flat then
    exploding'.  On semi-log axes, it's a perfectly straight line, and
    the SLOPE is the growth rate ln(r).  Animate the same dataset on
    both and highlight the straight-line signature."""

    def construct(self):
        title = Tex(
            r"Exponential growth: linear axes vs log axes",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ts = np.arange(0, 30, 1.0)
        r = 1.28
        ys = 3 * r ** ts

        lin_ax = Axes(
            x_range=[0, 30, 5],
            y_range=[0, 6000, 1000],
            x_length=5.8, y_length=4.5,
            tips=False,
            axis_config={"stroke_width": 1.5, "include_ticks": True},
        ).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        log_ax = Axes(
            x_range=[0, 30, 5],
            y_range=[0, 4.0, 1],
            x_length=5.8, y_length=4.5,
            tips=False,
            axis_config={"stroke_width": 1.5, "include_ticks": True},
        ).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.3)
        lin_cap = Tex(r"Linear $y$ axis", font_size=22,
                      color=BLUE).next_to(lin_ax, UP, buff=0.1)
        log_cap = Tex(r"$\log_{10} y$ axis", font_size=22,
                      color=GREEN).next_to(log_ax, UP, buff=0.1)
        self.play(Create(lin_ax), Create(log_ax),
                  FadeIn(lin_cap), FadeIn(log_cap))

        lin_dots = VGroup(*[
            Dot(lin_ax.c2p(t, y), radius=0.06, color=BLUE)
            for t, y in zip(ts, ys)
        ])
        log_dots = VGroup(*[
            Dot(log_ax.c2p(t, np.log10(y)), radius=0.06, color=GREEN)
            for t, y in zip(ts, ys)
        ])

        lin_curve = lin_ax.plot(
            lambda t: 3 * r ** t, x_range=[0, 29.5, 0.1],
            color=BLUE, stroke_width=2.5,
        )
        log_curve = log_ax.plot(
            lambda t: np.log10(3 * r ** t), x_range=[0, 29.5, 0.1],
            color=GREEN, stroke_width=2.5,
        )

        self.play(LaggedStart(*[FadeIn(d) for d in lin_dots],
                              lag_ratio=0.03, run_time=1.5))
        self.play(Create(lin_curve), run_time=1.5)
        self.play(LaggedStart(*[FadeIn(d) for d in log_dots],
                              lag_ratio=0.03, run_time=1.5))
        self.play(Create(log_curve), run_time=1.5)

        lin_desc = MathTex(
            r"y = 3\,r^t", font_size=24, color=BLUE,
        ).next_to(lin_ax, DOWN, buff=0.15)
        log_desc = MathTex(
            r"\log_{10} y = \log_{10}3 + t\,\log_{10}r",
            font_size=22, color=GREEN,
        ).next_to(log_ax, DOWN, buff=0.15)
        self.play(Write(lin_desc), Write(log_desc))

        slope_note = Tex(
            rf"Slope of the log line $= \log_{{10}}(r) = \log_{{10}}({r:.2f}) \approx {np.log10(r):.3f}$",
            font_size=24, color=YELLOW,
        ).to_edge(DOWN, buff=0.2)
        self.play(FadeIn(slope_note))
        self.wait(1.5)
