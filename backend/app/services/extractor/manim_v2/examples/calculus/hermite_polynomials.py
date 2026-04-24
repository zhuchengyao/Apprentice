from manim import *
import numpy as np


class HermitePolynomialsExample(Scene):
    """
    Hermite polynomials H_n(x) (physicist's) satisfy
      H_{n+1}(x) = 2x H_n(x) − 2n H_{n-1}(x),  H_0 = 1, H_1 = 2x.
    Orthogonal w.r.t. weight e^(-x²):
      ∫ H_m H_n e^(-x²) dx = √π · 2^n · n! · δ_{mn}.

    TWO_COLUMN: LEFT axes with weighted polynomials H_n(x)e^(-x²/2)
    (classic QM look); ValueTracker n_tr steps 0..5 via always_redraw
    YELLOW curve + TEAL history. RIGHT shows live ⟨H_n, H_n⟩_w via
    np.trapezoid matching √π·2^n·n!.
    """

    def construct(self):
        title = Tex(r"Hermite polynomials $H_n$, weight $e^{-x^2}$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[-3.5, 3.5, 1], y_range=[-5, 5, 2],
                    x_length=5.8, y_length=4.0,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(LEFT * 2.5 + DOWN * 0.2)
        self.play(Create(axes))

        def H(n, x):
            if n == 0: return np.ones_like(np.asarray(x, dtype=float))
            if n == 1: return 2 * np.asarray(x, dtype=float)
            Hm1 = np.ones_like(np.asarray(x, dtype=float))
            Hk = 2 * np.asarray(x, dtype=float)
            for k in range(1, n):
                Hp1 = 2 * x * Hk - 2 * k * Hm1
                Hm1, Hk = Hk, Hp1
            return Hk

        n_tr = ValueTracker(0.0)

        def curve():
            n = int(round(n_tr.get_value()))
            n = max(0, min(5, n))
            return axes.plot(lambda xx: float(H(n, np.array([xx])).item()
                                              * np.exp(-xx * xx / 2)),
                             x_range=[-3.5, 3.5], color=YELLOW, stroke_width=4)

        def history():
            n = int(round(n_tr.get_value()))
            n = max(0, min(5, n))
            grp = VGroup()
            for k in range(n):
                grp.add(axes.plot(lambda xx, kk=k: float(H(kk, np.array([xx])).item()
                                                         * np.exp(-xx * xx / 2)),
                                   x_range=[-3.5, 3.5],
                                   color=interpolate_color(BLUE, TEAL, k / 5),
                                   stroke_width=1.8, stroke_opacity=0.55))
            return grp

        self.add(always_redraw(curve), always_redraw(history))

        # Norm via trapezoid with weight e^(-x^2)
        def norm_sq():
            n = max(0, min(5, int(round(n_tr.get_value()))))
            xs = np.linspace(-6, 6, 400)
            w = np.exp(-xs * xs)
            return float(np.trapezoid(H(n, xs) ** 2 * w, xs))

        def analytic():
            n = max(0, min(5, int(round(n_tr.get_value()))))
            from math import factorial
            return np.sqrt(PI) * (2 ** n) * factorial(n)

        info = VGroup(
            VGroup(Tex(r"$n=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\int H_n^2 e^{-x^2}dx=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\sqrt{\pi}\,2^n n!=$", color=GREEN, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"orthogonality w.r.t. $e^{-x^2}$",
                color=TEAL, font_size=22),
            Tex(r"appears in QM harmonic oscillator",
                color=GREY_B, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.2)
        info[0][1].add_updater(lambda m: m.set_value(
            max(0, min(5, int(round(n_tr.get_value()))))))
        info[1][1].add_updater(lambda m: m.set_value(norm_sq()))
        info[2][1].add_updater(lambda m: m.set_value(analytic()))
        self.add(info)

        for k in range(1, 6):
            self.play(n_tr.animate.set_value(float(k)),
                      run_time=1.2, rate_func=smooth)
            self.wait(0.35)
        self.wait(0.5)
