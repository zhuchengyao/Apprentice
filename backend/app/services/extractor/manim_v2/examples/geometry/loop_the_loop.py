from manim import *
import numpy as np


class LoopTheLoopExample(Scene):
    def construct(self):
        title = Text("Loop-the-loop parametric track", font_size=28).to_edge(UP)
        self.play(Write(title))

        def loop(t):
            s = (6 * PI / 2) * (t - 0.5)
            return np.array([s / 2 - np.sin(s), np.cos(s) + s ** 2 / 10, 0]) * 0.45

        curve = ParametricFunction(loop, t_range=[0, 1], color=YELLOW)
        self.play(Create(curve, run_time=2.5))

        ball = Dot(color=BLUE, radius=0.1).move_to(curve.point_from_proportion(0))
        self.add(ball)
        self.play(MoveAlongPath(ball, curve, run_time=3, rate_func=linear))
        self.wait(0.4)
