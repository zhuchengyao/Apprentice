from manim import *
import numpy as np


class SphericalLawCosinesExample(ThreeDScene):
    """
    Spherical law of cosines:
       cos a = cos b cos c + sin b sin c cos A,
    where a, b, c are arc-length sides on a unit sphere and A is the
    angle between sides b and c at their common vertex.

    ValueTracker A_tr sweeps the angle A, rotating vertex C around.
    always_redraw rebuilds the spherical triangle (BLUE arcs); live
    panel shows a, b, c (arclengths), A, and LHS = RHS check.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=40 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.05)

        sphere = Sphere(radius=1.0, resolution=(24, 40), fill_opacity=0.15).set_color(BLUE)
        self.add(sphere)

        # Fixed vertex A at (0, 0, 1)
        A = np.array([0.0, 0.0, 1.0])
        # B at longitude 0, latitude some
        b_arclen = 1.0  # fixed
        c_arclen = 0.9
        B = np.array([np.sin(b_arclen), 0, np.cos(b_arclen)])

        angle_A_tr = ValueTracker(PI / 3)

        def C_pt():
            alpha = angle_A_tr.get_value()
            # C is at arclength c from A, in the direction rotated by alpha from B's direction
            # Start: B is at angle 0 longitude. C at angle alpha from A
            # Parametrize C on small circle around A at arclength c_arclen
            # C = cos(c)·A + sin(c)·(cos(alpha)·u + sin(alpha)·v)
            # where (u, v) is orthonormal basis in tangent plane at A with u pointing toward B.
            # Tangent at A pointing toward B: projection of B onto TA = B - (B·A)A
            u = B - (np.dot(B, A)) * A
            u = u / np.linalg.norm(u)
            v = np.cross(A, u)
            return np.cos(c_arclen) * A + np.sin(c_arclen) * (
                np.cos(alpha) * u + np.sin(alpha) * v)

        def great_circle_arc(P, Q, col=BLUE, n=40):
            # renormalize, then interpolate via slerp
            P = P / np.linalg.norm(P)
            Q = Q / np.linalg.norm(Q)
            omega = np.arccos(np.clip(np.dot(P, Q), -1, 1))
            if omega < 1e-6:
                return VMobject()
            pts = []
            for t in np.linspace(0, 1, n):
                s = (np.sin((1 - t) * omega) * P + np.sin(t * omega) * Q) / np.sin(omega)
                pts.append(s)
            return VMobject().set_points_as_corners(pts).set_color(col).set_stroke(width=4)

        def triangle_arcs():
            C = C_pt()
            return VGroup(
                great_circle_arc(A, B, YELLOW),  # side c (between A and B, opposite C)
                great_circle_arc(A, C, GREEN),   # side b
                great_circle_arc(B, C, RED),     # side a
            )

        def vertex_dots():
            C = C_pt()
            return VGroup(
                Dot3D(point=A, color=YELLOW, radius=0.04),
                Dot3D(point=B, color=GREEN, radius=0.04),
                Dot3D(point=C, color=RED, radius=0.04),
            )

        self.add(always_redraw(triangle_arcs), always_redraw(vertex_dots))

        # Arclengths and verification
        def sides():
            C = C_pt()
            def arclen(P, Q):
                return np.arccos(np.clip(np.dot(P, Q), -1, 1))
            return (arclen(B, C), arclen(A, C), arclen(A, B),
                    angle_A_tr.get_value())  # (a, b, c, A)

        def lhs():
            a, b, c, A_ang = sides()
            return np.cos(a)

        def rhs():
            a, b, c, A_ang = sides()
            return np.cos(b) * np.cos(c) + np.sin(b) * np.sin(c) * np.cos(A_ang)

        title = Tex(r"Spherical law of cosines: $\cos a = \cos b\cos c+\sin b\sin c\cos A$",
                    font_size=22)
        panel = VGroup(
            VGroup(Tex(r"$A=$", font_size=22),
                   DecimalNumber(60, num_decimal_places=1,
                                 font_size=22)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$a=$", color=RED, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$b=$", color=GREEN, font_size=22),
                   DecimalNumber(0.9, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$c=$", color=YELLOW, font_size=22),
                   DecimalNumber(1.0, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"LHS $\cos a=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=4,
                                 font_size=22)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"RHS$=$", color=GREEN, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=4,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.17)

        self.add_fixed_in_frame_mobjects(title, panel)
        title.to_edge(UP, buff=0.3)
        panel.to_edge(RIGHT, buff=0.3).shift(DOWN * 0.3)

        def update_nums():
            a, b, c, A_ang = sides()
            panel[0][1].set_value(np.degrees(A_ang))
            panel[1][1].set_value(a)
            panel[4][1].set_value(lhs())
            panel[5][1].set_value(rhs())
            return panel
        panel.add_updater(lambda m, dt: update_nums())

        for target in [PI / 2, 2 * PI / 3, PI / 4, 5 * PI / 6, PI / 3]:
            self.play(angle_A_tr.animate.set_value(target),
                      run_time=2.2, rate_func=smooth)
            self.wait(0.4)
        self.stop_ambient_camera_rotation()
        self.wait(0.5)
