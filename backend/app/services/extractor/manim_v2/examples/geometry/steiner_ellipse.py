from manim import *
import numpy as np


class SteinerEllipseExample(Scene):
    """
    Steiner's inellipse: unique ellipse inscribed in a triangle,
    tangent to each side at its midpoint, with center = centroid.
    Has max area among inscribed ellipses.

    SINGLE_FOCUS:
      Variable-apex triangle + always_redraw Steiner inellipse
      computed via centroid + affine transformation of unit circle.
    """

    def construct(self):
        title = Tex(r"Steiner inellipse: tangent to sides at midpoints",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        A = np.array([-2.5, -1.3, 0])
        B = np.array([2.5, -1.3, 0])

        theta_tr = ValueTracker(100 * DEGREES)

        def C_pt():
            t = theta_tr.get_value()
            return np.array([0.7 * np.cos(t),
                              1.3 + 2.0 * np.sin(t), 0])

        def geom():
            C = C_pt()
            centroid = (A + B + C) / 3
            # Midpoints of sides
            M_AB = (A + B) / 2
            M_BC = (B + C) / 2
            M_CA = (C + A) / 2

            # Steiner inellipse is image of a specific inscribed
            # circle under an affine map; easier to compute via
            # parametric formula:
            # Points on the inellipse are (in barycentric-ish form):
            #   P(t) = centroid + (1/3)[(A-centroid) cos t + (B-centroid - A_proj) sin t ... ]
            # Simpler: the Steiner inellipse is the image of the unit
            # circle under the affine map whose image at 0 is the centroid
            # and at the vertices of a reference equilateral triangle
            # are the triangle vertices A, B, C.
            # Equilateral reference: v_i = (cos(2πi/3 + π/2), sin(2πi/3 + π/2))
            # Steiner ellipse from centroid using:
            # semi-axes derived from (A-centroid) and (B-centroid)
            u = (A - centroid)[:2]
            v = (B - centroid)[:2]
            # Parametrize: point = centroid + (u cos t + v sin t)/√3 * (1/r) — actually the
            # standard formula uses the affine map T where the equilateral triangle
            # maps to ABC. For simplicity, sample many points:
            pts = []
            for s in np.linspace(0, 2 * PI, 120):
                # Parametrize the inscribed ellipse using the affine approach:
                # inscribed ellipse = image of unit circle under T(x, y) = centroid + (u cos(ang)/√3 + v sin(ang)/√3)
                # Actually the inscribed Steiner ellipse has semi-major along the longest median direction.
                # A cleaner formula: center at centroid, parametric:
                # P(s) = centroid + r · (cos(s) · d1 + sin(s) · d2)
                # where d1, d2 derived from triangle vertices.
                # We use the fact: Steiner inellipse = image of unit-circle under the affine map that
                # sends (1, 0) and (-1/2, √3/2) to A-centroid and B-centroid:
                # compute T mapping equilateral to ABC, then scale by 1/3
                # v1_ref = (1, 0), v2_ref = (-1/2, √3/2); A-cent = u, B-cent = v
                # T maps v1_ref to u, v2_ref to v. So for unit circle point (cos s, sin s):
                # T(cos s, sin s) = α·cos s + β·sin s where α = (?)...
                # Simpler: use α_mat inverse
                v1_ref = np.array([1.0, 0.0])
                v2_ref = np.array([-0.5, np.sqrt(3) / 2])
                M_ref = np.column_stack([v1_ref, v2_ref])
                M_tri = np.column_stack([u, v])
                T_mat = M_tri @ np.linalg.inv(M_ref)
                scaled = (1 / np.sqrt(3)) * T_mat @ np.array([np.cos(s), np.sin(s)])
                p = centroid[:2] + scaled
                pts.append(np.array([p[0], p[1], 0]))

            grp = VGroup()
            grp.add(Polygon(A, B, C, color=YELLOW,
                              fill_opacity=0.15, stroke_width=3))
            ellipse = VMobject(color=GREEN, fill_opacity=0.3,
                                 stroke_width=3)
            ellipse.set_points_as_corners(pts + [pts[0]])
            grp.add(ellipse)

            # Midpoint dots
            for p in [M_AB, M_BC, M_CA]:
                grp.add(Dot(p, color=RED, radius=0.08))
            # Centroid
            grp.add(Dot(centroid, color=BLUE, radius=0.1))
            return grp

        self.add(always_redraw(geom))

        info = VGroup(
            Tex(r"GREEN: Steiner inellipse", color=GREEN, font_size=20),
            Tex(r"RED: side midpoints (tangent pts)",
                 color=RED, font_size=18),
            Tex(r"BLUE: centroid (ellipse center)",
                 color=BLUE, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.3)
        self.play(Write(info))

        for deg in [80, 130, 60, 100, 140]:
            self.play(theta_tr.animate.set_value(deg * DEGREES),
                       run_time=1.5, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
