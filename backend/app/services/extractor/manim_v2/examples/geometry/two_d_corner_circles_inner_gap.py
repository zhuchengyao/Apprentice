from manim import *
import numpy as np


class TwoDCornerCirclesInnerGap(Scene):
    """2D setup for the high-dimensional inner-sphere-escapes-the-box
    phenomenon.  A 2x2 box with four YELLOW unit circles centered at the
    corners (±1, ±1).  A GREEN inner circle tangent to all four has radius
    r = sqrt(2) - 1 ≈ 0.414 — derived from a right triangle with legs 1, 1
    and hypotenuse sqrt(2)."""

    def construct(self):
        title = Tex(
            r"Four unit circles in a $2\times 2$ box: how big is the gap?",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=6.5, y_length=6.5,
            background_line_style={"stroke_opacity": 0.25},
        ).shift(LEFT * 2.3 + DOWN * 0.2)
        origin = plane.c2p(0, 0)
        unit = plane.c2p(1, 0)[0] - origin[0]
        self.play(Create(plane))

        box = Polygon(
            plane.c2p(-2, -2), plane.c2p(2, -2),
            plane.c2p(2, 2), plane.c2p(-2, 2),
            color=RED, stroke_width=4,
        )
        self.play(Create(box))

        corner_circles = VGroup(*[
            Circle(radius=unit, color=YELLOW, stroke_width=3).move_to(
                plane.c2p(x, y)
            )
            for x, y in [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        ])
        corner_dots = VGroup(*[
            Dot(plane.c2p(x, y), radius=0.05, color=YELLOW)
            for x, y in [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        ])
        self.play(LaggedStart(*[Create(c) for c in corner_circles],
                              lag_ratio=0.15))
        self.play(FadeIn(corner_dots))

        diag = Line(origin, plane.c2p(1, 1), color=WHITE, stroke_width=3)
        leg_x = Line(origin, plane.c2p(1, 0), color=GREEN, stroke_width=4)
        leg_y = Line(plane.c2p(1, 0), plane.c2p(1, 1),
                     color=GREEN, stroke_width=4)
        self.play(Create(leg_x), Create(leg_y))

        l1 = MathTex("1", font_size=28, color=GREEN).next_to(
            leg_x, DOWN, buff=0.1
        )
        l2 = MathTex("1", font_size=28, color=GREEN).next_to(
            leg_y, RIGHT, buff=0.1
        )
        self.play(Write(l1), Write(l2))

        self.play(Create(diag))
        diag_label = MathTex(r"\sqrt{2}", font_size=28, color=WHITE).move_to(
            plane.c2p(0.42, 0.58)
        )
        self.play(Write(diag_label))
        self.wait(0.5)

        inner_r = np.sqrt(2) - 1
        inner_circle = Circle(
            radius=inner_r * unit, color=GREEN,
            stroke_width=4, fill_opacity=0.25,
        ).move_to(origin)
        self.play(GrowFromCenter(inner_circle))

        r_line = Line(origin, plane.c2p(inner_r, 0),
                      color=GREEN, stroke_width=3)
        self.play(Create(r_line))

        derivation = VGroup(
            MathTex(r"d_{0 \to (1,1)} = \sqrt{1^2 + 1^2} = \sqrt{2}",
                    font_size=26),
            MathTex(r"r_{\text{inner}} = \sqrt{2} - 1", font_size=30,
                    color=GREEN),
            MathTex(r"\approx 0.414", font_size=26, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        derivation.to_edge(RIGHT, buff=0.4).shift(UP * 0.4)
        self.play(Write(derivation[0]))
        self.play(Write(derivation[1]))
        self.play(Write(derivation[2]))
        self.wait(1.3)
