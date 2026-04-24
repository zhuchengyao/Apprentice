from manim import *
import numpy as np


class TorusHomologyExample(ThreeDScene):
    """
    Homology of torus T²: H_0=ℤ, H_1=ℤ², H_2=ℤ. The two generators
    of H_1 are the meridian and longitude circles; they are not
    homologous to a point.

    ThreeDScene: torus + meridian (RED) + longitude (GREEN) + a
    "contractible" small circle (BLUE) that IS homologous to zero.
    ValueTracker s_tr shrinks the contractible circle to a point.
    """

    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.06)

        axes = ThreeDAxes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[-1.5, 1.5, 1],
                          x_length=4.5, y_length=4.5, z_length=3.0)
        self.add(axes)

        R = 2.0
        r = 0.7

        def torus_pt(u, v):
            return np.array([(R + r * np.cos(v)) * np.cos(u),
                              (R + r * np.cos(v)) * np.sin(u),
                              r * np.sin(v)])

        torus = Surface(
            lambda u, v: torus_pt(u, v),
            u_range=[0, TAU], v_range=[0, TAU],
            resolution=(40, 16),
            fill_opacity=0.3,
        ).set_color(BLUE)
        self.add(torus)

        # Meridian (v varies, u fixed) - passes through handle
        meridian = ParametricFunction(
            lambda v: torus_pt(0, v), t_range=[0, TAU],
            color=RED, stroke_width=4,
        )
        self.add(meridian)
        self.add_fixed_in_frame_mobjects(
            Tex(r"meridian (RED)", color=RED, font_size=22).to_corner(UL, buff=0.4))

        # Longitude (u varies, v fixed) - goes around the hole
        longitude = ParametricFunction(
            lambda u: torus_pt(u, 0), t_range=[0, TAU],
            color=GREEN, stroke_width=4,
        )
        self.add(longitude)
        self.add_fixed_in_frame_mobjects(
            Tex(r"longitude (GREEN)", color=GREEN, font_size=22).to_corner(UL, buff=0.4).shift(DOWN * 0.4))

        # Contractible circle
        s_tr = ValueTracker(1.0)  # 1 = full small circle, 0 = point

        def contractible():
            s = s_tr.get_value()
            # small circle at v=0, u varies in small range
            u0 = PI / 2
            v0 = PI / 2
            pts = []
            for phi in np.linspace(0, TAU, 50):
                # small circle in tangent plane
                du = 0.3 * s * np.cos(phi)
                dv = 0.3 * s * np.sin(phi)
                pts.append(torus_pt(u0 + du, v0 + dv))
            return VMobject().set_points_as_corners(pts + [pts[0]])\
                .set_color(YELLOW).set_stroke(width=3)

        self.add(always_redraw(contractible))
        self.add_fixed_in_frame_mobjects(
            Tex(r"contractible (YELLOW)",
                color=YELLOW, font_size=22).to_corner(UL, buff=0.4).shift(DOWN * 0.8))

        info = VGroup(
            Tex(r"$H_0(T^2)=\mathbb{Z}$ (connected)", font_size=20),
            Tex(r"$H_1(T^2)=\mathbb{Z}^2$ (two generators)",
                color=YELLOW, font_size=20),
            Tex(r"$H_2(T^2)=\mathbb{Z}$ (orientable surface)",
                font_size=20),
            Tex(r"$\chi=1-2+1=0$",
                color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        self.add_fixed_in_frame_mobjects(info)
        info.to_corner(DR, buff=0.3)

        title = Tex(r"Torus homology", font_size=26)
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(UP, buff=0.3)

        self.wait(2)
        self.play(s_tr.animate.set_value(0.05),
                  run_time=3, rate_func=smooth)
        self.wait(0.5)
        self.play(s_tr.animate.set_value(1.0),
                  run_time=2, rate_func=smooth)
        self.wait(0.5)
        self.stop_ambient_camera_rotation()
