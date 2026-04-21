from manim import *
import numpy as np


class SineCurveUnitCircleExample(Scene):
    def construct(self):
        circle_center = LEFT * 3
        circle = Circle(radius=1, color=BLUE).move_to(circle_center)
        self.play(Create(circle))

        theta = ValueTracker(0.0)
        radius = always_redraw(
            lambda: Line(
                circle_center,
                circle_center + np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0]),
                color=YELLOW,
            )
        )
        dot = always_redraw(
            lambda: Dot(color=RED).move_to(
                circle_center + np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0])
            )
        )

        axes = Axes(
            x_range=[0, TAU, PI / 2],
            y_range=[-1.3, 1.3, 1],
            x_length=6,
            y_length=2.2,
            tips=False,
        ).shift(RIGHT * 1.2)
        self.play(Create(axes))

        curve = always_redraw(
            lambda: axes.plot(
                np.sin,
                x_range=[0, max(0.01, theta.get_value())],
                color=RED,
            )
        )

        self.add(radius, dot, curve)
        self.play(theta.animate.set_value(TAU), run_time=5, rate_func=linear)
        self.wait(0.4)
