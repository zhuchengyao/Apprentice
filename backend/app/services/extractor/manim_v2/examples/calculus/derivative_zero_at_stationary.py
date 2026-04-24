from manim import *
import numpy as np


class DerivativeZeroAtStationaryExample(Scene):
    """
    At t=0, s(t)=t³ has v = 3·0² = 0. The car is momentarily 'not
    moving'. But for t > 0 it moves. Paradox resolved: 'instantaneous
    velocity 0' means the rate is zero at that instant — not that
    the car stops.
    """

    def construct(self):
        title = Tex(r"Paradox: at $t=0$, $s(t)=t^3$ has $v=0$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[-1, 2, 0.5], y_range=[-1, 4, 1],
                    x_length=8, y_length=4.5,
                    axis_config={"include_numbers": True, "font_size": 16}
                    ).shift(DOWN * 0.3)
        self.play(Create(axes))
        self.add(Tex(r"$s(t)=t^3$", color=BLUE, font_size=24).next_to(axes, UP, buff=0.15))

        s_curve = axes.plot(lambda t: t ** 3, x_range=[-1, 1.7], color=BLUE, stroke_width=3)
        self.add(s_curve)

        t_tr = ValueTracker(-0.8)

        def car_dot():
            t = t_tr.get_value()
            return Dot(axes.c2p(t, t ** 3), color=RED, radius=0.13)

        def tangent_line():
            t = t_tr.get_value()
            slope = 3 * t * t
            dx = 0.5
            return Line(axes.c2p(t - dx, t ** 3 - slope * dx),
                         axes.c2p(t + dx, t ** 3 + slope * dx),
                         color=GREEN, stroke_width=3)

        self.add(always_redraw(car_dot), always_redraw(tangent_line))

        # Mark t=0 special
        zero_dot = Dot(axes.c2p(0, 0), color=YELLOW, radius=0.15)
        zero_lbl = Tex(r"at $t=0$: slope $=0$", color=YELLOW,
                        font_size=22).next_to(zero_dot, DR, buff=0.15)
        self.add(zero_dot, zero_lbl)

        # Info
        info = VGroup(
            VGroup(Tex(r"$t=$", font_size=22),
                   DecimalNumber(-0.8, num_decimal_places=2,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$v=3t^2=$", color=GREEN, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"$v=0$ at $t=0$: momentarily stationary",
                color=YELLOW, font_size=20),
            Tex(r"but car moves for $t>0$!",
                color=RED, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(t_tr.get_value()))
        info[1][1].add_updater(lambda m: m.set_value(3 * t_tr.get_value() ** 2))
        self.add(info)

        self.play(t_tr.animate.set_value(1.5), run_time=5, rate_func=linear)
        self.wait(0.8)
