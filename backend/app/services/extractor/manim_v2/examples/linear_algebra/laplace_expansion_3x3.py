from manim import *
import numpy as np


class LaplaceExpansion3x3Example(Scene):
    """
    Laplace expansion of 3×3 determinant along the first row:
      det A = a·det(minor_a) - b·det(minor_b) + c·det(minor_c)
    where each minor is the 2×2 obtained by deleting row 1 and column of the entry.
    """

    def construct(self):
        title = Tex(r"Laplace expansion: $\det\!A = a\,|M_a|-b\,|M_b|+c\,|M_c|$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # 3x3 matrix
        A_tex = Matrix([["a", "b", "c"], ["d", "e", "f"], ["g", "h", "i"]])
        A_tex.get_columns()[0].set_color(BLUE)
        A_tex.get_columns()[1].set_color(GREEN)
        A_tex.get_columns()[2].set_color(ORANGE)
        A_tex.scale(0.9).shift(UP * 2)
        det_lbl = MathTex(r"\det A=", font_size=36).next_to(A_tex, LEFT, buff=0.2)
        self.play(Create(A_tex), Write(det_lbl))

        # 3 minors
        M_a = Matrix([["e", "f"], ["h", "i"]]).scale(0.75).set_color(GREEN)
        M_b = Matrix([["d", "f"], ["g", "i"]]).scale(0.75).set_color(BLUE)
        M_c = Matrix([["d", "e"], ["g", "h"]]).scale(0.75).set_color(BLUE)

        # Assemble: a·det(M_a) - b·det(M_b) + c·det(M_c)
        a_part = VGroup(Tex(r"$a\cdot$", font_size=32, color=BLUE),
                         M_a).arrange(RIGHT, buff=0.15)
        sign1 = Tex(r"$-$", font_size=36)
        b_part = VGroup(Tex(r"$b\cdot$", font_size=32, color=GREEN),
                         M_b).arrange(RIGHT, buff=0.15)
        sign2 = Tex(r"$+$", font_size=36)
        c_part = VGroup(Tex(r"$c\cdot$", font_size=32, color=ORANGE),
                         M_c).arrange(RIGHT, buff=0.15)

        formula = VGroup(a_part, sign1, b_part, sign2, c_part).arrange(RIGHT, buff=0.3)
        formula.shift(DOWN * 0.5)

        # Reveal sequentially via ValueTracker for variety
        step_tr = ValueTracker(0.0)

        self.play(Write(a_part))
        self.wait(0.5)

        # Highlight which row/col is struck in A_tex
        def striker():
            k = int(round(step_tr.get_value()))
            # k=0: a; k=1: b; k=2: c
            k = max(0, min(2, k))
            row_idx = 0
            col_idx = k
            # Strike row 1 (indices 0, 1, 2) and column col_idx
            row_group = VGroup(*[A_tex.get_entries()[row_idx * 3 + j] for j in range(3)])
            col_group = VGroup(*[A_tex.get_entries()[i * 3 + col_idx] for i in range(3)])
            rect_row = SurroundingRectangle(row_group, color=YELLOW, stroke_width=2, buff=0.05)
            rect_col = SurroundingRectangle(col_group, color=YELLOW, stroke_width=2, buff=0.05)
            return VGroup(rect_row, rect_col)

        self.add(always_redraw(striker))

        self.play(Write(sign1), Write(b_part), step_tr.animate.set_value(1))
        self.wait(0.5)
        self.play(Write(sign2), Write(c_part), step_tr.animate.set_value(2))
        self.wait(0.8)

        # Final caption
        caption = Tex(r"alternating $+, -, +$ (cofactor signs)",
                       color=YELLOW, font_size=24).to_edge(DOWN, buff=0.5)
        self.play(Write(caption))
        self.wait(1.0)
