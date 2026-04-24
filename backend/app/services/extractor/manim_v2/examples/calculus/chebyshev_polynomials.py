from manim import *
import numpy as np


class ChebyshevPolynomialsExample(Scene):
    """
    Chebyshev polynomials T_n(cos θ) = cos(nθ). Recurrence
    T_{n+1}(x) = 2x T_n(x) − T_{n-1}(x), T_0=1, T_1=x. Orthogonal
    on [-1, 1] with weight 1/√(1−x²).

    TWO_COLUMN: LEFT axes with T_0..T_6 (ValueTracker n_tr);
    always_redraw YELLOW T_n + TEAL fading lower orders.
    RIGHT: minimax property — T_n has smallest sup |T|=1 on [-1, 1]
    among monic poly (after rescaling); live n + max values.
    """

    def construct(self):
        title = Tex(r"Chebyshev: $T_n(\cos\theta)=\cos(n\theta)$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[-1.1, 1.1, 0.5], y_range=[-1.2, 1.2, 0.5],
                    x_length=5.8, y_length=4.0,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(LEFT * 2.5 + DOWN * 0.2)
        self.play(Create(axes))

        def T(n, x):
            xa = np.asarray(x, dtype=float)
            if n == 0: return np.ones_like(xa)
            if n == 1: return xa
            Tm1 = np.ones_like(xa)
            Tk = xa
            for k in range(1, n):
                Tp1 = 2 * xa * Tk - Tm1
                Tm1, Tk = Tk, Tp1
            return Tk

        n_tr = ValueTracker(0.0)

        def curve():
            n = int(round(n_tr.get_value()))
            n = max(0, min(6, n))
            return axes.plot(lambda xx: float(T(n, xx)),
                             x_range=[-1, 1], color=YELLOW, stroke_width=4)

        def history():
            n = int(round(n_tr.get_value()))
            n = max(0, min(6, n))
            grp = VGroup()
            for k in range(n):
                grp.add(axes.plot(lambda xx, kk=k: float(T(kk, xx)),
                                   x_range=[-1, 1],
                                   color=interpolate_color(BLUE, TEAL, k / 6),
                                   stroke_width=1.8, stroke_opacity=0.55))
            return grp

        self.add(always_redraw(curve), always_redraw(history))

        # Extrema points for current T_n
        def extrema_dots():
            n = int(round(n_tr.get_value()))
            n = max(0, min(6, n))
            if n == 0:
                return VGroup()
            grp = VGroup()
            for k in range(n + 1):
                x = np.cos(k * PI / n)
                y = (-1) ** k
                grp.add(Dot(axes.c2p(x, y), color=RED, radius=0.08))
            return grp

        self.add(always_redraw(extrema_dots))

        def n_now():
            return max(0, min(6, int(round(n_tr.get_value()))))

        info = VGroup(
            VGroup(Tex(r"$n=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"$T_n$ oscillates between $\pm 1$",
                color=YELLOW, font_size=22),
            VGroup(Tex(r"extrema count $=n+1=$", color=RED, font_size=22),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
            Tex(r"minimax property on $[-1,1]$",
                color=GREEN, font_size=20),
            Tex(r"roots: $x_k=\cos\frac{(2k-1)\pi}{2n}$",
                color=GREY_B, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.2)
        info[0][1].add_updater(lambda m: m.set_value(n_now()))
        info[2][1].add_updater(lambda m: m.set_value(n_now() + 1))
        self.add(info)

        for k in range(1, 7):
            self.play(n_tr.animate.set_value(float(k)),
                      run_time=1.1, rate_func=smooth)
            self.wait(0.3)
        self.wait(0.5)
