from manim import *
import numpy as np


class PowerOfAPointExample(Scene):
    """
    Power of a point theorem: for a fixed circle and an external
    point P, any line through P meeting the circle at A, B
    satisfies |PA|·|PB| = d² - R² (power), independent of the line.

    SINGLE_FOCUS:
      Circle of radius R=2 at origin; external point P at (4, 1).
      ValueTracker theta_tr rotates a line through P; always_redraw
      chord AB + products |PA|, |PB|, product. Invariant across θ.
    """

    def construct(self):
        title = Tex(r"Power of a point: $|PA|\cdot|PB| = d^2 - R^2$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        R = 2.0
        P_pos = np.array([4.0, 1.0, 0])
        d = np.linalg.norm(P_pos)
        power = d ** 2 - R ** 2

        circ = Circle(radius=R, color=BLUE, stroke_width=3).move_to(ORIGIN)
        P_dot = Dot(P_pos, color=YELLOW, radius=0.14)
        P_lbl = MathTex(r"P", color=YELLOW, font_size=22
                          ).next_to(P_dot, UR, buff=0.1)
        O_dot = Dot(ORIGIN, color=WHITE, radius=0.08)
        self.play(Create(circ), FadeIn(P_dot, O_dot), Write(P_lbl))

        theta_tr = ValueTracker(30 * DEGREES)

        def chord_endpoints(theta):
            """Line through P in direction (cos θ, sin θ); find
            intersections with circle x² + y² = R²."""
            cx, sy = np.cos(theta), np.sin(theta)
            # P + t·(cx, sy): (P.x + t cx)² + (P.y + t sy)² = R²
            a = 1.0
            b = 2 * (P_pos[0] * cx + P_pos[1] * sy)
            c = P_pos[0] ** 2 + P_pos[1] ** 2 - R ** 2
            disc = b * b - 4 * a * c
            if disc < 0:
                return None, None
            t1 = (-b - np.sqrt(disc)) / (2 * a)
            t2 = (-b + np.sqrt(disc)) / (2 * a)
            A = P_pos + t1 * np.array([cx, sy, 0])
            B = P_pos + t2 * np.array([cx, sy, 0])
            return A, B

        def chord():
            t = theta_tr.get_value()
            A, B = chord_endpoints(t)
            if A is None:
                return VGroup()
            grp = VGroup()
            # Extended line from P past A
            # PA direction
            direction = np.array([np.cos(t), np.sin(t), 0])
            grp.add(Line(P_pos - 0.3 * direction, B + 0.3 * direction,
                           color=RED, stroke_width=2.5))
            grp.add(Dot(A, color=GREEN, radius=0.11))
            grp.add(Dot(B, color=ORANGE, radius=0.11))
            grp.add(MathTex(r"A", color=GREEN, font_size=20).next_to(A, DL, buff=0.05))
            grp.add(MathTex(r"B", color=ORANGE, font_size=20).next_to(B, UR, buff=0.05))
            return grp

        self.add(always_redraw(chord))

        def info():
            t = theta_tr.get_value()
            A, B = chord_endpoints(t)
            if A is None:
                return VGroup()
            PA = np.linalg.norm(A - P_pos)
            PB = np.linalg.norm(B - P_pos)
            prod = PA * PB
            return VGroup(
                MathTex(rf"\theta = {np.degrees(t):.0f}^\circ",
                         color=WHITE, font_size=22),
                MathTex(rf"|PA| = {PA:.3f}",
                         color=GREEN, font_size=22),
                MathTex(rf"|PB| = {PB:.3f}",
                         color=ORANGE, font_size=22),
                MathTex(rf"|PA|\cdot|PB| = {prod:.3f}",
                         color=YELLOW, font_size=22),
                MathTex(rf"d^2 - R^2 = {power:.3f}",
                         color=GREEN, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(LEFT, buff=0.3).shift(UP * 1.0)

        self.add(always_redraw(info))

        for deg in [60, 90, 160, 200, 300, 30]:
            self.play(theta_tr.animate.set_value(deg * DEGREES),
                       run_time=1.4, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.4)
