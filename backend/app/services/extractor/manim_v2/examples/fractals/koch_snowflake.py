from manim import *
import numpy as np


def koch_iterate(points):
    rot = np.array([
        [np.cos(-PI / 3), -np.sin(-PI / 3), 0],
        [np.sin(-PI / 3), np.cos(-PI / 3), 0],
        [0, 0, 1],
    ])
    new = []
    for i in range(len(points) - 1):
        a = np.array(points[i])
        b = np.array(points[i + 1])
        p1 = a + (b - a) / 3
        p3 = a + 2 * (b - a) / 3
        bump = p1 + rot @ (p3 - p1)
        new.extend([tuple(a), tuple(p1), tuple(bump), tuple(p3)])
    new.append(points[-1])
    return new


class KochSnowflakeExample(Scene):
    def construct(self):
        title = Text("Koch snowflake — iterations 1..4", font_size=28).to_edge(UP)
        self.play(Write(title))

        size = 3.5
        base = [
            (-size / 2, -size / (2 * np.sqrt(3)), 0),
            (size / 2, -size / (2 * np.sqrt(3)), 0),
            (0, size / np.sqrt(3), 0),
            (-size / 2, -size / (2 * np.sqrt(3)), 0),
        ]

        curves = []
        pts = base
        for _ in range(4):
            curve = VMobject(stroke_color=BLUE, stroke_width=3)
            curve.set_points_as_corners([np.array(p) for p in pts])
            curves.append(curve)
            pts = koch_iterate(pts)

        current = curves[0]
        self.play(Create(current))
        for nxt in curves[1:]:
            self.play(Transform(current, nxt), run_time=1.2)
        self.wait(0.6)
