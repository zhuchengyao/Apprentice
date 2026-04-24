from manim import *
import numpy as np


class DerivativeAsMatrixPolynomialsExample(Scene):
    """
    Polynomials of degree ≤ 3 form a 4D vector space with basis
    {1, x, x², x³}. Derivative maps this space to itself. In this basis:
    d/dx matrix =
      [[0, 1, 0, 0],
       [0, 0, 2, 0],
       [0, 0, 0, 3],
       [0, 0, 0, 0]]
    Apply to polynomial (2 + 3x + 0x² + 4x³) gives (3, 0, 12, 0) = 3 + 0x + 12x² + 0x³.
    Wait, derivative of 2 + 3x + 0x² + 4x³ = 3 + 12x². In our basis (1, x, x², x³)
    that's (3, 0, 12, 0). Matrix application: D @ (2, 3, 0, 4)^T = (3, 0, 12, 0)^T. ✓
    """

    def construct(self):
        title = Tex(r"Derivative as matrix on polynomial basis $\{1, x, x^2, x^3\}$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Matrix D
        D = Matrix([[0, 1, 0, 0], [0, 0, 2, 0], [0, 0, 0, 3], [0, 0, 0, 0]]).scale(0.85)
        D_lbl = MathTex(r"D=", font_size=32)
        d_row = VGroup(D_lbl, D).arrange(RIGHT, buff=0.2).shift(UP * 1.2 + LEFT * 3.3)
        self.play(Write(d_row))

        # Apply to p = 2 + 3x + 0x² + 4x³
        p_col = Matrix([[2], [3], [0], [4]], v_buff=0.45).scale(0.75).set_color(BLUE)
        p_lbl = MathTex(r"\vec p=", font_size=26)
        p_row = VGroup(p_lbl, p_col).arrange(RIGHT, buff=0.15).shift(UP * 1.2 + LEFT * 0.5)
        self.play(Write(p_row))

        arrow = MathTex(r"\to", font_size=36).shift(UP * 1.2 + RIGHT * 1.2)
        self.play(Write(arrow))

        # Result: D p = (3, 0, 12, 0)
        dp_col = Matrix([[3], [0], [12], [0]], v_buff=0.45).scale(0.75).set_color(GREEN)
        dp_lbl = MathTex(r"D\vec p=", font_size=26)
        dp_row = VGroup(dp_lbl, dp_col).arrange(RIGHT, buff=0.15).shift(UP * 1.2 + RIGHT * 2.8)
        self.play(Write(dp_row))

        self.wait(0.4)

        # Interpretation
        interp = VGroup(
            Tex(r"input $\vec p\to 2+3x+4x^3$", color=BLUE, font_size=24),
            Tex(r"$D\vec p\to 3+12x^2$", color=GREEN, font_size=24),
            Tex(r"$\frac{d}{dx}(2+3x+4x^3)=3+12x^2$",
                 color=YELLOW, font_size=24),
            Tex(r"derivative IS matrix multiplication",
                 color=YELLOW, font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).shift(DOWN * 1.4)
        self.play(Write(interp))
        self.wait(1.0)
