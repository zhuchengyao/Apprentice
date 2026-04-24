from manim import *
import numpy as np


class JacobianLocalLinearExample(Scene):
    def construct(self):
        title = Text(
            "Zoomed in, a smooth map looks linear — that's the Jacobian",
            font_size=22,
        ).to_edge(UP)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-0.5, 0.5, 0.1], y_range=[-0.3, 0.3, 0.1],
            x_length=7, y_length=4.5,
            background_line_style={"stroke_opacity": 0.5},
        )
        self.play(Create(plane))

        def bend(p):
            x, y, z = p[0], p[1], p[2]
            return np.array([x + 0.3 * np.sin(5 * y), y + 0.3 * np.sin(5 * x), z])

        self.play(ApplyPointwiseFunction(bend, plane), run_time=2.5)

        caption = MathTex(
            r"DF\bigg|_{(0,0)} = \begin{bmatrix} 1 & 1.5 \\ 1.5 & 1 \end{bmatrix}",
            font_size=32,
        ).to_corner(DL).add_background_rectangle()
        self.play(Write(caption))
        self.wait(0.6)
