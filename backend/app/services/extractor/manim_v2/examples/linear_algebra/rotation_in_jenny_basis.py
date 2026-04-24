from manim import *


class RotationInJennyBasisExample(Scene):
    """R=[[0, -1], [1, 0]] in Jenny's basis."""

    def construct(self):
        title = Tex(r"$R=[[0, -1], [1, 0]]$ in Jenny's basis",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        R_std = Matrix([[0, -1], [1, 0]]).scale(0.9)
        R_lbl = MathTex(r"R_{\text{std}}=", font_size=32)
        r_row = VGroup(R_lbl, R_std).arrange(RIGHT, buff=0.2).shift(UP * 1.8 + LEFT * 3)
        self.play(Write(r_row))

        A = Matrix([[2, -1], [1, 1]]).scale(0.8)
        A_lbl = MathTex(r"A=", font_size=28)
        A_row = VGroup(A_lbl, A).arrange(RIGHT, buff=0.15).shift(UP * 0.7 + LEFT * 3)
        self.play(Write(A_row))

        A_inv = Matrix([["1/3", "1/3"], ["-1/3", "2/3"]]).scale(0.8)
        A_inv_lbl = MathTex(r"A^{-1}=", font_size=28)
        A_inv_row = VGroup(A_inv_lbl, A_inv).arrange(RIGHT, buff=0.15).shift(UP * 0.7 + RIGHT * 2)
        self.play(Write(A_inv_row))
        self.wait(0.3)

        formula = MathTex(r"R_J = A^{-1} R A = \tfrac{1}{3}\begin{pmatrix}1&-2\\5&-1\end{pmatrix}",
                           font_size=32, color=YELLOW).shift(DOWN * 0.6)
        self.play(Write(formula))
        self.wait(0.5)

        self.play(Write(
            Tex(r"Same rotation, different matrix because of different basis",
                 color=GREEN, font_size=22).to_edge(DOWN, buff=0.5)
        ))
        self.wait(1.0)
