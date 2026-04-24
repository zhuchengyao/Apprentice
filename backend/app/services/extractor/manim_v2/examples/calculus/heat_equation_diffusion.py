from manim import *
import numpy as np


class HeatEquationDiffusionExample(Scene):
    def construct(self):
        title = Text("1D heat equation: a delta diffuses into a Gaussian", font_size=26).to_edge(UP)
        self.play(Write(title))

        axes = Axes(
            x_range=[-5, 5, 1], y_range=[0, 1.2, 0.3],
            x_length=9, y_length=4,
            axis_config={"include_tip": True},
        ).shift(0.2 * DOWN)
        self.play(Create(axes))

        t_tracker = ValueTracker(0.05)

        def heat_profile():
            t = t_tracker.get_value()
            return axes.plot(
                lambda x: np.exp(-x * x / (4 * t)) / np.sqrt(4 * PI * t),
                x_range=[-4.9, 4.9],
                color=BLUE,
            )

        profile = always_redraw(heat_profile)
        self.add(profile)

        readout = always_redraw(lambda: MathTex(
            rf"t = {t_tracker.get_value():.2f}",
            font_size=30,
        ).to_corner(UR).shift(DOWN * 0.4 + LEFT * 0.4))
        self.add(readout)

        self.play(t_tracker.animate.set_value(3.0), run_time=4, rate_func=linear)
        self.wait(0.3)

        equation = MathTex(r"\partial_t u = \partial_{xx} u,\;\; u(x,0) = \delta(x)",
                           font_size=28, color=YELLOW).to_edge(DOWN)
        self.play(Write(equation))
        self.wait(0.6)
