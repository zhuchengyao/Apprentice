from manim import *
import numpy as np
from math import factorial


class TaylorRemainderExample(Scene):
    """
    Taylor's theorem with remainder: for f(x) = e^x around x=0,
      f(x) = Σ_{k=0}^n x^k/k! + R_n(x),
      R_n(x) = f^(n+1)(ξ) x^(n+1)/(n+1)! for some ξ ∈ (0, x).

    Bound: |R_n(x)| ≤ e^|x| · |x|^(n+1)/(n+1)!.

    TWO_COLUMN: LEFT axes show f(x)=e^x vs partial Taylor sums P_n;
    RED filled |f-P_n| error band. ValueTracker n_tr steps through
    n=1..8, morphing P_n and error band via always_redraw. RIGHT
    shows live n, sup-error on [-1.5, 1.5], and bound.
    """

    def construct(self):
        title = Tex(r"Taylor remainder for $f(x)=e^x$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[-1.5, 1.5, 0.5], y_range=[0, 5, 1],
                    x_length=6.0, y_length=4.0,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(LEFT * 2.3 + DOWN * 0.2)
        self.play(Create(axes))

        ref = axes.plot(lambda x: np.exp(x), x_range=[-1.5, 1.5],
                        color=BLUE, stroke_width=4)
        ref_lbl = Tex(r"$e^x$", color=BLUE, font_size=22).next_to(axes, UR, buff=0.1)
        self.play(Create(ref), Write(ref_lbl))

        n_tr = ValueTracker(1.0)

        def Pn(n, x):
            s = 0.0
            term = 1.0
            for k in range(n + 1):
                if k == 0:
                    s = 1.0
                    term = 1.0
                else:
                    term *= x / k
                    s += term
            return s

        def partial_curve():
            n = int(round(n_tr.get_value()))
            n = max(1, min(8, n))
            return axes.plot(lambda x: Pn(n, x), x_range=[-1.5, 1.5],
                             color=YELLOW, stroke_width=3)

        self.add(always_redraw(partial_curve))

        def error_band():
            n = int(round(n_tr.get_value()))
            n = max(1, min(8, n))
            xs = np.linspace(-1.5, 1.5, 100)
            top_pts = [axes.c2p(x, max(Pn(n, x), np.exp(x))) for x in xs]
            bot_pts = [axes.c2p(x, min(Pn(n, x), np.exp(x))) for x in xs]
            poly = Polygon(*top_pts, *reversed(bot_pts),
                           color=RED, stroke_width=0, fill_color=RED,
                           fill_opacity=0.35)
            return poly

        self.add(always_redraw(error_band))

        # Right column
        def n_now():
            return max(1, min(8, int(round(n_tr.get_value()))))

        def sup_err():
            n = n_now()
            xs = np.linspace(-1.5, 1.5, 50)
            return float(max(abs(Pn(n, x) - np.exp(x)) for x in xs))

        def bound():
            n = n_now()
            xmax = 1.5
            return np.exp(xmax) * xmax ** (n + 1) / factorial(n + 1)

        info = VGroup(
            VGroup(Tex(r"$n=$", font_size=22),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"sup $|e^x - P_n|=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=5,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"bound $\frac{e x_{\max}^{n+1}}{(n+1)!}=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=5,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"actual $\le$ bound always", color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.2)
        info[0][1].add_updater(lambda m: m.set_value(n_now()))
        info[1][1].add_updater(lambda m: m.set_value(sup_err()))
        info[2][1].add_updater(lambda m: m.set_value(bound()))
        self.add(info)

        for n_val in range(2, 9):
            self.play(n_tr.animate.set_value(float(n_val)),
                      run_time=0.8, rate_func=smooth)
            self.wait(0.3)
        self.wait(0.5)
