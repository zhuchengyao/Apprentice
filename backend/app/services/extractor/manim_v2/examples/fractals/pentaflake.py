from manim import *
import numpy as np


class PentaflakeExample(Scene):
    def construct(self):
        title = Text("Pentaflake (5-fold Sierpinski analog)", font_size=28).to_edge(UP)
        self.play(Write(title))

        r = 1 / (1 + 2 * np.cos(np.pi / 5))

        def centers(depth, center, radius):
            if depth == 0:
                return [(center, radius)]
            out = []
            sub = radius * r
            out.extend(centers(depth - 1, center, sub))
            for k in range(5):
                theta = np.pi / 2 + 2 * np.pi * k / 5
                offset = (radius - sub) * np.array([np.cos(theta), np.sin(theta), 0])
                out.extend(centers(depth - 1, center + offset, sub))
            return out

        def pentaflake(depth, radius=2.6):
            group = VGroup()
            for c, rad in centers(depth, ORIGIN, radius):
                p = RegularPolygon(n=5, color=TEAL, fill_opacity=0.8, stroke_width=1)
                p.scale(rad).move_to(c)
                group.add(p)
            return group

        f0 = pentaflake(0)
        self.play(FadeIn(f0))
        self.wait(0.4)
        for d in range(1, 4):
            nxt = pentaflake(d)
            self.play(Transform(f0, nxt), run_time=1.3)
            self.wait(0.3)
