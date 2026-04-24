from manim import *
import numpy as np


class PrimitiveVsMultipleTriplesRadial(Scene):
    """All multiples of a primitive triple (3,4,5) lie on one ray from the
    origin; each primitive triple gets its own ray."""

    def construct(self):
        title = Tex(
            r"Multiples of $(3,4,5)$ share a radial line",
            font_size=26,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-1, 16, 2], y_range=[-1, 20, 2],
            x_length=6.5, y_length=6.5,
            background_line_style={"stroke_opacity": 0.3},
        ).shift(DOWN * 0.2)
        self.play(Create(plane))

        ray345 = Line(
            plane.c2p(0, 0), plane.c2p(12, 16),
            color=GREEN, stroke_width=2,
        )
        self.play(Create(ray345))

        family = [(3, 4, 5), (6, 8, 10), (9, 12, 15), (12, 16, 20)]
        dots345 = VGroup()
        labs345 = VGroup()
        for a, b, c in family:
            d = Dot(plane.c2p(a, b), radius=0.1, color=GREEN).set_z_index(4)
            lab = MathTex(
                f"({a},{b},{c})", font_size=20, color=GREEN,
            ).next_to(d, UR, buff=0.02)
            dots345.add(d)
            labs345.add(lab)
        self.play(LaggedStart(*[FadeIn(d) for d in dots345], lag_ratio=0.25))
        self.play(LaggedStart(*[Write(l) for l in labs345], lag_ratio=0.25))
        self.wait(0.4)

        prim_hi = SurroundingRectangle(
            VGroup(dots345[0], labs345[0]), color=RED, buff=0.08,
        )
        prim_txt = Tex(
            r"primitive: $\gcd(3,4,5)=1$",
            font_size=24, color=RED,
        ).to_corner(DL, buff=0.4)
        self.play(Create(prim_hi), Write(prim_txt))
        self.wait(0.7)

        ray512 = Line(
            plane.c2p(0, 0), plane.c2p(7.5, 18),
            color=YELLOW, stroke_width=2,
        )
        d512 = Dot(plane.c2p(5, 12), radius=0.1, color=YELLOW).set_z_index(4)
        lab512 = MathTex(
            "(5,12,13)", font_size=22, color=YELLOW,
        ).next_to(d512, UL, buff=0.05)
        self.play(Create(ray512), FadeIn(d512), Write(lab512))
        self.wait(0.3)

        ray815 = Line(
            plane.c2p(0, 0), plane.c2p(10.67, 20),
            color=BLUE, stroke_width=2,
        )
        d815 = Dot(plane.c2p(8, 15), radius=0.1, color=BLUE).set_z_index(4)
        lab815 = MathTex(
            "(8,15,17)", font_size=22, color=BLUE,
        ).next_to(d815, UL, buff=0.05)
        self.play(Create(ray815), FadeIn(d815), Write(lab815))
        self.wait(1.2)
