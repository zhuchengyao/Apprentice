from manim import *
import numpy as np


class FrenetSerretFramesExample(ThreeDScene):
    """
    Frenet-Serret frame on a helix r(t) = (cos t, sin t, 0.3 t):
        T = r'/|r'|, N = T'/|T'|, B = T × N.

    ValueTracker t_tr sweeps 0 → 4π; always_redraw draws T (RED),
    N (GREEN), B (BLUE) arrows at current point + persistent helix
    trace. Fixed-in-frame panel shows live curvature κ and torsion τ,
    both constant for a helix.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=45 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.06)

        axes = ThreeDAxes(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                          z_range=[0, 4, 1], x_length=4, y_length=4, z_length=4)
        self.add(axes)

        def r(t):
            return np.array([np.cos(t), np.sin(t), 0.3 * t])

        def T_vec(t):
            d = np.array([-np.sin(t), np.cos(t), 0.3])
            return d / np.linalg.norm(d)

        def N_vec(t):
            # curvature vector = dT/ds; here compute dT/dt then normalize
            dT = np.array([-np.cos(t), -np.sin(t), 0.0])
            return dT / np.linalg.norm(dT)

        def B_vec(t):
            return np.cross(T_vec(t), N_vec(t))

        helix = ParametricFunction(lambda t: r(t),
                                    t_range=[0, 4 * PI], color=GREY_B, stroke_width=2)
        self.add(helix)

        t_tr = ValueTracker(0.0)

        def T_arrow():
            t = t_tr.get_value()
            p = r(t)
            return Arrow3D(start=p, end=p + 0.7 * T_vec(t),
                           color=RED, thickness=0.022)

        def N_arrow():
            t = t_tr.get_value()
            p = r(t)
            return Arrow3D(start=p, end=p + 0.7 * N_vec(t),
                           color=GREEN, thickness=0.022)

        def B_arrow():
            t = t_tr.get_value()
            p = r(t)
            return Arrow3D(start=p, end=p + 0.7 * B_vec(t),
                           color=BLUE, thickness=0.022)

        def trace():
            t = t_tr.get_value()
            if t < 0.02:
                return VMobject()
            return ParametricFunction(r, t_range=[0, t],
                                       color=YELLOW, stroke_width=4)

        def pt_dot():
            t = t_tr.get_value()
            return Dot3D(point=r(t), color=YELLOW, radius=0.08)

        self.add(always_redraw(T_arrow), always_redraw(N_arrow),
                 always_redraw(B_arrow), always_redraw(trace),
                 always_redraw(pt_dot))

        # For r(t)=(cos t, sin t, bt), |r'|=√(1+b²), κ=1/(1+b²), τ=b/(1+b²)
        b = 0.3
        kappa = 1 / (1 + b ** 2)
        tau = b / (1 + b ** 2)

        title = Tex(r"Frenet–Serret frame on helix $r=(\cos t, \sin t, 0.3t)$",
                    font_size=24)
        panel = VGroup(
            Tex(r"\textcolor{red}{T}, \textcolor{green}{N}, \textcolor{blue}{B}",
                font_size=22),
            Tex(rf"$\kappa={kappa:.4f}$ (constant)", color=GREEN, font_size=22),
            Tex(rf"$\tau={tau:.4f}$ (constant)", color=BLUE, font_size=22),
            Tex(r"$T'=\kappa N,\ N'=-\kappa T+\tau B,\ B'=-\tau N$",
                font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        self.add_fixed_in_frame_mobjects(title, panel)
        title.to_edge(UP, buff=0.3)
        panel.to_corner(UR, buff=0.35)

        self.play(t_tr.animate.set_value(4 * PI),
                  run_time=8, rate_func=linear)
        self.wait(0.8)
        self.stop_ambient_camera_rotation()
