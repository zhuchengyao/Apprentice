from manim import *


class MatrixShearExample(Scene):
    def construct(self):
        plane = NumberPlane(background_line_style={"stroke_opacity": 0.5})
        unit_square = Polygon(
            ORIGIN, RIGHT, RIGHT + UP, UP,
            color=YELLOW, fill_opacity=0.5,
        )
        matrix = [[1, 1], [0, 1]]
        label = MathTex(
            r"\begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}",
            font_size=42,
        ).to_corner(UL).add_background_rectangle()

        self.add(plane, unit_square)
        self.play(Write(label))
        self.play(
            ApplyMatrix(matrix, plane),
            ApplyMatrix(matrix, unit_square),
            run_time=2,
        )
        self.wait(0.6)
