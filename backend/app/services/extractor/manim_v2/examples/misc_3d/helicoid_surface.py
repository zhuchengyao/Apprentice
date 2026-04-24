from manim import *
import numpy as np


class HelicoidSurfaceExample(ThreeDScene):
    """
    Helicoid: a minimal surface (zero mean curvature) parametrized by
    (u cos v, u sin v, cv). Connects to catenoid via isometric
    deformation family.

    3D scene:
      Helicoid surface with variable pitch c; ValueTracker c_tr sweeps
      pitch. Ambient camera rotation.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-35 * DEGREES)
        axes = ThreeDAxes(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                           z_range=[-2, 2, 1],
                           x_length=4, y_length=4, z_length=4)
        self.add(axes)

        c_tr = ValueTracker(0.4)

        def helicoid_surface():
            c = c_tr.get_value()

            def param(u, v):
                return axes.c2p(u * np.cos(v),
                                 u * np.sin(v),
                                 c * v)

            return Surface(param, u_range=[-1.5, 1.5],
                             v_range=[-2 * PI, 2 * PI],
                             resolution=(10, 40),
                             fill_opacity=0.65,
                             checkerboard_colors=[BLUE, PURPLE])

        self.add(always_redraw(helicoid_surface))

        title = Tex(r"Helicoid: $(u\cos v,\ u\sin v,\ c v)$ — minimal surface",
                    font_size=22).to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        def panel():
            c = c_tr.get_value()
            return VGroup(
                MathTex(rf"c = {c:.2f}", color=YELLOW, font_size=24),
                Tex(r"minimal (mean curvature = 0)",
                     color=GREEN, font_size=20),
                Tex(r"isometric to catenoid",
                     color=WHITE, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DR, buff=0.4)

        pnl = panel()
        self.add_fixed_in_frame_mobjects(pnl)

        self.begin_ambient_camera_rotation(rate=0.15)
        for cv in [0.8, 1.2, 0.2, 0.5]:
            self.play(c_tr.animate.set_value(cv),
                       run_time=1.8, rate_func=smooth)
            new_pnl = panel()
            self.add_fixed_in_frame_mobjects(new_pnl)
            self.play(Transform(pnl, new_pnl), run_time=0.2)
            self.wait(0.4)
        self.stop_ambient_camera_rotation()
