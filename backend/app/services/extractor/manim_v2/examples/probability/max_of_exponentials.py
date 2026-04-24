from manim import *
import numpy as np


class MaxOfExponentialsExample(Scene):
    """
    Max of n i.i.d. Exp(λ=1) random variables:
      CDF:  F_n(x) = (1 - e^{-x})^n
      PDF:  f_n(x) = n · e^{-x} · (1 - e^{-x})^{n-1}
      E[max] = H_n ≈ ln(n) + γ

    TWO_COLUMN:
      LEFT  — axes with always_redraw PDF curve + shaded area;
              ValueTracker n_tr steps n = 1, 2, 3, 5, 10, 20, 50.
              Dashed vertical at E[max] = H_n.
      RIGHT — live n, mode, E[max] = H_n, and 90th percentile.
    """

    def construct(self):
        title = Tex(r"Max of $n$ i.i.d.\ $\mathrm{Exp}(1)$: density + mean $H_n$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ax = Axes(x_range=[0, 8, 1], y_range=[0, 1.0, 0.25],
                   x_length=7, y_length=4.5, tips=False,
                   axis_config={"font_size": 16, "include_numbers": True}
                   ).move_to([-2.6, -0.3, 0])
        xlbl = MathTex(r"x", font_size=22).next_to(ax, DOWN, buff=0.1)
        ylbl = MathTex(r"f_n(x)", font_size=22).next_to(ax, LEFT, buff=0.1)
        self.play(Create(ax), Write(xlbl), Write(ylbl))

        n_tr = ValueTracker(1.0)

        def f(x, n):
            if x < 0:
                return 0.0
            return n * np.exp(-x) * (1 - np.exp(-x)) ** (n - 1)

        def H(n):
            return float(np.sum(1.0 / np.arange(1, int(n) + 1)))

        def curve():
            n = n_tr.get_value()
            return ax.plot(lambda x: f(x, n),
                            x_range=[0.001, 8, 0.03],
                            color=BLUE, stroke_width=4)

        def mean_line():
            n = int(round(n_tr.get_value()))
            h = H(n)
            if h > 8:
                h = 8
            return DashedLine(ax.c2p(h, 0), ax.c2p(h, 0.8),
                               color=YELLOW, stroke_width=2)

        def mean_dot():
            n = int(round(n_tr.get_value()))
            h = H(n)
            if h > 8:
                h = 8
            return Dot(ax.c2p(h, f(h, n)), color=YELLOW, radius=0.1)

        self.add(always_redraw(curve),
                  always_redraw(mean_line),
                  always_redraw(mean_dot))

        def info():
            n = int(round(n_tr.get_value()))
            h = H(n)
            # mode: solve d/dx = 0 → mode ≈ ln(n) for large n
            mode = np.log(n) if n > 1 else 0
            # 90th percentile: F(q) = 0.9 ⇒ q = -ln(1 - 0.9^(1/n))
            q90 = -np.log(1 - 0.9 ** (1 / n))
            return VGroup(
                MathTex(rf"n = {n}", color=YELLOW, font_size=26),
                MathTex(rf"E[\max] = H_n = {h:.3f}",
                         color=YELLOW, font_size=22),
                MathTex(rf"\text{{mode}} \approx \ln n = {mode:.3f}",
                         color=BLUE, font_size=22),
                MathTex(rf"q_{{.9}} = {q90:.3f}",
                         color=GREEN, font_size=22),
                MathTex(r"H_n \sim \ln n + \gamma",
                         color=GREY_B, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([4.3, 0.0, 0])

        self.add(always_redraw(info))

        for n_target in [2, 3, 5, 10, 20, 50]:
            self.play(n_tr.animate.set_value(n_target),
                       run_time=1.4, rate_func=smooth)
            self.wait(0.45)
        self.wait(0.4)
