from manim import *
import numpy as np


class DotVsCrossComparisonExample(Scene):
    """
    Compare dot and cross products side-by-side:
    v·w: scalar, projection-based, = |v||w|cos θ
    v×w: vector (in 3D) or scalar (in 2D), area-based, = |v||w|sin θ (magnitude)
    """

    def construct(self):
        title = Tex(r"Dot vs Cross: scalar/projection vs vector/area",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Two halves
        # LEFT: dot product
        left_center = LEFT * 3.3 + DOWN * 0.3
        right_center = RIGHT * 2.7 + DOWN * 0.3

        v = np.array([1.5, 0.3])
        w = np.array([0.8, 1.5])

        left_plane = NumberPlane(x_range=[-1, 3, 1], y_range=[-0.5, 2, 1],
                                  x_length=4, y_length=4,
                                  background_line_style={"stroke_opacity": 0.3}
                                  ).move_to(left_center)
        right_plane = NumberPlane(x_range=[-1, 3, 1], y_range=[-0.5, 2, 1],
                                   x_length=4, y_length=4,
                                   background_line_style={"stroke_opacity": 0.3}
                                   ).move_to(right_center)
        self.add(left_plane, right_plane)

        # Draw v, w in both
        for pl, c in [(left_plane, left_center), (right_plane, right_center)]:
            self.add(Arrow(pl.c2p(0, 0), pl.c2p(v[0], v[1]),
                            color=BLUE, buff=0, stroke_width=4))
            self.add(Arrow(pl.c2p(0, 0), pl.c2p(w[0], w[1]),
                            color=ORANGE, buff=0, stroke_width=4))

        # LEFT: projection annotation
        u_hat = w / np.linalg.norm(w)
        proj = np.dot(v, u_hat) * u_hat
        self.add(DashedLine(left_plane.c2p(v[0], v[1]),
                             left_plane.c2p(proj[0], proj[1]),
                             color=GREY_B, stroke_width=2))
        self.add(Arrow(left_plane.c2p(0, 0), left_plane.c2p(proj[0], proj[1]),
                        color=YELLOW, buff=0, stroke_width=4))
        self.add(Tex(r"projection $\to$ scalar",
                     color=YELLOW, font_size=18).next_to(left_plane, DOWN, buff=0.15))

        # RIGHT: parallelogram
        self.add(Polygon(right_plane.c2p(0, 0),
                          right_plane.c2p(v[0], v[1]),
                          right_plane.c2p(v[0] + w[0], v[1] + w[1]),
                          right_plane.c2p(w[0], w[1]),
                          color=GREEN, stroke_width=3,
                          fill_color=GREEN, fill_opacity=0.35))
        self.add(Tex(r"parallelogram area",
                     color=GREEN, font_size=18).next_to(right_plane, DOWN, buff=0.15))

        # Headers
        self.add(Tex(r"$\vec v\cdot\vec w$", color=BLUE,
                     font_size=28).next_to(left_plane, UP, buff=0.2))
        self.add(Tex(r"$\vec v\times\vec w$", color=ORANGE,
                     font_size=28).next_to(right_plane, UP, buff=0.2))

        # Compute
        dot_val = float(np.dot(v, w))
        cross_val = float(v[0] * w[1] - v[1] * w[0])

        left_note = Tex(rf"$={dot_val:.2f}$", color=YELLOW,
                         font_size=24).to_edge(DOWN, buff=0.4).shift(LEFT * 3.3)
        right_note = Tex(rf"$={cross_val:.2f}$", color=GREEN,
                          font_size=24).to_edge(DOWN, buff=0.4).shift(RIGHT * 2.7)
        self.play(Write(left_note), Write(right_note))

        self.wait(1.0)

        # Summary
        summary = Tex(r"$|\vec v\cdot\vec w|=|\vec v||\vec w|\cos\theta$; $|\vec v\times\vec w|=|\vec v||\vec w|\sin\theta$",
                       color=YELLOW, font_size=22).to_edge(DOWN, buff=0.1)
        self.play(Write(summary))
        self.wait(0.8)
