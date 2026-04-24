from manim import *
import numpy as np


class ChernoffBoundExample(Scene):
    """
    Chernoff bound for a sum of n iid Bernoulli(p): P(S_n ≥ (1+δ)np)
    ≤ exp(-δ² np / (2 + δ)). Compare to empirical tail probability.

    TWO_COLUMN:
      LEFT  — PMF of Bin(n, p) with shaded tail region; ValueTracker
              delta_tr controls (1+δ)np threshold.
      RIGHT — live tail probability vs Chernoff bound (exponential).
    """

    def construct(self):
        title = Tex(r"Chernoff bound: $P(S_n \ge (1+\delta)np) \le e^{-\delta^2 np / (2+\delta)}$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        n = 40
        p = 0.4

        ax = Axes(x_range=[0, n + 1, 5], y_range=[0, 0.15, 0.05],
                   x_length=7, y_length=4, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-2.8, -0.3, 0])
        xl = MathTex(r"k", font_size=20).next_to(ax, DOWN, buff=0.1)
        yl = MathTex(r"P(S_n=k)", font_size=18).next_to(ax, LEFT, buff=0.1)
        self.play(Create(ax), Write(xl), Write(yl))

        from math import comb

        # Static PMF bars
        bar_w = ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]
        for k in range(n + 1):
            pr = comb(n, k) * p ** k * (1 - p) ** (n - k)
            h_scene = ax.c2p(0, pr)[1] - ax.c2p(0, 0)[1]
            if h_scene < 0.003:
                continue
            bar = Rectangle(width=bar_w * 0.9, height=h_scene,
                             color=BLUE, fill_opacity=0.35,
                             stroke_width=0.5)
            bar.move_to([ax.c2p(k, 0)[0],
                         ax.c2p(0, 0)[1] + h_scene / 2, 0])
            self.add(bar)

        delta_tr = ValueTracker(0.2)

        def threshold_bars():
            delta = delta_tr.get_value()
            threshold = int(np.ceil((1 + delta) * n * p))
            grp = VGroup()
            for k in range(threshold, n + 1):
                pr = comb(n, k) * p ** k * (1 - p) ** (n - k)
                h_scene = ax.c2p(0, pr)[1] - ax.c2p(0, 0)[1]
                if h_scene < 0.003:
                    continue
                bar = Rectangle(width=bar_w * 0.9, height=h_scene,
                                 color=RED, fill_opacity=0.75,
                                 stroke_width=0.5)
                bar.move_to([ax.c2p(k, 0)[0],
                             ax.c2p(0, 0)[1] + h_scene / 2, 0])
                grp.add(bar)
            # threshold line
            t_line = DashedLine(ax.c2p(threshold, 0),
                                  ax.c2p(threshold, 0.15),
                                  color=YELLOW, stroke_width=2)
            grp.add(t_line)
            return grp

        self.add(always_redraw(threshold_bars))

        def empirical_tail(delta):
            threshold = int(np.ceil((1 + delta) * n * p))
            return sum(comb(n, k) * p ** k * (1 - p) ** (n - k)
                        for k in range(threshold, n + 1))

        def chernoff(delta):
            return np.exp(-delta ** 2 * n * p / (2 + delta))

        def info():
            delta = delta_tr.get_value()
            th = int(np.ceil((1 + delta) * n * p))
            emp = empirical_tail(delta)
            bound = chernoff(delta)
            return VGroup(
                MathTex(rf"n = {n},\ p = {p}",
                         color=WHITE, font_size=20),
                MathTex(rf"\delta = {delta:.2f}",
                         color=YELLOW, font_size=22),
                MathTex(rf"\text{{threshold}} = (1+\delta)np = {th}",
                         color=YELLOW, font_size=20),
                MathTex(rf"P(S_n \ge {th}) = {emp:.5f}",
                         color=RED, font_size=20),
                MathTex(rf"\text{{Chernoff bound}} = {bound:.5f}",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for dv in [0.4, 0.8, 1.2, 0.2]:
            self.play(delta_tr.animate.set_value(dv),
                       run_time=1.5, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
