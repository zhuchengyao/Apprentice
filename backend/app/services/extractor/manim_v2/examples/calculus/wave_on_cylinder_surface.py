from manim import *
import numpy as np


class WaveOnCylinderSurfaceExample(ThreeDScene):
    """
    Wave on a cylinder (from _2023/optics_puzzles/cylinder): a
    traveling wave on the surface of a cylinder of radius R gets
    wrapped around, so horizontal displacement φ behaves like x.
    u(φ, z, t) = A cos(k z - ω t) cos(n φ).

    3D scene:
      Parametric surface whose radial displacement is modulated by
      the wave function; ValueTracker t_tr advances time.
    """

    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=-35 * DEGREES)
        axes = ThreeDAxes(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                           z_range=[-3, 3, 1],
                           x_length=4, y_length=4, z_length=5)
        self.add(axes)

        R = 1.2
        A = 0.25
        k = 2.0
        omega = 1.0
        n = 2  # angular mode number

        t_tr = ValueTracker(0.0)

        def cyl_surface():
            t = t_tr.get_value()

            def param(phi, z):
                r = R + A * np.cos(k * z - omega * t) * np.cos(n * phi)
                x = r * np.cos(phi)
                y = r * np.sin(phi)
                return axes.c2p(x, y, z)

            return Surface(param, u_range=[0, 2 * PI],
                             v_range=[-2.5, 2.5],
                             resolution=(36, 30),
                             fill_opacity=0.85,
                             checkerboard_colors=[BLUE, BLUE_D])

        self.add(always_redraw(cyl_surface))

        title = Tex(r"Wave on cylinder: $u(\phi, z, t) = A\cos(kz - \omega t)\cos(n\phi)$",
                    font_size=22).to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        def panel():
            t = t_tr.get_value()
            return VGroup(
                MathTex(rf"t = {t:.2f}", color=YELLOW, font_size=22),
                MathTex(rf"k = {k},\ \omega = {omega}",
                         color=WHITE, font_size=20),
                MathTex(rf"n = {n}\ \text{{angular modes}}",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DR, buff=0.4)

        p = panel()
        self.add_fixed_in_frame_mobjects(p)

        self.begin_ambient_camera_rotation(rate=0.15)
        self.play(t_tr.animate.set_value(10),
                   run_time=8, rate_func=linear)
        new_p = panel()
        self.add_fixed_in_frame_mobjects(new_p)
        self.play(Transform(p, new_p), run_time=0.2)
        self.stop_ambient_camera_rotation()
        self.wait(0.4)
