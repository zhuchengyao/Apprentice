from manim import *
import numpy as np


class ExpHomomorphismAddToMultiply(Scene):
    """The exponential is the homomorphism from (R, +) to (R_>0, ×):
    exp(a + b) = exp(a) * exp(b).
    Show a GREEN dot on the additive line moving from 0 to a=0.7 to a+b=1.2,
    with its image on the multiplicative line jumping from 1 to e^0.7 to
    e^1.2, demonstrating sliding → stretching."""

    def construct(self):
        title = MathTex(
            r"\exp:\ (\mathbb{R},\,+)\ \longrightarrow\ (\mathbb{R}_{>0},\,\times)",
            font_size=32,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        sub_title = Tex(
            r"$e^{a+b} = e^a \cdot e^b$ — sliding maps to stretching",
            font_size=26, color=YELLOW,
        ).next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(sub_title))

        add_line = NumberLine(
            x_range=[-1, 3, 1], length=9, include_numbers=True,
            font_size=22, color=GREEN,
        ).shift(UP * 0.8)
        mul_line = NumberLine(
            x_range=[0, 10, 1], length=9, include_numbers=True,
            font_size=22, color=ORANGE,
        ).shift(DOWN * 1.8)
        add_tag = MathTex(r"+", font_size=32, color=GREEN).next_to(
            add_line, LEFT, buff=0.3
        )
        mul_tag = MathTex(r"\times", font_size=32, color=ORANGE).next_to(
            mul_line, LEFT, buff=0.3
        )
        self.play(Create(add_line), Create(mul_line),
                  Write(add_tag), Write(mul_tag))

        a_tr = ValueTracker(0.0)

        def get_add_dot():
            return Dot(add_line.n2p(a_tr.get_value()),
                       radius=0.1, color=YELLOW).set_z_index(5)

        def get_mul_dot():
            return Dot(mul_line.n2p(np.exp(a_tr.get_value())),
                       radius=0.1, color=RED).set_z_index(5)

        def get_arrow():
            a = a_tr.get_value()
            return Arrow(
                add_line.n2p(a), mul_line.n2p(np.exp(a)),
                buff=0.1, color=BLUE, stroke_width=3,
                max_tip_length_to_length_ratio=0.04,
            )

        def get_a_readout():
            a = a_tr.get_value()
            row = VGroup(
                MathTex(r"a=", font_size=24, color=GREEN),
                DecimalNumber(a, num_decimal_places=2, font_size=24,
                              color=GREEN),
                MathTex(r"\quad e^a=", font_size=24, color=RED),
                DecimalNumber(np.exp(a), num_decimal_places=3, font_size=24,
                              color=RED),
            ).arrange(RIGHT, buff=0.1)
            row.to_corner(DR, buff=0.4).shift(UP * 0.25)
            return row

        add_dot = always_redraw(get_add_dot)
        mul_dot = always_redraw(get_mul_dot)
        arrow = always_redraw(get_arrow)
        readout = always_redraw(get_a_readout)
        self.add(add_dot, mul_dot, arrow, readout)

        self.play(a_tr.animate.set_value(0.7), run_time=2)
        self.wait(0.3)
        self.play(a_tr.animate.set_value(1.2), run_time=2)
        self.wait(0.3)
        self.play(a_tr.animate.set_value(2.0), run_time=2)
        self.wait(0.3)
        self.play(a_tr.animate.set_value(-0.5), run_time=2)
        self.wait(1.0)

        caption = MathTex(
            r"\text{slide by }a\ \Longleftrightarrow\ \text{stretch by }e^a",
            font_size=28, color=YELLOW,
        ).move_to(ORIGIN + DOWN * 0.5)
        self.play(FadeIn(caption))
        self.wait(1.5)
