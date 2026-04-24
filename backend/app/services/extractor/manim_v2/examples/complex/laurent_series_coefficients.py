from manim import *
import numpy as np


class LaurentSeriesCoefficientsExample(Scene):
    """
    Laurent series of f(z) = e^(1/z) at z=0:
       e^(1/z) = Σ_{k=0}^∞ z^(-k)/k!
    All coefficients of positive powers are zero; negative-power
    coefficients are 1/k!.

    Compare to f(z) = 1/(z(z-1)) with Laurent expansion around 0:
       1/(z(z-1)) = -1/z · 1/(1-z) = -1/z - 1 - z - z² - ...

    TWO_COLUMN: LEFT bar chart of Laurent coefficients indexed k=-5..5.
    Two configs toggled via ValueTracker. RIGHT annotations explain
    each expansion; live k-th coefficient.
    """

    def construct(self):
        title = Tex(r"Laurent series: $\sum_{k=-\infty}^{\infty} a_k z^k$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ks = list(range(-5, 6))
        n = len(ks)

        # Coefficients
        def coeffs_exp():
            from math import factorial
            c = np.zeros(n)
            for i, k in enumerate(ks):
                if k <= 0:
                    c[i] = 1.0 / factorial(-k)
                else:
                    c[i] = 0.0
            return c

        def coeffs_rat():
            c = np.zeros(n)
            for i, k in enumerate(ks):
                if k == -1:
                    c[i] = -1.0
                elif k >= 0:
                    c[i] = -1.0
                else:
                    c[i] = 0.0
            return c

        axes = Axes(x_range=[-5.5, 5.5, 1], y_range=[-1.2, 1.2, 0.5],
                    x_length=7.0, y_length=3.6,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(LEFT * 1.5 + DOWN * 0.2)
        self.play(Create(axes))

        s_tr = ValueTracker(0.0)

        def bars():
            s = s_tr.get_value()
            c1 = coeffs_exp()
            c2 = coeffs_rat()
            c = (1 - s) * c1 + s * c2
            grp = VGroup()
            for i, k in enumerate(ks):
                h = c[i]
                col = BLUE if k < 0 else (GREEN if k > 0 else RED)
                rect = Rectangle(width=0.4,
                                 height=abs(h) * axes.y_length / 2.4,
                                 color=col, fill_color=col,
                                 fill_opacity=0.7,
                                 stroke_width=1)
                rect.move_to(axes.c2p(k, h / 2))
                grp.add(rect)
            return grp

        self.add(always_redraw(bars))

        # Labels for the two regimes
        def title_str():
            s = s_tr.get_value()
            if s < 0.5:
                return r"$f(z)=e^{1/z}$: essential singularity"
            return r"$f(z)=\dfrac{1}{z(z-1)}$: pole at 0"

        current_title = Tex(title_str(), font_size=26, color=YELLOW).to_edge(DOWN, buff=0.4)
        self.add(current_title)

        def update_ct(mob, dt):
            new = Tex(title_str(), font_size=26, color=YELLOW).move_to(current_title)
            current_title.become(new)
            return current_title
        current_title.add_updater(update_ct)

        # Info
        info = VGroup(
            VGroup(Tex(r"morph $s=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"BLUE: $k<0$ (principal part)",
                color=BLUE, font_size=20),
            Tex(r"RED: $k=0$ constant term",
                color=RED, font_size=20),
            Tex(r"GREEN: $k>0$ regular part",
                color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(s_tr.get_value()))
        self.add(info)

        self.play(s_tr.animate.set_value(1.0),
                  run_time=3, rate_func=smooth)
        self.wait(0.8)
        self.play(s_tr.animate.set_value(0.0),
                  run_time=2.5, rate_func=smooth)
        self.wait(0.5)
