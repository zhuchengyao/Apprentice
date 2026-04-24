from manim import *
import numpy as np


class SixTrigFunctionsOnUnitCircle(Scene):
    """All six trig functions shown as geometric segment lengths on the unit
    circle: sin (vertical rise), cos (horizontal run), tan (tangent segment at
    x = 1), sec (radius extension to x = 1), cot (tangent at y = 1), csc
    (radius extension to y = 1)."""

    def construct(self):
        title = Tex(
            r"Six trig functions as segment lengths on the unit circle",
            font_size=26,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-3.5, 3.5, 1], y_range=[-3.5, 3.5, 1],
            x_length=6.5, y_length=6.5,
            background_line_style={"stroke_opacity": 0.2},
        ).shift(LEFT * 2.0 + DOWN * 0.2)
        origin = plane.c2p(0, 0)
        unit = plane.c2p(1, 0)[0] - origin[0]
        circle = Circle(radius=unit, color=BLUE).move_to(origin)
        self.play(Create(plane), Create(circle))

        theta_tr = ValueTracker(0.6)

        def get_radius():
            t = theta_tr.get_value()
            return Line(
                origin, plane.c2p(np.cos(t), np.sin(t)),
                color=WHITE, stroke_width=3,
            )

        def get_point():
            t = theta_tr.get_value()
            return Dot(
                plane.c2p(np.cos(t), np.sin(t)),
                radius=0.08, color=YELLOW,
            ).set_z_index(5)

        def get_sin():
            t = theta_tr.get_value()
            return Line(
                plane.c2p(np.cos(t), 0),
                plane.c2p(np.cos(t), np.sin(t)),
                color=RED, stroke_width=4,
            )

        def get_cos():
            t = theta_tr.get_value()
            return Line(
                origin, plane.c2p(np.cos(t), 0),
                color=GREEN, stroke_width=4,
            )

        def get_tan():
            t = theta_tr.get_value()
            if abs(np.cos(t)) < 1e-3:
                return VMobject()
            return Line(
                plane.c2p(1, 0),
                plane.c2p(1, np.tan(t)),
                color=ORANGE, stroke_width=4,
            )

        def get_sec():
            t = theta_tr.get_value()
            if abs(np.cos(t)) < 1e-3:
                return VMobject()
            return Line(
                origin, plane.c2p(1, np.tan(t)),
                color=PURPLE, stroke_width=3,
            )

        def get_cot():
            t = theta_tr.get_value()
            if abs(np.sin(t)) < 1e-3:
                return VMobject()
            return Line(
                plane.c2p(0, 1),
                plane.c2p(1.0 / np.tan(t), 1),
                color=TEAL, stroke_width=4,
            )

        def get_csc():
            t = theta_tr.get_value()
            if abs(np.sin(t)) < 1e-3:
                return VMobject()
            return Line(
                origin, plane.c2p(1.0 / np.tan(t), 1),
                color=PINK, stroke_width=3,
            )

        self.add(
            always_redraw(get_radius),
            always_redraw(get_point),
            always_redraw(get_sin),
            always_redraw(get_cos),
            always_redraw(get_tan),
            always_redraw(get_sec),
            always_redraw(get_cot),
            always_redraw(get_csc),
        )

        legend = VGroup(
            Tex(r"$\sin\theta$", color=RED, font_size=26),
            Tex(r"$\cos\theta$", color=GREEN, font_size=26),
            Tex(r"$\tan\theta$", color=ORANGE, font_size=26),
            Tex(r"$\sec\theta$", color=PURPLE, font_size=26),
            Tex(r"$\csc\theta$", color=PINK, font_size=26),
            Tex(r"$\cot\theta$", color=TEAL, font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        legend.to_edge(RIGHT, buff=0.5).shift(UP * 0.3)

        theta_row = VGroup(
            MathTex(r"\theta = ", font_size=28),
            DecimalNumber(0.6, num_decimal_places=3, font_size=28),
        ).arrange(RIGHT, buff=0.1)
        theta_row[1].add_updater(lambda m: m.set_value(theta_tr.get_value()))
        theta_row.next_to(legend, DOWN, buff=0.35)
        self.play(FadeIn(legend), FadeIn(theta_row))

        self.play(theta_tr.animate.set_value(1.2), run_time=3, rate_func=smooth)
        self.play(theta_tr.animate.set_value(0.35), run_time=3, rate_func=smooth)
        self.play(theta_tr.animate.set_value(1.0), run_time=2, rate_func=smooth)
        self.wait(1.0)
