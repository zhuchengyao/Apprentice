from manim import *
import numpy as np


class SinCosPlotExample(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-PI, PI, PI / 2],
            y_range=[-1.5, 1.5, 0.5],
            x_length=8,
            y_length=4,
            tips=False,
        ).to_edge(DOWN, buff=0.6)
        labels = axes.get_axis_labels(x_label="x", y_label="y")

        sine = axes.plot(np.sin, color=BLUE)
        cosine = axes.plot(np.cos, color=YELLOW)
        sine_label = axes.get_graph_label(sine, label=r"\sin x").shift(UP * 0.2)
        cos_label = axes.get_graph_label(cosine, label=r"\cos x").shift(DOWN * 0.2)

        self.play(Create(axes), Write(labels))
        self.play(Create(sine), Write(sine_label))
        self.play(Create(cosine), Write(cos_label))
        self.wait(0.5)
