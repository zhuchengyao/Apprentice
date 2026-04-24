from manim import *
import numpy as np


class IsogonalConjugateExample(Scene):
    """
    Isogonal conjugate: for a point P and triangle ABC, the isogonal
    conjugate P* is obtained by reflecting each cevian AP, BP, CP
    across the corresponding angle bisector.

    ValueTracker s_tr moves P; always_redraw computes P* via explicit
    barycentric formula P* = (a²/P_a, b²/P_b, c²/P_c) normalized.
    """

    def construct(self):
        title = Tex(r"Isogonal conjugate $P^*$: reflect cevians across bisectors",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 4, 1], y_range=[-2.5, 2.5, 1],
                            x_length=9, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(DOWN * 0.1)
        self.play(Create(plane))

        A = np.array([-3.0, -1.3, 0])
        B = np.array([3.0, -1.3, 0])
        C = np.array([-0.5, 2.0, 0])
        tri = Polygon(A, B, C, color=BLUE, stroke_width=3)
        self.play(Create(tri))
        self.add(Tex(r"A", color=BLUE, font_size=24).next_to(A, DL, buff=0.1))
        self.add(Tex(r"B", color=BLUE, font_size=24).next_to(B, DR, buff=0.1))
        self.add(Tex(r"C", color=BLUE, font_size=24).next_to(C, UR, buff=0.1))

        a = np.linalg.norm(B - C)
        b = np.linalg.norm(C - A)
        c = np.linalg.norm(A - B)

        # Parametric path for P
        t_tr = ValueTracker(0.0)

        def P_pt():
            t = t_tr.get_value()
            cx, cy = (A[0] + B[0] + C[0]) / 3, (A[1] + B[1] + C[1]) / 3
            r = 1.2
            return np.array([cx + r * np.cos(t), cy + 0.7 * np.sin(t), 0])

        def barycentric(P):
            # Compute barycentric coords (u, v, w) with u+v+w=1
            # Using signed area formulation
            def area(X, Y, Z):
                return 0.5 * ((Y[0] - X[0]) * (Z[1] - X[1])
                              - (Z[0] - X[0]) * (Y[1] - X[1]))
            total = area(A, B, C)
            u = area(P, B, C) / total
            v = area(A, P, C) / total
            w = area(A, B, P) / total
            return u, v, w

        def P_star():
            P = P_pt()
            u, v, w = barycentric(P)
            if abs(u) < 1e-6 or abs(v) < 1e-6 or abs(w) < 1e-6:
                return P
            u_star = a * a / u
            v_star = b * b / v
            w_star = c * c / w
            s = u_star + v_star + w_star
            u_star, v_star, w_star = u_star / s, v_star / s, w_star / s
            return u_star * A + v_star * B + w_star * C

        def P_dot():
            return Dot(P_pt(), color=GREEN, radius=0.13)

        def Pstar_dot():
            return Dot(P_star(), color=RED, radius=0.13)

        def cevians():
            P = P_pt()
            Ps = P_star()
            grp = VGroup()
            for vert, col in [(A, GREEN), (B, GREEN), (C, GREEN)]:
                grp.add(Line(vert, P, color=GREEN, stroke_width=1.5,
                              stroke_opacity=0.6))
            for vert, col in [(A, RED), (B, RED), (C, RED)]:
                grp.add(Line(vert, Ps, color=RED, stroke_width=1.5,
                              stroke_opacity=0.6))
            return grp

        self.add(always_redraw(cevians), always_redraw(P_dot), always_redraw(Pstar_dot))

        # Labels
        P_lbl = always_redraw(lambda: Tex(r"P", color=GREEN, font_size=22).move_to(
            P_pt() + UR * 0.2))
        Ps_lbl = always_redraw(lambda: Tex(r"$P^*$", color=RED, font_size=22).move_to(
            P_star() + UR * 0.2))
        self.add(P_lbl, Ps_lbl)

        info = VGroup(
            Tex(r"barycentric of $P^*$: $(a^2/P_a, b^2/P_b, c^2/P_c)$",
                font_size=20),
            Tex(r"circumcenter $\leftrightarrow$ orthocenter",
                color=YELLOW, font_size=20),
            Tex(r"incenter $\leftrightarrow$ incenter",
                color=YELLOW, font_size=20),
            Tex(r"centroid $\leftrightarrow$ symmedian point",
                color=YELLOW, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(DR, buff=0.3)
        self.add(info)

        self.play(t_tr.animate.set_value(TAU),
                  run_time=8, rate_func=linear)
        self.wait(0.8)
