from manim import *
import numpy as np


class RightTriangleComplementaryAnglesExample(Scene):
    """
    In a right triangle, the two non-right angles are complementary:
    α + β = 90°.

    SINGLE_FOCUS:
      Right triangle with variable leg ratio via ValueTracker
      ratio_tr = b/a sweeping 0.2 → 5. always_redraw the triangle,
      the two non-right angle arcs, live α, β. Sum label α + β
      always reads 90°.
    """

    def construct(self):
        title = Tex(r"Right triangle: $\alpha + \beta = 90^\circ$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ratio_tr = ValueTracker(1.0)
        scale = 2.5
        O = np.array([-3.0, -1.6, 0])

        def verts():
            r = ratio_tr.get_value()
            a = 1.0
            b = r
            norm = max(a, b)
            A = O
            B = O + scale * np.array([a / norm, 0, 0])
            C = O + scale * np.array([0, b / norm, 0])
            return A, B, C

        def triangle():
            A, B, C = verts()
            return Polygon(A, B, C, color=YELLOW, fill_opacity=0.3,
                            stroke_width=3)

        def right_angle_mark():
            A, B, C = verts()
            size = 0.22
            return Polygon(A, A + size * RIGHT, A + size * (UP + RIGHT),
                             A + size * UP,
                             color=WHITE, stroke_width=2)

        def alpha_arc():
            # angle at B
            A, B, C = verts()
            v1 = (A - B) / np.linalg.norm(A - B)
            v2 = (C - B) / np.linalg.norm(C - B)
            ang_start = np.arctan2(v1[1], v1[0])
            ang_end = np.arctan2(v2[1], v2[0])
            if ang_end < ang_start:
                ang_end += 2 * PI
            return Arc(radius=0.45, start_angle=ang_start,
                        angle=ang_end - ang_start,
                        color=RED, stroke_width=3).move_arc_center_to(B)

        def beta_arc():
            # angle at C
            A, B, C = verts()
            v1 = (A - C) / np.linalg.norm(A - C)
            v2 = (B - C) / np.linalg.norm(B - C)
            ang_start = np.arctan2(v2[1], v2[0])
            ang_end = np.arctan2(v1[1], v1[0])
            if ang_end < ang_start:
                ang_end += 2 * PI
            return Arc(radius=0.45, start_angle=ang_start,
                        angle=ang_end - ang_start,
                        color=BLUE, stroke_width=3).move_arc_center_to(C)

        def angle_labels():
            A, B, C = verts()
            r = ratio_tr.get_value()
            alpha = np.degrees(np.arctan2(r, 1))  # angle at B
            beta = 90 - alpha
            a_lbl = MathTex(rf"\alpha = {alpha:.1f}^\circ",
                             color=RED, font_size=22).move_to(B + LEFT * 0.8 + UP * 0.3)
            b_lbl = MathTex(rf"\beta = {beta:.1f}^\circ",
                             color=BLUE, font_size=22).move_to(C + DOWN * 0.2 + RIGHT * 0.6)
            return VGroup(a_lbl, b_lbl)

        self.add(always_redraw(triangle),
                  always_redraw(right_angle_mark),
                  always_redraw(alpha_arc),
                  always_redraw(beta_arc),
                  always_redraw(angle_labels))

        def info():
            r = ratio_tr.get_value()
            alpha = np.degrees(np.arctan2(r, 1))
            beta = 90 - alpha
            return VGroup(
                MathTex(rf"b/a = {r:.2f}", color=WHITE, font_size=24),
                MathTex(rf"\alpha = {alpha:.1f}^\circ", color=RED, font_size=24),
                MathTex(rf"\beta = {beta:.1f}^\circ", color=BLUE, font_size=24),
                MathTex(rf"\alpha + \beta = {alpha + beta:.1f}^\circ",
                         color=GREEN, font_size=26),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.8, 0.5, 0])

        self.add(always_redraw(info))

        for target in [0.3, 2.5, 5.0, 0.8, 1.2]:
            self.play(ratio_tr.animate.set_value(target),
                       run_time=1.5, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.4)
