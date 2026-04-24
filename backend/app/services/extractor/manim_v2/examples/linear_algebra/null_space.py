from manim import *
import numpy as np


class NullSpaceExample(Scene):
    def construct(self):
        title = Text("Null space: vectors that collapse to 0", font_size=28).to_edge(UP)
        self.play(Write(title))

        plane = NumberPlane(background_line_style={"stroke_opacity": 0.35})
        self.add(plane)

        matrix = [[1, 2], [2, 4]]
        null_dir = np.array([2, -1, 0]) / np.sqrt(5)
        null_line = Line(-5 * null_dir, 5 * null_dir, color=YELLOW, stroke_width=5)
        self.play(Create(null_line))

        eqn = MathTex(
            r"A = \begin{bmatrix}1 & 2\\ 2 & 4\end{bmatrix},\ "
            r"\ker A = \text{span}\!\begin{bmatrix}2\\ -1\end{bmatrix}",
            font_size=30,
        ).to_corner(UL).add_background_rectangle()
        self.play(Write(eqn))

        self.play(ApplyMatrix(matrix, plane), ApplyMatrix(matrix, null_line), run_time=2.5)
        self.wait(0.6)
