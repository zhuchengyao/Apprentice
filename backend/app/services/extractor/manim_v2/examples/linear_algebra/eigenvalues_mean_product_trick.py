from manim import *
import numpy as np


class EigenvaluesMeanProductTrick(Scene):
    """3Blue1Brown's 'one-minute eigenvalue' trick for 2x2 matrices.
    For A = [[a, b], [c, d]]:
        mean m = (a+d)/2 = tr(A)/2
        product p = ad - bc = det(A)
    Then the eigenvalues are m ± sqrt(m^2 - p).  Derive from the char
    polynomial lambda^2 - tr*lambda + det = 0 and show 3 examples."""

    def construct(self):
        title = Tex(
            r"Fast eigenvalues of a $2\times 2$: $\lambda = m \pm \sqrt{m^2 - p}$",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        derivation = VGroup(
            MathTex(r"A = \begin{pmatrix} a & b \\ c & d \end{pmatrix},"
                    r"\quad \det(A - \lambda I) = 0", font_size=26),
            MathTex(
                r"\lambda^2 - (a+d)\,\lambda + (ad - bc) = 0",
                font_size=26,
            ),
            MathTex(
                r"m = \tfrac{a+d}{2},\quad p = ad - bc",
                font_size=26, color=YELLOW,
            ),
            MathTex(
                r"\lambda = m \pm \sqrt{m^2 - p}",
                font_size=30, color=GREEN,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        derivation.to_edge(LEFT, buff=0.5).shift(UP * 0.5)
        for eq in derivation:
            self.play(Write(eq))

        examples = [
            ([[2, 1], [1, 2]], "symmetric"),
            ([[3, -1], [2, 0]], "mixed"),
            ([[0, -1], [1, 0]], "rotation"),
        ]

        cards = VGroup()
        for i, (M, name) in enumerate(examples):
            a, b = M[0]
            c, d = M[1]
            m = (a + d) / 2
            p = a * d - b * c
            disc = m * m - p
            if disc >= 0:
                sq = np.sqrt(disc)
                lambdas = f"{m + sq:.2f},\\ {m - sq:.2f}"
            else:
                sq = np.sqrt(-disc)
                lambdas = f"{m:.2f}\\pm{sq:.2f}i"
            card = VGroup(
                Tex(rf"Example: {name}",
                    font_size=22, color=BLUE),
                MathTex(
                    rf"A = \begin{{pmatrix}} {a} & {b} \\\\"
                    rf" {c} & {d} \end{{pmatrix}}",
                    font_size=24,
                ),
                MathTex(
                    rf"m={m:.1f},\ p={p:.1f}",
                    font_size=22, color=YELLOW,
                ),
                MathTex(
                    rf"\lambda = {lambdas}",
                    font_size=22, color=GREEN,
                ),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
            card.move_to([3.3, 1.8 - i * 1.95, 0])
            cards.add(card)

        self.play(LaggedStart(*[FadeIn(c) for c in cards],
                              lag_ratio=0.3, run_time=3))

        box = SurroundingRectangle(derivation[-1], color=GREEN,
                                   buff=0.15, stroke_width=3)
        self.play(Create(box))
        self.wait(1.5)
