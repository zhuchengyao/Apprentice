from manim import *
import numpy as np


class InversePythagoreanTheorem(Scene):
    """The Inverse Pythagorean Theorem (IPT): in a right triangle with legs
    a, b and the altitude h to the hypotenuse, 1/h^2 = 1/a^2 + 1/b^2.  This
    is the lemma 3Blue1Brown uses to derive the Basel sum via
    'splitting' a single lighthouse into two equivalent ones on a larger
    circle."""

    def construct(self):
        title = Tex(
            r"Inverse Pythagorean Theorem: $\tfrac{1}{h^2} = \tfrac{1}{a^2} + \tfrac{1}{b^2}$",
            font_size=30,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        A = np.array([-3, -1.5, 0])
        B = np.array([3, -1.5, 0])
        C = np.array([0.5, 2.2, 0])

        AB = B - A
        AC = C - A
        AB_len_sq = np.dot(AB, AB)
        t = np.dot(AC, AB) / AB_len_sq
        F = A + t * AB

        triangle = Polygon(A, B, C, color=WHITE, stroke_width=3,
                           fill_opacity=0.1)
        self.play(Create(triangle))

        right_mark = Square(side_length=0.22, color=YELLOW,
                            stroke_width=2).move_to(C + 0.11 * (A - C) / np.linalg.norm(A - C)
                                                    + 0.11 * (B - C) / np.linalg.norm(B - C))
        self.play(FadeIn(right_mark))

        altitude = Line(C, F, color=GREEN, stroke_width=4)
        self.play(Create(altitude))
        right_mark2 = Square(side_length=0.18, color=GREEN,
                             stroke_width=2).rotate(
            np.arctan2((C - F)[1], (C - F)[0])
        ).move_to(F + 0.14 * (C - F) / np.linalg.norm(C - F) + 0.14 * (B - F) / np.linalg.norm(B - F))
        self.play(FadeIn(right_mark2))

        a_len = np.linalg.norm(C - A)
        b_len = np.linalg.norm(C - B)
        h_len = np.linalg.norm(C - F)

        a_lab = MathTex(rf"a={a_len:.2f}", font_size=26, color=BLUE).move_to(
            (A + C) / 2 + UP * 0.25 + LEFT * 0.25
        )
        b_lab = MathTex(rf"b={b_len:.2f}", font_size=26, color=RED).move_to(
            (B + C) / 2 + UP * 0.25 + RIGHT * 0.25
        )
        h_lab = MathTex(rf"h={h_len:.2f}", font_size=26,
                        color=GREEN).move_to(
            (C + F) / 2 + RIGHT * 0.55
        )
        self.play(Write(a_lab), Write(b_lab), Write(h_lab))

        check = VGroup(
            MathTex(r"\tfrac{1}{h^2} \stackrel{?}{=} \tfrac{1}{a^2} + \tfrac{1}{b^2}",
                    font_size=28),
            MathTex(
                rf"\tfrac{{1}}{{h^2}} = {1/h_len**2:.4f}",
                font_size=26, color=GREEN,
            ),
            MathTex(
                rf"\tfrac{{1}}{{a^2}} + \tfrac{{1}}{{b^2}} ="
                rf" {1/a_len**2:.4f} + {1/b_len**2:.4f} ="
                rf" {1/a_len**2 + 1/b_len**2:.4f}",
                font_size=26, color=YELLOW,
            ),
            MathTex(r"\checkmark", font_size=40, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        check.to_edge(RIGHT, buff=0.4).shift(DOWN * 0.2)
        check[-1].next_to(check[2], RIGHT, buff=0.3)
        self.play(FadeIn(check[0]))
        self.play(Write(check[1]))
        self.play(Write(check[2]))
        self.play(Write(check[3]))
        self.wait(1.2)

        use_note = Tex(
            r"Used in the Basel proof to split one lighthouse into two\\"
            r"on a circle of double diameter — intensity is preserved.",
            font_size=24, color=YELLOW,
        ).to_edge(DOWN, buff=0.2)
        self.play(FadeIn(use_note))
        self.wait(1.3)
