from manim import *
import numpy as np


class GradientDescent2DExample(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=-50 * DEGREES)

        axes = ThreeDAxes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[0, 6, 2],
            x_length=6, y_length=6, z_length=3,
        )

        def loss(x, y): return 0.4 * (x ** 2 + y ** 2) + 0.2

        surface = Surface(
            lambda u, v: axes.c2p(u, v, loss(u, v)),
            u_range=[-2.8, 2.8], v_range=[-2.8, 2.8],
            resolution=(24, 24),
        ).set_style(fill_opacity=0.6, stroke_width=0.5)
        surface.set_fill_by_checkerboard(BLUE_D, BLUE_B, opacity=0.6)

        self.add(axes, surface)
        self.wait(0.4)

        path_pts = []
        x, y = -2.5, 2.2
        lr = 0.25
        for _ in range(15):
            path_pts.append(axes.c2p(x, y, loss(x, y) + 0.05))
            gx, gy = 0.8 * x, 0.8 * y
            x -= lr * gx
            y -= lr * gy

        path = VMobject(stroke_color=YELLOW, stroke_width=4)
        path.set_points_as_corners(path_pts)
        ball = Sphere(radius=0.15).set_color(YELLOW).move_to(path_pts[0])

        self.add(ball)
        self.play(Create(path), MoveAlongPath(ball, path), run_time=4)
        self.wait(0.4)
