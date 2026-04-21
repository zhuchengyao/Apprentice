from manim import *
import numpy as np


class ThreeDLightSourceExample(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[-2, 2, 1])
        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)
        # Move the light closer so shading is visible.
        self.renderer.camera.light_source.move_to(3 * IN)

        surface = Surface(
            lambda u, v: np.array([u, v, 0.5 * (u ** 2 - v ** 2)]),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(25, 25),
        )
        surface.set_style(fill_opacity=0.9, stroke_width=0.3)
        surface.set_fill_by_checkerboard(GREEN_D, GREEN_B, opacity=0.9)

        self.play(Create(axes))
        self.play(Create(surface), run_time=3)
        self.wait(0.5)
