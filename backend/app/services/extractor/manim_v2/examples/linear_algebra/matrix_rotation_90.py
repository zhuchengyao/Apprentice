from manim import *


class MatrixRotation90Example(Scene):
    def construct(self):
        plane = NumberPlane(background_line_style={"stroke_opacity": 0.5})
        i_hat = Arrow(ORIGIN, RIGHT, color=GREEN, buff=0, stroke_width=6)
        j_hat = Arrow(ORIGIN, UP, color=RED, buff=0, stroke_width=6)
        label = MathTex(
            r"R_{90^\circ} = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}",
            font_size=36,
        ).to_corner(UL).add_background_rectangle()

        self.add(plane, i_hat, j_hat)
        self.play(Write(label))
        self.play(
            Rotate(plane, PI / 2, about_point=ORIGIN),
            Rotate(i_hat, PI / 2, about_point=ORIGIN),
            Rotate(j_hat, PI / 2, about_point=ORIGIN),
            run_time=2,
        )
        self.wait(0.6)
