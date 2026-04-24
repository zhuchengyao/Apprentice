from manim import *
import numpy as np


class SteinerTreeExample(Scene):
    """
    Steiner tree: minimum total length of a network connecting 3
    points. For a triangle with all angles < 120°, the Steiner point
    is the Fermat point where all three connecting segments meet at
    120° angles. Length is less than any 2-segment path.

    SINGLE_FOCUS:
      3 fixed cities A, B, C; show the naive "Y-tree" (through
      centroid) vs Steiner tree (through Fermat point); compare
      total lengths.
    """

    def construct(self):
        title = Tex(r"Steiner tree: shortest network with 120° angles",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        A = np.array([-3.0, -1.5, 0])
        B = np.array([3.0, -1.5, 0])
        C = np.array([0.0, 2.0, 0])

        # Dots
        A_dot = Dot(A, color=GREEN, radius=0.12)
        B_dot = Dot(B, color=GREEN, radius=0.12)
        C_dot = Dot(C, color=GREEN, radius=0.12)
        A_lbl = MathTex(r"A", color=GREEN, font_size=22).next_to(A, DL, buff=0.1)
        B_lbl = MathTex(r"B", color=GREEN, font_size=22).next_to(B, DR, buff=0.1)
        C_lbl = MathTex(r"C", color=GREEN, font_size=22).next_to(C, UP, buff=0.1)
        self.play(FadeIn(A_dot, B_dot, C_dot),
                   Write(A_lbl), Write(B_lbl), Write(C_lbl))

        # Naive: minimum spanning tree is just 2 longest edges skipped
        # MST of triangle = 2 shortest edges. Let's use centroid for visual comparison.
        centroid = (A + B + C) / 3
        AB = np.linalg.norm(A - B)
        BC = np.linalg.norm(B - C)
        CA = np.linalg.norm(C - A)
        mst_sides = sorted([AB, BC, CA])
        mst_length = mst_sides[0] + mst_sides[1]

        # Fermat point: point F such that angles A-F-B, B-F-C, C-F-A
        # are all 120°. For acute triangle, F is interior.
        # Compute via rotation trick: rotate B around C by 60° to get B'; then AB' passes through F.
        def rotate_pt(P, center, angle):
            c, s = np.cos(angle), np.sin(angle)
            dx, dy = P[0] - center[0], P[1] - center[1]
            return np.array([center[0] + c * dx - s * dy,
                             center[1] + s * dx + c * dy, 0])

        B_rot = rotate_pt(B, C, -PI / 3)  # rotate B around C by -60°
        # Fermat length = |A to B_rot|
        fermat_length = np.linalg.norm(A - B_rot)

        # Find F: intersection of line A-B_rot with line through (construction)
        # Equivalently, Torricelli's construction. For simplicity, compute F
        # numerically by minimizing |FA| + |FB| + |FC|.
        from scipy.optimize import minimize
        res = minimize(lambda p: (np.linalg.norm([p[0] - A[0], p[1] - A[1]]) +
                                     np.linalg.norm([p[0] - B[0], p[1] - B[1]]) +
                                     np.linalg.norm([p[0] - C[0], p[1] - C[1]])),
                        x0=[0, 0])
        F = np.array([res.x[0], res.x[1], 0])

        step_tr = ValueTracker(0)

        def naive_y_tree():
            s = int(round(step_tr.get_value()))
            if s < 1:
                return VGroup()
            grp = VGroup()
            for V in [A, B, C]:
                grp.add(Line(V, centroid, color=RED, stroke_width=2.5,
                               stroke_opacity=0.7))
            grp.add(Dot(centroid, color=RED, radius=0.09))
            return grp

        def steiner_tree():
            s = int(round(step_tr.get_value()))
            if s < 2:
                return VGroup()
            grp = VGroup()
            for V in [A, B, C]:
                grp.add(Line(V, F, color=YELLOW, stroke_width=3))
            grp.add(Dot(F, color=YELLOW, radius=0.1))
            grp.add(MathTex(r"F", color=YELLOW, font_size=22
                              ).next_to(F, UR, buff=0.1))
            return grp

        self.add(always_redraw(naive_y_tree), always_redraw(steiner_tree))

        naive_length = sum(np.linalg.norm(V - centroid) for V in [A, B, C])

        def info():
            s = int(round(step_tr.get_value()))
            return VGroup(
                Tex(r"RED: centroid tree", color=RED, font_size=20),
                MathTex(rf"\ell_{{\text{{centroid}}}} = {naive_length:.3f}",
                         color=RED, font_size=20),
                Tex(r"YELLOW: Steiner tree", color=YELLOW, font_size=20),
                MathTex(rf"\ell_{{\text{{Steiner}}}} = {fermat_length:.3f}",
                         color=YELLOW, font_size=20),
                MathTex(rf"\text{{savings}} = {naive_length - fermat_length:.3f}",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        self.play(step_tr.animate.set_value(1), run_time=1.0)
        self.wait(1.0)
        self.play(step_tr.animate.set_value(2), run_time=1.0)
        self.wait(1.5)
