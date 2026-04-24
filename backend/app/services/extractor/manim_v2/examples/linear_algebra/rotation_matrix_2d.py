from manim import *
import numpy as np


class RotationMatrix2DExample(Scene):
    """
    2D rotation matrix R(θ) = [[cos θ, -sin θ], [sin θ, cos θ]]
    rotating the standard basis into (cos θ, sin θ) and
    (-sin θ, cos θ).

    TWO_COLUMN:
      LEFT  — NumberPlane with orthogonal basis arrows ê_1 (RED) and
              ê_2 (BLUE) that rotate together as ValueTracker θ_tr
              sweeps; always_redraw.
      RIGHT — live R(θ) matrix + dot products ê_1·ê_2 = 0 check.
    """

    def construct(self):
        title = Tex(r"Rotation matrix $R(\theta)$ rotates the basis",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-3, 3, 1], y_range=[-2.5, 2.5, 1],
                             x_length=6, y_length=5,
                             background_line_style={"stroke_opacity": 0.3}
                             ).move_to([-2.8, -0.3, 0])
        self.play(Create(plane))

        theta_tr = ValueTracker(0.0)

        def e1_arrow():
            t = theta_tr.get_value()
            return Arrow(plane.c2p(0, 0),
                          plane.c2p(2 * np.cos(t), 2 * np.sin(t)),
                          color=RED, buff=0, stroke_width=5,
                          max_tip_length_to_length_ratio=0.15)

        def e2_arrow():
            t = theta_tr.get_value()
            return Arrow(plane.c2p(0, 0),
                          plane.c2p(-2 * np.sin(t), 2 * np.cos(t)),
                          color=BLUE, buff=0, stroke_width=5,
                          max_tip_length_to_length_ratio=0.15)

        def angle_arc():
            t = theta_tr.get_value()
            if t < 0.01:
                return VGroup()
            return Arc(radius=0.5, start_angle=0, angle=t,
                        color=YELLOW, stroke_width=3
                        ).move_arc_center_to(plane.c2p(0, 0))

        self.add(always_redraw(e1_arrow),
                  always_redraw(e2_arrow),
                  always_redraw(angle_arc))

        def info():
            t = theta_tr.get_value()
            c = np.cos(t)
            s = np.sin(t)
            # Dot product e1·e2 = -cos·sin + sin·cos = 0
            dot = -c * s + s * c
            return VGroup(
                MathTex(rf"\theta = {np.degrees(t):.0f}^\circ",
                         color=YELLOW, font_size=26),
                MathTex(rf"R(\theta) = \begin{{pmatrix}} {c:+.2f} & {-s:+.2f} \\ {s:+.2f} & {c:+.2f} \end{{pmatrix}}",
                         color=WHITE, font_size=22),
                MathTex(rf"\hat e_1 \cdot \hat e_2 = {dot:.2e}",
                         color=GREEN, font_size=22),
                MathTex(r"\det R = \cos^2 + \sin^2 = 1",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.8, 0.0, 0])

        self.add(always_redraw(info))

        self.play(theta_tr.animate.set_value(2 * PI),
                   run_time=8, rate_func=linear)
        self.wait(0.4)
