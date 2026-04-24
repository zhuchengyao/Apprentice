from manim import *
import numpy as np


class SystemOfEquationsToMatrixExample(Scene):
    """
    Transform a linear system into matrix form Ax = v.

    System: 2x + 5y + 3z = -3
            4x + 0y + 8z = 0
            1x + 3y + 0z = 2
    → A = [[2, 5, 3], [4, 0, 8], [1, 3, 0]], x = (x, y, z)^T, v = (-3, 0, 2)^T.
    """

    def construct(self):
        title = Tex(r"Linear system $\to A\vec x=\vec v$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Stage 1: system
        sys_tex = MathTex(
            r"2x+5y+3z&=-3\\",
            r"4x+0y+8z&=0\\",
            r"1x+3y+0z&=2",
            font_size=36,
        ).shift(UP * 0.5)
        self.play(Write(sys_tex))
        self.wait(0.5)

        # Stage 2: matrix form (arrow + factored)
        arrow = MathTex(r"\longrightarrow", font_size=48).next_to(sys_tex, DOWN, buff=0.5)
        self.play(Write(arrow))

        A = Matrix([[2, 5, 3], [4, 0, 8], [1, 3, 0]])
        A.set_column_colors(BLUE, GREEN, ORANGE)
        x_vec = Matrix(["x", "y", "z"])
        x_vec.get_entries().set_submobject_colors_by_gradient(BLUE, GREEN, ORANGE)
        eq = MathTex("=", font_size=42)
        v_vec = Matrix([-3, 0, 2]).set_color(YELLOW)

        matrix_eq = VGroup(A, x_vec, eq, v_vec).arrange(RIGHT, buff=0.3)
        matrix_eq.scale(0.85)
        matrix_eq.next_to(arrow, DOWN, buff=0.5)

        # Reveal parts with labeled braces
        for mob, lbl_str, col in [(A, r"coefficients $A$", WHITE),
                                    (x_vec, r"unknowns $\vec x$", PINK),
                                    (v_vec, r"constants $\vec v$", YELLOW)]:
            brace = Brace(mob, DOWN)
            lbl = Tex(lbl_str, font_size=22, color=col).next_to(brace, DOWN, buff=0.1)
            mob.brace = brace
            mob.lbl = lbl

        self.play(Write(A), Write(x_vec), Write(eq), Write(v_vec))
        self.wait(0.5)
        for mob in (A, x_vec, v_vec):
            self.play(GrowFromCenter(mob.brace), Write(mob.lbl), run_time=0.8)
            self.wait(0.3)
        self.wait(0.8)
