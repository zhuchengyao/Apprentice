from manim import *
import numpy as np


class QuaternionRotationExample(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

        axes = ThreeDAxes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[-3, 3, 1])
        self.add(axes)

        def rot_from_quat(q):
            w, x, y, z = q
            return np.array([
                [1 - 2 * (y**2 + z**2), 2 * (x*y - z*w), 2 * (x*z + y*w)],
                [2 * (x*y + z*w), 1 - 2 * (x**2 + z**2), 2 * (y*z - x*w)],
                [2 * (x*z - y*w), 2 * (y*z + x*w), 1 - 2 * (x**2 + y**2)],
            ])

        axis = np.array([1, 1, 0]) / np.sqrt(2)
        angle = PI / 2

        cube = Cube(side_length=1.4, fill_opacity=0.6, stroke_width=1).set_color(TEAL)
        self.play(FadeIn(cube))

        tracker = ValueTracker(0)

        def update_cube(m):
            theta = tracker.get_value()
            q = np.array([np.cos(theta / 2), *(np.sin(theta / 2) * axis)])
            R = rot_from_quat(q)
            template = Cube(side_length=1.4, fill_opacity=0.6, stroke_width=1).set_color(TEAL)
            template.apply_matrix(R)
            m.become(template)

        cube.add_updater(update_cube)
        self.play(tracker.animate.set_value(angle), run_time=3)
        cube.clear_updaters()

        label = MathTex(
            r"q = \cos(\theta/2) + (\hat{n})\sin(\theta/2)",
            font_size=32,
        )
        self.add_fixed_in_frame_mobjects(label)
        label.to_edge(UP)
        self.play(Write(label))
        self.wait(0.6)
