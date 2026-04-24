from manim import *
import numpy as np


class ComposeSinXSquaredExample(Scene):
    """
    Composition sin(x²): graph oscillates faster as x grows.
    Applies chain rule: d/dx sin(x²) = cos(x²) · 2x.
    """

    def construct(self):
        title = Tex(r"$\sin(x^2)$: composition $\Rightarrow$ chain rule",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[0, 3.5, 0.5], y_range=[-1.2, 1.2, 0.5],
                    x_length=9, y_length=4,
                    axis_config={"include_numbers": True, "font_size": 14}
                    ).shift(DOWN * 0.3)
        self.play(Create(axes))

        def h(x):
            return np.sin(x * x)

        def h_prime(x):
            return np.cos(x * x) * 2 * x

        # Plot h
        h_curve = axes.plot(h, x_range=[0, 3.4], color=BLUE, stroke_width=3)
        self.add(h_curve)
        self.add(Tex(r"$h(x)=\sin(x^2)$", color=BLUE, font_size=22).next_to(axes, UP, buff=0.1))

        x_tr = ValueTracker(0.5)

        def h_dot():
            x = x_tr.get_value()
            return Dot(axes.c2p(x, h(x)), color=YELLOW, radius=0.11)

        def tangent():
            x = x_tr.get_value()
            slope = h_prime(x)
            dx = 0.25
            return Line(axes.c2p(x - dx, h(x) - slope * dx),
                         axes.c2p(x + dx, h(x) + slope * dx),
                         color=GREEN, stroke_width=3)

        self.add(always_redraw(h_dot), always_redraw(tangent))

        info = VGroup(
            VGroup(Tex(r"$x=$", font_size=22),
                   DecimalNumber(0.5, num_decimal_places=2,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$h(x)=\sin(x^2)=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$h'(x)=\cos(x^2)\cdot 2x=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"chain rule: derivative of outer $\times$ inner",
                color=YELLOW, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(x_tr.get_value()))
        info[1][1].add_updater(lambda m: m.set_value(h(x_tr.get_value())))
        info[2][1].add_updater(lambda m: m.set_value(h_prime(x_tr.get_value())))
        self.add(info)

        self.play(x_tr.animate.set_value(3.3), run_time=6, rate_func=linear)
        self.wait(0.5)
