from manim import *
import numpy as np
from math import comb


class WeierstrassApproximationExample(Scene):
    """
    Weierstrass approximation: every continuous f on [a, b] can be
    uniformly approximated by polynomials. Bernstein polynomials
    B_n(f)(x) = Σ C(n, k) x^k (1-x)^(n-k) f(k/n) give an explicit
    constructive proof on [0, 1].

    TWO_COLUMN: LEFT axes show f(x) = |x − 0.5| + 0.3·sin(6πx) (non-
    smooth reference). ValueTracker n_tr steps n=2, 5, 10, 20, 50, 200;
    always_redraw YELLOW Bernstein polynomial B_n(f). RIGHT shows
    live sup-error → 0.
    """

    def construct(self):
        title = Tex(r"Weierstrass via Bernstein: $B_n(f)(x)\to f(x)$ uniformly",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[0, 1, 0.2], y_range=[-0.1, 0.9, 0.2],
                    x_length=5.8, y_length=3.8,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(LEFT * 2.5 + DOWN * 0.2)
        self.play(Create(axes))

        def f(x):
            return abs(x - 0.5) + 0.3 * np.sin(6 * PI * x) / 2 + 0.2

        ref = axes.plot(f, x_range=[0, 1], color=BLUE, stroke_width=3)
        ref_lbl = Tex(r"$f$", color=BLUE, font_size=22).next_to(axes, UR, buff=0.1)
        self.play(Create(ref), Write(ref_lbl))

        def B_n(n, x):
            total = 0.0
            for k in range(n + 1):
                total += comb(n, k) * (x ** k) * ((1 - x) ** (n - k)) * f(k / n)
            return total

        n_values = [2, 5, 10, 20, 50, 200]
        n_idx_tr = ValueTracker(0.0)

        def n_now():
            idx = max(0, min(len(n_values) - 1, int(round(n_idx_tr.get_value()))))
            return n_values[idx]

        def bern_curve():
            n = n_now()
            return axes.plot(lambda xx: float(B_n(n, xx)),
                             x_range=[0, 1], color=YELLOW, stroke_width=3)

        self.add(always_redraw(bern_curve))

        # Sup error
        def sup_err():
            n = n_now()
            xs = np.linspace(0, 1, 60)
            return float(max(abs(B_n(n, x) - f(x)) for x in xs))

        info = VGroup(
            VGroup(Tex(r"$n=$", font_size=22),
                   DecimalNumber(2, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"sup-error $=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=4,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"$B_n(f)(x)=\sum\binom{n}{k}x^k(1-x)^{n-k}f(k/n)$",
                font_size=18),
            Tex(r"no smoothness needed",
                color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.2)
        info[0][1].add_updater(lambda m: m.set_value(n_now()))
        info[1][1].add_updater(lambda m: m.set_value(sup_err()))
        self.add(info)

        for k in range(1, len(n_values)):
            self.play(n_idx_tr.animate.set_value(float(k)),
                      run_time=1.5, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.8)
