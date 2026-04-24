from manim import *
import numpy as np


class CharPolyDetZeroExample(Scene):
    """
    To find eigenvalues, solve (A − λI)v = 0 for nonzero v.
    That requires det(A − λI) = 0 (characteristic polynomial).
    Example: A = [[3, 1], [0, 2]] gives det = (3-λ)(2-λ) = 0 → λ = 3, 2.
    """

    def construct(self):
        title = Tex(r"$A\vec v = \lambda\vec v \Rightarrow \det(A-\lambda I) = 0$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Line 1: Av = λv
        l1 = MathTex(r"A\vec v", r"=", r"\lambda\vec v", font_size=40).shift(UP * 1.8)
        self.play(Write(l1))
        self.wait(0.3)

        # Line 2: (A − λI)v = 0
        l2 = MathTex(r"(A - \lambda I)", r"\vec v", r"=", r"\vec 0",
                      font_size=40).shift(UP * 0.8)
        self.play(Write(l2))
        self.wait(0.3)

        # Line 3: for nonzero v, determinant must be zero
        l3 = MathTex(r"\det(A - \lambda I)", r"=", r"0",
                      font_size=42, color=YELLOW).shift(DOWN * 0.3)
        self.play(Write(l3))
        self.wait(0.3)

        # Example
        example = MathTex(r"A=\begin{pmatrix}3&1\\0&2\end{pmatrix}:\quad (3-\lambda)(2-\lambda)=0",
                           font_size=32).shift(DOWN * 1.5)
        self.play(Write(example))
        self.wait(0.4)

        roots = MathTex(r"\Rightarrow\lambda=3,\ \lambda=2",
                         color=GREEN, font_size=34).to_edge(DOWN, buff=0.5)
        self.play(Write(roots))
        self.wait(1.0)
