from manim import *
import numpy as np


class TorusKnotsExample(ThreeDScene):
    """
    Torus knot T(p, q): curve that winds p times around the "big"
    circle and q times around the "small" circle of a torus.
    Examples: T(2, 3) = trefoil, T(3, 2) same knot.

    3D scene:
      Toroidal surface + ValueTracker t_tr traces the knot on it;
      always_redraw the knot curve; ambient camera rotation. State
      cycles through T(2, 3) and T(3, 2) via Transform.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-40 * DEGREES)
        axes = ThreeDAxes(x_range=[-3, 3, 1], y_range=[-3, 3, 1],
                           z_range=[-1.5, 1.5, 1],
                           x_length=4, y_length=4, z_length=2.5)
        self.add(axes)

        R_outer = 1.8
        r_inner = 0.6

        # Torus surface
        def torus_param(u, v):
            x = (R_outer + r_inner * np.cos(v)) * np.cos(u)
            y = (R_outer + r_inner * np.cos(v)) * np.sin(u)
            z = r_inner * np.sin(v)
            return axes.c2p(x, y, z)

        torus = Surface(torus_param, u_range=[0, 2 * PI],
                          v_range=[0, 2 * PI],
                          resolution=(30, 15),
                          fill_opacity=0.15,
                          checkerboard_colors=[GREY, GREY_B])
        self.add(torus)

        state = {"p": 2, "q": 3}
        t_tr = ValueTracker(0.001)

        def knot_curve():
            t_cur = t_tr.get_value()
            p, q = state["p"], state["q"]
            pts = []
            for s in np.linspace(0, t_cur, max(10, int(200 * t_cur / (2 * PI)))):
                u = p * s
                v = q * s
                x = (R_outer + r_inner * np.cos(v)) * np.cos(u)
                y = (R_outer + r_inner * np.cos(v)) * np.sin(u)
                z = r_inner * np.sin(v)
                pts.append(axes.c2p(x, y, z))
            m = VMobject(color=YELLOW, stroke_width=4)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        def knot_head():
            t_cur = t_tr.get_value()
            p, q = state["p"], state["q"]
            u = p * t_cur
            v = q * t_cur
            x = (R_outer + r_inner * np.cos(v)) * np.cos(u)
            y = (R_outer + r_inner * np.cos(v)) * np.sin(u)
            z = r_inner * np.sin(v)
            return Dot3D(axes.c2p(x, y, z), color=RED, radius=0.1)

        self.add(always_redraw(knot_curve), always_redraw(knot_head))

        title = Tex(r"Torus knot $T(p, q)$",
                    font_size=28).to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        def panel():
            p, q = state["p"], state["q"]
            return VGroup(
                MathTex(rf"T({p}, {q})", color=YELLOW, font_size=26),
                Tex(r"trefoil" if (p, q) == (2, 3) else "variant",
                     color=GREEN, font_size=20),
                Tex(rf"wraps ${p}\times$ big, ${q}\times$ small",
                     color=WHITE, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)

        pnl = panel()
        pnl.to_corner(DR, buff=0.4)
        self.add_fixed_in_frame_mobjects(pnl)

        self.begin_ambient_camera_rotation(rate=0.15)
        self.play(t_tr.animate.set_value(2 * PI), run_time=5, rate_func=linear)
        self.wait(0.4)

        # Switch to T(3, 2)
        state["p"] = 3
        state["q"] = 2
        new_pnl = panel()
        new_pnl.to_corner(DR, buff=0.4)
        self.add_fixed_in_frame_mobjects(new_pnl)
        self.play(Transform(pnl, new_pnl), run_time=0.2)
        t_tr.set_value(0.001)
        self.play(t_tr.animate.set_value(2 * PI), run_time=5, rate_func=linear)
        self.stop_ambient_camera_rotation()
        self.wait(0.4)
