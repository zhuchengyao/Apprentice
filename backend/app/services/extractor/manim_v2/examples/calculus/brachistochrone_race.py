from manim import *
import numpy as np


class BrachistochroneRaceExample(Scene):
    def construct(self):
        title = Text(
            "Ball race: cycloid beats line and parabola",
            font_size=26,
        ).to_edge(UP)
        self.play(Write(title))

        axes = Axes(
            x_range=[0, 2 * PI, PI], y_range=[-2, 0.3, 1],
            x_length=10, y_length=3.5, tips=False,
        ).to_edge(DOWN, buff=0.6)
        self.play(Create(axes))

        end_x = 2 * PI

        def cycloid_y(x):
            t = x
            return -(1 - np.cos(t))

        line = axes.plot(lambda x: -x / PI, x_range=[0, end_x], color=RED)
        parab = axes.plot(lambda x: -0.16 * x ** 2, x_range=[0, end_x], color=GREEN)
        cyc = axes.plot(cycloid_y, x_range=[0.01, end_x], color=YELLOW)
        self.play(Create(line), Create(parab), Create(cyc))

        def ball_on(path, color):
            dot = Dot(path.point_from_proportion(0), color=color, radius=0.1)
            return dot

        d1 = ball_on(line, RED)
        d2 = ball_on(parab, GREEN)
        d3 = ball_on(cyc, YELLOW)
        self.add(d1, d2, d3)

        self.play(
            MoveAlongPath(d1, line, rate_func=linear, run_time=3.5),
            MoveAlongPath(d2, parab, rate_func=rush_into, run_time=2.8),
            MoveAlongPath(d3, cyc, rate_func=rush_into, run_time=2.2),
        )
        self.wait(0.4)
