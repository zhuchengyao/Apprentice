from manim import *
import numpy as np


class PtolemyTheoremExample(Scene):
    """
    Ptolemy's theorem: for a cyclic quadrilateral ABCD,
    |AC| · |BD| = |AB| · |CD| + |AD| · |BC|.

    SINGLE_FOCUS:
      Circle with 4 points on it (variable); ValueTracker for one
      vertex; always_redraw quadrilateral + two diagonals; live
      product check.
    """

    def construct(self):
        title = Tex(r"Ptolemy: $|AC|\cdot|BD| = |AB|\cdot|CD| + |AD|\cdot|BC|$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        R = 2.3
        center = np.array([-1.5, -0.3, 0])
        circ = Circle(radius=R, color=BLUE_D, stroke_width=2
                       ).move_to(center)
        self.play(Create(circ))

        # 4 points; make one variable
        theta_A = 30 * DEGREES
        theta_B = 110 * DEGREES
        theta_D = 290 * DEGREES
        theta_tr = ValueTracker(200 * DEGREES)  # C is variable

        def pt_at(theta):
            return center + R * np.array([np.cos(theta), np.sin(theta), 0])

        def geom():
            A = pt_at(theta_A)
            B = pt_at(theta_B)
            C = pt_at(theta_tr.get_value())
            D = pt_at(theta_D)
            grp = VGroup()
            grp.add(Polygon(A, B, C, D, color=YELLOW,
                              fill_opacity=0.15, stroke_width=3))
            # Diagonals
            grp.add(Line(A, C, color=RED, stroke_width=2))
            grp.add(Line(B, D, color=RED, stroke_width=2))
            # Dots + labels
            for (p, lbl_s) in [(A, "A"), (B, "B"), (C, "C"), (D, "D")]:
                grp.add(Dot(p, color=GREEN, radius=0.09))
                grp.add(MathTex(lbl_s, color=GREEN, font_size=22
                                  ).move_to(p + 0.35 * (p - center) / np.linalg.norm(p - center)))
            return grp

        self.add(always_redraw(geom))

        def info():
            A = pt_at(theta_A)
            B = pt_at(theta_B)
            C = pt_at(theta_tr.get_value())
            D = pt_at(theta_D)
            AB = np.linalg.norm(A - B)
            BC = np.linalg.norm(B - C)
            CD = np.linalg.norm(C - D)
            DA = np.linalg.norm(D - A)
            AC = np.linalg.norm(A - C)
            BD = np.linalg.norm(B - D)
            lhs = AC * BD
            rhs = AB * CD + DA * BC
            return VGroup(
                MathTex(rf"|AC|\cdot|BD| = {lhs:.3f}",
                         color=RED, font_size=22),
                MathTex(rf"|AB|\cdot|CD| = {AB * CD:.3f}",
                         color=BLUE, font_size=20),
                MathTex(rf"|AD|\cdot|BC| = {DA * BC:.3f}",
                         color=ORANGE, font_size=20),
                MathTex(rf"\text{{sum}} = {rhs:.3f}",
                         color=GREEN, font_size=22),
                MathTex(rf"|\text{{diff}}| = {abs(lhs - rhs):.4f}",
                         color=YELLOW, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for deg in [230, 170, 260, 200]:
            self.play(theta_tr.animate.set_value(deg * DEGREES),
                       run_time=1.5, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
