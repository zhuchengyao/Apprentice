from manim import *
import numpy as np


class Rotation3DEigenvectorAxisExample(ThreeDScene):
    """
    In 3D, a rotation's axis of rotation IS its eigenvector with
    eigenvalue 1. Every other vector rotates away from its original span.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=35 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.05)

        axes = ThreeDAxes(x_range=[-2, 2, 1], y_range=[-2, 2, 1], z_range=[-2, 2, 1],
                          x_length=4.5, y_length=4.5, z_length=4.5)
        self.add(axes)

        # Rotation axis is z-axis. Rotation by θ around z.
        theta_tr = ValueTracker(0.0)

        def R_of():
            t = theta_tr.get_value()
            c, s = np.cos(t), np.sin(t)
            return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])

        # Eigenvector: (0, 0, 1) — axis
        eigen_axis = np.array([0, 0, 1.5])
        self.add(Arrow3D(start=ORIGIN, end=eigen_axis, color=GREEN, thickness=0.04))

        # A non-eigenvector: (1, 0.5, 0.3)
        v_non = np.array([1.0, 0.5, 0.3])

        def non_eigen_arrow():
            R = R_of()
            p = R @ v_non
            return Arrow3D(start=ORIGIN, end=p, color=YELLOW, thickness=0.03)

        def non_eigen_trail():
            t = theta_tr.get_value()
            if t < 0.02: return VMobject()
            ts = np.linspace(0, t, 40)
            pts = []
            for tk in ts:
                c, s = np.cos(tk), np.sin(tk)
                R = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
                pts.append(R @ v_non)
            return VMobject().set_points_as_corners(pts).set_color(YELLOW).set_stroke(width=3)

        self.add(always_redraw(non_eigen_arrow), always_redraw(non_eigen_trail))

        title = Tex(r"3D rotation: axis $=$ eigenvector with $\lambda=1$",
                    font_size=22)
        info = VGroup(
            Tex(r"GREEN: axis (eigenvector, $\lambda=1$)",
                color=GREEN, font_size=20),
            Tex(r"YELLOW: generic, sweeps arc",
                color=YELLOW, font_size=20),
            Tex(r"only axis stays on span",
                color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        self.add_fixed_in_frame_mobjects(title, info)
        title.to_edge(UP, buff=0.3)
        info.to_corner(UR, buff=0.3)

        self.play(theta_tr.animate.set_value(TAU), run_time=6, rate_func=linear)
        self.wait(0.5)
        self.stop_ambient_camera_rotation()
