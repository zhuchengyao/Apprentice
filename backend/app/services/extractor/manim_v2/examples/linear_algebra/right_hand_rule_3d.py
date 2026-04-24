from manim import *
import numpy as np


class RightHandRule3DExample(ThreeDScene):
    """
    Right-hand rule for 3D orientation: if î × ĵ = k̂ (right-handed),
    then a transformation with det>0 preserves orientation. det<0
    flips to left-handed.

    ThreeDScene: show standard basis as right-handed frame; apply a
    flipping transformation and show resulting left-handed frame.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=35 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.06)

        axes = ThreeDAxes(x_range=[-2, 2, 1], y_range=[-2, 2, 1], z_range=[-2, 2, 1],
                          x_length=4.5, y_length=4.5, z_length=4.5)
        self.add(axes)

        # Two flipping regimes
        t_tr = ValueTracker(0.0)

        # Start: identity (RH). Flip via negative-det matrix [[1, 0, 0], [0, 1, 0], [0, 0, -1]]
        F = np.diag([1.0, 1.0, -1.0])

        def M_of():
            t = t_tr.get_value()
            return (1 - t) * np.eye(3) + t * F

        def i_arrow():
            M = M_of()
            p = M @ np.array([1, 0, 0])
            return Arrow3D(start=ORIGIN, end=1.5 * p, color=GREEN, thickness=0.03)

        def j_arrow():
            M = M_of()
            p = M @ np.array([0, 1, 0])
            return Arrow3D(start=ORIGIN, end=1.5 * p, color=RED, thickness=0.03)

        def k_arrow():
            M = M_of()
            p = M @ np.array([0, 0, 1])
            return Arrow3D(start=ORIGIN, end=1.5 * p, color=BLUE, thickness=0.03)

        # Cross product î × ĵ
        def cross_arrow():
            M = M_of()
            i = M @ np.array([1, 0, 0])
            j = M @ np.array([0, 1, 0])
            c = np.cross(i, j)
            col = PURPLE if np.dot(c, M @ np.array([0, 0, 1])) > 0 else YELLOW
            return Arrow3D(start=ORIGIN, end=1.5 * c, color=col, thickness=0.04)

        self.add(always_redraw(i_arrow), always_redraw(j_arrow),
                 always_redraw(k_arrow), always_redraw(cross_arrow))

        # Fixed-in-frame info
        title = Tex(r"Right-hand rule: $\hat\imath\times\hat\jmath=\hat k$",
                    font_size=24)
        info = VGroup(
            VGroup(Tex(r"flip $t=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\det=$", font_size=22),
                   DecimalNumber(1.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"PURPLE $\hat\imath\times\hat\jmath$ aligned w/ $\hat k$:",
                color=PURPLE, font_size=18),
            Tex(r"right-handed",
                color=PURPLE, font_size=20),
            Tex(r"YELLOW: opposite to $\hat k$:",
                color=YELLOW, font_size=18),
            Tex(r"left-handed (flipped)",
                color=YELLOW, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        self.add_fixed_in_frame_mobjects(title, info)
        title.to_edge(UP, buff=0.3)
        info.to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(t_tr.get_value()))
        info[1][1].add_updater(lambda m: m.set_value(float(np.linalg.det(M_of()))))

        self.play(t_tr.animate.set_value(1.0), run_time=4, rate_func=smooth)
        self.wait(0.8)
        self.play(t_tr.animate.set_value(0.0), run_time=2.5, rate_func=smooth)
        self.wait(0.5)
        self.stop_ambient_camera_rotation()
