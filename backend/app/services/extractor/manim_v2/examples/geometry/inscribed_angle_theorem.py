from manim import *
import numpy as np


class InscribedAngleTheoremExample(Scene):
    """
    Inscribed-angle theorem: an inscribed angle is half the central
    angle subtending the same arc. ValueTracker moves the apex of
    the inscribed angle around the circle; the inscribed angle stays
    at a constant half the central angle.

    SINGLE_FOCUS:
      Circle with fixed chord AB; vertex P moves on the major arc;
      always_redraw inscribed ∠APB and central ∠AOB. Display both
      values.
    """

    def construct(self):
        title = Tex(r"Inscribed-angle theorem: $\angle APB = \tfrac{1}{2}\angle AOB$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        center = np.array([-0.5, -0.3, 0])
        R = 2.5
        circ = Circle(radius=R, color=BLUE, stroke_width=3
                       ).move_to(center)
        O_dot = Dot(center, color=WHITE, radius=0.08)
        O_lbl = MathTex(r"O", font_size=20).next_to(O_dot, UL, buff=0.05)
        self.play(Create(circ), FadeIn(O_dot), Write(O_lbl))

        # Fixed chord AB: A at angle 210°, B at angle 330°
        angA = 210 * DEGREES
        angB = 330 * DEGREES
        A = center + R * np.array([np.cos(angA), np.sin(angA), 0])
        B = center + R * np.array([np.cos(angB), np.sin(angB), 0])
        A_dot = Dot(A, color=YELLOW, radius=0.1)
        B_dot = Dot(B, color=YELLOW, radius=0.1)
        A_lbl = MathTex(r"A", color=YELLOW, font_size=22
                          ).next_to(A_dot, DL, buff=0.05)
        B_lbl = MathTex(r"B", color=YELLOW, font_size=22
                          ).next_to(B_dot, DR, buff=0.05)

        chord_AB = Line(A, B, color=YELLOW, stroke_width=2)
        OA = Line(center, A, color=GREEN, stroke_width=2)
        OB = Line(center, B, color=GREEN, stroke_width=2)

        self.play(FadeIn(A_dot, B_dot), Write(A_lbl), Write(B_lbl),
                   Create(chord_AB), Create(OA), Create(OB))

        # Central angle ∠AOB (the one subtending major arc / minor arc?)
        # angB - angA = 120° (minor arc); we want the angle at O.
        # For the theorem we want the inscribed angle subtending the SAME arc.
        # If P is on major arc, inscribed ∠APB subtends arc AB (minor).
        # Central angle ∠AOB for that minor arc = 120°, inscribed = 60°.

        phi_tr = ValueTracker(PI / 2)

        def P_point():
            # P moves on major arc: angle from 30° (just above B) to 150° (just above A)
            phi = phi_tr.get_value()
            # Map phi ∈ [0, 1] to arc from angB+5° to angA-5° going CCW through top
            # phi_tr holds the actual angle directly; we'll constrain to major arc
            return center + R * np.array([np.cos(phi), np.sin(phi), 0])

        def P_dot():
            return Dot(P_point(), color=RED, radius=0.1)

        def PA_line():
            return Line(P_point(), A, color=RED, stroke_width=2)

        def PB_line():
            return Line(P_point(), B, color=RED, stroke_width=2)

        def P_lbl():
            return MathTex(r"P", color=RED, font_size=22
                             ).next_to(P_dot(), UP, buff=0.1)

        def central_arc():
            # Arc from B to A going through bottom (minor arc)
            return Arc(radius=0.5, start_angle=angB,
                        angle=-120 * DEGREES,
                        color=GREEN, stroke_width=4
                        ).move_arc_center_to(center)

        def inscribed_arc():
            # Arc at P
            P = P_point()
            v_to_A = A - P
            v_to_B = B - P
            ang_to_A = np.arctan2(v_to_A[1], v_to_A[0])
            ang_to_B = np.arctan2(v_to_B[1], v_to_B[0])
            # Sweep from A-direction to B-direction (shorter arc)
            diff = ang_to_B - ang_to_A
            # Normalize to [-π, π]
            if diff > PI:
                diff -= 2 * PI
            elif diff < -PI:
                diff += 2 * PI
            return Arc(radius=0.5, start_angle=ang_to_A,
                        angle=diff,
                        color=RED, stroke_width=4
                        ).move_arc_center_to(P)

        self.add(always_redraw(PA_line), always_redraw(PB_line),
                  always_redraw(central_arc),
                  always_redraw(inscribed_arc),
                  always_redraw(P_dot), always_redraw(P_lbl))

        def info():
            P = P_point()
            # Angles
            v_to_A = A - P
            v_to_B = B - P
            cos_ang = np.dot(v_to_A, v_to_B) / (np.linalg.norm(v_to_A) * np.linalg.norm(v_to_B) + 1e-8)
            insc_ang = np.degrees(np.arccos(max(-1.0, min(1.0, cos_ang))))
            return VGroup(
                MathTex(rf"\angle AOB = 120^\circ",
                         color=GREEN, font_size=24),
                MathTex(rf"\angle APB = {insc_ang:.1f}^\circ",
                         color=RED, font_size=24),
                MathTex(rf"\angle APB / \angle AOB = {insc_ang/120:.3f}",
                         color=YELLOW, font_size=22),
                Tex(r"constant $= 0.5$", color=YELLOW, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        # Tour P around major arc
        for phi_deg in [60, 120, 90, 140, 40, 90]:
            self.play(phi_tr.animate.set_value(phi_deg * DEGREES),
                       run_time=1.6, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.4)
