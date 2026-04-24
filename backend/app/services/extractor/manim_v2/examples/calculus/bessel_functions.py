from manim import *
import numpy as np
from scipy.special import jv


class BesselFunctionsExample(Scene):
    """
    Bessel functions J_n(x) solve x² y'' + x y' + (x² − n²) y = 0.
    J_0, J_1, J_2, J_3 plotted together — each is a damped
    oscillation with successive zeros.

    ValueTracker n_sel highlights current J_n by thickening its
    curve and updating a dashed vertical cursor x_tr sweeping across;
    live readouts of J_n(x_tr) values.
    """

    def construct(self):
        title = Tex(r"Bessel functions: $J_n$ for $n=0,1,2,3$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[0, 16, 2], y_range=[-0.6, 1.1, 0.3],
                    x_length=10, y_length=4.2,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(DOWN * 0.3)
        self.play(Create(axes))

        colors = [BLUE, GREEN, ORANGE, RED]
        curves = VGroup(*[
            axes.plot(lambda x, nn=nn: jv(nn, x),
                      x_range=[0, 16], color=colors[nn], stroke_width=2.5)
            for nn in range(4)
        ])
        self.play(Create(curves), run_time=2)

        labels = VGroup(
            Tex(r"$J_0$", color=BLUE, font_size=22),
            Tex(r"$J_1$", color=GREEN, font_size=22),
            Tex(r"$J_2$", color=ORANGE, font_size=22),
            Tex(r"$J_3$", color=RED, font_size=22),
        ).arrange(RIGHT, buff=0.5).to_edge(UP, buff=1.0)
        self.play(Write(labels))

        x_tr = ValueTracker(0.0)

        def cursor():
            x = x_tr.get_value()
            return DashedLine(axes.c2p(x, -0.6), axes.c2p(x, 1.1),
                              color=YELLOW, stroke_width=2)

        def tracking_dots():
            x = x_tr.get_value()
            grp = VGroup()
            for nn in range(4):
                grp.add(Dot(axes.c2p(x, jv(nn, x)), color=colors[nn], radius=0.08))
            return grp

        self.add(always_redraw(cursor), always_redraw(tracking_dots))

        # Live readout
        info = VGroup(
            VGroup(Tex(r"$x=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$J_0(x)=$", color=BLUE, font_size=22),
                   DecimalNumber(1.0, num_decimal_places=4,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$J_1(x)=$", color=GREEN, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=4,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$J_2(x)=$", color=ORANGE, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=4,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$J_3(x)=$", color=RED, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=4,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
            Tex(r"zeros: $j_{0,1}\approx 2.405$", color=YELLOW, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DR, buff=0.35)

        info[0][1].add_updater(lambda m: m.set_value(x_tr.get_value()))
        for i in range(4):
            info[i + 1][1].add_updater(lambda m, nn=i: m.set_value(float(jv(nn, x_tr.get_value()))))
        self.add(info)

        self.play(x_tr.animate.set_value(16),
                  run_time=8, rate_func=linear)
        self.wait(0.8)
