from manim import *
import numpy as np


class CircularFractalExample(Scene):
    def construct(self):
        title = Text("Circular fractal (7-ring self-similar)", font_size=30).to_edge(UP)
        self.play(Write(title))

        def build(depth, center=np.array([0.0, 0.0, 0.0]), radius=2.4):
            group = VGroup()
            if depth == 0:
                group.add(Circle(radius=radius, color=BLUE, stroke_width=2, fill_opacity=0.25))
                return group
            n = 6
            sub_r = radius / 3.0
            group.add(Circle(radius=sub_r, color=BLUE, stroke_width=1.5, fill_opacity=0.25).move_to(center))
            for k in range(n):
                theta = 2 * np.pi * k / n
                offset = (radius - sub_r) * np.array([np.cos(theta), np.sin(theta), 0.0])
                group.add(build(depth - 1, center + offset, sub_r))
            return group

        f = build(0)
        self.play(FadeIn(f))
        self.wait(0.3)
        for d in [1, 2, 3]:
            nxt = build(d)
            self.play(Transform(f, nxt), run_time=1.2)
            self.wait(0.3)
