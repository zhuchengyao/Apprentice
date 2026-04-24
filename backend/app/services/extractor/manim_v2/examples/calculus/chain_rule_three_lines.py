from manim import *
import numpy as np


class ChainRuleThreeLinesExample(Scene):
    """
    Chain rule via 3 coupled number lines: x, g(x), f(g(x)).
    A nudge dx on the first line produces dg = g'(x)·dx on the
    second, and df = f'(g(x))·dg = f'(g(x))·g'(x)·dx on the third.
    """

    def construct(self):
        title = Tex(r"Chain rule via 3 coupled number lines",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Three lines
        x_line = NumberLine(x_range=[-3, 3, 1], length=9, include_numbers=True,
                             font_size=16).shift(UP * 1.5)
        g_line = NumberLine(x_range=[0, 12, 2], length=9, include_numbers=True,
                             font_size=16)
        f_line = NumberLine(x_range=[-1, 1.1, 0.5], length=9, include_numbers=True,
                             font_size=16).shift(DOWN * 1.5)
        self.play(Create(x_line), Create(g_line), Create(f_line))
        self.add(Tex(r"$x$", font_size=22).next_to(x_line, LEFT, buff=0.3))
        self.add(Tex(r"$g(x)=x^2+3$", color=GREEN, font_size=20).next_to(g_line, LEFT, buff=0.3))
        self.add(Tex(r"$f(g)=\sin(g)$", color=BLUE, font_size=20).next_to(f_line, LEFT, buff=0.3))

        # Concrete: x=2 so g(x)=7, f(g)=sin(7)≈0.657
        x_tr = ValueTracker(1.5)

        def g_of(x):
            return x * x + 3

        def f_of(g):
            return np.sin(g)

        def x_dot():
            x = x_tr.get_value()
            return Dot(x_line.n2p(x), color=YELLOW, radius=0.12)

        def g_dot():
            x = x_tr.get_value()
            return Dot(g_line.n2p(g_of(x)), color=GREEN, radius=0.12)

        def f_dot():
            x = x_tr.get_value()
            return Dot(f_line.n2p(f_of(g_of(x))), color=BLUE, radius=0.12)

        def arrow1():
            x = x_tr.get_value()
            return Arrow(x_line.n2p(x) + DOWN * 0.1,
                          g_line.n2p(g_of(x)) + UP * 0.1,
                          color=GREEN, buff=0.05, stroke_width=2.5)

        def arrow2():
            x = x_tr.get_value()
            return Arrow(g_line.n2p(g_of(x)) + DOWN * 0.1,
                          f_line.n2p(f_of(g_of(x))) + UP * 0.1,
                          color=BLUE, buff=0.05, stroke_width=2.5)

        self.add(always_redraw(x_dot), always_redraw(g_dot), always_redraw(f_dot),
                 always_redraw(arrow1), always_redraw(arrow2))

        info = VGroup(
            VGroup(Tex(r"$x=$", font_size=22),
                   DecimalNumber(1.5, num_decimal_places=2,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$g'(x)=2x=$", color=GREEN, font_size=22),
                   DecimalNumber(3.0, num_decimal_places=2,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$f'(g)=\cos g=$", color=BLUE, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"chain: $f'(g)\cdot g'(x)=$",
                       color=YELLOW, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.3).shift(DOWN * 3)
        info[0][1].add_updater(lambda m: m.set_value(x_tr.get_value()))
        info[1][1].add_updater(lambda m: m.set_value(2 * x_tr.get_value()))
        info[2][1].add_updater(lambda m: m.set_value(float(np.cos(g_of(x_tr.get_value())))))
        info[3][1].add_updater(lambda m: m.set_value(
            float(np.cos(g_of(x_tr.get_value())) * 2 * x_tr.get_value())))
        self.add(info)

        self.play(x_tr.animate.set_value(2.5), run_time=4, rate_func=linear)
        self.wait(0.5)
