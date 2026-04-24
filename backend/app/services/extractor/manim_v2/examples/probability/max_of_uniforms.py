from manim import *
import numpy as np


class MaxOfUniformsExample(Scene):
    def construct(self):
        title = Text("Distribution of max(U₁, …, Uₙ) for Uᵢ ~ Uniform[0,1]",
                     font_size=25).to_edge(UP)
        self.play(Write(title))

        axes = Axes(
            x_range=[0, 1, 0.2], y_range=[0, 10, 2],
            x_length=9, y_length=4,
            axis_config={"include_tip": True, "include_numbers": True},
        ).shift(0.3 * DOWN)
        xlbl = MathTex("x", font_size=24).next_to(axes, DOWN, buff=0.1)
        ylbl = MathTex(r"f_{M_n}(x)", font_size=24).next_to(axes, LEFT, buff=0.1).rotate(PI / 2)
        self.play(Create(axes), Write(xlbl), Write(ylbl))

        colors = [BLUE, GREEN, ORANGE, YELLOW]
        graphs = VGroup()
        labels = VGroup()
        for i, n in enumerate([1, 2, 5, 10]):
            g = axes.plot(lambda x, n=n: n * x ** (n - 1) if x > 0 else 0,
                          x_range=[0.01, 0.999], color=colors[i])
            graphs.add(g)
            lbl = MathTex(f"n={n}", color=colors[i], font_size=24)
            labels.add(lbl)

        labels.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UL).shift(DOWN * 0.6 + RIGHT * 0.4)

        for g, lbl in zip(graphs, labels):
            self.play(Create(g), Write(lbl), run_time=0.8)

        formula = MathTex(
            r"F_{M_n}(x) = x^n \;\Rightarrow\; f_{M_n}(x) = n x^{n-1}",
            font_size=30, color=YELLOW,
        ).to_edge(DOWN)
        self.play(Write(formula))
        self.wait(0.6)
