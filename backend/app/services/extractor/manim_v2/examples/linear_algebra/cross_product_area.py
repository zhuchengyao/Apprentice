from manim import *
import numpy as np


class CrossProductAreaExample(ThreeDScene):
    """
    Cross product a × b magnitude = area of parallelogram spanned by
    a, b. Direction = normal by right-hand rule.
    |a × b| = |a||b|sin θ. Dot product: a · b = |a||b|cos θ.

    ValueTracker θ_tr rotates b in 3D; always_redraw parallelogram +
    normal arrow + dot/cross sign.
    """

    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=40 * DEGREES)

        axes = ThreeDAxes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[-3, 3, 1],
                          x_length=5.0, y_length=5.0, z_length=5.0)
        self.add(axes)

        a = np.array([2.0, 0.0, 0.0])
        theta_tr = ValueTracker(PI / 4)

        def b_vec():
            t = theta_tr.get_value()
            return np.array([2.0 * np.cos(t), 2.0 * np.sin(t), 0.0])

        def a_arrow():
            return Arrow3D(ORIGIN, a, color=BLUE, thickness=0.025)

        def b_arrow():
            return Arrow3D(ORIGIN, b_vec(), color=GREEN, thickness=0.025)

        def parallelogram():
            b = b_vec()
            return Polygon(ORIGIN, a, a + b, b,
                            color=YELLOW, stroke_width=2,
                            fill_color=YELLOW, fill_opacity=0.35)

        def cross_arrow():
            b = b_vec()
            cp = np.cross(a, b)
            return Arrow3D(ORIGIN, cp, color=RED, thickness=0.03)

        self.add(always_redraw(parallelogram),
                 always_redraw(a_arrow), always_redraw(b_arrow),
                 always_redraw(cross_arrow))

        title = Tex(r"$a\times b$: area $=|a||b|\sin\theta$, direction by RH rule",
                    font_size=22)
        info = VGroup(
            VGroup(Tex(r"$\theta=$", font_size=22),
                   DecimalNumber(45, num_decimal_places=1,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$|a\times b|=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$|a||b|\sin\theta=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$a\cdot b=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        self.add_fixed_in_frame_mobjects(title, info)
        title.to_edge(UP, buff=0.3)
        info.to_corner(UR, buff=0.3)

        info[0][1].add_updater(lambda m: m.set_value(np.degrees(theta_tr.get_value())))
        info[1][1].add_updater(lambda m: m.set_value(float(np.linalg.norm(np.cross(a, b_vec())))))
        info[2][1].add_updater(lambda m: m.set_value(
            float(np.linalg.norm(a) * np.linalg.norm(b_vec()) * np.sin(theta_tr.get_value()))))
        info[3][1].add_updater(lambda m: m.set_value(float(np.dot(a, b_vec()))))

        self.begin_ambient_camera_rotation(rate=0.05)
        for target in [PI / 2, 2 * PI / 3, PI / 6, 5 * PI / 6, PI / 4]:
            self.play(theta_tr.animate.set_value(target),
                      run_time=2.2, rate_func=smooth)
            self.wait(0.4)
        self.stop_ambient_camera_rotation()
