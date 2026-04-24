from manim import *
import numpy as np


class RotationCompositionExample(Scene):
    """
    Composition of 2D rotations: R(α) · R(β) = R(α + β). Visualize
    by applying R(α) then R(β) to a basis vector; result equals
    R(α + β) applied once.

    SINGLE_FOCUS:
      Plane with 3 arrows: initial ê_1 (BLUE), intermediate after
      R(α) (GREEN), final after R(β)·R(α) (YELLOW). Overlaid with
      ORANGE arrow = R(α+β)·ê_1. They coincide.
    """

    def construct(self):
        title = Tex(r"Composition: $R(\alpha)\,R(\beta) = R(\alpha+\beta)$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-3, 3, 1], y_range=[-2.5, 2.5, 1],
                             x_length=7, y_length=5.5,
                             background_line_style={"stroke_opacity": 0.3}
                             ).move_to([-2.5, -0.3, 0])
        self.play(Create(plane))

        alpha_tr = ValueTracker(0.0)
        beta_tr = ValueTracker(0.0)

        def e1_original():
            return Arrow(plane.c2p(0, 0), plane.c2p(2, 0),
                          color=BLUE, buff=0, stroke_width=5,
                          max_tip_length_to_length_ratio=0.15)

        def e1_after_R_alpha():
            a = alpha_tr.get_value()
            x = 2 * np.cos(a)
            y = 2 * np.sin(a)
            return Arrow(plane.c2p(0, 0), plane.c2p(x, y),
                          color=GREEN, buff=0, stroke_width=5,
                          max_tip_length_to_length_ratio=0.15)

        def e1_after_both():
            a = alpha_tr.get_value()
            b = beta_tr.get_value()
            # R(b) R(a) ê_1 = (cos(a+b), sin(a+b))
            x = 2 * np.cos(a + b)
            y = 2 * np.sin(a + b)
            return Arrow(plane.c2p(0, 0), plane.c2p(x, y),
                          color=YELLOW, buff=0, stroke_width=6,
                          max_tip_length_to_length_ratio=0.2)

        def e1_direct():
            a = alpha_tr.get_value()
            b = beta_tr.get_value()
            x = 2 * np.cos(a + b) + 0.03
            y = 2 * np.sin(a + b) + 0.03
            return Arrow(plane.c2p(0, 0), plane.c2p(x, y),
                          color=ORANGE, buff=0, stroke_width=3,
                          max_tip_length_to_length_ratio=0.15)

        self.add(e1_original(),
                  always_redraw(e1_after_R_alpha),
                  always_redraw(e1_after_both),
                  always_redraw(e1_direct))

        def info():
            a = alpha_tr.get_value()
            b = beta_tr.get_value()
            total = a + b
            return VGroup(
                MathTex(rf"\alpha = {np.degrees(a):.0f}^\circ",
                         color=GREEN, font_size=24),
                MathTex(rf"\beta = {np.degrees(b):.0f}^\circ",
                         color=YELLOW, font_size=24),
                MathTex(rf"\alpha + \beta = {np.degrees(total):.0f}^\circ",
                         color=ORANGE, font_size=24),
                Tex(r"YELLOW = $R(\beta)R(\alpha)\hat e_1$",
                     color=YELLOW, font_size=18),
                Tex(r"ORANGE = $R(\alpha+\beta)\hat e_1$",
                     color=ORANGE, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        self.play(alpha_tr.animate.set_value(60 * DEGREES),
                   run_time=2, rate_func=smooth)
        self.play(beta_tr.animate.set_value(40 * DEGREES),
                   run_time=2, rate_func=smooth)
        self.play(alpha_tr.animate.set_value(120 * DEGREES),
                   beta_tr.animate.set_value(30 * DEGREES),
                   run_time=2, rate_func=smooth)
        self.play(alpha_tr.animate.set_value(-45 * DEGREES),
                   beta_tr.animate.set_value(90 * DEGREES),
                   run_time=2, rate_func=smooth)
        self.wait(0.4)
