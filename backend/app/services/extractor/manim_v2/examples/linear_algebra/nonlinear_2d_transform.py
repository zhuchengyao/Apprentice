from manim import *
import numpy as np


class Nonlinear2DTransformExample(Scene):
    def construct(self):
        title = Text("Nonlinear: grid lines bend", font_size=30, color=RED_B).to_edge(UP)
        plane = NumberPlane(
            x_range=[-6, 6, 1], y_range=[-4, 4, 1],
            background_line_style={"stroke_opacity": 0.6},
        )
        self.play(Write(title), Create(plane, run_time=1.5))

        def squiggle(p):
            x, y, z = p
            return np.array([x + 0.5 * np.sin(y), y + 0.4 * np.cos(x), z])

        self.play(ApplyPointwiseFunction(squiggle, plane), run_time=3)
        self.wait(0.8)
