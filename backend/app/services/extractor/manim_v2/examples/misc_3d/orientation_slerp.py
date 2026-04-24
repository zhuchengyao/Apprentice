from manim import *
import numpy as np


class OrientationSlerpExample(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)

        axes = ThreeDAxes(x_range=[-2, 2, 1], y_range=[-2, 2, 1], z_range=[-2, 2, 1])
        self.add(axes)

        q_start = np.array([1.0, 0.0, 0.0, 0.0])  # identity
        # 120° around (1,1,1)/sqrt(3)
        axis = np.array([1, 1, 1]) / np.sqrt(3)
        theta = 2 * PI / 3
        q_end = np.array([np.cos(theta / 2), *(np.sin(theta / 2) * axis)])

        def rot_from_quat(q):
            w, x, y, z = q
            return np.array([
                [1 - 2 * (y**2 + z**2), 2 * (x*y - z*w), 2 * (x*z + y*w)],
                [2 * (x*y + z*w), 1 - 2 * (x**2 + z**2), 2 * (y*z - x*w)],
                [2 * (x*z - y*w), 2 * (y*z + x*w), 1 - 2 * (x**2 + y**2)],
            ])

        def slerp(q0, q1, t):
            dot = np.dot(q0, q1)
            if dot < 0:
                q1 = -q1
                dot = -dot
            if dot > 0.9995:
                return (1 - t) * q0 + t * q1
            omega = np.arccos(dot)
            s0 = np.sin((1 - t) * omega) / np.sin(omega)
            s1 = np.sin(t * omega) / np.sin(omega)
            return s0 * q0 + s1 * q1

        arrow_template = Arrow3D(start=ORIGIN, end=RIGHT * 1.6, color=GREEN,
                                 thickness=0.03, height=0.3, base_radius=0.08)
        arrow_i = arrow_template.copy()
        arrow_j = Arrow3D(start=ORIGIN, end=UP * 1.6, color=RED,
                          thickness=0.03, height=0.3, base_radius=0.08)
        arrow_k = Arrow3D(start=ORIGIN, end=OUT * 1.6, color=BLUE,
                          thickness=0.03, height=0.3, base_radius=0.08)

        self.play(Create(arrow_i), Create(arrow_j), Create(arrow_k))

        tracker = ValueTracker(0)

        def update_frame(frame):
            q = slerp(q_start, q_end, tracker.get_value())
            R = rot_from_quat(q)
            new_i = Arrow3D(start=ORIGIN, end=R @ (RIGHT * 1.6), color=GREEN,
                            thickness=0.03, height=0.3, base_radius=0.08)
            new_j = Arrow3D(start=ORIGIN, end=R @ (UP * 1.6), color=RED,
                            thickness=0.03, height=0.3, base_radius=0.08)
            new_k = Arrow3D(start=ORIGIN, end=R @ (OUT * 1.6), color=BLUE,
                            thickness=0.03, height=0.3, base_radius=0.08)
            frame[0].become(new_i)
            frame[1].become(new_j)
            frame[2].become(new_k)

        frame_group = VGroup(arrow_i, arrow_j, arrow_k)
        frame_group.add_updater(update_frame)
        self.add(frame_group)

        self.play(tracker.animate.set_value(1.0), run_time=3)
        frame_group.clear_updaters()

        label = MathTex(r"\text{slerp}(q_0, q_1; t) = \frac{\sin((1-t)\Omega)}{\sin\Omega}q_0 + \frac{\sin(t\Omega)}{\sin\Omega}q_1",
                        font_size=26)
        self.add_fixed_in_frame_mobjects(label)
        label.to_edge(DOWN)
        self.play(Write(label))
        self.wait(0.6)
