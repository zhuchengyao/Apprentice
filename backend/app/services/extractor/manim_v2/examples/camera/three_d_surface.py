from manim import *
import numpy as np


class ThreeDSurfaceExample(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[-2, 2, 1])
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)
        self.play(Create(axes))

        surface = Surface(
            lambda u, v: np.array([u, v, np.sin(u) * np.cos(v)]),
            u_range=[-PI, PI],
            v_range=[-PI, PI],
            resolution=(30, 30),
        )
        surface.set_style(fill_opacity=0.75, stroke_width=0.5)
        surface.set_fill_by_checkerboard(BLUE_D, BLUE_B, opacity=0.75)

        self.play(Create(surface), run_time=3)
        self.wait(0.6)
