from manim import *
import numpy as np


class RationalPointUnitCircleLine(Scene):
    """Every rational point on x^2 + y^2 = 1 is parametrized by a line from
    (-1, 0) with rational slope t; the intersection is
    ((1-t^2)/(1+t^2), 2t/(1+t^2))."""

    def construct(self):
        title = Tex(
            r"Rational points on the unit circle: line sweep from $(-1,0)$",
            font_size=26,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-2.5, 2.5, 1], y_range=[-2.5, 2.5, 1],
            x_length=6.0, y_length=6.0,
            background_line_style={"stroke_opacity": 0.3},
        ).shift(LEFT * 2.0 + DOWN * 0.2)
        unit_radius = plane.c2p(1, 0)[0] - plane.c2p(0, 0)[0]
        circle = Circle(radius=unit_radius, color=BLUE).move_to(
            plane.c2p(0, 0)
        )
        pivot = Dot(plane.c2p(-1, 0), color=WHITE).set_z_index(5)
        pivot_lab = MathTex("(-1, 0)", font_size=22).next_to(
            pivot, DL, buff=0.05
        )
        self.play(Create(plane), Create(circle), FadeIn(pivot), Write(pivot_lab))

        t_tr = ValueTracker(0.4)

        def get_line():
            t = t_tr.get_value()
            p1 = plane.c2p(-1.0, 0.0)
            p2 = plane.c2p(2.0, t * 3.0)
            return Line(p1, p2, color=GREEN, stroke_width=3)

        def get_hit():
            t = t_tr.get_value()
            x = (1 - t * t) / (1 + t * t)
            y = 2 * t / (1 + t * t)
            return Dot(
                plane.c2p(x, y), radius=0.1, color=YELLOW
            ).set_z_index(6)

        line = always_redraw(get_line)
        hit = always_redraw(get_hit)
        self.add(line, hit)

        t_row = VGroup(
            MathTex("t = ", font_size=28),
            DecimalNumber(0.4, num_decimal_places=3, font_size=28),
        ).arrange(RIGHT, buff=0.1)
        t_row[1].add_updater(lambda m: m.set_value(t_tr.get_value()))

        xy_row = VGroup(
            MathTex("x = ", font_size=24),
            DecimalNumber(0.0, num_decimal_places=3, font_size=24),
            MathTex(",\ y = ", font_size=24),
            DecimalNumber(0.0, num_decimal_places=3, font_size=24),
        ).arrange(RIGHT, buff=0.1)
        xy_row[1].add_updater(
            lambda m: m.set_value(
                (1 - t_tr.get_value() ** 2) / (1 + t_tr.get_value() ** 2)
            )
        )
        xy_row[3].add_updater(
            lambda m: m.set_value(
                2 * t_tr.get_value() / (1 + t_tr.get_value() ** 2)
            )
        )

        param_form = MathTex(
            r"\left(\tfrac{1-t^{2}}{1+t^{2}},\; \tfrac{2t}{1+t^{2}}\right)",
            font_size=28, color=YELLOW,
        )
        panel = VGroup(t_row, xy_row, param_form).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25
        )
        panel.to_edge(RIGHT, buff=0.5).shift(UP * 0.2)
        self.add(panel)

        self.play(t_tr.animate.set_value(2.0), run_time=3, rate_func=smooth)
        self.wait(0.2)
        self.play(t_tr.animate.set_value(-1.8), run_time=4, rate_func=smooth)
        self.wait(0.2)
        self.play(t_tr.animate.set_value(0.5), run_time=2, rate_func=smooth)

        note = Tex(
            r"$t = 1/2 \Rightarrow (3/5,\; 4/5) \Rightarrow (3,4,5)$",
            font_size=26, color=YELLOW,
        ).to_edge(DOWN, buff=0.3)
        self.play(Write(note))
        self.wait(1.5)
