from manim import *
import numpy as np


class UniformSquaredDensityTransform(Scene):
    """If X is uniform on [0, 1], then Y = X^2 has density 1/(2*sqrt(y)) on
    [0, 1] — heavily biased toward zero even though X is uniform.
    Visualize with two stacked axes: input uniform density, and output
    arcsine-like density.  Sample 400 points and map them across."""

    def construct(self):
        title = Tex(
            r"If $X\sim\text{Uniform}(0,1)$, then $Y = X^2$ has density $\tfrac{1}{2\sqrt{y}}$",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ax_x = Axes(
            x_range=[0, 1, 0.2], y_range=[0, 3, 1],
            x_length=5.5, y_length=2.2,
            tips=False,
            axis_config={"stroke_width": 1.5, "include_ticks": True},
        ).move_to([-3.5, 0.8, 0])
        ax_y = Axes(
            x_range=[0, 1, 0.2], y_range=[0, 3, 1],
            x_length=5.5, y_length=2.2,
            tips=False,
            axis_config={"stroke_width": 1.5, "include_ticks": True},
        ).move_to([3.3, 0.8, 0])
        self.play(Create(ax_x), Create(ax_y))

        fx = ax_x.plot(lambda x: 1.0, x_range=[0, 1, 0.01],
                       color=BLUE, stroke_width=3)
        fy = ax_y.plot(lambda y: 1.0 / (2 * np.sqrt(max(y, 0.01))),
                       x_range=[0.01, 1, 0.005],
                       color=RED, stroke_width=3)
        fx_lab = MathTex(r"f_X(x) = 1", font_size=26,
                         color=BLUE).next_to(ax_x, UP, buff=0.15)
        fy_lab = MathTex(r"f_Y(y) = \tfrac{1}{2\sqrt{y}}", font_size=26,
                         color=RED).next_to(ax_y, UP, buff=0.15)
        self.play(Create(fx), Create(fy), Write(fx_lab), Write(fy_lab))

        rng = np.random.default_rng(9)
        n = 300
        xs = rng.uniform(0, 1, n)
        ys = xs ** 2

        left_dots = VGroup(*[
            Dot(ax_x.c2p(x, 0.2), radius=0.025, color=BLUE_B,
                fill_opacity=0.8)
            for x in xs
        ])
        self.play(LaggedStart(*[FadeIn(d) for d in left_dots],
                              lag_ratio=0.002, run_time=1.5))

        arrows = VGroup()
        right_dots = VGroup()
        for x, y in zip(xs, ys):
            arrows.add(Line(
                ax_x.c2p(x, 0.2), ax_y.c2p(y, 0.2),
                color=GREY_B, stroke_width=0.5, stroke_opacity=0.25,
            ))
            right_dots.add(Dot(ax_y.c2p(y, 0.2), radius=0.025,
                              color=RED_B, fill_opacity=0.8))

        self.play(Create(arrows, lag_ratio=0.005, run_time=2))
        self.play(LaggedStart(*[FadeIn(d) for d in right_dots],
                              lag_ratio=0.003, run_time=2))

        derivation = VGroup(
            MathTex(r"f_Y(y) = f_X(x(y))\,\left|\tfrac{dx}{dy}\right|",
                    font_size=24),
            MathTex(r"x = \sqrt{y}\Rightarrow \tfrac{dx}{dy} = \tfrac{1}{2\sqrt{y}}",
                    font_size=24),
            MathTex(r"f_Y(y) = 1 \cdot \tfrac{1}{2\sqrt{y}}"
                    r" = \tfrac{1}{2\sqrt{y}}",
                    font_size=26, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        derivation.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(derivation[0]))
        self.play(FadeIn(derivation[1]))
        self.play(FadeIn(derivation[2]))
        self.wait(1.5)
