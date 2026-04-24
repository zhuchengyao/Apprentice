from manim import *
import numpy as np


def hilbert_points(level, x=0.0, y=0.0, xi=1.0, xj=0.0, yi=0.0, yj=1.0):
    if level <= 0:
        return [(x + (xi + yi) / 2, y + (xj + yj) / 2)]
    out = []
    out += hilbert_points(level - 1, x, y, yi / 2, yj / 2, xi / 2, xj / 2)
    out += hilbert_points(level - 1, x + xi / 2, y + xj / 2, xi / 2, xj / 2, yi / 2, yj / 2)
    out += hilbert_points(level - 1, x + xi / 2 + yi / 2, y + xj / 2 + yj / 2,
                          xi / 2, xj / 2, yi / 2, yj / 2)
    out += hilbert_points(level - 1, x + xi / 2 + yi, y + xj / 2 + yj,
                          -yi / 2, -yj / 2, -xi / 2, -xj / 2)
    return out


class HilbertCurveExample(Scene):
    def construct(self):
        title = Text("Hilbert curve — iterations 1..4", font_size=28).to_edge(UP)
        self.play(Write(title))

        size = 5.0
        curves = []
        for lvl in [1, 2, 3, 4]:
            pts = hilbert_points(lvl)
            scaled = [np.array([(px - 0.5) * size, (py - 0.5) * size, 0]) for px, py in pts]
            curve = VMobject(stroke_color=YELLOW, stroke_width=3)
            curve.set_points_as_corners(scaled)
            curves.append(curve)

        current = curves[0]
        self.play(Create(current))
        for nxt in curves[1:]:
            self.play(Transform(current, nxt), run_time=1.5)
        self.wait(0.6)
