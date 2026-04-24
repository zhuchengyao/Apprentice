from manim import *
import numpy as np


class MorleyMiracleExample(Scene):
    """
    Morley's miracle: in any triangle, the three angle trisectors
    closest to each side form an equilateral triangle (Morley
    triangle).

    SINGLE_FOCUS:
      Variable-apex triangle ABC with trisectors; ValueTracker
      theta_tr moves apex; always_redraw the 6 trisectors and the
      GREEN equilateral Morley triangle formed by adjacent-trisector
      intersections.
    """

    def construct(self):
        title = Tex(r"Morley: adjacent trisectors meet at an equilateral triangle",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        A = np.array([-2.5, -1.5, 0])
        B = np.array([2.5, -1.5, 0])

        theta_tr = ValueTracker(110 * DEGREES)

        def C_pt():
            t = theta_tr.get_value()
            return np.array([0.5 * np.cos(t),
                              1.2 + 2.5 * np.sin(t), 0])

        def trisector_intersections():
            C = C_pt()
            # Angles at each vertex
            def vertex_angle(V, P1, P2):
                v1 = P1 - V
                v2 = P2 - V
                return np.arccos(np.dot(v1, v2) /
                                    (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-8))

            alpha = vertex_angle(A, B, C)
            beta = vertex_angle(B, A, C)
            gamma = vertex_angle(C, A, B)

            # Trisector from A toward BC side: direction AB rotated by
            # alpha/3 toward AC (the near-BC trisector is the one closest to BC)
            def rotate(v, ang):
                c, s = np.cos(ang), np.sin(ang)
                return np.array([c * v[0] - s * v[1], s * v[0] + c * v[1], 0])

            # From A, AB direction
            AB_dir = (B - A) / np.linalg.norm(B - A)
            AC_dir = (C - A) / np.linalg.norm(C - A)

            # Trisector near BC: the one at 2/3 of angle from AB toward AC
            # (other option is 1/3)
            # For Morley, we want the trisector CLOSEST to the opposite side BC
            # - from A: the one rotated 2α/3 from AB toward AC
            # Cross product sign determines direction
            cross_AB_AC = AB_dir[0] * AC_dir[1] - AB_dir[1] * AC_dir[0]
            sign = 1 if cross_AB_AC > 0 else -1
            tri_A_near_BC = rotate(AB_dir, sign * 2 * alpha / 3)
            tri_A_far = rotate(AB_dir, sign * alpha / 3)

            # From B, BA direction
            BA_dir = (A - B) / np.linalg.norm(A - B)
            BC_dir = (C - B) / np.linalg.norm(C - B)
            cross_BA_BC = BA_dir[0] * BC_dir[1] - BA_dir[1] * BC_dir[0]
            sign_B = 1 if cross_BA_BC > 0 else -1
            tri_B_near_AC = rotate(BA_dir, sign_B * 2 * beta / 3)
            tri_B_far = rotate(BA_dir, sign_B * beta / 3)

            # Actually the trisector pair for Morley is:
            # From A: near BC (rotate from AB by 2α/3 toward AC — same as from AC by α/3 toward AB)
            # Hmm, let's reformulate: for Morley, pair up trisectors
            # as follows: at each vertex, take the two trisectors.
            # At A: two lines at angles α/3 and 2α/3 from AB toward AC
            # The trisector "adjacent to side BC" (i.e., closer to side BC) is the one at 2α/3 from AB
            # (which is α/3 from AC).
            # At B: trisector adjacent to CA is at 2β/3 from BA.
            # At C: trisector adjacent to AB is at 2γ/3 from CB.

            # Morley triangle vertices: intersections of pairs of
            # ADJACENT trisectors from the two vertices OPPOSITE the side.
            # Vertex near BC: intersect (A's trisector near BC) and (B's trisector near CA)
            # But these are NOT adjacent; Morley is adjacent trisectors of the same side.
            #
            # Simpler Morley formulation: For each side (say AB), consider the
            # trisector from A closest to AB and from B closest to AB. They meet
            # at a point. The 3 such points form the Morley triangle.

            # From A, trisector CLOSEST to AB: the one at α/3 from AB = the "near-AB" trisector
            # From B, trisector closest to AB: at β/3 from BA
            tri_A_near_AB = rotate(AB_dir, sign * alpha / 3)
            tri_B_near_AB = rotate(BA_dir, sign_B * beta / 3)

            # From B, trisector closest to BC: at β/3 from BC
            tri_B_near_BC = rotate(BC_dir, -sign_B * beta / 3)
            # From C, trisector closest to BC: at γ/3 from CB
            CA_dir = (A - C) / np.linalg.norm(A - C)
            CB_dir = (B - C) / np.linalg.norm(B - C)
            cross_CB_CA = CB_dir[0] * CA_dir[1] - CB_dir[1] * CA_dir[0]
            sign_C = 1 if cross_CB_CA > 0 else -1
            tri_C_near_BC = rotate(CB_dir, sign_C * gamma / 3)

            # From C, trisector closest to CA: at γ/3 from CA
            tri_C_near_CA = rotate(CA_dir, -sign_C * gamma / 3)
            # From A, trisector closest to CA: at α/3 from AC
            tri_A_near_CA = rotate(AC_dir, -sign * alpha / 3)

            # Line intersect
            def line_inter(P1, d1, P2, d2):
                denom = d1[0] * d2[1] - d1[1] * d2[0]
                if abs(denom) < 1e-8:
                    return (A + B + C) / 3
                t1 = ((P2[0] - P1[0]) * d2[1] - (P2[1] - P1[1]) * d2[0]) / denom
                return P1 + t1 * d1

            # Vertex of Morley triangle opposite side AB:
            # intersection of (A's trisector near AB) and (B's trisector near AB)
            # Actually these two meet at a single point; that's one Morley vertex.
            M_AB = line_inter(A, tri_A_near_AB, B, tri_B_near_AB)
            M_BC = line_inter(B, tri_B_near_BC, C, tri_C_near_BC)
            M_CA = line_inter(C, tri_C_near_CA, A, tri_A_near_CA)

            return C, M_AB, M_BC, M_CA

        def geom():
            C, M_AB, M_BC, M_CA = trisector_intersections()
            grp = VGroup()
            # Triangle
            grp.add(Polygon(A, B, C, color=YELLOW,
                              fill_opacity=0.1, stroke_width=3))
            # Morley triangle
            grp.add(Polygon(M_AB, M_BC, M_CA, color=GREEN,
                              fill_opacity=0.55, stroke_width=3))
            # Morley vertex dots
            for p in [M_AB, M_BC, M_CA]:
                grp.add(Dot(p, color=GREEN, radius=0.09))
            return grp

        self.add(always_redraw(geom))

        def info():
            C, M_AB, M_BC, M_CA = trisector_intersections()
            d1 = np.linalg.norm(M_AB - M_BC)
            d2 = np.linalg.norm(M_BC - M_CA)
            d3 = np.linalg.norm(M_CA - M_AB)
            max_diff = max(abs(d1 - d2), abs(d2 - d3), abs(d1 - d3))
            return VGroup(
                MathTex(rf"|s_1| = {d1:.3f}", color=GREEN, font_size=18),
                MathTex(rf"|s_2| = {d2:.3f}", color=GREEN, font_size=18),
                MathTex(rf"|s_3| = {d3:.3f}", color=GREEN, font_size=18),
                MathTex(rf"\max\Delta = {max_diff:.2e}",
                         color=YELLOW, font_size=20),
                Tex(r"equilateral!", color=YELLOW, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for deg in [80, 130, 60, 100, 140]:
            self.play(theta_tr.animate.set_value(deg * DEGREES),
                       run_time=1.6, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
