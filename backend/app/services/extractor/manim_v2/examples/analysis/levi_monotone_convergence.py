from manim import *
import numpy as np


class LeviMonotoneConvergenceExample(Scene):
    """
    Monotone convergence theorem: if f_n ↑ f pointwise and f_n ≥ 0,
    then ∫ f_n ↑ ∫ f.

    Example: f_n(x) = (1 - 1/n)·x² on [0, 1]. Integrals:
    ∫f_n = (1 - 1/n)/3 ↑ 1/3.

    TWO_COLUMN: LEFT axes with f curve + f_n with shaded integral.
    ValueTracker n_tr sweeps 2→50. RIGHT live ∫f_n vs 1/3.
    """

    def construct(self):
        title = Tex(r"Monotone convergence: $f_n\uparrow f\Rightarrow \int f_n\uparrow \int f$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[0, 1.1, 0.2], y_range=[0, 1.1, 0.2],
                    x_length=6.0, y_length=4.0,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(LEFT * 2.3 + DOWN * 0.2)
        self.play(Create(axes))

        f_curve = axes.plot(lambda x: x * x, x_range=[0, 1],
                             color=BLUE, stroke_width=3)
        self.add(f_curve)
        self.add(Tex(r"$f(x)=x^2$", color=BLUE, font_size=22).next_to(
            axes, UR, buff=0.1))

        n_tr = ValueTracker(2.0)

        def n_now():
            return max(2, min(50, int(round(n_tr.get_value()))))

        def fn_curve():
            n = n_now()
            scale = 1 - 1 / n
            return axes.plot(lambda x: scale * x * x, x_range=[0, 1],
                             color=YELLOW, stroke_width=3)

        def shaded_region():
            n = n_now()
            scale = 1 - 1 / n
            xs = np.linspace(0, 1, 40)
            top = [axes.c2p(x, scale * x * x) for x in xs]
            bot = [axes.c2p(x, 0) for x in xs]
            return Polygon(*top, *reversed(bot),
                            color=YELLOW, stroke_width=0,
                            fill_color=YELLOW, fill_opacity=0.45)

        self.add(always_redraw(shaded_region), always_redraw(fn_curve))

        def int_fn():
            n = n_now()
            return (1 - 1 / n) / 3

        info = VGroup(
            VGroup(Tex(r"$n=$", font_size=22),
                   DecimalNumber(2, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$f_n(x)=(1-1/n)x^2$", color=YELLOW, font_size=20),
                    ).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\int f_n=$", font_size=22),
                   DecimalNumber(1 / 6, num_decimal_places=5,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\int f=1/3\approx$", color=BLUE, font_size=22),
                   DecimalNumber(1 / 3, num_decimal_places=5,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            Tex(r"$f_n$ increases to $f$ pointwise",
                color=YELLOW, font_size=20),
            Tex(r"integrals increase monotonically to $\int f$",
                color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.2)
        info[0][1].add_updater(lambda m: m.set_value(n_now()))
        info[2][1].add_updater(lambda m: m.set_value(int_fn()))
        self.add(info)

        self.play(n_tr.animate.set_value(50.0),
                  run_time=6, rate_func=linear)
        self.wait(0.8)
