from manim import *


class MatrixBasisVectorsExample(Scene):
    def construct(self):
        plane = NumberPlane(background_line_style={"stroke_opacity": 0.4})
        i_hat = Arrow(ORIGIN, RIGHT, color=GREEN, buff=0, stroke_width=6)
        j_hat = Arrow(ORIGIN, UP, color=RED, buff=0, stroke_width=6)
        i_lbl = MathTex(r"\hat{i}", color=GREEN).next_to(i_hat.get_end(), DR, buff=0.1)
        j_lbl = MathTex(r"\hat{j}", color=RED).next_to(j_hat.get_end(), UL, buff=0.1)

        matrix = [[2, -1], [1, 1]]
        self.add(plane, i_hat, j_hat, i_lbl, j_lbl)
        self.wait(0.3)

        new_i = Arrow(ORIGIN, 2 * RIGHT + UP, color=GREEN, buff=0, stroke_width=6)
        new_j = Arrow(ORIGIN, -1 * RIGHT + UP, color=RED, buff=0, stroke_width=6)

        self.play(
            ApplyMatrix(matrix, plane),
            Transform(i_hat, new_i),
            Transform(j_hat, new_j),
            i_lbl.animate.next_to(new_i.get_end(), DR, buff=0.1),
            j_lbl.animate.next_to(new_j.get_end(), UL, buff=0.1),
            run_time=2.5,
        )
        self.wait(0.8)
