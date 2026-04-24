from manim import *
import numpy as np


class QuaternionSlerpExample(ThreeDScene):
    """
    Quaternion spherical linear interpolation (slerp) on unit sphere
    S³ of quaternions gives the shortest-arc interpolation between
    two rotations. Project rotations to their action on e_3 to see
    motion on S² — it traces the great-circle arc.

    Two rotations: q_0 = (1, 0, 0, 0) (identity) and q_1 = rotation
    about y-axis by π/2. Compose slerp(q_0, q_1, t) and show its
    action on 3 reference axes via ValueTracker t_tr.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=40 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.05)

        axes = ThreeDAxes(x_range=[-2, 2, 1], y_range=[-2, 2, 1], z_range=[-2, 2, 1],
                          x_length=4.0, y_length=4.0, z_length=4.0)
        self.add(axes)

        sphere = Sphere(radius=1.0, resolution=(18, 36),
                        fill_opacity=0.15).set_color(BLUE)
        self.add(sphere)

        # quaternion q = (w, x, y, z)
        # q_0 = (1, 0, 0, 0), q_1 = rotate π/2 about y = (cos(π/4), 0, sin(π/4), 0)
        q0 = np.array([1.0, 0.0, 0.0, 0.0])
        q1 = np.array([np.cos(PI / 4), 0.0, np.sin(PI / 4), 0.0])

        def slerp(t):
            cos_omega = np.dot(q0, q1)
            omega = np.arccos(np.clip(cos_omega, -1, 1))
            if abs(omega) < 1e-6:
                return q0
            return (np.sin((1 - t) * omega) * q0 + np.sin(t * omega) * q1) / np.sin(omega)

        def quat_to_R(q):
            w, x, y, z = q
            return np.array([
                [1 - 2 * (y ** 2 + z ** 2), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                [2 * (x * y + z * w), 1 - 2 * (x ** 2 + z ** 2), 2 * (y * z - x * w)],
                [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x ** 2 + y ** 2)],
            ])

        t_tr = ValueTracker(0.0)

        def frame_arrows():
            q = slerp(t_tr.get_value())
            R = quat_to_R(q)
            grp = VGroup(
                Arrow3D(ORIGIN, R @ np.array([1.5, 0, 0]), color=RED, thickness=0.025),
                Arrow3D(ORIGIN, R @ np.array([0, 1.5, 0]), color=GREEN, thickness=0.025),
                Arrow3D(ORIGIN, R @ np.array([0, 0, 1.5]), color=BLUE, thickness=0.025),
            )
            return grp

        def e3_dot():
            q = slerp(t_tr.get_value())
            R = quat_to_R(q)
            return Dot3D(point=R @ np.array([0, 0, 1]),
                          color=YELLOW, radius=0.1)

        def trail_arc():
            t_cur = t_tr.get_value()
            if t_cur < 0.02:
                return VMobject()
            pts = []
            for tk in np.linspace(0, t_cur, 40):
                q = slerp(tk)
                R = quat_to_R(q)
                pts.append(R @ np.array([0, 0, 1]))
            return VMobject().set_points_as_corners(pts).set_color(YELLOW).set_stroke(width=3)

        self.add(always_redraw(frame_arrows),
                 always_redraw(e3_dot),
                 always_redraw(trail_arc))

        title = Tex(r"Quaternion slerp: shortest great-circle arc on $S^3$",
                    font_size=22)
        info = VGroup(
            VGroup(Tex(r"$t=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"$q_0=1,\ q_1=\cos\tfrac{\pi}{4}+\sin\tfrac{\pi}{4}\mathbf{j}$",
                font_size=20),
            Tex(r"projects to arc on $S^2$",
                color=YELLOW, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        self.add_fixed_in_frame_mobjects(title, info)
        title.to_edge(UP, buff=0.3)
        info.to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(t_tr.get_value()))

        self.play(t_tr.animate.set_value(1.0),
                  run_time=5, rate_func=smooth)
        self.wait(0.5)
        self.play(t_tr.animate.set_value(0.0),
                  run_time=2, rate_func=smooth)
        self.play(t_tr.animate.set_value(1.0),
                  run_time=3, rate_func=smooth)
        self.wait(0.8)
        self.stop_ambient_camera_rotation()
