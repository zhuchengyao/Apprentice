from manim import *
import numpy as np
from math import factorial


class TaylorRemainderBoundExample(Scene):
    """
    Lagrange remainder: R_N(x) = f^(N+1)(c) · x^(N+1) / (N+1)!
    for some c between 0 and x. Bound with max of f^(N+1) gives
    explicit error estimate.

    TWO_COLUMN:
      LEFT  — axes with cos(x) and T_N(x) Taylor approximation;
              ValueTracker N_tr grows N = 2, 4, 6, 8.
      RIGHT  — live |cos(x) - T_N(x)| at x=2 vs Lagrange bound
              M · x^(N+1)/(N+1)!.
    """

    def construct(self):
        title = Tex(r"Taylor remainder: $|R_N| \le M \cdot |x|^{N+1}/(N+1)!$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ax = Axes(x_range=[-3, 3, 1], y_range=[-1.5, 1.5, 0.5],
                   x_length=7, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-2.5, -0.3, 0])
        self.play(Create(ax))

        cos_curve = ax.plot(lambda x: np.cos(x), x_range=[-3, 3, 0.02],
                              color=BLUE, stroke_width=3)
        self.play(Create(cos_curve))

        N_tr = ValueTracker(2)

        def taylor_cos(x, N):
            total = 0.0
            for k in range(N + 1):
                if k % 2 == 0:
                    sign = 1 if (k // 2) % 2 == 0 else -1
                    total += sign * x ** k / factorial(k)
            return total

        def taylor_curve():
            N = int(round(N_tr.get_value()))
            N = max(0, min(N, 12))
            return ax.plot(lambda x: min(max(taylor_cos(x, N), -1.5), 1.5),
                            x_range=[-3, 3, 0.02],
                            color=YELLOW, stroke_width=3)

        self.add(always_redraw(taylor_curve))

        # Cursor at x = 2
        x_probe = 2.0
        probe_line = DashedLine(ax.c2p(x_probe, -1.5), ax.c2p(x_probe, 1.5),
                                  color=GREY_B, stroke_width=1.5)
        self.play(Create(probe_line))

        def info():
            N = int(round(N_tr.get_value()))
            N = max(0, min(N, 12))
            actual_err = abs(np.cos(x_probe) - taylor_cos(x_probe, N))
            # Lagrange: |R_N| <= 1 * |x|^(N+1) / (N+1)! since |cos^k| <= 1
            bound = abs(x_probe) ** (N + 1) / factorial(N + 1)
            return VGroup(
                MathTex(rf"N = {N}", color=YELLOW, font_size=24),
                MathTex(rf"T_N(2) = {taylor_cos(x_probe, N):.5f}",
                         color=YELLOW, font_size=20),
                MathTex(rf"\cos 2 = {np.cos(x_probe):.5f}",
                         color=BLUE, font_size=20),
                MathTex(rf"|R_N(2)| = {actual_err:.2e}",
                         color=RED, font_size=20),
                MathTex(rf"\text{{bound}} = 2^{{{N+1}}}/{(N+1)}! = {bound:.2e}",
                         color=GREEN, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for nv in [4, 6, 8, 12]:
            self.play(N_tr.animate.set_value(nv),
                       run_time=1.5, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
