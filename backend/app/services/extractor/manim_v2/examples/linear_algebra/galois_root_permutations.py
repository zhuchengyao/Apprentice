from manim import *
import numpy as np


class GaloisRootPermutations(Scene):
    """Galois theory in a nutshell.  The polynomial x^4 - 5x^2 + 6 has
    roots ±sqrt(2), ±sqrt(3).  The Galois group is the subgroup of S_4
    that respects algebraic relations: you CAN swap (sqrt(2) <-> -sqrt(2))
    and (sqrt(3) <-> -sqrt(3)) independently — this is V_4 of order 4.
    You CANNOT swap sqrt(2) <-> sqrt(3) because (sqrt(2))^2 = 2 not 3."""

    def construct(self):
        title = Tex(
            r"Galois group of $x^4 - 5x^2 + 6$: allowed root permutations",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        root_labels = [
            (r"\sqrt{2}", np.sqrt(2), BLUE),
            (r"-\sqrt{2}", -np.sqrt(2), BLUE),
            (r"\sqrt{3}", np.sqrt(3), GREEN),
            (r"-\sqrt{3}", -np.sqrt(3), GREEN),
        ]

        nl = NumberLine(
            x_range=[-2.5, 2.5, 0.5], length=10,
            include_numbers=False, color=WHITE,
        ).shift(UP * 1.6)
        self.play(Create(nl))

        dots = VGroup()
        labels = VGroup()
        for tex, val, color in root_labels:
            d = Dot(nl.n2p(val), radius=0.1, color=color).set_z_index(4)
            lab = MathTex(tex, font_size=24, color=color).next_to(
                d, UP, buff=0.2,
            )
            dots.add(d)
            labels.add(lab)
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.15))
        self.play(LaggedStart(*[Write(l) for l in labels],
                              lag_ratio=0.15))

        allowed = VGroup(
            Tex(r"\textbf{Allowed:}", font_size=24, color=GREEN),
            MathTex(r"e\ \ \text{(identity)}",
                    font_size=22),
            MathTex(r"\sigma: \sqrt{2} \leftrightarrow -\sqrt{2}",
                    font_size=22, color=BLUE),
            MathTex(r"\tau: \sqrt{3} \leftrightarrow -\sqrt{3}",
                    font_size=22, color=GREEN),
            MathTex(r"\sigma\tau: \text{both simultaneously}",
                    font_size=22, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        allowed.to_edge(LEFT, buff=0.5).shift(DOWN * 1.3)

        forbidden = VGroup(
            Tex(r"\textbf{Forbidden:}", font_size=24, color=RED),
            MathTex(r"\sqrt{2} \leftrightarrow \sqrt{3}",
                    font_size=22, color=RED),
            Tex(r"because $(\sqrt{2})^2 = 2 \ne 3 = (\sqrt{3})^2$",
                font_size=20, color=RED),
            Tex(r"algebraic relations must be preserved",
                font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        forbidden.to_edge(RIGHT, buff=0.5).shift(DOWN * 1.3)

        self.play(FadeIn(allowed))
        self.play(FadeIn(forbidden))

        conclusion = MathTex(
            r"\text{Gal}(\mathbb{Q}(\sqrt{2},\sqrt{3})/\mathbb{Q})"
            r" \cong \mathbb{Z}_2 \times \mathbb{Z}_2 = V_4",
            font_size=28, color=YELLOW,
        )
        conclusion.to_edge(DOWN, buff=0.3)
        self.play(Write(conclusion))
        box = SurroundingRectangle(conclusion, color=YELLOW,
                                   buff=0.15, stroke_width=3)
        self.play(Create(box))
        self.wait(1.5)
