from manim import *
import numpy as np


class SumRuleDerivativeExample(Scene):
    """
    Sum rule: (f + g)' = f' + g'. Graph f, g, and f+g. Their
    slopes at each point add.
    """

    def construct(self):
        title = Tex(r"Sum rule: $(f+g)'=f'+g'$",
                    font_size=30).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[-1, 5, 1], y_range=[-3, 6, 2],
                    x_length=9, y_length=4.5,
                    axis_config={"include_numbers": True, "font_size": 16}
                    ).shift(DOWN * 0.3)
        self.play(Create(axes))

        def f(x):
            return 0.5 * x * x - 1
        def g(x):
            return np.sin(x) + 0.5 * x

        f_curve = axes.plot(f, x_range=[0, 4], color=BLUE, stroke_width=3)
        g_curve = axes.plot(g, x_range=[0, 4], color=GREEN, stroke_width=3)
        sum_curve = axes.plot(lambda x: f(x) + g(x), x_range=[0, 4], color=YELLOW, stroke_width=3)
        self.add(f_curve, g_curve, sum_curve)

        self.add(Tex(r"$f$", color=BLUE, font_size=22).next_to(axes.c2p(4, f(4)), RIGHT, buff=0.05))
        self.add(Tex(r"$g$", color=GREEN, font_size=22).next_to(axes.c2p(4, g(4)), RIGHT, buff=0.05))
        self.add(Tex(r"$f+g$", color=YELLOW, font_size=22).next_to(axes.c2p(4, f(4) + g(4)), RIGHT, buff=0.05))

        x_tr = ValueTracker(0.5)

        def tangent_line_for(func, col, offset=0):
            def builder():
                x = x_tr.get_value()
                eps = 1e-3
                slope = (func(x + eps) - func(x - eps)) / (2 * eps)
                dx = 0.6
                return Line(axes.c2p(x - dx, func(x) - slope * dx),
                             axes.c2p(x + dx, func(x) + slope * dx),
                             color=col, stroke_width=3)
            return builder

        self.add(always_redraw(tangent_line_for(f, BLUE)))
        self.add(always_redraw(tangent_line_for(g, GREEN)))
        self.add(always_redraw(tangent_line_for(lambda x: f(x) + g(x), YELLOW)))

        # Dots
        def make_dot(func, col):
            def builder():
                x = x_tr.get_value()
                return Dot(axes.c2p(x, func(x)), color=col, radius=0.1)
            return builder
        self.add(always_redraw(make_dot(f, BLUE)),
                 always_redraw(make_dot(g, GREEN)),
                 always_redraw(make_dot(lambda x: f(x) + g(x), YELLOW)))

        def slope_of(func):
            x = x_tr.get_value()
            eps = 1e-3
            return (func(x + eps) - func(x - eps)) / (2 * eps)

        info = VGroup(
            VGroup(Tex(r"$x=$", font_size=22),
                   DecimalNumber(0.5, num_decimal_places=2,
                                 font_size=22)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$f'(x)=$", color=BLUE, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$g'(x)=$", color=GREEN, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$f'+g'=$", color=YELLOW, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(x_tr.get_value()))
        info[1][1].add_updater(lambda m: m.set_value(slope_of(f)))
        info[2][1].add_updater(lambda m: m.set_value(slope_of(g)))
        info[3][1].add_updater(lambda m: m.set_value(slope_of(lambda x: f(x) + g(x))))
        self.add(info)

        self.play(x_tr.animate.set_value(3.8), run_time=5, rate_func=linear)
        self.wait(0.5)
