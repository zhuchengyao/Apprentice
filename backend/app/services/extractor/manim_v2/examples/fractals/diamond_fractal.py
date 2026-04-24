from manim import *
import numpy as np


class DiamondFractalExample(Scene):
    def construct(self):
        title = Text("Diamond fractal (4-fold Sierpinski analog)", font_size=28).to_edge(UP)
        self.play(Write(title))

        def diamond(center, size, color):
            points = [
                center + np.array([0, size, 0]),
                center + np.array([size, 0, 0]),
                center + np.array([0, -size, 0]),
                center + np.array([-size, 0, 0]),
            ]
            p = Polygon(*points, color=color, fill_opacity=0.7, stroke_width=1)
            return p

        def build(depth, center=np.array([0.0, 0.0, 0.0]), size=2.4):
            group = VGroup()
            if depth == 0:
                group.add(diamond(center, size, TEAL))
                return group
            sub = size / 2
            offsets = [
                np.array([0, sub, 0]),
                np.array([sub, 0, 0]),
                np.array([0, -sub, 0]),
                np.array([-sub, 0, 0]),
            ]
            for off in offsets:
                group.add(build(depth - 1, center + off, sub))
            return group

        f = build(0)
        self.play(FadeIn(f))
        self.wait(0.3)
        for d in [1, 2, 3, 4]:
            nxt = build(d)
            self.play(Transform(f, nxt), run_time=1.1)
            self.wait(0.25)
