from manim import *
import numpy as np


class TemperatureSurface3DExample(ThreeDScene):
    """
    Heat equation evolution on a 1D rod visualized as a 3D surface
    u(x, t) (from _2019/diffyq/part4/three_d_graphs): time axis grows
    into the page; the initial square profile smooths as t → ∞.

    3D scene:
      Parametric surface (x, t, u(x, t)) with u evolving via 10-mode
      Fourier sum; ValueTracker t_max_tr extends the time axis;
      always_redraw Surface.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-55 * DEGREES)
        axes = ThreeDAxes(x_range=[0, 1, 0.25], y_range=[0, 150, 30],
                           z_range=[-0.2, 1.2, 0.5],
                           x_length=4, y_length=5, z_length=3)
        self.add(axes)

        L = 1.0
        alpha = 0.01

        def coef(n):
            return 2 / (n * PI) * (np.cos(0.3 * n * PI) - np.cos(0.7 * n * PI))

        N_modes = 10
        a = np.array([coef(n + 1) for n in range(N_modes)])

        def u(x, t):
            return float(np.sum([
                a[n - 1] * np.sin(n * PI * x / L)
                * np.exp(-alpha * (n * PI / L) ** 2 * t)
                for n in range(1, N_modes + 1)]))

        t_max_tr = ValueTracker(5)

        def surface():
            T = t_max_tr.get_value()

            def param(x, t):
                return axes.c2p(x, t, u(x, t))

            return Surface(param, u_range=[0, 1],
                             v_range=[0, T],
                             resolution=(20, max(10, int(T / 3))),
                             fill_opacity=0.8,
                             checkerboard_colors=[RED, ORANGE])

        self.add(always_redraw(surface))

        title = Tex(r"Heat-equation temperature $u(x, t)$ as a 3D surface",
                    font_size=24).to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        def panel():
            T = t_max_tr.get_value()
            return VGroup(
                MathTex(rf"t_{{\max}} = {T:.0f}", color=YELLOW, font_size=22),
                Tex(r"higher modes decay faster",
                     color=GREEN, font_size=20),
                MathTex(r"u_t = \alpha u_{xx}", color=RED, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DR, buff=0.4)

        p = panel()
        self.add_fixed_in_frame_mobjects(p)

        self.begin_ambient_camera_rotation(rate=0.1)
        self.play(t_max_tr.animate.set_value(150),
                   run_time=8, rate_func=smooth)
        new_p = panel()
        self.add_fixed_in_frame_mobjects(new_p)
        self.play(Transform(p, new_p), run_time=0.2)
        self.stop_ambient_camera_rotation()
        self.wait(0.5)
