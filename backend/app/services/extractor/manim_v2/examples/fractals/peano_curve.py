from manim import *
import numpy as np


class PeanoCurveExample(Scene):
    def construct(self):
        title = Text("Peano curve (space-filling iterates)", font_size=30).to_edge(UP)
        self.play(Write(title))

        def peano_points(order):
            if order == 0:
                return [np.array([0.0, 0.0])]
            prev = peano_points(order - 1)
            n = 3 ** (order - 1)
            scale = 1.0 / 3.0
            prev_s = [p * scale for p in prev]
            out = []
            patterns = [
                (np.array([0.0, 0.0]), 1),
                (np.array([0.0, n * scale]), 1),
                (np.array([0.0, 2 * n * scale]), 1),
                (np.array([n * scale, 2 * n * scale]), -1),
                (np.array([n * scale, n * scale]), -1),
                (np.array([n * scale, 0.0]), -1),
                (np.array([2 * n * scale, 0.0]), 1),
                (np.array([2 * n * scale, n * scale]), 1),
                (np.array([2 * n * scale, 2 * n * scale]), 1),
            ]
            for origin, direction in patterns:
                pts = prev_s if direction == 1 else list(reversed(prev_s))
                for p in pts:
                    out.append(origin + p)
            return out

        def make_path(order):
            pts = peano_points(order)
            arr = np.array(pts)
            arr -= arr.mean(axis=0)
            arr *= 5.0 / max(arr.max() - arr.min(), 1e-6)
            path = VMobject(color=BLUE, stroke_width=3)
            path.set_points_as_corners([np.array([x, y, 0]) for x, y in arr])
            return path

        path = make_path(1)
        lbl = Text("order 1", font_size=22).to_edge(DOWN)
        self.play(Create(path), Write(lbl), run_time=1.5)
        self.wait(0.4)

        for order in [2, 3]:
            new_path = make_path(order)
            new_lbl = Text(f"order {order}", font_size=22).to_edge(DOWN)
            self.play(Transform(path, new_path), Transform(lbl, new_lbl), run_time=1.8)
            self.wait(0.4)
