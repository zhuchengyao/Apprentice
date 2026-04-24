from manim import *
import numpy as np


class WaveEquationPlotExample(Scene):
    def construct(self):
        title = MathTex(r"\partial_{tt} u = c^2\, \partial_{xx} u", font_size=38).to_edge(UP)
        self.play(Write(title))

        axes = Axes(
            x_range=[0, 4 * PI, PI], y_range=[-1.2, 1.2, 0.5],
            x_length=10, y_length=4, tips=False,
        ).to_edge(DOWN, buff=0.6)
        self.play(Create(axes))

        t = ValueTracker(0)
        c = 0.8
        wave = always_redraw(lambda: axes.plot(
            lambda x: np.sin(x - c * t.get_value()) + 0.4 * np.sin(2 * (x - c * t.get_value())),
            color=YELLOW,
        ))
        self.add(wave)
        self.play(t.animate.set_value(8), run_time=5, rate_func=linear)
        self.wait(0.4)
