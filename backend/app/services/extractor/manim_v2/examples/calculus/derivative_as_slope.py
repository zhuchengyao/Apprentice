from manim import *
import numpy as np


class DerivativeAsSlopeExample(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-0.5, 3.5, 1], y_range=[-0.5, 6, 1],
            x_length=8, y_length=4.5, tips=False,
        ).to_edge(DOWN, buff=0.6)
        labels = axes.get_axis_labels("x", "y")

        def f(x): return 0.5 * x ** 2 + 0.3
        graph = axes.plot(f, color=BLUE)
        self.play(Create(axes), Write(labels))
        self.play(Create(graph))

        x0 = 1.5
        h = ValueTracker(1.3)

        p0 = always_redraw(lambda: Dot(axes.c2p(x0, f(x0)), color=YELLOW))
        p1 = always_redraw(lambda: Dot(axes.c2p(x0 + h.get_value(), f(x0 + h.get_value())), color=GREEN))

        secant = always_redraw(lambda: axes.plot(
            lambda x: (
                f(x0) + (f(x0 + h.get_value()) - f(x0)) / h.get_value() * (x - x0)
            ),
            x_range=[max(x0 - 1.5, -0.5), min(x0 + h.get_value() + 1.0, 3.4)],
            color=RED,
        ))
        caption = always_redraw(lambda: MathTex(
            rf"h = {h.get_value():.2f}", font_size=32,
        ).to_corner(UL).add_background_rectangle())

        self.add(p0, p1, secant, caption)
        self.play(h.animate.set_value(0.05), run_time=3)
        self.wait(0.5)
