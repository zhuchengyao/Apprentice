from manim import *
import numpy as np


class EigenbasisPowersEasyExample(Scene):
    """
    Non-diagonal matrix powers are painful; diagonal matrix powers are
    trivial. If we can diagonalize via eigenbasis: A = P D P^(-1),
    then A^k = P D^k P^(-1).
    """

    def construct(self):
        title = Tex(r"Eigenbasis makes matrix powers easy",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Side by side: non-diagonal vs diagonal
        # Non-diagonal: [[3, 1], [0, 2]]
        # After 4 steps: compute via Python
        # vs D = diag(3, 2): D^4 = diag(81, 16)

        # LEFT: non-diagonal
        l_lbl = Tex(r"Non-diagonal: repeated products painful",
                     color=ORANGE, font_size=22).shift(UP * 1.8 + LEFT * 3.3)
        A = np.array([[3, 1], [0, 2]])
        A4 = np.linalg.matrix_power(A, 4)  # [[81, 65], [0, 16]]
        l_ex = MathTex(rf"\begin{{pmatrix}}3&1\\0&2\end{{pmatrix}}^4=\begin{{pmatrix}}{A4[0, 0]}&{A4[0, 1]}\\{A4[1, 0]}&{A4[1, 1]}\end{{pmatrix}}",
                         font_size=28, color=ORANGE).shift(UP * 0.5 + LEFT * 3.3)

        # RIGHT: diagonal
        r_lbl = Tex(r"Diagonal: just power each entry",
                     color=GREEN, font_size=22).shift(UP * 1.8 + RIGHT * 3.0)
        r_ex = MathTex(r"\begin{pmatrix}3&0\\0&2\end{pmatrix}^4=\begin{pmatrix}81&0\\0&16\end{pmatrix}",
                         font_size=28, color=GREEN).shift(UP * 0.5 + RIGHT * 3.0)

        self.play(Write(l_lbl), Write(r_lbl))
        self.play(Write(l_ex), Write(r_ex))
        self.wait(0.5)

        # Big insight
        insight = MathTex(r"A=PDP^{-1}\ \Rightarrow\ A^k=P D^k P^{-1}",
                           color=YELLOW, font_size=36).shift(DOWN * 0.8)
        self.play(Write(insight))
        self.wait(0.5)

        self.play(Write(
            Tex(r"(if diagonalizable)",
                 color=GREY_B, font_size=22).to_edge(DOWN, buff=0.5)
        ))
        self.wait(1.0)
