from manim import *
import numpy as np


class Orbital3DPzExample(ThreeDScene):
    """
    Hydrogen 2p_z orbital: wave function ψ_{210} ∝ r·e^(-r/2) cos θ.
    Visualize isosurface |ψ|² = const. Two lobes ± along z-axis.

    ThreeDScene: parametric surfaces for upper and lower lobes.
    ValueTracker density_tr controls which isosurface level.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=35 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.06)

        axes = ThreeDAxes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[-3, 3, 1],
                          x_length=4.5, y_length=4.5, z_length=4.5)
        self.add(axes)

        density_tr = ValueTracker(0.3)

        def orbital_2pz(u, v):
            # u = theta in [0, pi]; v = phi in [0, 2pi]
            # Radius as function of theta such that |psi|^2 = const
            c = density_tr.get_value()
            # |ψ|² ∝ r² e^(-r) cos² θ
            # Want r² e^(-r) cos² θ = c² → r solves r² e^(-r) = c² / cos²θ
            cos2 = np.cos(u) ** 2
            if cos2 < 1e-3:
                cos2 = 1e-3
            target = c * c / cos2
            # Solve r² e^(-r) = target numerically via Newton-like
            r = 2.0  # initial guess
            for _ in range(20):
                f = r * r * np.exp(-r) - target
                df = (2 * r - r * r) * np.exp(-r)
                if abs(df) < 1e-6: break
                r = r - f / df
                if r <= 0: r = 0.5
                if r > 10: r = 10
            return np.array([r * np.sin(u) * np.cos(v),
                              r * np.sin(u) * np.sin(v),
                              r * np.cos(u)])

        def upper_lobe():
            return Surface(
                lambda u, v: orbital_2pz(u, v),
                u_range=[0.1, PI / 2 - 0.1],
                v_range=[0, TAU],
                resolution=(16, 28),
                fill_opacity=0.7,
            ).set_color_by_gradient(ORANGE, YELLOW)

        def lower_lobe():
            return Surface(
                lambda u, v: orbital_2pz(u, v),
                u_range=[PI / 2 + 0.1, PI - 0.1],
                v_range=[0, TAU],
                resolution=(16, 28),
                fill_opacity=0.7,
            ).set_color_by_gradient(BLUE, PURPLE)

        self.add(always_redraw(upper_lobe), always_redraw(lower_lobe))

        title = Tex(r"$2p_z$ orbital: $\psi\propto r e^{-r/2}\cos\theta$",
                    font_size=22)
        info = VGroup(
            VGroup(Tex(r"density level $c=$", font_size=22),
                   DecimalNumber(0.3, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"upper lobe $+$ (ORANGE)",
                color=ORANGE, font_size=20),
            Tex(r"lower lobe $-$ (BLUE)",
                color=BLUE, font_size=20),
            Tex(r"nodal plane $z=0$",
                color=GREY_B, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        self.add_fixed_in_frame_mobjects(title, info)
        title.to_edge(UP, buff=0.3)
        info.to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(density_tr.get_value()))

        for d in [0.5, 0.2, 0.1, 0.4]:
            self.play(density_tr.animate.set_value(d),
                      run_time=2.0, rate_func=smooth)
            self.wait(0.5)
        self.stop_ambient_camera_rotation()
