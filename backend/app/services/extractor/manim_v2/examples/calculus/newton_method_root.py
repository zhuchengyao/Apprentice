from manim import *
import numpy as np


class NewtonMethodRootExample(Scene):
    """
    Newton's root-finding method: x_{n+1} = x_n - f(x_n) / f'(x_n).
    Each iteration draws a tangent at x_n and lands at the zero of
    that tangent.

    SINGLE_FOCUS:
      Axes with f(x) = x³ - 2x - 5 (Wallis's original). ValueTracker
      step_tr steps 0..6; always_redraw tangent line + iteration dot.
      Converges quadratically to the root near x = 2.0946.
    """

    def construct(self):
        title = Tex(r"Newton's method: $x_{n+1} = x_n - f(x_n)/f'(x_n)$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        def f(x):
            return x ** 3 - 2 * x - 5

        def df(x):
            return 3 * x * x - 2

        ax = Axes(x_range=[-1, 4, 1], y_range=[-10, 20, 5],
                   x_length=7, y_length=5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-2.5, -0.3, 0])
        self.play(Create(ax))

        curve = ax.plot(f, x_range=[-1, 4], color=BLUE, stroke_width=3)
        self.play(Create(curve))

        # Root marker
        root_true = 2.09455  # near this
        root_dot = Dot(ax.c2p(root_true, 0), color=RED, radius=0.1)
        self.play(FadeIn(root_dot))

        # Precompute Newton iterations from x_0 = 4
        x_vals = [4.0]
        for _ in range(6):
            x_cur = x_vals[-1]
            x_next = x_cur - f(x_cur) / df(x_cur)
            x_vals.append(x_next)

        step_tr = ValueTracker(0)

        def current_x():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, len(x_vals) - 1))
            return x_vals[s]

        def iter_dot():
            x = current_x()
            return Dot(ax.c2p(x, 0), color=YELLOW, radius=0.11)

        def curve_dot():
            x = current_x()
            return Dot(ax.c2p(x, f(x)), color=YELLOW, radius=0.11)

        def tangent_line():
            x = current_x()
            slope = df(x)
            y = f(x)
            # Line from (x - 1, y - slope) to (x + 1, y + slope), or extend to y=0
            x_to_zero = x - y / slope if abs(slope) > 1e-4 else x
            return ax.plot(lambda t: slope * (t - x) + y,
                            x_range=[min(x, x_to_zero) - 0.3,
                                       max(x, x_to_zero) + 0.3],
                            color=GREEN, stroke_width=2)

        def drop_line():
            x = current_x()
            y = f(x)
            return DashedLine(ax.c2p(x, 0), ax.c2p(x, y),
                               color=GREY_B, stroke_width=1.5)

        self.add(always_redraw(drop_line),
                  always_redraw(tangent_line),
                  always_redraw(iter_dot),
                  always_redraw(curve_dot))

        def info():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, len(x_vals) - 1))
            x = x_vals[s]
            err = abs(x - root_true)
            return VGroup(
                MathTex(rf"n = {s}", color=WHITE, font_size=22),
                MathTex(rf"x_n = {x:.6f}",
                         color=YELLOW, font_size=22),
                MathTex(rf"f(x_n) = {f(x):.6f}",
                         color=BLUE, font_size=22),
                MathTex(rf"|x_n - x^*| = {err:.2e}",
                         color=RED, font_size=22),
                Tex(r"quadratic convergence",
                     color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for s in range(1, len(x_vals)):
            self.play(step_tr.animate.set_value(s),
                       run_time=1.4, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
