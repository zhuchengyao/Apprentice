from manim import *
import numpy as np


class ChangeOfBasisMatrixApplyExample(Scene):
    """[b_1 | b_2] translates Jenny's coords to standard."""

    def construct(self):
        title = Tex(r"Change of basis: Jenny $\to$ standard via $[\vec b_1 | \vec b_2]$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        jenny_coords = Matrix([[1], [2]], v_buff=0.6).set_color(YELLOW).scale(0.9)
        cob_matrix = Matrix([[2, -1], [1, 1]]).scale(0.9)
        cob_matrix.get_columns()[0].set_color(BLUE)
        cob_matrix.get_columns()[1].set_color(PURPLE)
        eq = MathTex("=", font_size=40)
        standard = Matrix([[0], [3]], v_buff=0.6).set_color(YELLOW).scale(0.9)

        row = VGroup(cob_matrix, jenny_coords, eq, standard).arrange(RIGHT, buff=0.3).shift(UP * 0.5)
        self.play(Write(row))
        self.wait(0.4)

        jenny_brace = Brace(jenny_coords, DOWN)
        cob_brace = Brace(cob_matrix, UP)
        std_brace = Brace(standard, DOWN)

        self.play(
            GrowFromCenter(cob_brace),
            Write(Tex(r"basis matrix $[\vec b_1 | \vec b_2]$", font_size=22).next_to(cob_brace, UP, buff=0.1)),
        )
        self.play(
            GrowFromCenter(jenny_brace),
            Write(Tex(r"Jenny's coords", color=YELLOW, font_size=22).next_to(jenny_brace, DOWN, buff=0.1)),
        )
        self.play(
            GrowFromCenter(std_brace),
            Write(Tex(r"standard coords", color=YELLOW, font_size=22).next_to(std_brace, DOWN, buff=0.1)),
        )
        self.wait(0.4)

        self.play(Write(
            Tex(r"reverse: standard $\to$ Jenny via $[\vec b_1 | \vec b_2]^{-1}$",
                 color=GREEN, font_size=22).to_edge(DOWN, buff=0.5)
        ))
        self.wait(1.0)
