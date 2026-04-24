from manim import *
import numpy as np


class SampleSpaceConditionalArea(Scene):
    """Visualize conditional probability as area.  Unit square sample space
    is split vertically by P(B) = 0.35 (BLUE region), then each column is
    split horizontally by its P(A|B) or P(A|B^c) to form four regions.
    Animate derivation of Bayes' rule: P(A|B) = P(A cap B) / P(B) as the
    highlighted area ratio."""

    def construct(self):
        title = Tex(
            r"Sample space as area: conditional probability",
            font_size=30,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        side = 4.5
        origin = np.array([-2.3, -2.0, 0])
        unit_square = Square(side_length=side, color=WHITE,
                             stroke_width=3).move_to(
            origin + np.array([side / 2, side / 2, 0])
        )
        label = Tex(r"sample space (area = 1)", font_size=22,
                    color=WHITE).next_to(unit_square, UP, buff=0.2)
        self.play(Create(unit_square), Write(label))

        pB = 0.35
        pA_given_B = 0.7
        pA_given_notB = 0.2

        B_col = Rectangle(
            width=pB * side, height=side,
            stroke_width=0, fill_opacity=0.25, fill_color=BLUE,
        ).move_to(origin + np.array([pB * side / 2, side / 2, 0]))
        notB_col = Rectangle(
            width=(1 - pB) * side, height=side,
            stroke_width=0, fill_opacity=0.10, fill_color=GREY_B,
        ).move_to(origin + np.array([pB * side + (1 - pB) * side / 2,
                                     side / 2, 0]))
        B_lab = MathTex(rf"P(B)={pB:.2f}", font_size=22,
                        color=BLUE).next_to(B_col, DOWN, buff=0.15)
        notB_lab = MathTex(rf"P(B^c)={1-pB:.2f}", font_size=22,
                           color=GREY_B).next_to(notB_col, DOWN, buff=0.15)
        self.play(FadeIn(B_col), FadeIn(notB_col),
                  Write(B_lab), Write(notB_lab))

        AcapB = Rectangle(
            width=pB * side, height=pA_given_B * side,
            stroke_width=2, stroke_color=GREEN,
            fill_opacity=0.55, fill_color=GREEN,
        ).move_to(origin + np.array([pB * side / 2,
                                     side - pA_given_B * side / 2, 0]))
        AcapNotB = Rectangle(
            width=(1 - pB) * side, height=pA_given_notB * side,
            stroke_width=2, stroke_color=GREEN,
            fill_opacity=0.25, fill_color=GREEN,
        ).move_to(origin + np.array([pB * side + (1 - pB) * side / 2,
                                     side - pA_given_notB * side / 2, 0]))
        AcapB_lab = MathTex(
            rf"P(A\cap B)={pB*pA_given_B:.3f}",
            font_size=20, color=GREEN,
        ).move_to(AcapB.get_center())
        AcapNotB_lab = MathTex(
            rf"P(A\cap B^c)={(1-pB)*pA_given_notB:.3f}",
            font_size=20, color=GREEN,
        ).move_to(AcapNotB.get_center())
        self.play(FadeIn(AcapB), FadeIn(AcapNotB))
        self.play(Write(AcapB_lab), Write(AcapNotB_lab))

        ratio = VGroup(
            MathTex(r"P(A \mid B) = \tfrac{P(A\cap B)}{P(B)}",
                    font_size=28),
            MathTex(
                rf"= \tfrac{{{pB*pA_given_B:.3f}}}{{{pB:.2f}}}"
                rf" = {pA_given_B:.2f}",
                font_size=28, color=GREEN,
            ),
            MathTex(
                rf"P(A) = P(A\cap B) + P(A\cap B^c) = "
                rf"{pB*pA_given_B + (1-pB)*pA_given_notB:.3f}",
                font_size=24, color=YELLOW,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        ratio.to_edge(RIGHT, buff=0.4).shift(DOWN * 0.3)
        self.play(FadeIn(ratio[0]))
        self.play(Write(ratio[1]))
        self.play(FadeIn(ratio[2]))
        self.wait(1.5)
