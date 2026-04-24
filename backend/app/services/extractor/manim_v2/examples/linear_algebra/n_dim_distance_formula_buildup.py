from manim import *
import numpy as np


class NDimDistanceFormulaBuildup(Scene):
    """Generalize the Pythagorean theorem from 2D to nD.  Start with a right
    triangle (|v|=sqrt(x^2+y^2)), add a z-leg (|v|=sqrt(x^2+y^2+z^2)), then
    abstract to n dimensions.  Reveal the rule by successive TransformFromCopy
    / ReplacementTransform on the formula text."""

    def construct(self):
        title = Tex(
            r"Pythagoras generalized: distance in $\mathbb{R}^n$",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-0.5, 5.5, 1], y_range=[-0.5, 4.5, 1],
            x_length=5.5, y_length=4.5,
            background_line_style={"stroke_opacity": 0.25},
        ).shift(LEFT * 3.2 + DOWN * 0.5)
        origin = plane.c2p(0, 0)
        p_xy = plane.c2p(4, 3)
        p_x = plane.c2p(4, 0)
        self.play(Create(plane))

        leg_x = Line(origin, p_x, color=GREEN, stroke_width=5)
        leg_y = Line(p_x, p_xy, color=RED, stroke_width=5)
        hyp = Line(origin, p_xy, color=WHITE, stroke_width=5)
        self.play(Create(leg_x), Create(leg_y))
        self.play(Create(hyp))

        x_lab = MathTex("x", font_size=28, color=GREEN).next_to(
            leg_x, DOWN, buff=0.1
        )
        y_lab = MathTex("y", font_size=28, color=RED).next_to(
            leg_y, RIGHT, buff=0.1
        )
        hyp_lab = MathTex(
            r"\sqrt{x^2+y^2}", font_size=28,
        ).move_to(plane.c2p(1.5, 2.2)).rotate(np.arctan(3 / 4))
        self.play(Write(x_lab), Write(y_lab), Write(hyp_lab))
        self.wait(0.5)

        formula_2d = MathTex(
            r"\|v\|", r"=", r"\sqrt{x^2 + y^2}",
            font_size=40,
        )
        formula_2d.to_edge(RIGHT, buff=0.5).shift(UP * 1.5)
        self.play(Write(formula_2d))
        self.wait(0.4)

        formula_3d = MathTex(
            r"\|v\|", r"=", r"\sqrt{x^2 + y^2 + z^2}",
            font_size=40,
        )
        formula_3d.next_to(formula_2d, DOWN, buff=0.7)
        self.play(TransformFromCopy(formula_2d, formula_3d))
        self.wait(0.4)

        formula_nd = MathTex(
            r"\|v\|", r"=",
            r"\sqrt{x_1^2 + x_2^2 + \cdots + x_n^2}",
            font_size=40,
        )
        formula_nd.next_to(formula_3d, DOWN, buff=0.7)
        self.play(TransformFromCopy(formula_3d, formula_nd))
        self.wait(0.3)

        box = SurroundingRectangle(formula_nd, color=YELLOW,
                                   buff=0.18, stroke_width=3)
        self.play(Create(box))

        note = Tex(
            r"(Definition of length in any $\mathbb{R}^n$)",
            font_size=22, color=YELLOW,
        ).next_to(box, DOWN, buff=0.3)
        self.play(FadeIn(note))
        self.wait(1.5)
