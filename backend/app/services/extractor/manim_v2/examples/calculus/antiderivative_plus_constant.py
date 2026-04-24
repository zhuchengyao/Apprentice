from manim import *
import numpy as np


class AntiderivativePlusConstantExample(Scene):
    """
    Antiderivative is not unique: F(x) + C all have derivative f(x)
    (constant has zero derivative). Graph: 5 parallel curves
    F(x) = x²/2 + C for C = -2, -1, 0, 1, 2 all have slope x.
    """

    def construct(self):
        title = Tex(r"Antiderivatives differ by a constant $C$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[-3, 3, 1], y_range=[-4, 6, 2],
                    x_length=9, y_length=4.5,
                    axis_config={"include_numbers": True, "font_size": 16}
                    ).shift(DOWN * 0.3)
        self.play(Create(axes))

        # Tangent at any x shows slope = x (same for all curves)
        constants = [-2, -1, 0, 1, 2]
        colors = [BLUE, TEAL, GREEN, YELLOW, ORANGE]

        for C, col in zip(constants, colors):
            curve = axes.plot(lambda x, C=C: x * x / 2 + C,
                                x_range=[-2.5, 2.5], color=col, stroke_width=2.5)
            self.add(curve)
            self.add(Tex(rf"$C={C:+d}$", color=col, font_size=18).next_to(
                axes.c2p(2.5, 2.5 * 2.5 / 2 + C), RIGHT, buff=0.1))

        x_tr = ValueTracker(-2.0)

        def tangent_lines():
            x = x_tr.get_value()
            slope = x
            dx = 0.7
            grp = VGroup()
            for C, col in zip(constants, colors):
                y = x * x / 2 + C
                grp.add(Line(axes.c2p(x - dx, y - slope * dx),
                              axes.c2p(x + dx, y + slope * dx),
                              color=col, stroke_width=3))
            return grp

        def dots():
            x = x_tr.get_value()
            grp = VGroup()
            for C, col in zip(constants, colors):
                y = x * x / 2 + C
                grp.add(Dot(axes.c2p(x, y), color=col, radius=0.09))
            return grp

        self.add(always_redraw(tangent_lines), always_redraw(dots))

        info = VGroup(
            VGroup(Tex(r"$x=$", font_size=22),
                   DecimalNumber(-2.0, num_decimal_places=2,
                                 font_size=22)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"slope $=x=$", color=YELLOW, font_size=22),
                   DecimalNumber(-2.0, num_decimal_places=2,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"All 5 curves share the same slope $x$",
                color=GREEN, font_size=20),
            Tex(r"$\Rightarrow \frac{dF}{dx}=x$ for any $C$",
                color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(x_tr.get_value()))
        info[1][1].add_updater(lambda m: m.set_value(x_tr.get_value()))
        self.add(info)

        self.play(x_tr.animate.set_value(2.0), run_time=5, rate_func=linear)
        self.wait(0.5)
