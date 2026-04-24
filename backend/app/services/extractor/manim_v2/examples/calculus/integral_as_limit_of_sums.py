from manim import *
import numpy as np


class IntegralAsLimitOfSumsExample(Scene):
    """
    ∫_a^b f(x) dx = limit of Riemann sums as dx → 0.

    SINGLE_FOCUS: plot f(x) = x²/2 + 1 on [0, 3]. ValueTracker n_tr
    steps through rectangle counts 4, 8, 16, 32, 64; always_redraw
    rectangles get thinner. The error (|exact - approx|) shrinks
    visibly, approaching the continuous integral.
    """

    def construct(self):
        title = Tex(r"$\int_a^b f\, dx = \lim_{n\to\infty}\sum f(x_i)\,\Delta x$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[0, 3, 0.5], y_range=[0, 6, 1],
                    x_length=7, y_length=4.2,
                    axis_config={"include_numbers": True, "font_size": 14}
                    ).shift(LEFT * 1.8 + DOWN * 0.2)
        self.play(Create(axes))

        def f(x):
            return x * x / 2 + 1

        f_curve = axes.plot(f, x_range=[0, 3], color=BLUE, stroke_width=3)
        self.add(f_curve)
        self.add(Tex(r"$f(x)=\frac{x^2}{2}+1$", color=BLUE, font_size=22).next_to(axes, UP, buff=0.1))

        # Exact integral: ∫_0^3 (x²/2 + 1) dx = 3³/6 + 3 = 4.5 + 3 = 7.5
        exact = 7.5

        n_tr = ValueTracker(4.0)

        def n_now():
            return max(4, min(64, int(round(n_tr.get_value()))))

        def rects():
            n = n_now()
            grp = VGroup()
            a_val, b_val = 0, 3
            dx = (b_val - a_val) / n
            for i in range(n):
                x_mid = a_val + (i + 0.5) * dx
                y = f(x_mid)
                rect = Rectangle(width=dx * axes.x_length / 3,
                                  height=y * axes.y_length / 6,
                                  color=GREEN, stroke_width=0.6,
                                  fill_color=GREEN, fill_opacity=0.55)
                rect.move_to(axes.c2p(x_mid, y / 2))
                grp.add(rect)
            return grp

        self.add(always_redraw(rects))

        def approx():
            n = n_now()
            dx = 3 / n
            return sum(f((i + 0.5) * dx) * dx for i in range(n))

        # Right panel
        info = VGroup(
            VGroup(Tex(r"$n=$", font_size=22),
                   DecimalNumber(4, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"Riemann sum $=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=4,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"exact $\int=$", font_size=22),
                   DecimalNumber(exact, num_decimal_places=4,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"error $=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=5,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.2)
        info[0][1].add_updater(lambda m: m.set_value(n_now()))
        info[1][1].add_updater(lambda m: m.set_value(approx()))
        info[3][1].add_updater(lambda m: m.set_value(abs(approx() - exact)))
        self.add(info)

        for n in [8, 16, 32, 64]:
            self.play(n_tr.animate.set_value(float(n)), run_time=1.3, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.5)
