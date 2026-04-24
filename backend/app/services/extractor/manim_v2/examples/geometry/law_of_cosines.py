from manim import *
import numpy as np


class LawOfCosinesExample(Scene):
    """
    Law of cosines: c² = a² + b² - 2ab·cos(γ). Specialization to
    γ=90° recovers Pythagoras.

    SINGLE_FOCUS:
      Triangle with sides a=3, b=2, and adjustable angle γ via
      ValueTracker gamma_tr; always_redraw triangle + squares on sides;
      live c² = a² + b² - 2ab·cos γ.
    """

    def construct(self):
        title = Tex(r"Law of cosines: $c^2 = a^2 + b^2 - 2ab\cos\gamma$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        a, b = 2.5, 1.7
        S = 0.9
        O = np.array([-4, -1, 0])

        gamma_tr = ValueTracker(90 * DEGREES)

        def triangle_and_squares():
            gamma = gamma_tr.get_value()
            A = O
            B = O + S * a * np.array([1, 0, 0])
            C = O + S * b * np.array([np.cos(gamma), np.sin(gamma), 0])
            c = np.sqrt(a * a + b * b - 2 * a * b * np.cos(gamma))

            grp = VGroup()
            tri = Polygon(A, B, C, color=YELLOW, fill_opacity=0.3,
                            stroke_width=3)
            grp.add(tri)

            # Angle arc at A
            ang_start = 0
            ang_end = gamma
            grp.add(Arc(radius=0.4, start_angle=ang_start,
                          angle=ang_end - ang_start,
                          color=BLUE, stroke_width=3
                          ).move_arc_center_to(A))
            grp.add(MathTex(r"\gamma", color=BLUE,
                              font_size=22).move_to(A + np.array([0.55 * np.cos(gamma / 2),
                                                                     0.55 * np.sin(gamma / 2), 0])))

            # Side label c on BC
            mid_BC = (B + C) / 2
            grp.add(MathTex(rf"c = {c:.2f}",
                              color=GREEN, font_size=20
                              ).move_to(mid_BC + np.array([0.4, 0.3, 0])))

            # Sides a and b labels
            grp.add(MathTex(rf"a = {a}",
                              color=RED, font_size=20
                              ).move_to((A + B) / 2 + DOWN * 0.25))
            grp.add(MathTex(rf"b = {b}",
                              color=PURPLE, font_size=20
                              ).move_to((A + C) / 2 + LEFT * 0.35 + UP * 0.1))
            return grp

        self.add(always_redraw(triangle_and_squares))

        def info():
            gamma = gamma_tr.get_value()
            c_sq = a * a + b * b - 2 * a * b * np.cos(gamma)
            c = np.sqrt(c_sq)
            return VGroup(
                MathTex(rf"\gamma = {np.degrees(gamma):.0f}^\circ",
                         color=BLUE, font_size=24),
                MathTex(rf"a^2 = {a*a:.2f},\ b^2 = {b*b:.2f}",
                         color=WHITE, font_size=20),
                MathTex(rf"2ab\cos\gamma = {2*a*b*np.cos(gamma):+.3f}",
                         color=ORANGE, font_size=20),
                MathTex(rf"c^2 = {c_sq:.3f}",
                         color=GREEN, font_size=22),
                MathTex(rf"c = {c:.3f}",
                         color=GREEN, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for deg in [60, 90, 120, 30, 150, 90]:
            self.play(gamma_tr.animate.set_value(deg * DEGREES),
                       run_time=1.5, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.4)
