from manim import *
import numpy as np


class TriangleCentersOverlayExample(Scene):
    """
    Overlay 4 triangle centers on one moving triangle:
      CENTROID G: (A+B+C)/3
      CIRCUMCENTER O: equidistant to vertices
      ORTHOCENTER H: intersection of altitudes
      INCENTER I: weighted by side lengths (aA+bB+cC)/(a+b+c)
    Euler line: G, O, H are collinear with OG:GH = 1:2.

    ValueTracker s_tr morphs triangle; always_redraw all 4 centers +
    Euler line.
    """

    def construct(self):
        title = Tex(r"Triangle centers: $G, O, H, I$ + Euler line $OG:GH=1:2$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        configs = [
            (np.array([-2.5, -1.3, 0]), np.array([2.5, -1.3, 0]), np.array([-0.3, 2.0, 0])),
            (np.array([-2.7, -1.4, 0]), np.array([2.5, -1.4, 0]), np.array([1.5, 1.9, 0])),
            (np.array([-2.2, -1.3, 0]), np.array([2.8, -1.3, 0]), np.array([-1.8, 2.1, 0])),
            (np.array([-2.5, -1.3, 0]), np.array([2.5, -1.3, 0]), np.array([0.0, 2.3, 0])),
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
            BC = C - B
            n_A = np.array([-BC[1], BC[0], 0])
            CA = A - C
            n_B = np.array([-CA[1], CA[0], 0])
            M = np.array([[n_A[0], -n_B[0]], [n_A[1], -n_B[1]]])
            rhs = np.array([B[0] - A[0], B[1] - A[1]])
            try:
                sol = np.linalg.solve(M, rhs)
                return A + sol[0] * n_A
            except np.linalg.LinAlgError:
                return (A + B + C) / 3

        def build():
            A, B, C = ABC()
            G = (A + B + C) / 3
            O = circumcenter(A, B, C)
            H = orthocenter(A, B, C)
            a = np.linalg.norm(B - C)
            b = np.linalg.norm(C - A)
            c = np.linalg.norm(A - B)
            I = (a * A + b * B + c * C) / (a + b + c)

            tri = Polygon(A, B, C, color=BLUE, stroke_width=3)
            verts = VGroup(
                Dot(A, color=BLUE, radius=0.08),
                Dot(B, color=BLUE, radius=0.08),
                Dot(C, color=BLUE, radius=0.08),
            )
            centers = VGroup(
                Dot(G, color=GREEN, radius=0.1),
                Dot(O, color=YELLOW, radius=0.1),
                Dot(H, color=ORANGE, radius=0.1),
                Dot(I, color=PURPLE, radius=0.1),
            )
            euler = Line(O + 2 * (O - H), H + 2 * (H - O),
                         color=RED, stroke_width=1.5, stroke_opacity=0.65)
            return VGroup(tri, verts, euler, centers)

        self.add(always_redraw(build))

        legend = VGroup(
            Tex(r"G centroid (GREEN)", color=GREEN, font_size=20),
            Tex(r"O circumcenter (YELLOW)", color=YELLOW, font_size=20),
            Tex(r"H orthocenter (ORANGE)", color=ORANGE, font_size=20),
            Tex(r"I incenter (PURPLE)", color=PURPLE, font_size=20),
            Tex(r"Euler line G, O, H (RED)", color=RED, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DR, buff=0.3)
        self.add(legend)

        for k in range(1, len(configs)):
            self.play(s_tr.animate.set_value(float(k)),
                      run_time=2.2, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.5)
