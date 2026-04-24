from manim import *
import numpy as np


class ExpSelfDerivativeExample(Scene):
    def construct(self):
        title = Text("Why d/dx eˣ = eˣ", font_size=30).to_edge(UP)
        self.play(Write(title))

        axes = Axes(
            x_range=[-2, 2.5, 1], y_range=[0, 8, 2],
            x_length=7, y_length=4,
            axis_config={"include_tip": True},
        ).shift(0.3 * DOWN)
        graph = axes.plot(np.exp, x_range=[-2, 2.1], color=BLUE)
        self.play(Create(axes), Create(graph))

        x_tracker = ValueTracker(-1.0)

        def point():
            x = x_tracker.get_value()
            return Dot(axes.c2p(x, np.exp(x)), color=YELLOW)

        def tangent():
            x = x_tracker.get_value()
            slope = np.exp(x)
            p = np.array(axes.c2p(x, np.exp(x)))
            direction = np.array([1, slope, 0])
            direction = direction / np.linalg.norm(direction)
            return Line(p - 1.5 * direction, p + 1.5 * direction, color=ORANGE, stroke_width=4)

        pt = always_redraw(point)
        tn = always_redraw(tangent)

        readout = always_redraw(lambda: MathTex(
            rf"x = {x_tracker.get_value():.2f},\; e^x = {np.exp(x_tracker.get_value()):.2f},\; \text{{slope}} = {np.exp(x_tracker.get_value()):.2f}",
            font_size=26,
        ).to_edge(DOWN))

        self.play(FadeIn(pt), Create(tn), FadeIn(readout))
        self.play(x_tracker.animate.set_value(1.8), run_time=3.5)
        self.wait(0.4)

        conclusion = MathTex(r"f(x) = f'(x) = e^x", color=YELLOW, font_size=38).to_corner(UR)
        self.play(Write(conclusion))
        self.wait(0.6)
