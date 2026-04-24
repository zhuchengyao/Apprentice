from manim import *
import numpy as np


class NonlinearityNotAllowedExample(Scene):
    """
    In a LINEAR system, only terms like c·x are allowed.
    Forbidden: x², sin(x), xy, etc.
    """

    def construct(self):
        title = Tex(r"Linear systems: only $c\cdot x_i$ terms allowed",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Allowed
        allowed_lbl = Tex(r"Allowed:", color=GREEN, font_size=26).shift(UP * 1.5 + LEFT * 4)
        allowed_terms = MathTex(r"3x,\quad -2y,\quad 5z,\quad c_1x + c_2y", font_size=36)
        allowed_terms.set_color(GREEN).next_to(allowed_lbl, RIGHT, buff=0.3)
        self.play(Write(allowed_lbl), Write(allowed_terms))
        self.wait(0.5)

        # Not allowed
        not_allowed_lbl = Tex(r"NOT allowed:", color=RED, font_size=26).shift(DOWN * 0.2 + LEFT * 4)
        self.play(Write(not_allowed_lbl))

        forbidden = [r"x^2", r"\sin(x)", r"xy", r"e^x", r"\sqrt{x}"]
        tex_objs = VGroup(*[MathTex(f, font_size=44, color=RED) for f in forbidden])
        tex_objs.arrange(RIGHT, buff=0.8).next_to(not_allowed_lbl, RIGHT, buff=0.3)

        # Circle-slash
        for tex in tex_objs:
            self.play(Write(tex), run_time=0.5)
            slash = Circle(radius=tex.get_width() * 0.6, color=RED,
                            stroke_width=3).move_to(tex)
            line = Line(slash.get_corner(UL), slash.get_corner(DR),
                         color=RED, stroke_width=3)
            self.play(ShowCreation(slash), ShowCreation(line), run_time=0.3)
            self.wait(0.2)

        # Summary
        summary = Tex(r"Linearity: each variable appears to first power, no products",
                       color=GREEN, font_size=24).to_edge(DOWN, buff=0.5)
        self.play(Write(summary))
        self.wait(1.0)
