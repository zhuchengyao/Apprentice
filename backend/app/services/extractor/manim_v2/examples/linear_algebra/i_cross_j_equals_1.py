from manim import *
import numpy as np


class ICrossJEquals1Example(Scene):
    """
    Fundamental basis identity: î × ĵ = +1 in 2D (unit area, CCW).
    Reversed order ĵ × î = -1 (CW, swaps sign).
    """

    def construct(self):
        title = Tex(r"Basis cross: $\hat\imath\times\hat\jmath=+1$ (ordered)",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-1, 2, 1], y_range=[-1, 2, 1],
                            x_length=5, y_length=5,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(LEFT * 2.5 + DOWN * 0.2)
        self.play(Create(plane))

        # î, ĵ unit square
        i_arrow = Arrow(plane.c2p(0, 0), plane.c2p(1, 0),
                         color=GREEN, buff=0, stroke_width=6)
        j_arrow = Arrow(plane.c2p(0, 0), plane.c2p(0, 1),
                         color=RED, buff=0, stroke_width=6)
        unit_square = Polygon(plane.c2p(0, 0), plane.c2p(1, 0),
                               plane.c2p(1, 1), plane.c2p(0, 1),
                               color=YELLOW, stroke_width=3,
                               fill_color=GREEN, fill_opacity=0.3)
        self.add(unit_square, i_arrow, j_arrow)
        self.add(Tex(r"$\hat\imath$", color=GREEN, font_size=24).next_to(i_arrow.get_end(), DR, buff=0.05))
        self.add(Tex(r"$\hat\jmath$", color=RED, font_size=24).next_to(j_arrow.get_end(), UL, buff=0.05))
        self.add(Tex(r"area $= 1$", color=YELLOW, font_size=22).move_to(plane.c2p(0.5, 0.5)))

        # Right column: identities
        ident = VGroup(
            MathTex(r"\hat\imath\times\hat\jmath = +1", color=GREEN, font_size=36),
            MathTex(r"\hat\jmath\times\hat\imath = -1", color=RED, font_size=36),
            Tex(r"order matters (anti-commutative)",
                 color=YELLOW, font_size=22),
            Tex(r"$\vec v\times\vec w = -\vec w\times\vec v$",
                 color=YELLOW, font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        self.play(Write(ident))
        self.wait(1.0)
