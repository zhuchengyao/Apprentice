from manim import *
import numpy as np


class DesarguesTheoremExample(Scene):
    """
    Desargues: two triangles are in perspective from a point iff they
    are in perspective from a line. That is, if lines AA', BB', CC'
    meet at a point P, then the 3 pairs of corresponding sides
    (AB ∩ A'B'), (BC ∩ B'C'), (CA ∩ C'A') are collinear.

    SINGLE_FOCUS: two triangles ABC and A'B'C' with concurrent
    perspective point P; always_redraw computes the 3 intersection
    points of corresponding sides — they lie on one line (GREEN).
    """

    def construct(self):
        title = Tex(r"Desargues: perspective from point $\Leftrightarrow$ from line",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        P = np.array([-4.5, 0.0, 0])
        t_tr = ValueTracker(0.0)

        # Triangle ABC (fixed direction)
        base_A = np.array([2.0, 2.0, 0])
        base_B = np.array([3.5, 0.0, 0])
        base_C = np.array([2.5, -1.5, 0])

        def A(): return base_A
        def B(): return base_B
        def C(): return base_C

        def Ap():
            # A' = P + t*(A - P), where t = ratio + small oscillation
            t = 0.5 + 0.3 * np.sin(t_tr.get_value())
            return P + t * (base_A - P)

        def Bp():
            t = 0.4 + 0.3 * np.cos(t_tr.get_value())
            return P + t * (base_B - P)

        def Cp():
            t = 0.55 + 0.3 * np.sin(t_tr.get_value() * 0.7)
            return P + t * (base_C - P)

        def line_intersection(p1, p2, p3, p4):
            # Intersection of line p1p2 and p3p4
            d1 = p2 - p1
            d2 = p4 - p3
            M = np.array([[d1[0], -d2[0]], [d1[1], -d2[1]]])
            rhs = np.array([p3[0] - p1[0], p3[1] - p1[1]])
            try:
                sol = np.linalg.solve(M, rhs)
                return p1 + sol[0] * d1
            except np.linalg.LinAlgError:
                return (p1 + p3) / 2

        def triangle1():
            return Polygon(A(), B(), C(), color=BLUE, stroke_width=3)

        def triangle2():
            return Polygon(Ap(), Bp(), Cp(), color=ORANGE, stroke_width=3)

        def perspective_lines():
            return VGroup(
                Line(P, A(), color=GREY_B, stroke_width=1.5, stroke_opacity=0.5),
                Line(P, B(), color=GREY_B, stroke_width=1.5, stroke_opacity=0.5),
                Line(P, C(), color=GREY_B, stroke_width=1.5, stroke_opacity=0.5),
            )

        def intersections():
            # AB ∩ A'B'
            X1 = line_intersection(A(), B(), Ap(), Bp())
            X2 = line_intersection(B(), C(), Bp(), Cp())
            X3 = line_intersection(C(), A(), Cp(), Ap())
            # Collinearity line
            d = X3 - X1
            dlen = np.linalg.norm(d)
            if dlen < 1e-6:
                return VGroup()
            u = d / dlen
            t_vals = [np.dot(X - X1, u) for X in [X1, X2, X3]]
            t_min, t_max = min(t_vals) - 0.3, max(t_vals) + 0.3
            line = Line(X1 + t_min * u, X1 + t_max * u,
                         color=GREEN, stroke_width=4)
            dots = VGroup(
                Dot(X1, color=GREEN, radius=0.09),
                Dot(X2, color=GREEN, radius=0.09),
                Dot(X3, color=GREEN, radius=0.09),
            )
            return VGroup(line, dots)

        self.add(Dot(P, color=RED, radius=0.15),
                 always_redraw(perspective_lines),
                 always_redraw(triangle1),
                 always_redraw(triangle2),
                 always_redraw(intersections))

        self.add(Tex(r"$P$ (center of perspective)",
                     color=RED, font_size=20).next_to(P, LEFT, buff=0.2))

        info = VGroup(
            Tex(r"two triangles $\triangle ABC, \triangle A'B'C'$",
                font_size=20),
            Tex(r"$AA', BB', CC'$ concurrent at $P$",
                color=RED, font_size=20),
            Tex(r"GREEN dots: $AB\cap A'B'$, etc.",
                color=GREEN, font_size=20),
            Tex(r"always collinear!",
                color=GREEN, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(DR, buff=0.3)
        self.add(info)

        self.play(t_tr.animate.set_value(2 * PI),
                  run_time=8, rate_func=linear)
        self.wait(0.8)
