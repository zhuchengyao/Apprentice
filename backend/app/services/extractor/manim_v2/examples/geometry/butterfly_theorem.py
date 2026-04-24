from manim import *
import numpy as np


class ButterflyTheoremExample(Scene):
    """
    Butterfly theorem: let M be the midpoint of chord PQ of a circle.
    Two other chords AB and CD through M intersect PQ at X and Y.
    Then M is also the midpoint of XY.

    SINGLE_FOCUS:
      Circle + chord PQ + midpoint M; two other chords through M
      with ValueTracker theta_tr varying their angles. always_redraw
      shows X, Y on PQ and verifies MX = MY.
    """

    def construct(self):
        title = Tex(r"Butterfly theorem: $M$ midpoint of $PQ \Rightarrow MX = MY$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        R = 2.5
        center = ORIGIN
        circ = Circle(radius=R, color=BLUE_D, stroke_width=2
                       ).move_to(center)
        self.play(Create(circ))

        # Fixed chord PQ
        P = R * np.array([np.cos(PI * 0.7), np.sin(PI * 0.7), 0])
        Q = R * np.array([np.cos(-PI * 0.3), np.sin(-PI * 0.3), 0])
        M = (P + Q) / 2

        P_dot = Dot(P, color=GREEN, radius=0.11)
        Q_dot = Dot(Q, color=GREEN, radius=0.11)
        M_dot = Dot(M, color=YELLOW, radius=0.13)
        P_lbl = MathTex(r"P", color=GREEN, font_size=22).next_to(P, UL, buff=0.1)
        Q_lbl = MathTex(r"Q", color=GREEN, font_size=22).next_to(Q, DR, buff=0.1)
        M_lbl = MathTex(r"M", color=YELLOW, font_size=22).next_to(M, UR, buff=0.1)
        PQ_line = Line(P, Q, color=GREEN, stroke_width=2.5)
        self.play(Create(PQ_line), FadeIn(P_dot, Q_dot, M_dot),
                   Write(P_lbl), Write(Q_lbl), Write(M_lbl))

        theta_tr = ValueTracker(PI / 4)

        def chord_intersections(direction_angle):
            """Line through M at angle direction_angle intersects circle
            at two points."""
            d = np.array([np.cos(direction_angle),
                          np.sin(direction_angle), 0])
            # M + t*d, solve |M + t*d|² = R²
            a = np.dot(d, d)
            b = 2 * np.dot(d, M)
            c = np.dot(M, M) - R ** 2
            disc = b * b - 4 * a * c
            if disc < 0:
                return M, M
            t1 = (-b - np.sqrt(disc)) / (2 * a)
            t2 = (-b + np.sqrt(disc)) / (2 * a)
            return M + t1 * d, M + t2 * d

        def line_segment_intersect(P1, P2, Q1, Q2):
            """Intersect line P1P2 with line Q1Q2."""
            d1 = P2 - P1
            d2 = Q2 - Q1
            denom = d1[0] * d2[1] - d1[1] * d2[0]
            if abs(denom) < 1e-8:
                return M
            t = ((Q1[0] - P1[0]) * d2[1] - (Q1[1] - P1[1]) * d2[0]) / denom
            return P1 + t * d1

        def butterfly():
            theta = theta_tr.get_value()
            # Chord 1: through M at angle theta
            A, B = chord_intersections(theta)
            # Chord 2: through M at angle -theta (symmetric)
            C, D = chord_intersections(theta + PI / 3)
            # The 4 endpoints form a quadrilateral; X = AD ∩ PQ, Y = BC ∩ PQ
            X = line_segment_intersect(A, D, P, Q)
            Y = line_segment_intersect(B, C, P, Q)

            grp = VGroup()
            # Chord lines
            grp.add(Line(A, B, color=RED, stroke_width=2))
            grp.add(Line(C, D, color=ORANGE, stroke_width=2))
            # Cross-diagonal lines AD and BC
            grp.add(Line(A, D, color=PURPLE, stroke_width=2,
                           stroke_opacity=0.7))
            grp.add(Line(B, C, color=PINK, stroke_width=2,
                           stroke_opacity=0.7))
            # X, Y
            grp.add(Dot(X, color=RED, radius=0.11))
            grp.add(Dot(Y, color=RED, radius=0.11))
            grp.add(MathTex(r"X", color=RED, font_size=20
                              ).next_to(X, UP, buff=0.1))
            grp.add(MathTex(r"Y", color=RED, font_size=20
                              ).next_to(Y, DOWN, buff=0.1))
            # Circle points
            for p, col in [(A, RED), (B, RED), (C, ORANGE), (D, ORANGE)]:
                grp.add(Dot(p, color=col, radius=0.08))
            return grp

        self.add(always_redraw(butterfly))

        def info():
            theta = theta_tr.get_value()
            A, B = chord_intersections(theta)
            C, D = chord_intersections(theta + PI / 3)
            X = line_segment_intersect(A, D, P, Q)
            Y = line_segment_intersect(B, C, P, Q)
            MX = np.linalg.norm(X - M)
            MY = np.linalg.norm(Y - M)
            return VGroup(
                MathTex(rf"\theta = {np.degrees(theta):.0f}^\circ",
                         color=YELLOW, font_size=20),
                MathTex(rf"|MX| = {MX:.3f}",
                         color=RED, font_size=20),
                MathTex(rf"|MY| = {MY:.3f}",
                         color=RED, font_size=20),
                MathTex(rf"|MX - MY| = {abs(MX - MY):.4f}",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for deg in [30, 60, 20, 75, 45]:
            self.play(theta_tr.animate.set_value(deg * DEGREES),
                       run_time=1.4, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.4)
