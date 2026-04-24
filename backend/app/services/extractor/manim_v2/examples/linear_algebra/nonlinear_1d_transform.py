from manim import *
import numpy as np


class Nonlinear1DTransformExample(Scene):
    def construct(self):
        title = Text("Nonlinear: even spacing breaks", font_size=30, color=RED_B).to_edge(UP)

        axis = Line(LEFT * 5, RIGHT * 5, color=BLUE)
        integers = list(range(-4, 5))
        ticks = VGroup(*[Dot(np.array([x, 0, 0]), color=YELLOW, radius=0.07) for x in integers])
        labels = VGroup(*[
            MathTex(str(x), font_size=24).next_to(ticks[i], DOWN, buff=0.12)
            for i, x in enumerate(integers)
        ])

        def bend(p):
            return np.array([np.sin(p[0]) + p[0], p[1], p[2]])

        self.play(Write(title))
        self.play(Create(axis), FadeIn(ticks), FadeIn(labels))

        new_positions = [bend(np.array([x, 0, 0])) for x in integers]
        self.play(
            ApplyPointwiseFunction(bend, axis),
            *[
                VGroup(ticks[i], labels[i]).animate.shift(new_positions[i] - ticks[i].get_center())
                for i in range(len(integers))
            ],
            run_time=2,
        )
        self.wait(0.8)
