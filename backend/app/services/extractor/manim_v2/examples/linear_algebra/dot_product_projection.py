from manim import *
import numpy as np


class DotProductProjectionExample(Scene):
    """
    Dot product as the signed length of one vector's shadow on the other.

    TWO_COLUMN layout:
      LEFT  — fixed reference vector v on a NumberPlane and a rotating
              vector w of fixed length 2.5. ValueTracker θ sweeps the
              angle of w through 360°. A dashed perpendicular drops
              from w's tip to the line spanned by v; the projection
              vector along v redraws each frame.
      RIGHT — live readouts of θ (degrees), |w|·cos(θ), and the dot
              product v·w. A bonus axes panel underneath plots v·w
              versus θ as a cosine curve, with a moving dot tracking
              the current value.
    """

    def construct(self):
        title = Tex(r"Dot product $=$ projection length $\times |\vec v|$",
                    font_size=32).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # LEFT: plane with v, w, and projection
        plane = NumberPlane(
            x_range=[-4, 4, 1], y_range=[-3, 3, 1],
            x_length=6.6, y_length=5.0,
            background_line_style={"stroke_opacity": 0.3},
        ).move_to([-2.6, -0.2, 0])
        self.play(Create(plane))

        v_vec = np.array([3.0, 0.0])
        v_unit = v_vec / np.linalg.norm(v_vec)

        v_arrow = Arrow(plane.c2p(0, 0), plane.c2p(*v_vec), buff=0,
                        color=GREEN, stroke_width=5,
                        max_tip_length_to_length_ratio=0.10)
        v_lbl = MathTex(r"\vec v", color=GREEN, font_size=30).next_to(
            plane.c2p(*v_vec), DR, buff=0.15)
        self.play(GrowArrow(v_arrow), Write(v_lbl))

        theta = ValueTracker(0.6)  # start at ~34°
        w_len = 2.5

        def w_vec():
            t = theta.get_value()
            return np.array([w_len * np.cos(t), w_len * np.sin(t)])

        def w_arrow():
            return Arrow(plane.c2p(0, 0), plane.c2p(*w_vec()),
                         buff=0, color=RED, stroke_width=5,
                         max_tip_length_to_length_ratio=0.12)

        def proj_arrow():
            w = w_vec()
            proj_len = np.dot(w, v_unit)
            end = proj_len * v_unit
            return Arrow(plane.c2p(0, 0), plane.c2p(*end),
                         buff=0, color=YELLOW, stroke_width=6,
                         max_tip_length_to_length_ratio=0.12)

        def perp_drop():
            w = w_vec()
            proj_len = np.dot(w, v_unit)
            end = proj_len * v_unit
            return DashedLine(plane.c2p(*w), plane.c2p(*end),
                              color=GREY_B, stroke_width=2)

        def w_label():
            return MathTex(r"\vec w", color=RED, font_size=30).next_to(
                plane.c2p(*w_vec()), UR, buff=0.1)

        self.add(always_redraw(w_arrow), always_redraw(perp_drop),
                 always_redraw(proj_arrow), always_redraw(w_label))

        # RIGHT COLUMN: readouts and a small cos plot
        rcol_x = +4.0

        def info_panel():
            t = theta.get_value()
            w = w_vec()
            dot = float(np.dot(v_vec, w))
            return VGroup(
                MathTex(rf"\theta = {np.degrees(t):+.0f}^\circ",
                        color=WHITE, font_size=28),
                MathTex(rf"|\vec v|=3,\;|\vec w|={w_len:.1f}",
                        color=GREY_B, font_size=24),
                MathTex(rf"\vec v\cdot\vec w = |\vec v||\vec w|\cos\theta = {dot:+.2f}",
                        color=YELLOW, font_size=24),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([rcol_x, +2.5, 0])

        self.add(always_redraw(info_panel))

        # Mini-axes plotting v·w vs θ
        mini_axes = Axes(
            x_range=[0, 2 * PI, PI / 2], y_range=[-8, 8, 4],
            x_length=3.4, y_length=2.0,
            axis_config={"include_tip": False, "include_numbers": False, "font_size": 16},
        ).move_to([rcol_x, 0.0, 0])
        cos_curve = mini_axes.plot(
            lambda t: 3 * w_len * np.cos(t),
            x_range=[0, 2 * PI - 0.01], color=YELLOW,
        )
        cos_lbl = MathTex(r"\vec v\cdot\vec w(\theta) = 7.5\cos\theta",
                          color=YELLOW, font_size=20).next_to(mini_axes, UP, buff=0.1)
        self.play(Create(mini_axes), Create(cos_curve), Write(cos_lbl))

        def moving_marker():
            t = theta.get_value() % (2 * PI)
            return Dot(mini_axes.c2p(t, 3 * w_len * np.cos(t)),
                       color=YELLOW, radius=0.07)

        self.add(always_redraw(moving_marker))

        # Sweep θ through a full rotation, then back partway
        self.play(theta.animate.set_value(2 * PI + 0.6),
                  run_time=8, rate_func=linear)
        self.wait(0.4)

        formula = MathTex(
            r"\vec v\cdot\vec w = |\vec v|\,|\vec w|\,\cos\theta",
            font_size=28, color=YELLOW,
        ).move_to([rcol_x, -2.7, 0])
        self.play(Write(formula))
        self.wait(1.0)
