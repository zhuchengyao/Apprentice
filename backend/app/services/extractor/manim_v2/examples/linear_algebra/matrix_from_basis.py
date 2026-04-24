from manim import *


class MatrixFromBasisExample(Scene):
    def construct(self):
        title = Text(
            "Matrix columns = where i-hat and j-hat land",
            font_size=26,
        ).to_edge(UP)
        self.play(Write(title))

        plane = NumberPlane(background_line_style={"stroke_opacity": 0.35})
        i_hat = Arrow(ORIGIN, RIGHT, buff=0, color=GREEN, stroke_width=6)
        j_hat = Arrow(ORIGIN, UP, buff=0, color=RED, stroke_width=6)
        self.add(plane, i_hat, j_hat)

        matrix_tex = MathTex(
            r"A = \begin{bmatrix} \vec{i}_\text{new} & \vec{j}_\text{new} \end{bmatrix}"
            r" = \begin{bmatrix} 3 & 1 \\ 1 & 2 \end{bmatrix}",
            font_size=30,
        ).to_corner(UL).add_background_rectangle()
        self.play(Write(matrix_tex))

        new_i = Arrow(ORIGIN, 3 * RIGHT + UP, buff=0, color=GREEN, stroke_width=6)
        new_j = Arrow(ORIGIN, RIGHT + 2 * UP, buff=0, color=RED, stroke_width=6)
        self.play(ApplyMatrix([[3, 1], [1, 2]], plane),
                  Transform(i_hat, new_i),
                  Transform(j_hat, new_j), run_time=2.5)
        self.wait(0.4)
