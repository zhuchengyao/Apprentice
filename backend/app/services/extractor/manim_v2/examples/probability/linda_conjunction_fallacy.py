from manim import *
import numpy as np


class LindaConjunctionFallacy(Scene):
    """Kahneman-Tversky's Linda problem.  Given a character sketch, people
    often judge 'Linda is a bank teller AND active in feminism' as more
    probable than 'Linda is a bank teller'.  But conjunction always has
    smaller or equal probability:  P(A cap B) <= P(A).  Visualize as
    nested sample-space regions — the conjunction circle is strictly
    contained within the bank-teller circle."""

    def construct(self):
        title = Tex(
            r"Conjunction fallacy (Linda problem): $P(A\cap B) \le P(A)$",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        sketch = Tex(
            r"Linda is a 31-year-old, single, outspoken,"
            r" bright, majored in philosophy,\\"
            r"concerned with discrimination and social justice.",
            font_size=22, color=GREY_A,
        ).move_to(UP * 2.0)
        self.play(FadeIn(sketch))

        universe = Square(side_length=5.5, color=WHITE,
                          stroke_width=2).shift(LEFT * 3 + DOWN * 0.6)
        u_lab = Tex("all possible people", font_size=20,
                    color=WHITE).next_to(universe, DOWN, buff=0.15)

        bank_teller = Circle(radius=1.8, color=BLUE, stroke_width=3,
                             fill_opacity=0.2).move_to(
            universe.get_center() + RIGHT * 0.3
        )
        feminist = Circle(radius=1.5, color=PURPLE, stroke_width=3,
                          fill_opacity=0.2).move_to(
            universe.get_center() + LEFT * 0.6 + UP * 0.3
        )
        both = Intersection(bank_teller, feminist,
                            color=YELLOW, stroke_width=3,
                            fill_opacity=0.45)

        bt_lab = Tex("bank teller", font_size=22, color=BLUE).move_to(
            bank_teller.get_center() + RIGHT * 0.9 + DOWN * 0.9
        )
        f_lab = Tex("feminist", font_size=22, color=PURPLE).move_to(
            feminist.get_center() + LEFT * 0.9 + UP * 0.5
        )
        b_lab = Tex("both", font_size=22, color=YELLOW).move_to(
            Intersection(bank_teller, feminist).get_center()
        )

        self.play(Create(universe), FadeIn(u_lab))
        self.play(Create(bank_teller), Write(bt_lab))
        self.play(Create(feminist), Write(f_lab))
        self.play(FadeIn(both), Write(b_lab))

        options = VGroup(
            Tex(r"A: Linda is a bank teller.", font_size=24, color=BLUE),
            Tex(r"A $\cap$ B: Linda is a bank teller AND a feminist.",
                font_size=24, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        options.to_edge(RIGHT, buff=0.4).shift(UP * 0.5)
        self.play(FadeIn(options))

        rule = VGroup(
            MathTex(r"P(A\cap B) \le P(A)",
                    font_size=30, color=YELLOW),
            Tex(r"\textit{always} — the yellow lens\\ cannot be larger than the blue circle.",
                font_size=22, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        rule.to_edge(RIGHT, buff=0.4).shift(DOWN * 1.2)
        self.play(FadeIn(rule))

        self.play(Indicate(bank_teller, color=BLUE, scale_factor=1.05))
        self.play(Indicate(both, color=YELLOW, scale_factor=1.15))
        self.wait(1.3)
