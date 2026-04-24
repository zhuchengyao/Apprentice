from manim import *
import numpy as np


class GroverRotationExample(Scene):
    """
    Grover's algorithm as a rotation in a 2D state space
    (from _2025/grover adaptation):

      State lives in the span of |α⟩ (non-target) and |β⟩ (target).
      Initial equal superposition |s⟩ = cos θ |α⟩ + sin θ |β⟩ with
      sin θ = √(M/N). Each Grover iteration rotates by 2θ toward |β⟩.

    SINGLE_FOCUS:
      2D state plane: x-axis = |α⟩, y-axis = |β⟩. ValueTracker k_tr
      steps iterations k = 0 → k_opt = π/(4θ); always_redraw state
      arrow + angle arc. Target band (|β⟩ amplitude ≥ 0.99) shown.
    """

    def construct(self):
        title = Tex(r"Grover's algorithm: rotation in $|\alpha\rangle$-$|\beta\rangle$ plane",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-0.2, 1.2, 0.25],
                             y_range=[-0.2, 1.2, 0.25],
                             x_length=5.5, y_length=5.5,
                             background_line_style={"stroke_opacity": 0.3}
                             ).move_to([-3.2, -0.3, 0])

        unit_circle = Circle(radius=plane.c2p(1, 0)[0] - plane.c2p(0, 0)[0],
                               color=GREY_B, stroke_width=2
                               ).move_to(plane.c2p(0, 0))
        self.play(Create(plane), Create(unit_circle))

        # Axis labels
        a_lbl = MathTex(r"|\alpha\rangle", color=BLUE, font_size=26
                         ).next_to(plane.c2p(1, 0), DR, buff=0.2)
        b_lbl = MathTex(r"|\beta\rangle", color=RED, font_size=26
                         ).next_to(plane.c2p(0, 1), UL, buff=0.2)
        self.play(Write(a_lbl), Write(b_lbl))

        # Grover parameters: N = 100, M = 1 → sin θ = 1/10
        N, M = 100, 1
        theta = np.arcsin(np.sqrt(M / N))
        k_opt = PI / (4 * theta) - 0.5  # ≈ 7.85

        # Initial state angle = θ (nearly horizontal)
        k_tr = ValueTracker(0.0)

        def current_angle():
            k = k_tr.get_value()
            return (2 * k + 1) * theta

        def state_arrow():
            ang = current_angle()
            return Arrow(plane.c2p(0, 0),
                          plane.c2p(np.cos(ang), np.sin(ang)),
                          color=YELLOW, buff=0, stroke_width=5,
                          max_tip_length_to_length_ratio=0.12)

        def state_dot():
            ang = current_angle()
            return Dot(plane.c2p(np.cos(ang), np.sin(ang)),
                        color=YELLOW, radius=0.1)

        def angle_arc():
            ang = current_angle()
            return Arc(radius=0.5, start_angle=0, angle=ang,
                        color=YELLOW, stroke_width=3
                        ).move_arc_center_to(plane.c2p(0, 0))

        self.add(always_redraw(state_arrow),
                  always_redraw(state_dot),
                  always_redraw(angle_arc))

        # Target threshold band
        target_band = Rectangle(
            width=plane.c2p(0.15, 0)[0] - plane.c2p(0, 0)[0],
            height=plane.c2p(0, 1)[1] - plane.c2p(0, 0)[1],
            color=GREEN, fill_opacity=0.15, stroke_width=0
        ).move_to(plane.c2p(0.075, 0.5))
        self.play(FadeIn(target_band))

        def info():
            k = k_tr.get_value()
            ang = current_angle()
            amp_b = np.sin(ang)
            prob_b = amp_b ** 2
            return VGroup(
                MathTex(rf"N = {N},\ M = {M}",
                         color=WHITE, font_size=22),
                MathTex(rf"\sin\theta = \sqrt{{M/N}} = {np.sin(theta):.3f}",
                         color=BLUE, font_size=22),
                MathTex(rf"k = {k:.2f}", color=YELLOW, font_size=22),
                MathTex(rf"\text{{angle}} = (2k+1)\theta = {np.degrees(ang):.1f}^\circ",
                         color=YELLOW, font_size=20),
                MathTex(rf"|\langle\beta|\psi\rangle|^2 = \sin^2 = {prob_b:.4f}",
                         color=RED, font_size=22),
                MathTex(rf"k^* \approx \tfrac{{\pi}}{{4\theta}} - \tfrac{{1}}{{2}} \approx {k_opt:.2f}",
                         color=GREEN, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.8, 0.0, 0])

        self.add(always_redraw(info))

        self.play(k_tr.animate.set_value(float(k_opt)),
                   run_time=6, rate_func=linear)
        self.wait(0.7)
