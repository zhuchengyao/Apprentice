from manim import *
import numpy as np


class TorusSurfaceExample(ThreeDScene):
    """
    Torus parametrization: ValueTrackers R (major radius) and r (minor)
    morph the torus from a thin ring to a fat doughnut.

    ThreeDScene:
      A torus surface is built via Surface; ValueTrackers R, r drive
      the parametrization. always_redraw rebuilds the surface each
      frame as R, r sweep through several configs. A guide circle
      shows the major (centerline) ring and a perpendicular small
      circle the minor cross-section.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-40 * DEGREES)

        title = Tex(r"Torus: $(R + r\cos v)\,\hat\rho + r\sin v\,\hat z$",
                    font_size=24)
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = ThreeDAxes(x_range=[-3.5, 3.5, 1], y_range=[-3.5, 3.5, 1],
                          z_range=[-2, 2, 1])
        self.add(axes)

        R_tr = ValueTracker(2.0)
        r_tr = ValueTracker(0.7)

        def torus_surface():
            R, r = R_tr.get_value(), r_tr.get_value()
            return Surface(
                lambda u, v: np.array([
                    (R + r * np.cos(v)) * np.cos(u),
                    (R + r * np.cos(v)) * np.sin(u),
                    r * np.sin(v),
                ]),
                u_range=[0, 2 * PI], v_range=[0, 2 * PI],
                resolution=(28, 12),
                fill_opacity=0.65,
                checkerboard_colors=[BLUE_D, TEAL],
                stroke_width=0.5,
            )

        torus = always_redraw(torus_surface)
        self.add(torus)

        # Guide circles
        def major_circle():
            R = R_tr.get_value()
            return ParametricFunction(
                lambda t: np.array([R * np.cos(t), R * np.sin(t), 0]),
                t_range=[0, 2 * PI],
                color=YELLOW, stroke_width=3,
            )

        def minor_circle():
            R, r = R_tr.get_value(), r_tr.get_value()
            return ParametricFunction(
                lambda t: np.array([R + r * np.cos(t),
                                    0,
                                    r * np.sin(t)]),
                t_range=[0, 2 * PI],
                color=ORANGE, stroke_width=3,
            )

        self.add(always_redraw(major_circle), always_redraw(minor_circle))

        # Right-corner readouts (fixed in frame)
        def info_panel():
            R, r = R_tr.get_value(), r_tr.get_value()
            volume = 2 * PI * PI * R * r * r
            surface_area = 4 * PI * PI * R * r
            return VGroup(
                MathTex(rf"R = {R:.2f}", color=YELLOW, font_size=22),
                MathTex(rf"r = {r:.2f}", color=ORANGE, font_size=22),
                MathTex(rf"V = 2\pi^2 R r^2 \approx {volume:.2f}",
                        color=WHITE, font_size=20),
                MathTex(rf"A = 4\pi^2 R r \approx {surface_area:.2f}",
                        color=WHITE, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UR).shift(LEFT * 0.3 + DOWN * 0.5)

        info = always_redraw(info_panel)
        self.add_fixed_in_frame_mobjects(info)
        # add_fixed_in_frame_mobjects on a redrawable would be tricky;
        # redraw runs but in 2D — that's OK because info is built from MathTex (2D)

        # Sweep through 4 (R, r) configs
        for R_v, r_v in [(2.5, 0.5), (1.5, 1.2), (3.0, 0.4), (2.0, 0.8)]:
            self.play(R_tr.animate.set_value(R_v),
                      r_tr.animate.set_value(r_v),
                      run_time=2.5, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.6)
