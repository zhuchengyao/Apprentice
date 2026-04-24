from manim import *
import numpy as np


class SumOfSinesExample(Scene):
    def construct(self):
        title = Text("A square wave as a sum of sines", font_size=28).to_edge(UP)
        self.play(Write(title))

        axes = Axes(
            x_range=[-PI, PI, PI / 2], y_range=[-1.5, 1.5, 0.5],
            x_length=9, y_length=3.5,
            axis_config={"include_tip": True},
        ).shift(0.4 * DOWN)
        self.play(Create(axes))

        def partial(n_terms):
            return axes.plot(
                lambda x: sum(
                    (4 / PI) * np.sin((2 * k + 1) * x) / (2 * k + 1)
                    for k in range(n_terms)
                ),
                x_range=[-PI + 0.01, PI - 0.01],
                color=BLUE,
            )

        wave = partial(1)
        label = MathTex(r"N = 1", font_size=28).to_edge(DOWN)
        self.play(Create(wave), Write(label))

        for n in [3, 5, 10, 25]:
            new_wave = partial(n)
            new_lbl = MathTex(f"N = {n}", font_size=28).to_edge(DOWN)
            self.play(Transform(wave, new_wave), Transform(label, new_lbl), run_time=1.2)
            self.wait(0.2)

        formula = MathTex(
            r"f(x) = \tfrac{4}{\pi}\sum_{k=0}^{\infty} \tfrac{\sin((2k+1)x)}{2k+1}",
            font_size=28, color=YELLOW,
        ).next_to(axes, UP, buff=0.6)
        title.generate_target()
        title.target = title.copy().scale(0.001).set_opacity(0)
        self.play(MoveToTarget(title))
        self.play(Write(formula))
        self.wait(0.6)
