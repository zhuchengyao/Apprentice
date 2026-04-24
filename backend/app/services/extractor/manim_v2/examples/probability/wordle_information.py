from manim import *
import numpy as np


class WordleInformationExample(Scene):
    def construct(self):
        title = Text("Information gained by a Wordle guess", font_size=28).to_edge(UP)
        self.play(Write(title))

        formula = MathTex(
            r"I(\text{guess}) = \sum_p p(\text{pattern})\,\log_2\!\frac{1}{p(\text{pattern})}",
            font_size=32,
        )
        self.play(Write(formula))
        self.wait(0.3)

        axes = Axes(
            x_range=[0, 1, 0.2], y_range=[0, 5, 1],
            x_length=6, y_length=3.2,
            axis_config={"include_numbers": True},
        ).shift(DOWN * 0.6)
        graph = axes.plot(lambda p: -np.log2(p) if p > 0.001 else 10, x_range=[0.02, 1.0], color=BLUE)
        self.play(Create(axes), Create(graph))

        xlbl = Text("p(pattern)", font_size=22).next_to(axes, DOWN, buff=0.05)
        ylbl = MathTex(r"\log_2(1/p)", font_size=24).next_to(axes, LEFT, buff=0.1).rotate(PI / 2)
        self.play(Write(xlbl), Write(ylbl))

        caption = Text("Rare patterns carry more bits; average weighted by probability.",
                       font_size=20, color=YELLOW).to_edge(DOWN)
        self.play(Write(caption))
        self.wait(0.6)
