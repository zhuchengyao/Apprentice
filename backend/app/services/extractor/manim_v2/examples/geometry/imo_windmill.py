from manim import *
import numpy as np


class ImoWindmillExample(Scene):
    def construct(self):
        title = Text("IMO 2011 windmill: pivot rotates, line keeps splitting points", font_size=24).to_edge(UP)
        self.play(Write(title))

        np.random.seed(2)
        points = [np.array([np.random.uniform(-4, 4), np.random.uniform(-2.5, 2.5), 0]) for _ in range(9)]
        dots = VGroup(*[Dot(p, color=BLUE, radius=0.08) for p in points])
        self.play(FadeIn(dots))

        pivot_idx = 4
        pivot_dot = dots[pivot_idx].copy().set_color(YELLOW).scale(1.3)
        self.play(Transform(dots[pivot_idx], pivot_dot))

        def windmill_line(pivot, angle):
            direction = np.array([np.cos(angle), np.sin(angle), 0])
            return Line(pivot - 6 * direction, pivot + 6 * direction, color=ORANGE, stroke_width=3)

        angle = ValueTracker(0.1)
        line = always_redraw(lambda: windmill_line(points[pivot_idx], angle.get_value()))
        self.play(Create(line))

        self.play(angle.animate.set_value(PI + 0.1), run_time=4, rate_func=linear)
        self.wait(0.3)

        cap = Text("A line through a chosen point rotates; whenever it meets another point, that becomes the new pivot.",
                   font_size=18, color=YELLOW).to_edge(DOWN)
        self.play(Write(cap))
        self.wait(0.6)
