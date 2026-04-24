from manim import *
import numpy as np


class NinePointCircleRebuildExample(Scene):
    """
    Nine-point circle: for any triangle, 9 specific points lie on a
    common circle:
      - 3 midpoints of sides
      - 3 feet of altitudes
      - 3 midpoints between vertices and orthocenter

    ValueTracker s_tr morphs triangle ABC through 4 configs;
    always_redraw recomputes all 9 points + the circumscribing circle
    (center = midpoint of circumcenter and orthocenter; radius = R/2).
    """

    def construct(self):
        title = Tex(r"Nine-point circle: 9 distinguished points lie on one circle",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        configs = [
            (np.array([-2.5, -1.2, 0]), np.array([2.5, -1.2, 0]), np.array([-0.6, 2.0, 0])),
            (np.array([-2.8, -1.4, 0]), np.array([2.4, -1.4, 0]), np.array([1.0, 1.9, 0])),
            (np.array([-2.2, -1.3, 0]), np.array([2.6, -1.3, 0]), np.array([-1.3, 2.1, 0])),
            (np.array([-2.5, -1.2, 0]), np.array([2.5, -1.2, 0]), np.array([0.0, 2.3, 0])),
        ]

        s_tr = ValueTracker(0.0)

        def ABC():
            s = s_tr.get_value()
            k = int(s)
            frac = s - k
            k_next = min(len(configs) - 1, k + 1)
            return [(1 - frac) * configs[k][i] + frac * configs[k_next][i]
                    for i in range(3)]

        def circumcenter(A, B, C):
            # solve |P-A|=|P-B| and |P-A|=|P-C|
            ax, ay = A[:2]; bx, by = B[:2]; cx, cy = C[:2]
            d = 2 * ((bx - ax) * (cy - ay) - (cx - ax) * (by - ay))
            if abs(d) < 1e-9:
                return (A + B + C) / 3
            ux = ((bx ** 2 - ax ** 2 + by ** 2 - ay ** 2) * (cy - ay)
                   - (cx ** 2 - ax ** 2 + cy ** 2 - ay ** 2) * (by - ay)) / d
            uy = ((cx ** 2 - ax ** 2 + cy ** 2 - ay ** 2) * (bx - ax)
                   - (bx ** 2 - ax ** 2 + by ** 2 - ay ** 2) * (cx - ax)) / d
            return np.array([ux, uy, 0.0])

        def orthocenter(A, B, C):
            # altitude from A: perpendicular to BC through A.
            # altitude from B: perpendicular to CA through B.
            # solve for intersection.
            BC = C - B
            CA = A - C
            n_A = np.array([-BC[1], BC[0], 0])
            n_B = np.array([-CA[1], CA[0], 0])
            # Line A + t*n_A = B + s*n_B
            # 2×2 solve
            M = np.array([[n_A[0], -n_B[0]], [n_A[1], -n_B[1]]])
            rhs = np.array([B[0] - A[0], B[1] - A[1]])
            try:
                sol = np.linalg.solve(M, rhs)
                return A + sol[0] * n_A
            except np.linalg.LinAlgError:
                return (A + B + C) / 3

        def foot_of_altitude(P, Q, R):
            # foot of perp from R onto line PQ
            d = Q - P
            t = np.dot(R - P, d) / np.dot(d, d)
            return P + t * d

        def build():
            A, B, C = ABC()
            M_AB = (A + B) / 2
            M_BC = (B + C) / 2
            M_CA = (C + A) / 2
            H = orthocenter(A, B, C)
            F_A = foot_of_altitude(B, C, A)
            F_B = foot_of_altitude(C, A, B)
            F_C = foot_of_altitude(A, B, C)
            N_A = (A + H) / 2
            N_B = (B + H) / 2
            N_C = (C + H) / 2
            O = circumcenter(A, B, C)
            np_center = (O + H) / 2
            R_circ = np.linalg.norm(A - O)
            r9 = R_circ / 2

            tri = Polygon(A, B, C, color=BLUE, stroke_width=3)
            nine_pts = VGroup(
                *[Dot(p, color=RED, radius=0.08)
                  for p in [M_AB, M_BC, M_CA, F_A, F_B, F_C, N_A, N_B, N_C]]
            )
            circ9 = Circle(radius=r9, color=YELLOW,
                           stroke_width=3).move_to(np_center)

            # Dashed altitudes
            alt = VGroup(
                DashedLine(A, F_A, color=GREY_B, stroke_width=1.5, stroke_opacity=0.55),
                DashedLine(B, F_B, color=GREY_B, stroke_width=1.5, stroke_opacity=0.55),
                DashedLine(C, F_C, color=GREY_B, stroke_width=1.5, stroke_opacity=0.55),
            )
            return VGroup(alt, tri, circ9, nine_pts,
                           Dot(H, color=ORANGE, radius=0.07),
                           Dot(O, color=GREEN, radius=0.07),
                           Dot(np_center, color=YELLOW, radius=0.07))

        self.add(always_redraw(build))

        legend = VGroup(
            Tex(r"YELLOW: 9-point circle", color=YELLOW, font_size=20),
            Tex(r"RED: 9 points (mid + alt + mid-to-H)",
                color=RED, font_size=20),
            Tex(r"GREEN: circumcenter $O$",
                color=GREEN, font_size=20),
            Tex(r"ORANGE: orthocenter $H$",
                color=ORANGE, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DR, buff=0.3)
        self.add(legend)

        for k in range(1, len(configs)):
            self.play(s_tr.animate.set_value(float(k)),
                      run_time=2.0, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.8)
