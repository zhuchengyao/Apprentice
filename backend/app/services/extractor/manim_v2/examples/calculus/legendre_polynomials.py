from manim import *
import numpy as np


class LegendrePolynomialsExample(Scene):
    """
    Legendre polynomials P_n(x) on [-1, 1]. P_0=1, P_1=x,
    P_{n+1} = ((2n+1) x P_n − n P_{n-1}) / (n+1).

    Orthogonality: ∫_{-1}^{1} P_m P_n dx = 2/(2n+1) δ_{mn}.

    Phase 1: ValueTracker n_tr steps n=0..6 and Transform-morphs
    a YELLOW curve through P_n sequence.
    Phase 2: dot product matrix as scalar readout — P_3 · P_3 ≈ 2/7,
    P_2 · P_3 ≈ 0.
    """

    def construct(self):
        title = Tex(r"Legendre polynomials $P_n$ on $[-1,1]$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[-1.1, 1.1, 0.5], y_range=[-1.1, 1.1, 0.5],
                    x_length=5.6, y_length=4.0,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(LEFT * 2.5 + DOWN * 0.2)
        self.play(Create(axes))

        def P(n, x):
            if n == 0: return np.ones_like(x)
            if n == 1: return x
            P0 = np.ones_like(x)
            P1 = x
            for k in range(1, n):
                P_next = ((2 * k + 1) * x * P1 - k * P0) / (k + 1)
                P0, P1 = P1, P_next
            return P1

        n_tr = ValueTracker(0.0)

        def curve():
            n = int(round(n_tr.get_value()))
            n = max(0, min(6, n))
            return axes.plot(lambda xx: P(n, np.array([xx])).item(),
                             x_range=[-1, 1], color=YELLOW, stroke_width=4)

        self.add(always_redraw(curve))

        # Fading "history" curves of lower n
        def history():
            n = int(round(n_tr.get_value()))
            n = max(0, min(6, n))
            grp = VGroup()
            for k in range(n):
                grp.add(axes.plot(lambda xx, kk=k: P(kk, np.array([xx])).item(),
                                   x_range=[-1, 1],
                                   color=interpolate_color(BLUE, TEAL, k / 6),
                                   stroke_width=1.8, stroke_opacity=0.55))
            return grp

        self.add(always_redraw(history))

        # Right column
        def dotted(m_idx, n_idx):
            xs = np.linspace(-1, 1, 200)
            return float(np.trapezoid(P(m_idx, xs) * P(n_idx, xs), xs))

        def n_now():
            return max(0, min(6, int(round(n_tr.get_value()))))

        info = VGroup(
            VGroup(Tex(r"$n=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\langle P_n,P_n\rangle=$", font_size=22),
                   DecimalNumber(2.0, num_decimal_places=4,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$2/(2n+1)=$", color=GREEN, font_size=22),
                   DecimalNumber(2.0, num_decimal_places=4,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"$P_n\perp P_m$ for $m\neq n$", color=BLUE, font_size=22),
            Tex(r"recurrence:", color=TEAL, font_size=20),
            Tex(r"$P_{n+1}=\tfrac{(2n+1)xP_n-nP_{n-1}}{n+1}$",
                color=TEAL, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.2)

        info[0][1].add_updater(lambda m: m.set_value(n_now()))
        info[1][1].add_updater(lambda m: m.set_value(dotted(n_now(), n_now())))
        info[2][1].add_updater(lambda m: m.set_value(2 / (2 * n_now() + 1)))
        self.add(info)

        for n in range(1, 7):
            self.play(n_tr.animate.set_value(float(n)),
                      run_time=1.2, rate_func=smooth)
            self.wait(0.3)
        self.wait(0.8)
