from manim import *
import numpy as np


class NaturalLogInverseExpExample(Scene):
    """
    Natural log ln(x) is the inverse of e^x: ln(e^x) = x.
    Graphs: y = e^x reflected over y=x gives y = ln x.
    Derivative: d(ln x)/dx = 1/x.
    """

    def construct(self):
        title = Tex(r"$\ln x$ inverts $e^x$; $\frac{d\ln x}{dx}=\frac{1}{x}$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[-0.5, 5, 1], y_range=[-3, 5, 1],
                    x_length=9, y_length=5,
                    axis_config={"include_numbers": True, "font_size": 16}
                    ).shift(DOWN * 0.2)
        self.play(Create(axes))

        # e^x
        exp_curve = axes.plot(lambda x: np.exp(x), x_range=[-0.5, 1.6],
                               color=RED, stroke_width=3)
        exp_lbl = Tex(r"$e^x$", color=RED, font_size=22).next_to(axes.c2p(1.6, np.exp(1.6)), UP, buff=0.1)
        self.add(exp_curve, exp_lbl)

        # y = x
        id_line = axes.plot(lambda x: x, x_range=[-0.5, 5], color=GREY_B,
                             stroke_width=1.5, stroke_opacity=0.6)
        self.add(id_line)
        self.add(Tex(r"$y=x$", color=GREY_B, font_size=20).move_to(axes.c2p(4.5, 4.0)))

        # ln x (reflection over y=x)
        ln_curve = axes.plot(lambda x: np.log(x), x_range=[0.05, 5],
                              color=GREEN, stroke_width=3)
        ln_lbl = Tex(r"$\ln x$", color=GREEN, font_size=22).next_to(axes.c2p(4.5, np.log(4.5)), UP, buff=0.1)
        self.add(ln_curve, ln_lbl)

        x_tr = ValueTracker(1.0)

        def ln_dot():
            x = x_tr.get_value()
            return Dot(axes.c2p(x, np.log(x)), color=YELLOW, radius=0.11)

        def tangent():
            x = x_tr.get_value()
            slope = 1 / x
            dx = 0.7
            return Line(axes.c2p(x - dx, np.log(x) - slope * dx),
                         axes.c2p(x + dx, np.log(x) + slope * dx),
                         color=ORANGE, stroke_width=3)

        self.add(always_redraw(ln_dot), always_redraw(tangent))

        info = VGroup(
            VGroup(Tex(r"$x=$", font_size=22),
                   DecimalNumber(1.0, num_decimal_places=2,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\ln x=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"slope $=1/x=$", color=ORANGE, font_size=22),
                   DecimalNumber(1.0, num_decimal_places=3,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(x_tr.get_value()))
        info[1][1].add_updater(lambda m: m.set_value(np.log(max(0.01, x_tr.get_value()))))
        info[2][1].add_updater(lambda m: m.set_value(1 / max(0.01, x_tr.get_value())))
        self.add(info)

        self.play(x_tr.animate.set_value(4.5), run_time=5, rate_func=linear)
        self.wait(0.5)
