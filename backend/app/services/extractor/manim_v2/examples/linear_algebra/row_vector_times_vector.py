from manim import *
import numpy as np


class RowVectorTimesVectorExample(Scene):
    """
    A 1×2 row matrix [a b] times a 2×1 column [x y]ᵀ gives scalar ax+by.
    This is exactly the dot product of (a, b) with (x, y).

    Rote computation + annotation showing equivalence to dot product.
    """

    def construct(self):
        title = Tex(r"$1\!\times\!2$ matrix $\cdot$ vector $=$ scalar $=$ dot product",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Matrix equation
        row_tex = Matrix([["2", "-1"]]).scale(1.1)
        row_tex.set_color(GREEN)
        col_tex = Matrix([["3"], ["4"]], v_buff=0.7).scale(1.1)
        col_tex.set_color(BLUE)
        eq1 = MathTex(r"=", font_size=48)
        result = MathTex(r"2\cdot 3+(-1)\cdot 4=2", font_size=40, color=YELLOW)

        row = VGroup(row_tex, col_tex, eq1, result).arrange(RIGHT, buff=0.3).shift(UP * 1.2)
        self.play(Write(row))
        self.wait(0.4)

        # Equivalence note
        equiv_arrow = MathTex(r"\updownarrow", font_size=42).next_to(row, DOWN, buff=0.3)
        self.play(Write(equiv_arrow))
        self.wait(0.2)

        # Dot product version
        v_tex = Matrix([[2], [-1]], v_buff=0.7).scale(1.1)
        v_tex.set_color(GREEN)
        dot = MathTex(r"\cdot", font_size=48)
        w_tex = Matrix([[3], [4]], v_buff=0.7).scale(1.1)
        w_tex.set_color(BLUE)
        eq2 = MathTex(r"=", font_size=48)
        result2 = MathTex(r"2\cdot 3+(-1)\cdot 4=2", font_size=40, color=YELLOW)

        dot_row = VGroup(v_tex, dot, w_tex, eq2, result2).arrange(RIGHT, buff=0.3).next_to(equiv_arrow, DOWN, buff=0.3)
        self.play(Write(dot_row))
        self.wait(0.5)

        note = Tex(r"transposing a column matrix gives the same scalar",
                    color=GREEN, font_size=22).to_edge(DOWN, buff=0.5)
        self.play(Write(note))
        self.wait(1.0)
