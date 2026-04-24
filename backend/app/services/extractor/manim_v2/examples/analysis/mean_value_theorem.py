from manim import *
import numpy as np


class MeanValueTheoremExample(Scene):
    """
    Mean-value theorem: for f continuous on [a, b] and differentiable
    on (a, b), there exists c ∈ (a, b) with f'(c) = (f(b) - f(a))/(b - a).

    SINGLE_FOCUS:
      Axes with f(x) = x + sin(x) on [0.5, 6]. Secant line through
      endpoints drawn. ValueTracker c_tr sweeps c; always_redraw
      tangent at c. At the MVT point c*, tangent is parallel to secant.
    """

    def construct(self):
        title = Tex(r"MVT: $\exists\,c \in (a, b)$ with $f'(c) = \tfrac{f(b)-f(a)}{b-a}$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        def f(x):
            return x + np.sin(x)

        def df(x):
            return 1 + np.cos(x)

        ax = Axes(x_range=[0, 7, 1], y_range=[0, 8, 1],
                   x_length=8, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-1, -0.3, 0])
        self.play(Create(ax))

        curve = ax.plot(f, x_range=[0.3, 6.5], color=BLUE, stroke_width=3)
        self.play(Create(curve))

        a, b = 0.5, 6
        fa, fb = f(a), f(b)
        secant_slope = (fb - fa) / (b - a)

        # Secant (fixed)
        secant = ax.plot(lambda x: fa + secant_slope * (x - a),
                           x_range=[0, 6.8], color=ORANGE,
                           stroke_width=2.5)
        A_dot = Dot(ax.c2p(a, fa), color=ORANGE, radius=0.1)
        B_dot = Dot(ax.c2p(b, fb), color=ORANGE, radius=0.1)
        self.play(Create(secant), FadeIn(A_dot, B_dot))

        sec_lbl = MathTex(rf"\text{{secant slope}} = {secant_slope:.4f}",
                            color=ORANGE, font_size=22
                            ).next_to(ax, UP, buff=0.25).shift(RIGHT * 2.5)
        self.play(Write(sec_lbl))

        c_tr = ValueTracker(1.0)

        def tangent_at_c():
            c = c_tr.get_value()
            slope = df(c)
            y_c = f(c)
            return ax.plot(lambda x: y_c + slope * (x - c),
                            x_range=[max(0, c - 1.5), min(6.8, c + 1.5)],
                            color=GREEN, stroke_width=3)

        def c_dot():
            c = c_tr.get_value()
            return Dot(ax.c2p(c, f(c)), color=YELLOW, radius=0.12)

        def c_vertical():
            c = c_tr.get_value()
            return DashedLine(ax.c2p(c, 0), ax.c2p(c, f(c)),
                               color=GREY_B, stroke_width=1.5)

        self.add(always_redraw(c_vertical),
                  always_redraw(tangent_at_c),
                  always_redraw(c_dot))

        def info():
            c = c_tr.get_value()
            slope_c = df(c)
            diff = abs(slope_c - secant_slope)
            match = diff < 0.02
            return VGroup(
                MathTex(rf"c = {c:.3f}", color=YELLOW, font_size=22),
                MathTex(rf"f'(c) = 1 + \cos c = {slope_c:.4f}",
                         color=GREEN, font_size=22),
                MathTex(rf"|f'(c) - \text{{secant}}| = {diff:.4f}",
                         color=RED if not match else GREEN, font_size=20),
                Tex(r"match!" if match else r"keep sweeping",
                     color=GREEN if match else GREY_B, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.3).shift(DOWN * 1.5)

        self.add(always_redraw(info))

        self.play(c_tr.animate.set_value(5.5),
                   run_time=7, rate_func=linear)
        self.wait(0.4)
