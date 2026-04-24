from manim import *
import numpy as np


class WonkyHexagonFractalExample(Scene):
    def construct(self):
        title = Text("Wonky hexagon fractal (offset children)", font_size=28).to_edge(UP)
        self.play(Write(title))

        def hexagon(center, radius, color):
            hex_ = RegularPolygon(n=6, color=color, fill_opacity=0.6, stroke_width=1)
            hex_.scale(radius).move_to(center).rotate(PI / 6)
            return hex_

        def build(depth, center=np.array([0.0, 0.0, 0.0]), radius=2.6, color=TEAL):
            group = VGroup()
            if depth == 0:
                group.add(hexagon(center, radius, color))
                return group
            sub_r = radius * 0.38
            group.add(hexagon(center, sub_r, color))
            for k in range(6):
                theta = 2 * np.pi * k / 6 + 0.18
                offset = (radius - sub_r * 0.9) * np.array([np.cos(theta), np.sin(theta), 0.0])
                group.add(build(depth - 1, center + offset, sub_r, color))
            return group

        f = build(0)
        self.play(FadeIn(f))
        self.wait(0.3)
        for d in [1, 2, 3]:
            nxt = build(d)
            self.play(Transform(f, nxt), run_time=1.2)
            self.wait(0.3)
