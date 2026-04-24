from manim import *
import numpy as np


class DarbouxIntegrabilityExample(Scene):
    """
    A function f is Darboux integrable on [a, b] iff for every ε > 0
    there exists a partition P with U(P, f) − L(P, f) < ε.

    Take f(x) = x² on [0, 1]. Upper and lower sums converge as n → ∞.

    TWO_COLUMN: LEFT axes with f(x)=x² + upper step (BLUE) and lower
    step (GREEN) rectangles. ValueTracker n_tr sweeps 2→32. RIGHT
    shows U(P, f), L(P, f), gap → 0.
    """

    def construct(self):
        title = Tex(r"Darboux integrability: $U(P,f)-L(P,f)\to 0$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[0, 1.1, 0.2], y_range=[0, 1.1, 0.2],
                    x_length=5.5, y_length=4.0,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(LEFT * 2.7 + DOWN * 0.3)
        self.play(Create(axes))

        f_curve = axes.plot(lambda x: x * x, x_range=[0, 1],
                             color=RED, stroke_width=3)
        self.play(Create(f_curve))

        n_tr = ValueTracker(2.0)

        def n_now():
            return max(2, min(32, int(round(n_tr.get_value()))))

        def upper_rects():
            n = n_now()
            w = 1.0 / n
            grp = VGroup()
            for k in range(n):
                x0 = k * w
                x1 = (k + 1) * w
                h = x1 * x1  # increasing so max at right end
                rect = Rectangle(width=w * axes.x_length / 1.0,
                                 height=h * axes.y_length / 1.0,
                                 color=BLUE, stroke_width=1,
                                 fill_color=BLUE, fill_opacity=0.3)
                rect.move_to(axes.c2p((x0 + x1) / 2, h / 2))
                grp.add(rect)
            return grp

        def lower_rects():
            n = n_now()
            w = 1.0 / n
            grp = VGroup()
            for k in range(n):
                x0 = k * w
                x1 = (k + 1) * w
                h = x0 * x0  # min at left end for x²
                rect = Rectangle(width=w * axes.x_length / 1.0,
                                 height=h * axes.y_length / 1.0,
                                 color=GREEN, stroke_width=1,
                                 fill_color=GREEN, fill_opacity=0.6)
                rect.move_to(axes.c2p((x0 + x1) / 2, h / 2))
                grp.add(rect)
            return grp

        self.add(always_redraw(upper_rects), always_redraw(lower_rects))

        # Info
        def U_of():
            n = n_now()
            w = 1.0 / n
            return sum(((k + 1) * w) ** 2 * w for k in range(n))

        def L_of():
            n = n_now()
            w = 1.0 / n
            return sum((k * w) ** 2 * w for k in range(n))

        info = VGroup(
            VGroup(Tex(r"$n=$", font_size=22),
                   DecimalNumber(2, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$U(P,f)=$", color=BLUE, font_size=22),
                   DecimalNumber(0.625, num_decimal_places=5,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$L(P,f)=$", color=GREEN, font_size=22),
                   DecimalNumber(0.125, num_decimal_places=5,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$U-L=$", color=RED, font_size=22),
                   DecimalNumber(0.5, num_decimal_places=5,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
            Tex(r"$\int_0^1 x^2\,dx=1/3\approx 0.333$",
                color=YELLOW, font_size=22),
            Tex(r"$U-L=1/n\to 0$ (Darboux)",
                color=YELLOW, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.2)
        info[0][1].add_updater(lambda m: m.set_value(n_now()))
        info[1][1].add_updater(lambda m: m.set_value(U_of()))
        info[2][1].add_updater(lambda m: m.set_value(L_of()))
        info[3][1].add_updater(lambda m: m.set_value(U_of() - L_of()))
        self.add(info)

        for target in [4, 8, 16, 32]:
            self.play(n_tr.animate.set_value(float(target)),
                      run_time=1.5, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.5)
