from manim import *
import numpy as np


class ChangeToEigenBasisExample(Scene):
    """
    Change of basis into eigenbasis: matrix becomes diagonal.
    A = [[3, 1], [0, 2]] with eigenvectors (1, 0), (-1, 1), i.e.
    P = [[1, -1], [0, 1]]. In eigenbasis, matrix is diag(3, 2).
    """

    def construct(self):
        title = Tex(r"Change to eigenbasis: $A\to$ diagonal",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        A_tex = MathTex(r"A=\begin{pmatrix}3&1\\0&2\end{pmatrix}",
                         font_size=36).shift(UP * 2 + LEFT * 3)
        self.play(Write(A_tex))

        P_tex = MathTex(r"P=[\vec e_1\ |\ \vec e_2]=\begin{pmatrix}1&-1\\0&1\end{pmatrix}",
                         font_size=30, color=GREEN).shift(UP * 0.5 + LEFT * 3)
        self.play(Write(P_tex))
        self.wait(0.3)

        P_inv = MathTex(r"P^{-1}=\begin{pmatrix}1&1\\0&1\end{pmatrix}",
                          font_size=30, color=GREEN).shift(UP * 0.5 + RIGHT * 3)
        self.play(Write(P_inv))
        self.wait(0.3)

        D_tex = MathTex(r"D=P^{-1}AP=\begin{pmatrix}3&0\\0&2\end{pmatrix}",
                         font_size=36, color=YELLOW).shift(DOWN * 1.0)
        self.play(Write(D_tex))
        self.wait(0.4)

        # Verification: P^-1 A P = D
        # check: P^-1 A = [[1, 1], [0, 1]] @ [[3, 1], [0, 2]] = [[3, 3], [0, 2]]
        # Then @ P: [[3, 3], [0, 2]] @ [[1, -1], [0, 1]] = [[3, 0], [0, 2]] ✓

        self.play(Write(
            Tex(r"matrix in eigenbasis: eigenvalues on the diagonal",
                 color=GREEN, font_size=22).to_edge(DOWN, buff=0.5)
        ))
        self.wait(1.0)
