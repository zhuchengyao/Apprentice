from manim import *
import numpy as np


class EllipseDefinitionsExample(Scene):
    """
    Ellipse defined by focal sum: |PF₁| + |PF₂| = 2a is constant
    as P moves around the ellipse.

    SINGLE_FOCUS: ellipse with two foci. ValueTracker θ moves the
    point P around the ellipse; two always_redraw segments PF₁ (red)
    and PF₂ (orange) draw with their lengths labeled live, plus the
    sum |PF₁| + |PF₂| = 2a — which stays constant!
    """

    def construct(self):
        title = Tex(r"Ellipse: $|PF_1| + |PF_2| = 2a$ is invariant as $P$ moves",
                    font_size=26).to_edge(UP, buff=0.4)
        self.play(Write(title))

        a, b = 2.5, 1.5
        c = np.sqrt(a ** 2 - b ** 2)

        center = np.array([-1.5, -0.4, 0])

        ellipse = Ellipse(width=2 * a, height=2 * b, color=BLUE,
                          stroke_width=3).move_to(center)
        F1 = center + LEFT * c
        F2 = center + RIGHT * c
        f1_dot = Dot(F1, color=RED, radius=0.10)
        f2_dot = Dot(F2, color=RED, radius=0.10)
        f1_lbl = Tex(r"$F_1$", color=RED, font_size=22).next_to(f1_dot, DOWN, buff=0.05)
        f2_lbl = Tex(r"$F_2$", color=RED, font_size=22).next_to(f2_dot, DOWN, buff=0.05)
        self.play(Create(ellipse), FadeIn(f1_dot), FadeIn(f2_dot),
                  Write(f1_lbl), Write(f2_lbl))

        theta_tr = ValueTracker(0.5)

        def P_pt():
            t = theta_tr.get_value()
            return center + np.array([a * np.cos(t), b * np.sin(t), 0])

        def p_dot():
            return Dot(P_pt(), color=YELLOW, radius=0.10)

        def p_lbl():
            return Tex(r"$P$", color=YELLOW, font_size=22).next_to(
                p_dot(), UR, buff=0.05)

        def seg_F1P():
            return Line(F1, P_pt(), color=ORANGE, stroke_width=3)

        def seg_F2P():
            return Line(F2, P_pt(), color=GREEN, stroke_width=3)

        self.add(always_redraw(seg_F1P), always_redraw(seg_F2P),
                 always_redraw(p_dot), always_redraw(p_lbl))

        # RIGHT COLUMN
        rcol_x = +4.4

        def info_panel():
            P = P_pt()
            d1 = np.linalg.norm(P - F1)
            d2 = np.linalg.norm(P - F2)
            return VGroup(
                MathTex(rf"|PF_1| = {d1:.3f}", color=ORANGE, font_size=24),
                MathTex(rf"|PF_2| = {d2:.3f}", color=GREEN, font_size=24),
                MathTex(rf"|PF_1| + |PF_2| = {d1+d2:.3f}",
                        color=YELLOW, font_size=26),
                MathTex(rf"2a = {2*a:.1f}",
                        color=YELLOW, font_size=26),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([rcol_x, +0.6, 0])

        self.add(always_redraw(info_panel))

        principle = Tex(r"Sum of focal distances $=$ constant",
                        color=GREEN, font_size=22).move_to([rcol_x, -2.4, 0])
        self.play(Write(principle))

        # Sweep P all the way around twice
        self.play(theta_tr.animate.set_value(0.5 + 4 * PI),
                  run_time=10, rate_func=linear)
        self.wait(0.6)
