from manim import *
import numpy as np


class MatrixExponentialExample(Scene):
    """
    e^(At) for A = [[0, -1], [1, 0]] = pure rotation through angle t.

    TWO_COLUMN:
      LEFT  — NumberPlane with i-hat (green) and j-hat (red) under
              the action of e^(At). ValueTracker t sweeps; both basis
              arrows rotate via always_redraw to e^(At) · ê.
      RIGHT — live readouts of t, the rotation matrix entries cos t,
              sin t, plus the partial-sum approximation
              I + At + (At)²/2! + (At)³/3! + (At)⁴/4! comparing to
              the closed form. The two agree to ~5 decimals at t=π/2.
    """

    def construct(self):
        title = Tex(r"$e^{At}$ for $A = \begin{bmatrix}0 & -1 \\ 1 & 0\end{bmatrix}$ is rotation by $t$",
                    font_size=26).to_edge(UP, buff=0.4)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-2, 2, 1], y_range=[-2, 2, 1],
            x_length=5.0, y_length=5.0,
            background_line_style={"stroke_opacity": 0.3},
        ).move_to([-3.0, -0.4, 0])
        self.play(Create(plane))

        t_tr = ValueTracker(0.001)

        def rot(t):
            return np.array([[np.cos(t), -np.sin(t)],
                             [np.sin(t),  np.cos(t)]])

        def i_arrow():
            v = rot(t_tr.get_value()) @ np.array([1.5, 0])
            return Arrow(plane.c2p(0, 0), plane.c2p(v[0], v[1]),
                         buff=0, color=GREEN, stroke_width=5,
                         max_tip_length_to_length_ratio=0.12)

        def j_arrow():
            v = rot(t_tr.get_value()) @ np.array([0, 1.5])
            return Arrow(plane.c2p(0, 0), plane.c2p(v[0], v[1]),
                         buff=0, color=RED, stroke_width=5,
                         max_tip_length_to_length_ratio=0.12)

        def i_lbl():
            v = rot(t_tr.get_value()) @ np.array([1.5, 0])
            return MathTex(r"\hat i", color=GREEN, font_size=22).next_to(
                plane.c2p(v[0], v[1]), UR, buff=0.05)

        def j_lbl():
            v = rot(t_tr.get_value()) @ np.array([0, 1.5])
            return MathTex(r"\hat j", color=RED, font_size=22).next_to(
                plane.c2p(v[0], v[1]), UR, buff=0.05)

        self.add(always_redraw(i_arrow), always_redraw(j_arrow),
                 always_redraw(i_lbl), always_redraw(j_lbl))

        # RIGHT COLUMN
        rcol_x = +3.6

        def matrix_panel():
            t = t_tr.get_value()
            # Closed form
            c = np.cos(t)
            s = np.sin(t)
            # Partial sum I + At + (At)^2/2! + (At)^3/3! + (At)^4/4!
            A = np.array([[0.0, -1.0], [1.0, 0.0]])
            P = np.eye(2)
            partial = np.eye(2).copy()
            for k in range(1, 8):
                P = (P @ A) * t / k
                partial = partial + P
            return VGroup(
                MathTex(rf"t = {t:.3f}", color=WHITE, font_size=24),
                MathTex(rf"\cos t = {c:+.4f}", color=GREEN, font_size=22),
                MathTex(rf"\sin t = {s:+.4f}", color=GREEN, font_size=22),
                MathTex(
                    r"e^{At} = \begin{bmatrix}\cos t & -\sin t \\ \sin t & \cos t\end{bmatrix}",
                    color=YELLOW, font_size=24,
                ),
                MathTex(
                    rf"\approx \begin{{bmatrix}}{partial[0,0]:+.4f} & {partial[0,1]:+.4f} \\ "
                    rf"{partial[1,0]:+.4f} & {partial[1,1]:+.4f}\end{{bmatrix}}",
                    color=ORANGE, font_size=22,
                ),
                MathTex(r"\text{(7-term partial sum)}",
                        color=GREY_B, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([rcol_x, +0.4, 0])

        self.add(always_redraw(matrix_panel))

        defn = MathTex(r"e^{At} = \sum_{k=0}^{\infty} \frac{(At)^k}{k!}",
                       color=YELLOW, font_size=26).move_to([rcol_x, -3.0, 0])
        self.play(Write(defn))

        # Sweep t through 2π
        self.play(t_tr.animate.set_value(2 * PI),
                  run_time=8, rate_func=linear)
        self.wait(0.5)
