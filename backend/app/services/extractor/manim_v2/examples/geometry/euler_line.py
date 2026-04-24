from manim import *
import numpy as np


class EulerLineExample(Scene):
    """
    Euler line: in any non-equilateral triangle, the orthocenter H,
    centroid G, and circumcenter O are collinear, with HG : GO = 2 : 1.

    SINGLE_FOCUS:
      Variable-apex triangle; always_redraw H (orthocenter), G
      (centroid), O (circumcenter), and the RED Euler line through
      them.
    """

    def construct(self):
        title = Tex(r"Euler line: $H, G, O$ collinear, $HG : GO = 2 : 1$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        A = np.array([-2.5, -1.5, 0])
        B = np.array([2.5, -1.5, 0])

        theta_tr = ValueTracker(100 * DEGREES)

        def C_pt():
            t = theta_tr.get_value()
            return np.array([0.8 * np.cos(t),
                              1.2 + 2.0 * np.sin(t), 0])

        def line_intersect(P1, d1, P2, d2):
            denom = d1[0] * d2[1] - d1[1] * d2[0]
            if abs(denom) < 1e-8:
                return None
            t = ((P2[0] - P1[0]) * d2[1] - (P2[1] - P1[1]) * d2[0]) / denom
            return P1 + t * d1

        def geom():
            C = C_pt()
            centroid = (A + B + C) / 3

            # Orthocenter: intersection of altitudes
            # Altitude from A perpendicular to BC
            BC_dir = C - B
            BC_perp = np.array([-BC_dir[1], BC_dir[0], 0])
            # Altitude from B perpendicular to AC
            AC_dir = C - A
            AC_perp = np.array([-AC_dir[1], AC_dir[0], 0])
            H = line_intersect(A, BC_perp, B, AC_perp)
            if H is None:
                H = centroid

            # Circumcenter: intersection of perpendicular bisectors
            M_AB = (A + B) / 2
            M_AC = (A + C) / 2
            AB_perp = np.array([-(B - A)[1], (B - A)[0], 0])
            AC_perp2 = np.array([-(C - A)[1], (C - A)[0], 0])
            O = line_intersect(M_AB, AB_perp, M_AC, AC_perp2)
            if O is None:
                O = centroid

            grp = VGroup()
            grp.add(Polygon(A, B, C, color=YELLOW,
                              fill_opacity=0.15, stroke_width=3))
            # Euler line (extended)
            direction = O - H
            if np.linalg.norm(direction) > 1e-6:
                direction = direction / np.linalg.norm(direction)
                line_start = H - 2 * direction
                line_end = O + 2 * direction
                grp.add(Line(line_start, line_end,
                               color=RED, stroke_width=3))

            # Points
            grp.add(Dot(H, color=GREEN, radius=0.1))
            grp.add(Dot(centroid, color=BLUE, radius=0.1))
            grp.add(Dot(O, color=PURPLE, radius=0.1))
            grp.add(MathTex(r"H", color=GREEN, font_size=20).next_to(H, UL, buff=0.05))
            grp.add(MathTex(r"G", color=BLUE, font_size=20).next_to(centroid, UR, buff=0.05))
            grp.add(MathTex(r"O", color=PURPLE, font_size=20).next_to(O, DR, buff=0.05))
            return grp

        self.add(always_redraw(geom))

        def info():
            C = C_pt()
            centroid = (A + B + C) / 3
            BC_dir = C - B
            BC_perp = np.array([-BC_dir[1], BC_dir[0], 0])
            AC_dir = C - A
            AC_perp = np.array([-AC_dir[1], AC_dir[0], 0])
            H = line_intersect(A, BC_perp, B, AC_perp)
            M_AB = (A + B) / 2
            M_AC = (A + C) / 2
            AB_perp = np.array([-(B - A)[1], (B - A)[0], 0])
            AC_perp2 = np.array([-(C - A)[1], (C - A)[0], 0])
            O = line_intersect(M_AB, AB_perp, M_AC, AC_perp2)
            if H is None or O is None:
                HG = GO = 0.0
            else:
                HG = np.linalg.norm(H - centroid)
                GO = np.linalg.norm(centroid - O)
            return VGroup(
                MathTex(rf"|HG| = {HG:.3f}", color=GREEN, font_size=20),
                MathTex(rf"|GO| = {GO:.3f}", color=PURPLE, font_size=20),
                MathTex(rf"HG/GO = {HG/(GO + 1e-9):.3f}",
                         color=YELLOW, font_size=22),
                MathTex(r"\text{expected} = 2.000",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for deg in [80, 130, 60, 110, 140]:
            self.play(theta_tr.animate.set_value(deg * DEGREES),
                       run_time=1.6, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
