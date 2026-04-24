from manim import *
import numpy as np


class StoneWeierstrassExample(Scene):
    """
    Stone-Weierstrass: polynomials are dense in C([0, 1]) under
    sup-norm. Demonstrate with approximating f(x) = |sin(πx)| on
    [0, 1] by its Chebyshev polynomial approximation T_n(x).

    TWO_COLUMN: LEFT axes with target f(x) + polynomial approximation
    P_n(x). ValueTracker n_tr steps n=1, 3, 5, 7, 9, 15; always_redraw
    Chebyshev expansion computed via np.polynomial.chebyshev.
    RIGHT shows sup-norm error → 0.
    """

    def construct(self):
        title = Tex(r"Stone-Weierstrass: polys dense in $C([0,1])$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[0, 1, 0.2], y_range=[-0.2, 1.2, 0.2],
                    x_length=6.0, y_length=4.0,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(LEFT * 2.3 + DOWN * 0.2)
        self.play(Create(axes))

        def f(x):
            return abs(np.sin(PI * x))

        ref = axes.plot(f, x_range=[0, 1], color=BLUE, stroke_width=3)
        self.play(Create(ref))

        from numpy.polynomial import chebyshev as C

        # Precompute Chebyshev coefficients for f on [0, 1]
        # Use sampling for least-squares fit in Chebyshev basis
        xs_sample = 0.5 * (1 + np.cos(np.linspace(0, PI, 60)))  # Chebyshev nodes in [0, 1]
        ys_sample = np.array([f(x) for x in xs_sample])
        # Shift to [-1, 1] for fitting
        ts_sample = 2 * xs_sample - 1

        # Cache coefficients up to degree 20
        max_deg = 20
        full_coeffs = C.chebfit(ts_sample, ys_sample, max_deg)

        n_values = [1, 3, 5, 7, 9, 15]
        n_idx_tr = ValueTracker(0.0)

        def n_now():
            idx = max(0, min(len(n_values) - 1, int(round(n_idx_tr.get_value()))))
            return n_values[idx]

        def poly_curve():
            n = n_now()
            coefs = full_coeffs.copy()
            coefs[n + 1:] = 0
            return axes.plot(lambda x: float(C.chebval(2 * x - 1, coefs)),
                             x_range=[0, 1], color=YELLOW, stroke_width=3)

        self.add(always_redraw(poly_curve))

        def sup_err():
            n = n_now()
            coefs = full_coeffs.copy()
            coefs[n + 1:] = 0
            xs = np.linspace(0, 1, 60)
            ts = 2 * xs - 1
            errs = [abs(f(x) - C.chebval(t, coefs)) for x, t in zip(xs, ts)]
            return float(max(errs))

        info = VGroup(
            Tex(r"$f(x)=|\sin(\pi x)|$", color=BLUE, font_size=22),
            VGroup(Tex(r"degree $n=$", font_size=22),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"sup-error $=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=5,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"sup-error $\to 0$ as $n\to\infty$",
                color=GREEN, font_size=20),
            Tex(r"polynomials form sub-algebra of $C([0,1])$",
                color=GREY_B, font_size=18),
            Tex(r"closed under $+, \times$, includes constants",
                color=GREY_B, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.2)
        info[1][1].add_updater(lambda m: m.set_value(n_now()))
        info[2][1].add_updater(lambda m: m.set_value(sup_err()))
        self.add(info)

        for k in range(1, len(n_values)):
            self.play(n_idx_tr.animate.set_value(float(k)),
                      run_time=1.5, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.8)
