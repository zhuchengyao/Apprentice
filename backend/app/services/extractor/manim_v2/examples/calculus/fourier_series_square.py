from manim import *
import numpy as np


class FourierSeriesSquareExample(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-PI, PI, PI / 2], y_range=[-1.5, 1.5, 0.5],
            x_length=10, y_length=4, tips=False,
        ).to_edge(DOWN, buff=0.8)
        self.play(Create(axes))

        def partial(n_terms):
            def f(x):
                return sum(
                    4 / (PI * (2 * k + 1)) * np.sin((2 * k + 1) * x)
                    for k in range(n_terms)
                )
            return f

        colors = color_gradient([BLUE, YELLOW], 5)
        prev = axes.plot(partial(1), color=colors[0])
        self.play(Create(prev))

        for i, n in enumerate([2, 3, 5, 10]):
            nxt = axes.plot(partial(n), color=colors[i + 1])
            self.play(Transform(prev, nxt), run_time=1)

        caption = MathTex(
            r"\sum_{k=0}^{\infty}\frac{4}{\pi(2k+1)}\sin((2k+1)x)",
            font_size=32,
        ).to_edge(UP)
        self.play(Write(caption))
        self.wait(0.6)
