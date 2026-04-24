from manim import *
import numpy as np


class ConwayFourTriangleExample(Scene):
    """
    Conway's circle theorem: extend each side of a triangle beyond
    its farthest vertex by the length of the opposite side. The 6
    endpoints lie on a common circle (Conway circle).

    SINGLE_FOCUS: triangle ABC with extensions; draw 6 endpoints and
    their circumscribing circle. ValueTracker morphs triangle through
    3 configurations.
    """

    def construct(self):
        title = Tex(r"Conway circle: 6 side-extension endpoints are concyclic",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        configs = [
            (np.array([-2.5, -1.4, 0]), np.array([2.5, -1.4, 0]), np.array([-0.5, 1.6, 0])),
            (np.array([-2.7, -1.5, 0]), np.array([2.3, -1.5, 0]), np.array([1.2, 1.7, 0])),
            (np.array([-2.0, -1.3, 0]), np.array([2.5, -1.3, 0]), np.array([-1.3, 1.5, 0])),
        ]

        s_tr = ValueTracker(0.0)

        def ABC():
            s = s_tr.get_value()
            k = int(s)
            frac = s - k
            k_next = min(len(configs) - 1, k + 1)
            return [(1 - frac) * configs[k][i] + frac * configs[k_next][i]
                    for i in range(3)]

        def build():
            A, B, C = ABC()
            a = np.linalg.norm(B - C)
            b = np.linalg.norm(C - A)
            c = np.linalg.norm(A - B)

            # Extensions:
            # From B along BA direction by length a (= |BC|); from A along AB by length a, etc.
            # Standard Conway: extend each side from each endpoint by the opposite-side length
            def unit(v):
                return v / np.linalg.norm(v)

            # A' on line AB extended past A, |AA'| = a (opposite to BC)
            # A_B: on AB extended past A, distance a
            # A_C: on AC extended past A, distance a
            A_B = A + a * unit(A - B)
            A_C = A + a * unit(A - C)
            B_A = B + b * unit(B - A)
            B_C = B + b * unit(B - C)
            C_A = C + c * unit(C - A)
            C_B = C + c * unit(C - B)

            tri = Polygon(A, B, C, color=BLUE, stroke_width=3)
            ext_lines = VGroup(
                Line(A, A_B, color=GREY_B, stroke_width=2, stroke_opacity=0.6),
                Line(A, A_C, color=GREY_B, stroke_width=2, stroke_opacity=0.6),
                Line(B, B_A, color=GREY_B, stroke_width=2, stroke_opacity=0.6),
                Line(B, B_C, color=GREY_B, stroke_width=2, stroke_opacity=0.6),
                Line(C, C_A, color=GREY_B, stroke_width=2, stroke_opacity=0.6),
                Line(C, C_B, color=GREY_B, stroke_width=2, stroke_opacity=0.6),
            )
            endpoints = VGroup(*[Dot(p, color=GREEN, radius=0.09)
                                  for p in [A_B, A_C, B_A, B_C, C_A, C_B]])

            # Circumscribing circle of 6 points: use first 3 to find center
            # (all 6 lie on circle centered at incenter with radius = incircle + Σ)
            # Actually Conway circle center = incenter; radius² = r² + s² where s = semi-perimeter
            sp = (a + b + c) / 2
            area = 0.5 * abs((B[0] - A[0]) * (C[1] - A[1]) - (C[0] - A[0]) * (B[1] - A[1]))
            r_incircle = area / sp
            I = (a * A + b * B + c * C) / (a + b + c)
            R_conway = np.sqrt(r_incircle ** 2 + sp ** 2)
            circle = Circle(radius=R_conway, color=YELLOW, stroke_width=3).move_to(I)

            return VGroup(ext_lines, tri, circle, endpoints,
                           Dot(I, color=RED, radius=0.08))

        self.add(always_redraw(build))

        info = VGroup(
            Tex(r"extend each side past vertex",
                color=GREY_B, font_size=20),
            Tex(r"by the opposite side's length",
                color=GREY_B, font_size=20),
            Tex(r"6 endpoints on common circle (GREEN)",
                color=GREEN, font_size=20),
            Tex(r"center = incenter (RED)",
                color=RED, font_size=20),
            Tex(r"radius $R=\sqrt{r^2+s^2}$",
                color=YELLOW, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(DR, buff=0.3)
        self.add(info)

        for k in range(1, len(configs)):
            self.play(s_tr.animate.set_value(float(k)),
                      run_time=2.5, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.5)
