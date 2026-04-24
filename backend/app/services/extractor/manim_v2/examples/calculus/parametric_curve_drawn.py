from manim import *
import numpy as np


class ParametricCurveDrawnExample(Scene):
    def construct(self):
        title = MathTex(r"\vec{r}(t) = (t\cos t,\ t\sin t)", font_size=34).to_edge(UP)
        self.play(Write(title))

        axes = Axes(
            x_range=[-6, 6, 2], y_range=[-6, 6, 2],
            x_length=6, y_length=6, tips=False,
        )
        self.play(Create(axes))

        t = ValueTracker(0.01)

        def r(s):
            return 0.4 * s * np.cos(s), 0.4 * s * np.sin(s)

        vec = always_redraw(lambda: Arrow(
            axes.c2p(0, 0), axes.c2p(*r(t.get_value())),
            buff=0, color=GREEN, stroke_width=5,
        ))
        curve = always_redraw(lambda: ParametricFunction(
            lambda s: axes.c2p(*r(s)),
            t_range=[0.01, max(0.02, t.get_value())],
            color=YELLOW,
        ))
        self.add(vec, curve)
        self.play(t.animate.set_value(10), run_time=5, rate_func=linear)
        self.wait(0.4)
