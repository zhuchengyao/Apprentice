from manim import *
import numpy as np


class ParametricSurfaceJacobianExample(ThreeDScene):
    """
    Surface area via parametric Jacobian: for r(u, v),
       A = ∫∫ |r_u × r_v| dA.
    Example: unit hemisphere r(u, v) = (sin u cos v, sin u sin v, cos u),
    u ∈ [0, π/2], v ∈ [0, 2π]. A = 2π.

    ThreeDScene: hemisphere with a grid patch highlighted. ValueTracker
    (u0, v0) moves highlighted patch with always_redraw |r_u × r_v|
    live readout.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=35 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.05)

        axes = ThreeDAxes(x_range=[-1.5, 1.5, 1], y_range=[-1.5, 1.5, 1], z_range=[0, 1.5, 0.5],
                          x_length=4.0, y_length=4.0, z_length=2.5)
        self.add(axes)

        hemi = Surface(
            lambda u, v: np.array([np.sin(u) * np.cos(v),
                                    np.sin(u) * np.sin(v),
                                    np.cos(u)]),
            u_range=[0.01, PI / 2 - 0.01], v_range=[0, TAU],
            resolution=(20, 32),
            fill_opacity=0.35,
        ).set_color(BLUE)
        self.add(hemi)

        u_tr = ValueTracker(PI / 4)
        v_tr = ValueTracker(PI / 3)

        def r(u, v):
            return np.array([np.sin(u) * np.cos(v),
                              np.sin(u) * np.sin(v),
                              np.cos(u)])

        def r_u(u, v):
            return np.array([np.cos(u) * np.cos(v),
                              np.cos(u) * np.sin(v),
                              -np.sin(u)])

        def r_v(u, v):
            return np.array([-np.sin(u) * np.sin(v),
                              np.sin(u) * np.cos(v),
                              0])

        def patch():
            u0, v0 = u_tr.get_value(), v_tr.get_value()
            du, dv = 0.25, 0.4
            corners = [r(u0, v0),
                        r(u0 + du, v0),
                        r(u0 + du, v0 + dv),
                        r(u0, v0 + dv)]
            return Polygon(*corners, color=YELLOW, stroke_width=3,
                            fill_color=YELLOW, fill_opacity=0.6)

        def ru_arrow():
            u0, v0 = u_tr.get_value(), v_tr.get_value()
            p = r(u0, v0)
            return Arrow3D(start=p, end=p + 0.4 * r_u(u0, v0),
                            color=GREEN, thickness=0.02)

        def rv_arrow():
            u0, v0 = u_tr.get_value(), v_tr.get_value()
            p = r(u0, v0)
            return Arrow3D(start=p, end=p + 0.4 * r_v(u0, v0),
                            color=ORANGE, thickness=0.02)

        def normal_arrow():
            u0, v0 = u_tr.get_value(), v_tr.get_value()
            p = r(u0, v0)
            n = np.cross(r_u(u0, v0), r_v(u0, v0))
            return Arrow3D(start=p, end=p + 0.6 * n,
                            color=RED, thickness=0.025)

        self.add(always_redraw(patch), always_redraw(ru_arrow),
                 always_redraw(rv_arrow), always_redraw(normal_arrow))

        title = Tex(r"Surface area: $A=\iint|r_u\times r_v|\,du\,dv$",
                    font_size=24)
        info = VGroup(
            VGroup(Tex(r"$u=$", font_size=22),
                   DecimalNumber(PI / 4, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$v=$", font_size=22),
                   DecimalNumber(PI / 3, num_decimal_places=3,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$|r_u\times r_v|=\sin u=$", font_size=22),
                   DecimalNumber(0.707, num_decimal_places=4,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
            Tex(r"$A=\int_0^{2\pi}\int_0^{\pi/2}\sin u\,du\,dv=2\pi$",
                color=YELLOW, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        self.add_fixed_in_frame_mobjects(title, info)
        title.to_edge(UP, buff=0.3)
        info.to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(u_tr.get_value()))
        info[1][1].add_updater(lambda m: m.set_value(v_tr.get_value()))
        info[2][1].add_updater(lambda m: m.set_value(
            float(np.linalg.norm(np.cross(
                r_u(u_tr.get_value(), v_tr.get_value()),
                r_v(u_tr.get_value(), v_tr.get_value()))))))

        # Sweep patch around
        for (u, v) in [(PI / 3, PI), (PI / 6, 3 * PI / 2), (PI / 2 - 0.1, PI / 4),
                       (PI / 4, PI / 3)]:
            self.play(u_tr.animate.set_value(u),
                      v_tr.animate.set_value(v),
                      run_time=2.0, rate_func=smooth)
            self.wait(0.4)
        self.stop_ambient_camera_rotation()
