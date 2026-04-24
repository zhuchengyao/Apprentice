from manim import *


class MatrixAsGridTransformExample(Scene):
    def construct(self):
        plane = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
            background_line_style={"stroke_opacity": 0.5},
        )
        matrix = [[1, 1.5], [-0.5, 1]]
        label = MathTex(
            r"A = \begin{bmatrix} 1 & 1.5 \\ -0.5 & 1 \end{bmatrix}",
            font_size=36,
        ).to_corner(UL).set_color(YELLOW).add_background_rectangle()

        self.add(plane)
        self.play(Write(label))
        self.play(ApplyMatrix(matrix, plane), run_time=2.5)
        self.wait(0.8)
