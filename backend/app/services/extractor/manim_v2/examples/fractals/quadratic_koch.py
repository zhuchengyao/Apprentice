from manim import *
import numpy as np


def quadratic_koch_iterate(points):
    new = []
    for i in range(len(points) - 1):
        a = np.array(points[i])
        b = np.array(points[i + 1])
        d = (b - a) / 4
        perp = np.array([-d[1], d[0], 0])
        p1 = a + d
        p2 = p1 + perp
        p3 = p2 + d
        p4 = p3 - perp
        p5 = p4 - perp
        p6 = p5 + d
        p7 = p6 + perp
        new.extend([tuple(a), tuple(p1), tuple(p2), tuple(p3), tuple(p4), tuple(p5), tuple(p6), tuple(p7)])
    new.append(points[-1])
    return new


class QuadraticKochExample(Scene):
    def construct(self):
        title = Text("Quadratic Koch curve — iterations 1..3", font_size=28).to_edge(UP)
        self.play(Write(title))

        base = [(-5.5, 0, 0), (5.5, 0, 0)]
        curves = []
        pts = base
        for _ in range(4):
            curve = VMobject(stroke_color=ORANGE, stroke_width=2)
            curve.set_points_as_corners([np.array(p) for p in pts])
            curves.append(curve)
            pts = quadratic_koch_iterate(pts)

        current = curves[0]
        self.play(Create(current))
        for nxt in curves[1:]:
            self.play(Transform(current, nxt), run_time=1.2)
        self.wait(0.4)
