from manim import *
import numpy as np


class SphericalTriangleExample(ThreeDScene):
    """
    Spherical triangle: angle sum minus π = area of the triangle
    (on unit sphere). For an equilateral spherical triangle with
    side a, angle A satisfies cos A = cos a / (1 + cos a).

    3D scene:
      Unit sphere + spherical triangle with vertices at fixed points;
      ValueTracker vertex_height_tr raises one vertex; always_redraw
      triangle + live angle-sum.
    """

    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=-40 * DEGREES)
        axes = ThreeDAxes(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                           z_range=[-2, 2, 1],
                           x_length=4, y_length=4, z_length=4)
        self.add(axes)

        sphere = Sphere(radius=1.0, resolution=(18, 18),
                          fill_opacity=0.2,
                          color=BLUE_D).move_to(axes.c2p(0, 0, 0))
        self.add(sphere)

        # Two fixed vertices near equator, one variable at top
        A = np.array([1.0, 0.0, 0.0])
        B = np.array([np.cos(2 * PI / 3), np.sin(2 * PI / 3), 0.0])

        h_tr = ValueTracker(0.3)

        def C_pt():
            h = h_tr.get_value()
            # Third vertex varies in height, with x-y computed to stay on sphere
            # Place at azimuth 2π/3 + π/3 with height h
            lat = np.arcsin(h)
            lon = 4 * PI / 3
            return np.array([np.cos(lat) * np.cos(lon),
                             np.cos(lat) * np.sin(lon),
                             h])

        def geodesic_pts(P, Q, n=30):
            theta = np.arccos(np.clip(np.dot(P, Q), -1, 1))
            pts = []
            for s in np.linspace(0, 1, n):
                a = np.sin((1 - s) * theta) / np.sin(theta + 1e-8)
                b = np.sin(s * theta) / np.sin(theta + 1e-8)
                pts.append(a * P + b * Q)
            return pts

        def spherical_tri():
            C = C_pt()
            # Three arcs
            grp = VGroup()
            for (P, Q, col) in [(A, B, RED), (B, C, GREEN), (C, A, YELLOW)]:
                pts = geodesic_pts(P, Q)
                m = VMobject(color=col, stroke_width=4)
                m.set_points_as_corners([axes.c2p(*p) for p in pts])
                grp.add(m)
            # Vertices
            for p, col in [(A, RED), (B, GREEN), (C, YELLOW)]:
                grp.add(Dot3D(axes.c2p(*p), color=col, radius=0.1))
            return grp

        self.add(always_redraw(spherical_tri))

        def angle_at(V, P1, P2):
            # Angle between tangent directions from V to P1 and to P2
            # Tangent from V to P: project (P - V) onto tangent plane at V
            e1 = P1 - V * np.dot(V, P1)
            e2 = P2 - V * np.dot(V, P2)
            e1n = e1 / (np.linalg.norm(e1) + 1e-8)
            e2n = e2 / (np.linalg.norm(e2) + 1e-8)
            return np.arccos(np.clip(np.dot(e1n, e2n), -1, 1))

        title = Tex(r"Spherical triangle: $\alpha + \beta + \gamma - \pi = $ area",
                    font_size=22).to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        def panel():
            C = C_pt()
            alpha = angle_at(A, B, C)
            beta = angle_at(B, A, C)
            gamma = angle_at(C, A, B)
            excess = alpha + beta + gamma - PI
            # Area = excess for unit sphere
            return VGroup(
                MathTex(rf"\alpha = {np.degrees(alpha):.1f}^\circ",
                         color=RED, font_size=20),
                MathTex(rf"\beta = {np.degrees(beta):.1f}^\circ",
                         color=GREEN, font_size=20),
                MathTex(rf"\gamma = {np.degrees(gamma):.1f}^\circ",
                         color=YELLOW, font_size=20),
                MathTex(rf"\text{{excess}} = {np.degrees(excess):.1f}^\circ",
                         color=ORANGE, font_size=20),
                MathTex(rf"\text{{area}} = {excess:.3f}",
                         color=ORANGE, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.13).to_corner(DR, buff=0.4)

        pnl = panel()
        self.add_fixed_in_frame_mobjects(pnl)

        self.begin_ambient_camera_rotation(rate=0.15)
        for hv in [0.6, 0.9, 0.3]:
            self.play(h_tr.animate.set_value(hv),
                       run_time=2, rate_func=smooth)
            new_pnl = panel()
            self.add_fixed_in_frame_mobjects(new_pnl)
            self.play(Transform(pnl, new_pnl), run_time=0.2)
            self.wait(0.5)
        self.stop_ambient_camera_rotation()
