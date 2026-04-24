from manim import *
import numpy as np
from math import factorial


class DerangementsExample(Scene):
    """
    Derangements D_n = n! Σ_{k=0}^{n} (-1)^k / k! ≈ n!/e.
    Visualize for n = 1..7 with explicit permutation counts.

    SINGLE_FOCUS:
      Bar chart of D_n alongside n! for n = 1..7. ValueTracker n_tr
      grows; always_redraw bars + ratio D_n/n! → 1/e ≈ 0.3679.
    """

    def construct(self):
        title = Tex(r"Derangements: $D_n / n! \to 1/e \approx 0.3679$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        N_MAX = 7

        def derangement(n):
            return round(n * factorial(n - 1) if n > 0 else 1) if False else \
                   round(factorial(n) * sum((-1) ** k / factorial(k) for k in range(n + 1)))

        # Precompute values
        D = {n: derangement(n) for n in range(0, N_MAX + 1)}
        Fac = {n: factorial(n) for n in range(0, N_MAX + 1)}

        ax = Axes(x_range=[0, N_MAX + 1, 1], y_range=[0, 6000, 1500],
                   x_length=7, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-2.5, -0.3, 0])
        xl = MathTex(r"n", font_size=20).next_to(ax, DOWN, buff=0.1)
        self.play(Create(ax), Write(xl))

        n_tr = ValueTracker(1)

        def bars():
            n_cur = int(round(n_tr.get_value()))
            n_cur = max(1, min(n_cur, N_MAX))
            grp = VGroup()
            for n in range(1, n_cur + 1):
                # n! bar (WHITE, thinner)
                h1 = ax.c2p(0, Fac[n])[1] - ax.c2p(0, 0)[1]
                if h1 > 0.005:
                    bar1 = Rectangle(width=0.3, height=h1,
                                       color=GREY_B, fill_opacity=0.4,
                                       stroke_width=0.5)
                    bar1.move_to([ax.c2p(n - 0.15, 0)[0],
                                  ax.c2p(0, 0)[1] + h1 / 2, 0])
                    grp.add(bar1)
                # D_n bar (BLUE)
                h2 = ax.c2p(0, D[n])[1] - ax.c2p(0, 0)[1]
                if h2 > 0.005:
                    bar2 = Rectangle(width=0.3, height=h2,
                                       color=BLUE, fill_opacity=0.7,
                                       stroke_width=0.5)
                    bar2.move_to([ax.c2p(n + 0.15, 0)[0],
                                  ax.c2p(0, 0)[1] + h2 / 2, 0])
                    grp.add(bar2)
            return grp

        self.add(always_redraw(bars))

        def info():
            n = int(round(n_tr.get_value()))
            n = max(1, min(n, N_MAX))
            ratio = D[n] / Fac[n]
            return VGroup(
                MathTex(rf"n = {n}", color=WHITE, font_size=24),
                MathTex(rf"n! = {Fac[n]}", color=GREY_B, font_size=22),
                MathTex(rf"D_n = {D[n]}", color=BLUE, font_size=22),
                MathTex(rf"D_n / n! = {ratio:.5f}",
                         color=GREEN, font_size=22),
                MathTex(rf"1/e = {1/np.e:.5f}",
                         color=YELLOW, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for nv in range(2, N_MAX + 1):
            self.play(n_tr.animate.set_value(nv),
                       run_time=0.9, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.4)
