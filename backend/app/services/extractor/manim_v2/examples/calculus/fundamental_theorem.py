from manim import *
import numpy as np


class FundamentalTheoremExample(Scene):
    def construct(self):
        title = Text(
            "Fundamental theorem: derivative of area = height",
            font_size=26,
        ).to_edge(UP)
        self.play(Write(title))

        axes = Axes(
            x_range=[0, 4, 1], y_range=[0, 3, 1],
            x_length=8, y_length=3.5, tips=False,
        ).to_edge(DOWN, buff=0.6)
        def f(x): return 0.4 * x + 0.5
        graph = axes.plot(f, color=BLUE)
        lbl = MathTex("f(x)", color=BLUE).next_to(axes.c2p(3.8, f(3.8)), UR, buff=0.1)
        self.play(Create(axes), Create(graph), Write(lbl))

        x_tracker = ValueTracker(2.5)
        area = always_redraw(lambda: axes.get_area(
            graph, x_range=[0, x_tracker.get_value()], color=YELLOW, opacity=0.5,
        ))
        vline = always_redraw(lambda: DashedLine(
            axes.c2p(x_tracker.get_value(), 0),
            axes.c2p(x_tracker.get_value(), f(x_tracker.get_value())),
            color=GREEN,
        ))

        self.add(area, vline)
        formula = MathTex(r"\frac{d}{dx}\!\int_0^x f(t)\,dt = f(x)", font_size=34)
        formula.to_edge(UP, buff=0.8).add_background_rectangle()
        self.play(Write(formula))

        self.play(x_tracker.animate.set_value(3.7), run_time=2)
        self.play(x_tracker.animate.set_value(1.2), run_time=2)
        self.wait(0.6)
