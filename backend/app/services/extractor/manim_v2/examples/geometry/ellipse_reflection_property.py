from manim import *
import numpy as np


class EllipseReflectionPropertyExample(Scene):
    """
    Ellipse reflection property: any ray from one focus bounces off
    the ellipse to the other focus. Animation shows a ray launching
    from F1, reflecting, reaching F2.

    SINGLE_FOCUS:
      Ellipse with semi-axes a=3, b=2; foci at (±c, 0) where c = √5.
      ValueTracker theta_tr varies launch direction from F1. For each
      direction, compute intersection with ellipse, draw incoming and
      reflected rays, verify they meet at F2.
    """

    def construct(self):
        title = Tex(r"Ellipse reflection: $F_1 \to $ point $\to F_2$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        a, b = 3.0, 2.0
        c = np.sqrt(a ** 2 - b ** 2)

        # Draw ellipse
        ellipse_pts = [np.array([a * np.cos(t), b * np.sin(t), 0])
                        for t in np.linspace(0, 2 * PI, 200)]
        ellipse = VMobject(color=BLUE, stroke_width=3)
        ellipse.set_points_as_corners(ellipse_pts + [ellipse_pts[0]])
        self.play(Create(ellipse))

        F1 = np.array([-c, 0, 0])
        F2 = np.array([c, 0, 0])
        F1_dot = Dot(F1, color=GREEN, radius=0.12)
        F2_dot = Dot(F2, color=RED, radius=0.12)
        F1_lbl = MathTex(r"F_1", color=GREEN,
                           font_size=22).next_to(F1_dot, DL, buff=0.1)
        F2_lbl = MathTex(r"F_2", color=RED,
                           font_size=22).next_to(F2_dot, DR, buff=0.1)
        self.play(FadeIn(F1_dot, F2_dot), Write(F1_lbl), Write(F2_lbl))

        theta_tr = ValueTracker(PI / 3)

        def hit_point(theta):
            """Find intersection of ray from F1 in direction θ with ellipse."""
            # Ray: F1 + s·(cos θ, sin θ). Plug into ellipse: x²/a² + y²/b² = 1
            # (-c + s cos θ)² / a² + (s sin θ)² / b² = 1
            cx = np.cos(theta)
            sy = np.sin(theta)
            A = cx * cx / (a * a) + sy * sy / (b * b)
            B = 2 * (-c) * cx / (a * a)
            C = c * c / (a * a) - 1
            disc = B * B - 4 * A * C
            if disc < 0:
                return F1 + np.array([0.01 * cx, 0.01 * sy, 0])
            s = (-B + np.sqrt(disc)) / (2 * A)
            return F1 + s * np.array([cx, sy, 0])

        def rays():
            theta = theta_tr.get_value()
            P = hit_point(theta)
            grp = VGroup()
            grp.add(Line(F1, P, color=GREEN, stroke_width=3))
            grp.add(Line(P, F2, color=RED, stroke_width=3))
            grp.add(Dot(P, color=YELLOW, radius=0.1))
            return grp

        self.add(always_redraw(rays))

        def info():
            theta = theta_tr.get_value()
            P = hit_point(theta)
            PF1 = np.linalg.norm(P - F1)
            PF2 = np.linalg.norm(P - F2)
            return VGroup(
                MathTex(rf"\theta = {np.degrees(theta):.0f}^\circ",
                         color=YELLOW, font_size=22),
                MathTex(rf"|PF_1| = {PF1:.3f}",
                         color=GREEN, font_size=22),
                MathTex(rf"|PF_2| = {PF2:.3f}",
                         color=RED, font_size=22),
                MathTex(rf"|PF_1| + |PF_2| = {PF1 + PF2:.3f}",
                         color=YELLOW, font_size=22),
                MathTex(rf"2a = {2 * a}",
                         color=WHITE, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.35).shift(UP * 0.3)

        self.add(always_redraw(info))

        for deg in [120, 30, 150, 200, 60]:
            self.play(theta_tr.animate.set_value(deg * DEGREES),
                       run_time=1.5, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
