from manim import *
import numpy as np


class FatouLemmaDemoExample(Scene):
    """
    Fatou's lemma: for f_n ≥ 0,
       ∫ liminf f_n  ≤  liminf ∫ f_n.
    Classic example where strict inequality holds:
       f_n(x) = n · 1_{[0, 1/n]}.  ∫f_n = 1 ∀ n, but f_n → 0
    pointwise so liminf f_n = 0 ⇒ 0 < 1.

    TWO_COLUMN: LEFT axes show f_n as tall skinny rectangle that
    gets taller/thinner with ValueTracker n_tr ∈ {1, 2, 5, 10, 25, 100}.
    RIGHT compares the integral (constant 1) vs liminf-limit (0).
    """

    def construct(self):
        title = Tex(r"Fatou's lemma: $\int \liminf f_n\le \liminf\int f_n$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[0, 1.1, 0.2], y_range=[0, 12, 2],
                    x_length=6.0, y_length=4.0,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(LEFT * 2.3 + DOWN * 0.3)
        self.play(Create(axes))

        n_values = [1, 2, 5, 10, 25, 100]
        n_idx_tr = ValueTracker(0.0)

        def n_now():
            idx = max(0, min(len(n_values) - 1, int(round(n_idx_tr.get_value()))))
            return n_values[idx]

        def bar():
            n = n_now()
            h = min(n, 12)
            w = 1.0 / n
            rect = Rectangle(width=w * axes.x_length,
                             height=h * axes.y_length / 12,
                             color=YELLOW, stroke_width=2,
                             fill_color=YELLOW, fill_opacity=0.55)
            rect.move_to(axes.c2p(w / 2, h / 2))
            return rect

        def pointwise_limit():
            # f_n → 0 pointwise
            return axes.plot(lambda x: 0.0, x_range=[0, 1],
                             color=BLUE, stroke_width=4)

        self.add(always_redraw(bar))
        self.add(pointwise_limit())

        # Info
        info = VGroup(
            VGroup(Tex(r"$n=$", font_size=22),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\int f_n=$", font_size=22),
                   DecimalNumber(1.0, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\liminf f_n(x)=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=1,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            Tex(r"$\int\liminf f_n =0$", color=BLUE, font_size=22),
            Tex(r"$\liminf\int f_n=1$", color=YELLOW, font_size=22),
            Tex(r"strict: $0<1$", color=RED, font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.2)
        info[0][1].add_updater(lambda m: m.set_value(n_now()))
        self.add(info)

        for k in range(1, len(n_values)):
            self.play(n_idx_tr.animate.set_value(float(k)),
                      run_time=1.4, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.8)
