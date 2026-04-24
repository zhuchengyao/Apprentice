from manim import *
import numpy as np


class MobiusStripExample(ThreeDScene):
    """
    Möbius strip: non-orientable. Parametrization
        r(u, v) = ((1 + v cos(u/2)) cos u, (1 + v cos(u/2)) sin u, v sin(u/2))
    with u ∈ [0, 2π], v ∈ [-0.3, 0.3].

    Phase 1: build the strip surface with ValueTracker u_max sweeping
    2π so it grows. Phase 2: a GREEN normal arrow at u=u_tr walks
    around the strip; after one full revolution the normal points the
    opposite direction — the tell-tale sign of non-orientability.
    """

    def construct(self):
        self.set_camera_orientation(phi=68 * DEGREES, theta=45 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.05)

        def R(u, v):
            return np.array([(1 + v * np.cos(u / 2)) * np.cos(u),
                              (1 + v * np.cos(u / 2)) * np.sin(u),
                              v * np.sin(u / 2)])

        u_max_tr = ValueTracker(0.2)

        def strip():
            return Surface(
                lambda u, v: R(u, v),
                u_range=[0, u_max_tr.get_value()], v_range=[-0.3, 0.3],
                resolution=(48, 8), fill_opacity=0.65,
            ).set_color(BLUE)

        self.add(always_redraw(strip))

        title = Tex(r"Möbius strip: $r(u,v)=\big((1+v\cos\tfrac{u}{2})\cos u,\;(1+v\cos\tfrac{u}{2})\sin u,\;v\sin\tfrac{u}{2}\big)$",
                    font_size=22)
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(UP, buff=0.3)

        self.play(u_max_tr.animate.set_value(TAU),
                  run_time=4, rate_func=smooth)
        self.wait(0.5)

        # Phase 2: moving normal probe
        u_probe = ValueTracker(0.0)

        def r_u(u, v):
            return np.array([-np.sin(u) * (1 + v * np.cos(u / 2))
                              - 0.5 * v * np.sin(u / 2) * np.cos(u),
                              np.cos(u) * (1 + v * np.cos(u / 2))
                              - 0.5 * v * np.sin(u / 2) * np.sin(u),
                              0.5 * v * np.cos(u / 2)])

        def r_v(u, v):
            return np.array([np.cos(u / 2) * np.cos(u),
                              np.cos(u / 2) * np.sin(u),
                              np.sin(u / 2)])

        def normal_arrow():
            u = u_probe.get_value()
            p = R(u, 0.0)
            n = np.cross(r_u(u, 0.0), r_v(u, 0.0))
            n = n / (np.linalg.norm(n) + 1e-9)
            return Arrow3D(start=p, end=p + 0.7 * n, color=GREEN, thickness=0.03)

        def probe_dot():
            u = u_probe.get_value()
            return Dot3D(point=R(u, 0.0), color=YELLOW, radius=0.08)

        self.add(always_redraw(normal_arrow), always_redraw(probe_dot))

        note = Tex(r"After one loop ($u:0\!\to\!2\pi$), the normal flips $\Rightarrow$ non-orientable",
                   font_size=22, color=YELLOW)
        self.add_fixed_in_frame_mobjects(note)
        note.to_edge(DOWN, buff=0.3)

        self.play(u_probe.animate.set_value(TAU),
                  run_time=6, rate_func=linear)
        self.wait(1.0)
        self.stop_ambient_camera_rotation()
