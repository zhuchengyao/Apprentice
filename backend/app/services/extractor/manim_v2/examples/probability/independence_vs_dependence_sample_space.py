from manim import *
import numpy as np


class IndependenceVsDependenceSampleSpace(Scene):
    """A picture of independence.  LEFT panel: two events A and B are
    independent — P(A|B) = P(A).  The sample-space grid splits cleanly
    into a rectangular product.  RIGHT panel: A and B are dependent —
    P(A|B) ≠ P(A).  The shape of A-given-B 'warps' compared to A-given-
    not-B."""

    def construct(self):
        title = Tex(
            r"Independence vs dependence as sample-space shape",
            font_size=30,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        def make_panel(center, pB, pA_B, pA_notB, cap_color, cap):
            side = 3.6
            origin = np.array([center[0] - side / 2, center[1] - side / 2, 0])
            outer = Square(side_length=side, color=WHITE,
                           stroke_width=3).move_to(
                origin + np.array([side / 2, side / 2, 0])
            )

            B_col = Rectangle(
                width=pB * side, height=side,
                stroke_width=0, fill_opacity=0.25, fill_color=BLUE,
            ).move_to(origin + np.array([pB * side / 2, side / 2, 0]))
            AcapB = Rectangle(
                width=pB * side, height=pA_B * side,
                stroke_width=2, stroke_color=GREEN,
                fill_opacity=0.55, fill_color=GREEN,
            ).move_to(
                origin + np.array([pB * side / 2,
                                   side - pA_B * side / 2, 0])
            )
            AcapNotB = Rectangle(
                width=(1 - pB) * side, height=pA_notB * side,
                stroke_width=2, stroke_color=GREEN,
                fill_opacity=0.3, fill_color=GREEN,
            ).move_to(
                origin + np.array([pB * side + (1 - pB) * side / 2,
                                   side - pA_notB * side / 2, 0])
            )

            B_label = MathTex(r"B", font_size=22, color=BLUE).move_to(
                origin + np.array([pB * side / 2, 0.3, 0])
            )
            notB_label = MathTex(r"B^c", font_size=22, color=GREY_B).move_to(
                origin + np.array([pB * side + (1 - pB) * side / 2, 0.3, 0])
            )
            cap_tex = Tex(cap, font_size=26, color=cap_color).next_to(
                outer, UP, buff=0.2
            )
            nums = VGroup(
                MathTex(rf"P(A|B)={pA_B:.2f}", font_size=22, color=GREEN),
                MathTex(rf"P(A|B^c)={pA_notB:.2f}", font_size=22, color=GREEN),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            nums.next_to(outer, DOWN, buff=0.3)
            return VGroup(outer, B_col, AcapB, AcapNotB,
                          B_label, notB_label, cap_tex, nums)

        indep = make_panel(
            center=[-3.5, -0.3], pB=0.45,
            pA_B=0.6, pA_notB=0.6,
            cap_color=GREEN, cap="Independent",
        )
        dep = make_panel(
            center=[3.5, -0.3], pB=0.45,
            pA_B=0.85, pA_notB=0.25,
            cap_color=RED, cap="Dependent",
        )
        self.play(FadeIn(indep))
        self.wait(0.3)
        self.play(FadeIn(dep))

        rule_indep = MathTex(
            r"\text{indep.:}\ P(A|B) = P(A|B^c) = P(A)",
            font_size=24, color=GREEN,
        )
        rule_dep = MathTex(
            r"\text{dep.:}\ P(A|B) \ne P(A|B^c)",
            font_size=24, color=RED,
        )
        rules = VGroup(rule_indep, rule_dep).arrange(DOWN,
                                                     aligned_edge=LEFT,
                                                     buff=0.2)
        rules.to_edge(DOWN, buff=0.25)
        self.play(FadeIn(rules))
        self.wait(1.4)
