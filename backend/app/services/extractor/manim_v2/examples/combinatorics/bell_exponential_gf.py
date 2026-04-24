from manim import *
import numpy as np
from math import factorial


class BellExponentialGFExample(Scene):
    """
    Bell numbers B_n have exponential generating function
    Σ B_n x^n / n! = exp(e^x - 1). Partial sums of the left side
    approach exp(e^x - 1).

    SINGLE_FOCUS:
      Axes with GREY true curve g(x) = exp(e^x - 1); BLUE partial
      sum with first N Bell numbers. ValueTracker N_tr grows terms.
    """

    def construct(self):
        title = Tex(r"Bell numbers: $\sum_{n \ge 0} B_n\,\tfrac{x^n}{n!} = e^{e^x - 1}$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Bell numbers
        def bell(n):
            if n == 0:
                return 1
            row = [1]
            for _ in range(n):
                new_row = [row[-1]]
                for v in row:
                    new_row.append(new_row[-1] + v)
                row = new_row
            return row[0]

        B = [bell(n) for n in range(12)]

        ax = Axes(x_range=[-1, 2, 0.5], y_range=[0, 8, 1],
                   x_length=8, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-1, -0.3, 0])
        xl = MathTex(r"x", font_size=20).next_to(ax, DOWN, buff=0.1)
        self.play(Create(ax), Write(xl))

        # True EGF: exp(e^x - 1)
        true_curve = ax.plot(lambda x: np.exp(np.exp(x) - 1),
                               x_range=[-1, 2, 0.02],
                               color=GREY_B, stroke_width=2.5)
        true_lbl = MathTex(r"e^{e^x - 1}",
                             color=GREY_B, font_size=20
                             ).move_to(ax.c2p(2.0, 6) + np.array([0.2, 0.1, 0]))
        self.play(Create(true_curve), Write(true_lbl))

        N_tr = ValueTracker(1)

        def partial_sum(x, N):
            return sum(B[n] * x ** n / factorial(n) for n in range(N + 1))

        def partial_curve():
            N = int(round(N_tr.get_value()))
            N = max(0, min(N, 11))
            return ax.plot(lambda x: min(partial_sum(x, N), 8),
                            x_range=[-1, 2, 0.02],
                            color=BLUE, stroke_width=3.5)

        self.add(always_redraw(partial_curve))

        def info():
            N = int(round(N_tr.get_value()))
            N = max(0, min(N, 11))
            val = partial_sum(1.0, N)
            true_val = np.exp(np.exp(1) - 1)
            return VGroup(
                MathTex(rf"N = {N}", color=BLUE, font_size=24),
                MathTex(rf"S_N(1) = \sum_{{n=0}}^{N} B_n/n! = {val:.5f}",
                         color=BLUE, font_size=20),
                MathTex(rf"e^{{e - 1}} = {true_val:.5f}",
                         color=GREY_B, font_size=20),
                MathTex(rf"B_0..B_{N}: " + ", ".join(str(B[k]) for k in range(min(N + 1, 8))) + (r"\ldots" if N >= 8 else ""),
                         color=YELLOW, font_size=16),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for nv in [2, 4, 6, 8, 11]:
            self.play(N_tr.animate.set_value(nv),
                       run_time=1.4, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
