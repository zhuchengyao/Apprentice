from manim import *
import numpy as np


class TaylorSeriesConvergenceExample(Scene):
    """
    Taylor series of e^x around x=0: T_N(x) = Σ_{k=0}^{N} x^k / k!.
    As N grows, partial sum approximates e^x over wider intervals.

    SINGLE_FOCUS:
      Axes with y = e^x (GREY); ValueTracker N_tr steps N = 1..12;
      always_redraw BLUE T_N(x) Taylor partial sum. Wider agreement
      range as N grows.
    """

    def construct(self):
        title = Tex(r"Taylor series: $e^x \approx \sum_{k=0}^{N} x^k/k!$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ax = Axes(x_range=[-4, 4, 1], y_range=[-2, 20, 5],
                   x_length=9, y_length=5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-0.5, -0.3, 0])
        self.play(Create(ax))

        # Static e^x
        exp_curve = ax.plot(lambda x: np.exp(x),
                              x_range=[-4, 3, 0.02],
                              color=GREY_B, stroke_width=2.5)
        exp_lbl = MathTex(r"e^x", color=GREY_B,
                            font_size=22
                            ).next_to(ax.c2p(3, np.exp(3)), UR, buff=0.1)
        self.play(Create(exp_curve), Write(exp_lbl))

        N_tr = ValueTracker(1)

        from math import factorial

        def taylor(x, N):
            return sum(x ** k / factorial(k) for k in range(N + 1))

        def taylor_curve():
            N = int(round(N_tr.get_value()))
            N = max(1, min(N, 12))
            return ax.plot(lambda x: min(max(taylor(x, N), -2), 20),
                            x_range=[-4, 3, 0.02],
                            color=BLUE, stroke_width=3.5)

        self.add(always_redraw(taylor_curve))

        def info():
            N = int(round(N_tr.get_value()))
            N = max(1, min(N, 12))
            # Error at x=2
            err = abs(taylor(2, N) - np.exp(2))
            # Rough radius of convergence (infinite for exp, but show range
            # where |T - f| < 0.5)
            r_conv = 0
            for rx in np.arange(0.5, 4, 0.1):
                if abs(taylor(rx, N) - np.exp(rx)) < 0.5 * np.exp(rx):
                    r_conv = rx
                else:
                    break
            return VGroup(
                MathTex(rf"N = {N}", color=BLUE, font_size=26),
                MathTex(rf"T_N(2) = {taylor(2, N):.4f}",
                         color=BLUE, font_size=22),
                MathTex(rf"e^2 = {np.exp(2):.4f}",
                         color=GREY_B, font_size=22),
                MathTex(rf"|\text{{err at }} x=2| = {err:.4f}",
                         color=RED, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.3).shift(UP * 0.5)

        self.add(always_redraw(info))

        for target in [2, 3, 5, 8, 12]:
            self.play(N_tr.animate.set_value(target),
                       run_time=1.4, rate_func=smooth)
            self.wait(0.6)
        self.wait(0.4)
