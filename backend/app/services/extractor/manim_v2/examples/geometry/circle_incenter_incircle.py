from manim import *
import numpy as np


class CircleIncenterIncircleExample(Scene):
    """
    The incircle of a triangle: tangent to all three sides, centered
    at the incenter I (intersection of angle bisectors), with radius
    r = Area / s (semiperimeter).

    SINGLE_FOCUS:
      Triangle with variable vertex C; ValueTracker theta_tr moves C
      on a circle around fixed A, B; always_redraw triangle, incenter,
      incircle.
    """

    def construct(self):
        title = Tex(r"Incircle: $r = \text{Area} / s$ (semiperimeter)",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        A = np.array([-2.5, -1.0, 0])
        B = np.array([2.5, -1.0, 0])

        theta_tr = ValueTracker(2 * PI / 3)

        def C_pt():
            t = theta_tr.get_value()
            return np.array([0.5 * np.cos(t), 2 + 2.5 * np.sin(t) * 0.8, 0])

        def incenter(A, B, C):
            # Incenter = (a·A + b·B + c·C) / (a+b+c), where a = |BC|, etc.
            a = np.linalg.norm(B - C)
            b = np.linalg.norm(A - C)
            c = np.linalg.norm(A - B)
            return (a * A + b * B + c * C) / (a + b + c)

        def inradius(A, B, C):
            a = np.linalg.norm(B - C)
            b = np.linalg.norm(A - C)
            c = np.linalg.norm(A - B)
            s = (a + b + c) / 2
            # Heron: area = √(s(s-a)(s-b)(s-c))
            area = np.sqrt(max(s * (s - a) * (s - b) * (s - c), 1e-8))
            return area / s

        def geom():
            C = C_pt()
            I = incenter(A, B, C)
            r = inradius(A, B, C)
            grp = VGroup()
            # Triangle
            grp.add(Polygon(A, B, C, color=YELLOW,
                              fill_opacity=0.2, stroke_width=3))
            # Incircle
            grp.add(Circle(radius=r, color=RED, stroke_width=3,
                             fill_opacity=0.15).move_to(I))
            # Incenter dot
            grp.add(Dot(I, color=RED, radius=0.09))
            # Angle bisectors (lines from each vertex through I to opposite side)
            for V in [A, B, C]:
                grp.add(DashedLine(V, I + 1.5 * (I - V) / (np.linalg.norm(I - V) + 1e-6),
                                     color=BLUE, stroke_width=1.5,
                                     stroke_opacity=0.5))
            return grp

        def vertex_dots():
            return VGroup(
                Dot(A, color=GREEN, radius=0.1),
                Dot(B, color=GREEN, radius=0.1),
                Dot(C_pt(), color=GREEN, radius=0.1),
            )

        self.add(always_redraw(geom), always_redraw(vertex_dots))

        A_lbl = MathTex(r"A", color=GREEN, font_size=22).next_to(A, DL, buff=0.1)
        B_lbl = MathTex(r"B", color=GREEN, font_size=22).next_to(B, DR, buff=0.1)
        self.play(Write(A_lbl), Write(B_lbl))

        def info():
            C = C_pt()
            I = incenter(A, B, C)
            r = inradius(A, B, C)
            a = np.linalg.norm(B - C)
            b = np.linalg.norm(A - C)
            c_side = np.linalg.norm(A - B)
            s = (a + b + c_side) / 2
            area = np.sqrt(max(s * (s - a) * (s - b) * (s - c_side), 1e-8))
            return VGroup(
                MathTex(rf"a, b, c = {a:.2f}, {b:.2f}, {c_side:.2f}",
                         color=WHITE, font_size=20),
                MathTex(rf"s = {s:.3f}", color=WHITE, font_size=22),
                MathTex(rf"\text{{Area}} = {area:.3f}",
                         color=YELLOW, font_size=22),
                MathTex(rf"r = {r:.3f}", color=RED, font_size=24),
                MathTex(rf"r \cdot s = {r * s:.3f}",
                         color=GREEN, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for deg in [90, 120, 60, 100, 80, 120]:
            self.play(theta_tr.animate.set_value(deg * DEGREES),
                       run_time=1.5, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.4)
