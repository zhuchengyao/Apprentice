from manim import *
import numpy as np
from math import comb


class BinomialQuizExample(Scene):
    def construct(self):
        title = Text("Binomial: probability of k correct on a 10-question quiz",
                     font_size=24).to_edge(UP)
        self.play(Write(title))

        n = 10
        p = 0.7
        ks = list(range(n + 1))
        probs = [comb(n, k) * p**k * (1 - p)**(n - k) for k in ks]

        axes = Axes(
            x_range=[0, 11, 1], y_range=[0, 0.3, 0.05],
            x_length=9, y_length=3.8,
            axis_config={"include_tip": True, "include_numbers": True},
        ).shift(0.3 * DOWN)
        xlbl = Text("k correct", font_size=20).next_to(axes, DOWN, buff=0.1)
        ylbl = MathTex("P(k)", font_size=22).next_to(axes, LEFT, buff=0.1).rotate(PI / 2)
        self.play(Create(axes), Write(xlbl), Write(ylbl))

        bars = VGroup()
        for k, pr in zip(ks, probs):
            base = axes.c2p(k, 0)
            top = axes.c2p(k, pr)
            h = abs(top[1] - base[1])
            bar = Rectangle(width=0.35, height=h, color=BLUE, fill_opacity=0.55, stroke_width=1)
            bar.move_to((np.array(base) + np.array(top)) / 2)
            bars.add(bar)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.06))

        # Highlight mode at k = np = 7
        mode_k = 7
        bars[mode_k].set_color(YELLOW).set_fill(YELLOW, opacity=0.8)
        arrow = Arrow(axes.c2p(mode_k, 0.28), axes.c2p(mode_k, probs[mode_k] + 0.01),
                      color=YELLOW, buff=0.05, stroke_width=3)
        lbl = MathTex(rf"P(7) = \binom{{10}}{{7}}(0.7)^7(0.3)^3 \approx {probs[7]:.3f}",
                      font_size=26, color=YELLOW).to_edge(DOWN)
        self.play(GrowArrow(arrow), Write(lbl))
        self.wait(0.6)
