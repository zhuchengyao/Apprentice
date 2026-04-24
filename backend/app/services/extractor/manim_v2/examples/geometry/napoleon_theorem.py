from manim import *
import numpy as np


class NapoleonTheoremExample(Scene):
    """
    Napoleon's theorem: on each side of any triangle build an outward
    equilateral triangle; the centroids of these three form an
    equilateral triangle ("Napoleon's triangle"), regardless of the
    original.

    SINGLE_FOCUS:
      Variable triangle ABC; ValueTracker theta_tr moves apex C;
      always_redraw the 3 outer equilateral triangles + their 3
      centroids; the 3 centroids always form an equilateral triangle
      (side-length differences shown).
    """

    def construct(self):
        title = Tex(r"Napoleon's theorem: centroids always equilateral",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        A = np.array([-2.0, -1.2, 0])
        B = np.array([2.2, -1.2, 0])

        theta_tr = ValueTracker(100 * DEGREES)

        def C_pt():
            t = theta_tr.get_value()
            return np.array([0.5 * np.cos(t),
                              1.2 + 1.8 * np.sin(t), 0])

        def equilateral_apex(P, Q):
            """Third vertex of equilateral triangle on PQ, outward (rotated +60°)."""
            v = Q - P
            # Rotate v by -60° (clockwise) for outward
            c, s = np.cos(-PI / 3), np.sin(-PI / 3)
            rot = np.array([c * v[0] - s * v[1], s * v[0] + c * v[1], 0])
            return P + rot

        def all_elements():
            C = C_pt()
            # Outer vertices on each side
            out_AB = equilateral_apex(B, A)  # outward means we choose the correct side
            out_BC = equilateral_apex(C, B)
            out_CA = equilateral_apex(A, C)

            # Centroids of outer triangles
            cent_AB = (A + B + out_AB) / 3
            cent_BC = (B + C + out_BC) / 3
            cent_CA = (C + A + out_CA) / 3

            grp = VGroup()
            # Central triangle
            grp.add(Polygon(A, B, C, color=YELLOW,
                              fill_opacity=0.2, stroke_width=3))
            # 3 outer equilaterals
            grp.add(Polygon(A, B, out_AB, color=BLUE,
                              fill_opacity=0.15, stroke_width=2))
            grp.add(Polygon(B, C, out_BC, color=BLUE,
                              fill_opacity=0.15, stroke_width=2))
            grp.add(Polygon(C, A, out_CA, color=BLUE,
                              fill_opacity=0.15, stroke_width=2))
            # Centroid triangle (Napoleon triangle)
            grp.add(Polygon(cent_AB, cent_BC, cent_CA,
                              color=GREEN, fill_opacity=0.45,
                              stroke_width=3))
            # Centroid dots
            for p in [cent_AB, cent_BC, cent_CA]:
                grp.add(Dot(p, color=GREEN, radius=0.1))
            return grp

        self.add(always_redraw(all_elements))

        def info():
            C = C_pt()
            out_AB = equilateral_apex(B, A)
            out_BC = equilateral_apex(C, B)
            out_CA = equilateral_apex(A, C)
            cent_AB = (A + B + out_AB) / 3
            cent_BC = (B + C + out_BC) / 3
            cent_CA = (C + A + out_CA) / 3
            s1 = np.linalg.norm(cent_AB - cent_BC)
            s2 = np.linalg.norm(cent_BC - cent_CA)
            s3 = np.linalg.norm(cent_CA - cent_AB)
            return VGroup(
                MathTex(rf"|s_1| = {s1:.3f}", color=GREEN, font_size=20),
                MathTex(rf"|s_2| = {s2:.3f}", color=GREEN, font_size=20),
                MathTex(rf"|s_3| = {s3:.3f}", color=GREEN, font_size=20),
                MathTex(rf"\max \Delta = {max(abs(s1-s2), abs(s2-s3), abs(s1-s3)):.3e}",
                         color=YELLOW, font_size=20),
                Tex(r"always equilateral!", color=YELLOW, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for deg in [80, 130, 50, 95, 120]:
            self.play(theta_tr.animate.set_value(deg * DEGREES),
                       run_time=1.6, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
