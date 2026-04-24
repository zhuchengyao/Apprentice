from manim import *
import numpy as np


class AdditiveVsMultiplicativeRealLine(Scene):
    """Two different group structures on the number line:
    (R, +)  — adding a shifts the line by a  (translation).
    (R_+, ×) — multiplying by k stretches the line by factor k from 1."""

    def construct(self):
        title = Tex(
            r"Two groups, two actions on the number line",
            font_size=30,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        add_label = MathTex(r"(\mathbb{R},\, +)", font_size=36,
                            color=GREEN).move_to([-5, 1.7, 0])
        mul_label = MathTex(r"(\mathbb{R}_{>0},\, \times)",
                            font_size=36, color=ORANGE).move_to(
            [-5, -1.7, 0]
        )
        self.play(Write(add_label), Write(mul_label))

        add_line = NumberLine(
            x_range=[-3, 5, 1], length=10, include_numbers=True,
            font_size=22, color=GREEN,
        ).shift(UP * 1.0)
        mul_line = NumberLine(
            x_range=[0, 8, 1], length=10, include_numbers=True,
            font_size=22, color=ORANGE,
        ).shift(DOWN * 1.5)
        self.play(Create(add_line), Create(mul_line))

        add_dot = Dot(add_line.n2p(0), radius=0.1,
                      color=YELLOW).set_z_index(4)
        mul_dot = Dot(mul_line.n2p(1), radius=0.1,
                      color=YELLOW).set_z_index(4)
        add_marker_lab = MathTex("0", font_size=28,
                                 color=YELLOW).next_to(add_dot, UP, buff=0.15)
        mul_marker_lab = MathTex("1", font_size=28,
                                 color=YELLOW).next_to(mul_dot, UP, buff=0.15)
        self.play(FadeIn(add_dot), FadeIn(mul_dot),
                  Write(add_marker_lab), Write(mul_marker_lab))

        add_op = MathTex(r"+2", font_size=34, color=GREEN).next_to(
            add_line, RIGHT, buff=0.3
        )
        mul_op = MathTex(r"\times 2", font_size=34, color=ORANGE).next_to(
            mul_line, RIGHT, buff=0.3
        )
        self.play(Write(add_op), Write(mul_op))

        self.play(
            add_line.animate.shift(LEFT * add_line.unit_size * 2),
            add_dot.animate.shift(LEFT * 0),
            add_marker_lab.animate.shift(LEFT * 0),
            run_time=2,
        )
        self.wait(0.3)

        self.play(
            mul_line.animate.stretch(
                2, dim=0, about_point=mul_line.n2p(0),
            ),
            run_time=2,
        )
        self.wait(0.3)

        summary = VGroup(
            Tex(r"add $a$: slide by $a$", font_size=26, color=GREEN),
            Tex(r"mult by $k$: stretch by factor $k$ from $1$",
                font_size=26, color=ORANGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        summary.to_corner(DR, buff=0.4).shift(UP * 0.3)
        self.play(FadeIn(summary))
        self.wait(1.5)
