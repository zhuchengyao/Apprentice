from manim import *
import numpy as np


class AngleBisectorTheoremExample(Scene):
    """
    Angle bisector theorem: in △ABC, the angle bisector from A hits
    side BC at D with BD/DC = AB/AC.

    SINGLE_FOCUS:
      Variable-apex triangle; ValueTracker theta_tr moves apex C;
      always_redraw bisector AD + ratio BD/DC verified against AB/AC.
    """

    def construct(self):
        title = Tex(r"Angle bisector: $BD/DC = AB/AC$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        A = np.array([0, 2.2, 0])
        B = np.array([-3, -1.3, 0])

        theta_tr = ValueTracker(0.0)

        def C_pt():
            t = theta_tr.get_value()
            return np.array([1.8 + 2 * np.cos(t), -1.3 + np.sin(t) * 0.5, 0])

        def geom():
            C = C_pt()
            # Angle bisector from A goes to D on BC such that BD/DC = AB/AC
            AB = np.linalg.norm(A - B)
            AC = np.linalg.norm(A - C)
            # D = B + (BD/(BD+DC)) (C - B) = B + (AB/(AB+AC)) (C - B)
            ratio = AB / (AB + AC)
            D = B + ratio * (C - B)

            grp = VGroup()
            grp.add(Polygon(A, B, C, color=YELLOW,
                              fill_opacity=0.2, stroke_width=3))
            grp.add(Line(A, D, color=RED, stroke_width=3))  # bisector
            # Dots
            grp.add(Dot(A, color=GREEN, radius=0.1))
            grp.add(Dot(B, color=GREEN, radius=0.1))
            grp.add(Dot(C, color=GREEN, radius=0.1))
            grp.add(Dot(D, color=RED, radius=0.1))
            # Labels
            grp.add(MathTex(r"A", color=GREEN, font_size=22).next_to(A, UP, buff=0.1))
            grp.add(MathTex(r"B", color=GREEN, font_size=22).next_to(B, DL, buff=0.1))
            grp.add(MathTex(r"C", color=GREEN, font_size=22).next_to(C, DR, buff=0.1))
            grp.add(MathTex(r"D", color=RED, font_size=22).next_to(D, DOWN, buff=0.1))
            return grp

        self.add(always_redraw(geom))

        def info():
            C = C_pt()
            AB = np.linalg.norm(A - B)
            AC = np.linalg.norm(A - C)
            ratio = AB / (AB + AC)
            D = B + ratio * (C - B)
            BD = np.linalg.norm(B - D)
            DC = np.linalg.norm(D - C)
            return VGroup(
                MathTex(rf"AB = {AB:.3f}", color=YELLOW, font_size=20),
                MathTex(rf"AC = {AC:.3f}", color=YELLOW, font_size=20),
                MathTex(rf"AB/AC = {AB/AC:.4f}",
                         color=GREEN, font_size=20),
                MathTex(rf"BD/DC = {BD/DC:.4f}",
                         color=GREEN, font_size=20),
                MathTex(rf"|\text{{diff}}| = {abs(AB/AC - BD/DC):.2e}",
                         color=GREEN, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for tv in [1.2, -0.8, 2.0, -1.5, 0.5]:
            self.play(theta_tr.animate.set_value(tv),
                       run_time=1.5, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
