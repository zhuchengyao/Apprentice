from manim import *
import numpy as np


class CoordinatesOnBasisScalarsExample(Scene):
    """
    Coordinates are scalars: v = (3, 2) means "3 î + 2 ĵ".
    """

    def construct(self):
        title = Tex(r"Coordinates $=$ scalars on basis: $(3, 2) = 3\hat\imath+2\hat\jmath$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-1, 4, 1], y_range=[-1, 3, 1],
                            x_length=8, y_length=5,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.2)
        self.play(Create(plane))

        i_arrow = Arrow(plane.c2p(0, 0), plane.c2p(1, 0), color=GREEN, buff=0, stroke_width=5)
        j_arrow = Arrow(plane.c2p(0, 0), plane.c2p(0, 1), color=RED, buff=0, stroke_width=5)
        self.add(i_arrow, j_arrow)
        self.add(Tex(r"$\hat\imath$", color=GREEN, font_size=22).next_to(i_arrow.get_end(), DR, buff=0.05))
        self.add(Tex(r"$\hat\jmath$", color=RED, font_size=22).next_to(j_arrow.get_end(), UL, buff=0.05))
        self.wait(0.3)

        scaled_i = Arrow(plane.c2p(0, 0), plane.c2p(3, 0), color=GREEN, buff=0, stroke_width=4)
        self.play(Transform(i_arrow.copy(), scaled_i))
        self.add(Tex(r"$3\hat\imath$", color=GREEN, font_size=22).next_to(plane.c2p(3, 0), DOWN, buff=0.15))
        self.wait(0.3)

        scaled_j_shifted = Arrow(plane.c2p(3, 0), plane.c2p(3, 2), color=RED, buff=0, stroke_width=4)
        self.play(Create(scaled_j_shifted))
        self.add(Tex(r"$2\hat\jmath$", color=RED, font_size=22).next_to(plane.c2p(3, 1), RIGHT, buff=0.15))
        self.wait(0.3)

        v_arrow = Arrow(plane.c2p(0, 0), plane.c2p(3, 2), color=YELLOW, buff=0, stroke_width=6)
        self.play(Create(v_arrow))
        self.add(Tex(r"$\vec v=(3, 2)$", color=YELLOW, font_size=24).next_to(v_arrow.get_end(), UR, buff=0.1))
        self.play(Write(
            MathTex(r"(3, 2)", r"=", r"3\hat\imath", r"+", r"2\hat\jmath",
                     font_size=32).shift(DOWN * 2.3).set_color_by_tex("3", GREEN).set_color_by_tex("2", RED)
        ))
        self.wait(1.0)
