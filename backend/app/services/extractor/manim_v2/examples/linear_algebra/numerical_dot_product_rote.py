from manim import *
import numpy as np


class NumericalDotProductRoteExample(Scene):
    """
    Rote numerical dot product in 2D and 4D.
    v · w = Σ v_i · w_i

    2D: (1, 2) · (3, -1) = 1·3 + 2·(-1) = 3 - 2 = 1
    4D: (2, 5, -3, 1) · (1, -2, 0, 4) = 2 - 10 + 0 + 4 = -4
    """

    def construct(self):
        title = Tex(r"Numerical dot product: $\vec v\cdot\vec w=\sum v_i w_i$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # 2D example
        v2 = Matrix([[1], [2]], v_buff=0.7).set_color(BLUE)
        dot = MathTex(r"\cdot", font_size=54)
        w2 = Matrix([[3], [-1]], v_buff=0.7).set_color(ORANGE)
        eq1 = MathTex("=", font_size=48)
        comp1 = MathTex(r"1\cdot 3 + 2\cdot(-1) = 1", font_size=36, color=YELLOW)

        row1 = VGroup(v2, dot, w2, eq1, comp1).arrange(RIGHT, buff=0.3).shift(UP * 1.3)
        self.play(Write(row1))
        self.wait(0.4)

        # Highlight each term
        for (v_idx, w_idx) in [(0, 0), (1, 1)]:
            v_cell = v2.get_entries()[v_idx]
            w_cell = w2.get_entries()[w_idx]
            v_rect = SurroundingRectangle(v_cell, color=YELLOW, stroke_width=3, buff=0.05)
            w_rect = SurroundingRectangle(w_cell, color=YELLOW, stroke_width=3, buff=0.05)
            self.play(Create(v_rect), Create(w_rect), run_time=0.6)
            self.wait(0.3)
            self.play(FadeOut(v_rect), FadeOut(w_rect), run_time=0.3)

        # 4D example
        v4 = Matrix([[2], [5], [-3], [1]], v_buff=0.45).set_color(BLUE).scale(0.85)
        dot4 = MathTex(r"\cdot", font_size=40)
        w4 = Matrix([[1], [-2], [0], [4]], v_buff=0.45).set_color(ORANGE).scale(0.85)
        eq4 = MathTex("=", font_size=40)
        comp4 = MathTex(r"2-10+0+4=-4", font_size=32, color=YELLOW)

        row4 = VGroup(v4, dot4, w4, eq4, comp4).arrange(RIGHT, buff=0.3).shift(DOWN * 1.3)
        self.play(Write(row4))
        self.wait(0.5)

        note = Tex(r"pair up, multiply, add — works in any dimension",
                    color=GREEN, font_size=22).to_edge(DOWN, buff=0.4)
        self.play(Write(note))
        self.wait(1.0)
