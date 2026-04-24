from manim import *
import numpy as np


class PiEqualsFourParadoxExample(Scene):
    def construct(self):
        title = Text("π = 4? The staircase paradox", font_size=28).to_edge(UP)
        self.play(Write(title))

        r = 2.0
        circle = Circle(radius=r, color=BLUE).shift(0.2 * DOWN)
        square = Square(side_length=2 * r, color=YELLOW).shift(0.2 * DOWN)
        self.play(Create(circle), Create(square))

        def staircase(level):
            segs = []
            n = 2 ** level
            cx, cy = 0, 0.2 * -1  # match circle shift
            center = circle.get_center()
            step = 2 * r / n
            pts = []
            # Build staircase going around the square but tucked inward to the circle
            for side in range(4):
                for k in range(n):
                    # corner positions on the square
                    pass
            # Simpler: start from +r top-right, step staircase left then down etc.
            start = center + np.array([r, r, 0])
            pts.append(start)
            # Approximate quarter circle by staircase
            for i in range(n):
                next_h = center + np.array([r - step * (i + 1), r, 0])
                pts.append(next_h)
                next_v = center + np.array([r - step * (i + 1), r - step * (i + 1), 0])
                pts.append(next_v)
            path = VMobject(color=ORANGE, stroke_width=3)
            path.set_points_as_corners(pts)
            return path

        stair = staircase(2)
        self.play(Create(stair))

        for level in [3, 4, 5]:
            new_stair = staircase(level)
            self.play(Transform(stair, new_stair), run_time=1.0)
            self.wait(0.2)

        perim = MathTex(r"\text{staircase perimeter} = 4\cdot 2r = 4 \cdot (2r)", font_size=28).next_to(square, DOWN, buff=0.35)
        catch = Text("but the limit shape is not rectifiable pointwise",
                     font_size=22, color=RED).to_edge(DOWN)
        self.play(Write(perim))
        self.play(Write(catch))
        self.wait(0.6)
