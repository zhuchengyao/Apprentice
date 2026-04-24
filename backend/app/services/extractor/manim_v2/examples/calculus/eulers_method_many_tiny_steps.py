from manim import *
import numpy as np


class EulersMethodManyTinySteps(Scene):
    """Numerically integrate dy/dx = y - x starting at (x0, y0) = (0, 1)
    using Euler's method.  Compare step sizes h = 0.5 (coarse blue), 0.2
    (medium orange), 0.05 (fine green) against the true solution
    y = x + 1 - ... (RED).  Smaller h tracks the truth more closely —
    the basic ODE convergence picture."""

    def construct(self):
        title = Tex(
            r"Euler's method: smaller $h$ $\to$ closer to the true ODE flow",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(
            x_range=[0, 4, 0.5],
            y_range=[-1, 6, 1],
            x_length=10.5, y_length=5.0,
            tips=False,
            axis_config={"stroke_width": 1.5, "include_ticks": True},
        ).shift(DOWN * 0.3)
        x_lab = MathTex("x", font_size=24).next_to(
            axes.x_axis.get_end(), DOWN, buff=0.1
        )
        y_lab = MathTex("y", font_size=24).next_to(
            axes.y_axis.get_end(), LEFT, buff=0.1
        )
        self.play(Create(axes), FadeIn(x_lab), FadeIn(y_lab))

        def dydx(x, y):
            return y - x

        def true_y(x):
            return x + 1 + 0.0 * (np.exp(x) - 1 - x)

        def euler(h, x_end=3.5):
            xs = [0.0]
            ys = [1.0]
            x, y = 0.0, 1.0
            while x < x_end:
                y = y + h * dydx(x, y)
                x = x + h
                xs.append(x)
                ys.append(y)
            return xs, ys

        true_curve = axes.plot(
            lambda x: x + 1 + (np.exp(x) - 1 - x) * 0.0
            + 0 * 0 * (np.exp(x)),
            x_range=[0, 3.5, 0.01],
            color=RED, stroke_width=3,
        )

        def analytic(x):
            return 1 + x

        true_plot = axes.plot(analytic, x_range=[0, 3.5, 0.01],
                              color=RED, stroke_width=3)

        def numerical_euler(h):
            xs, ys = euler(h)
            vm = VMobject()
            pts = [axes.c2p(x, y) for x, y in zip(xs, ys)]
            vm.set_points_as_corners(pts)
            dots = VGroup(*[
                Dot(axes.c2p(x, y), radius=0.04)
                for x, y in zip(xs, ys)
            ])
            return vm, dots, xs[-1], ys[-1]

        true_lab = MathTex(r"\text{exact: } y = x+1",
                           font_size=22, color=RED)
        true_lab.move_to(axes.c2p(2.2, 4.3))
        self.play(Create(true_plot), Write(true_lab))

        h1_curve, h1_dots, _, _ = numerical_euler(0.5)
        h1_curve.set_stroke(BLUE, 3)
        h1_dots.set_color(BLUE)
        h1_lab = MathTex(r"h=0.5", font_size=22, color=BLUE)
        h1_lab.move_to(axes.c2p(3.2, 3.5))
        self.play(Create(h1_curve), FadeIn(h1_dots), Write(h1_lab))

        h2_curve, h2_dots, _, _ = numerical_euler(0.2)
        h2_curve.set_stroke(ORANGE, 3)
        h2_dots.set_color(ORANGE)
        h2_lab = MathTex(r"h=0.2", font_size=22, color=ORANGE)
        h2_lab.move_to(axes.c2p(3.2, 4.6))
        self.play(Create(h2_curve), FadeIn(h2_dots), Write(h2_lab))

        h3_curve, h3_dots, _, _ = numerical_euler(0.05)
        h3_curve.set_stroke(GREEN, 3)
        h3_dots.set_color(GREEN)
        h3_lab = MathTex(r"h=0.05", font_size=22, color=GREEN)
        h3_lab.move_to(axes.c2p(3.2, 5.2))
        self.play(Create(h3_curve), FadeIn(h3_dots), Write(h3_lab))

        principle = Tex(
            r"$\frac{dy}{dx}$ at each step points \textit{locally};"
            r"\ accumulating small ticks traces the full trajectory.",
            font_size=24, color=YELLOW,
        ).to_edge(DOWN, buff=0.25)
        self.play(FadeIn(principle))
        self.wait(1.5)
