from manim import *
import numpy as np


class NinePointCircleExample(Scene):
    """
    Nine-point circle: a triangle has 9 special points on a single
    circle — 3 midpoints of sides, 3 feet of altitudes, 3 midpoints
    of segments from orthocenter to vertices.

    SINGLE_FOCUS:
      Triangle with variable apex via ValueTracker. Highlight:
      3 BLUE midpoints, 3 GREEN altitude feet, 3 RED mid-ortho;
      ORANGE 9-point circle. All 9 dots lie on the circle.
    """

    def construct(self):
        title = Tex(r"Nine-point circle: 9 special points on one circle",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        A = np.array([-2.7, -1.5, 0])
        B = np.array([2.7, -1.5, 0])

        theta_tr = ValueTracker(100 * DEGREES)

        def C_pt():
            t = theta_tr.get_value()
            return np.array([0.7 * np.cos(t),
                              1.0 + 2.4 * np.sin(t) * 0.8, 0])

        def geom():
            C = C_pt()
            # 3 midpoints
            M_AB = (A + B) / 2
            M_BC = (B + C) / 2
            M_CA = (C + A) / 2

            # 3 altitude feet
            def foot_on_line(P, Q, X):
                # Foot of perpendicular from X to line PQ
                d = Q - P
                t = np.dot(X - P, d) / np.dot(d, d)
                return P + t * d

            H_A = foot_on_line(B, C, A)
            H_B = foot_on_line(A, C, B)
            H_C = foot_on_line(A, B, C)

            # Orthocenter
            def line_intersect(P1, P2, Q1, Q2):
                d1 = P2 - P1
                d2 = Q2 - Q1
                denom = d1[0] * d2[1] - d1[1] * d2[0]
                if abs(denom) < 1e-8:
                    return None
                t = ((Q1[0] - P1[0]) * d2[1] - (Q1[1] - P1[1]) * d2[0]) / denom
                return P1 + t * d1

            # Altitude from A perpendicular to BC, passing through A & H_A
            ortho = line_intersect(A, H_A, B, H_B)
            if ortho is None:
                ortho = (A + B + C) / 3

            # 3 midpoints from orthocenter to vertices
            N_A = (A + ortho) / 2
            N_B = (B + ortho) / 2
            N_C = (C + ortho) / 2

            # 9-point center = midpoint of orthocenter and circumcenter
            def circumcenter(P1, P2, P3):
                # Via perpendicular bisectors
                mid12 = (P1 + P2) / 2
                mid13 = (P1 + P3) / 2
                d12 = P2 - P1
                d13 = P3 - P1
                # perp dirs
                perp12 = np.array([-d12[1], d12[0], 0])
                perp13 = np.array([-d13[1], d13[0], 0])
                center = line_intersect(mid12, mid12 + perp12,
                                           mid13, mid13 + perp13)
                if center is None:
                    return (P1 + P2 + P3) / 3
                return center

            circ = circumcenter(A, B, C)
            nine_center = (circ + ortho) / 2
            # Nine-point radius = half circumradius
            R_circ = np.linalg.norm(A - circ)
            R_nine = R_circ / 2

            grp = VGroup()
            grp.add(Polygon(A, B, C, color=YELLOW, fill_opacity=0.1,
                              stroke_width=3))
            # 9 points
            for p in [M_AB, M_BC, M_CA]:
                grp.add(Dot(p, color=BLUE, radius=0.08))
            for p in [H_A, H_B, H_C]:
                grp.add(Dot(p, color=GREEN, radius=0.08))
            for p in [N_A, N_B, N_C]:
                grp.add(Dot(p, color=RED, radius=0.08))
            # Nine-point circle
            grp.add(Circle(radius=R_nine, color=ORANGE,
                             stroke_width=3, fill_opacity=0.1
                             ).move_to(nine_center))
            # Ortho dot
            grp.add(Dot(ortho, color=PURPLE, radius=0.08))
            # Circumcenter
            grp.add(Dot(circ, color=PINK, radius=0.08))
            # Altitudes (faint)
            grp.add(DashedLine(A, H_A, color=GREY_B, stroke_width=1,
                                 stroke_opacity=0.4))
            grp.add(DashedLine(B, H_B, color=GREY_B, stroke_width=1,
                                 stroke_opacity=0.4))
            grp.add(DashedLine(C, H_C, color=GREY_B, stroke_width=1,
                                 stroke_opacity=0.4))
            return grp

        self.add(always_redraw(geom))

        legend = VGroup(
            Tex(r"BLUE: side midpoints",
                 color=BLUE, font_size=18),
            Tex(r"GREEN: altitude feet",
                 color=GREEN, font_size=18),
            Tex(r"RED: mid-ortho-vertex",
                 color=RED, font_size=18),
            Tex(r"ORANGE: 9-point circle",
                 color=ORANGE, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.3)
        self.play(Write(legend))

        for deg in [80, 120, 60, 100, 130]:
            self.play(theta_tr.animate.set_value(deg * DEGREES),
                       run_time=1.6, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
