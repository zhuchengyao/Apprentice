from manim import *
import numpy as np


class DetEigenBasisIndependentExample(Scene):
    """
    Determinant and eigenvalues are basis-independent. Compute them
    for A in standard basis and for A_J = P^(-1) A P in a different
    basis — same det, same eigenvalues.
    """

    def construct(self):
        title = Tex(r"$\det$ and eigenvalues: basis-independent invariants",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        A = np.array([[3.0, 1.0], [0.0, 2.0]])
        P = np.array([[2.0, 1.0], [1.0, 1.0]])  # some change of basis
        A_J = np.linalg.inv(P) @ A @ P  # different-looking matrix

        det_A = float(np.linalg.det(A))  # 6
        det_AJ = float(np.linalg.det(A_J))  # 6

        eigs_A = np.sort(np.linalg.eigvals(A).real)
        eigs_AJ = np.sort(np.linalg.eigvals(A_J).real)

        # LEFT: standard basis
        A_lbl = MathTex(r"A=\begin{pmatrix}3&1\\0&2\end{pmatrix}",
                         font_size=36, color=BLUE).shift(UP * 1.0 + LEFT * 3)
        A_det = MathTex(rf"\det A={det_A:.0f}", color=BLUE, font_size=28).shift(LEFT * 3 + DOWN * 0.2)
        A_eig = MathTex(rf"\text{{eig}}(A)=\{{{eigs_A[0]:.0f}, {eigs_A[1]:.0f}\}}",
                          color=BLUE, font_size=28).shift(LEFT * 3 + DOWN * 1.0)

        # RIGHT: Jenny's basis
        A_J_lbl = MathTex(rf"A_J=\begin{{pmatrix}}{A_J[0, 0]:+.1f}&{A_J[0, 1]:+.1f}\\{A_J[1, 0]:+.1f}&{A_J[1, 1]:+.1f}\end{{pmatrix}}",
                            font_size=36, color=ORANGE).shift(UP * 1.0 + RIGHT * 3)
        AJ_det = MathTex(rf"\det A_J={det_AJ:.0f}", color=ORANGE, font_size=28).shift(RIGHT * 3 + DOWN * 0.2)
        AJ_eig = MathTex(rf"\text{{eig}}(A_J)=\{{{eigs_AJ[0]:.0f}, {eigs_AJ[1]:.0f}\}}",
                           color=ORANGE, font_size=28).shift(RIGHT * 3 + DOWN * 1.0)

        self.play(Write(A_lbl), Write(A_J_lbl))
        self.play(Write(A_det), Write(AJ_det))
        self.play(Write(A_eig), Write(AJ_eig))
        self.wait(0.5)

        self.play(Write(
            Tex(r"same $\det$, same eigenvalues $\Rightarrow$ basis-independent!",
                 color=YELLOW, font_size=24).to_edge(DOWN, buff=0.5)
        ))
        self.wait(1.0)
