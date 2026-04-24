from manim import *
import numpy as np


class LaplaceInverseTransformExample(Scene):
    """
    Inverse Laplace transform via partial fractions: for F(s) =
    1/((s+1)(s+2)), partial fractions = 1/(s+1) - 1/(s+2) which
    inverts to e^(-t) - e^(-2t). Show both pieces converging to the
    sum.

    TWO_COLUMN:
      LEFT  — axes with BLUE e^(-t), ORANGE -e^(-2t), GREEN sum;
              ValueTracker t_tr moves cursor.
      RIGHT  — Laplace-domain F(s) curve.
    """

    def construct(self):
        title = Tex(r"Inverse Laplace: $\mathcal L^{-1}\{\tfrac{1}{(s+1)(s+2)}\} = e^{-t} - e^{-2t}$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ax_L = Axes(x_range=[0, 5, 1], y_range=[-0.5, 1.1, 0.25],
                     x_length=7, y_length=4, tips=False,
                     axis_config={"font_size": 14, "include_numbers": True}
                     ).move_to([-2.5, -0.3, 0])
        xl = MathTex(r"t", font_size=18).next_to(ax_L, DOWN, buff=0.1)
        self.play(Create(ax_L), Write(xl))

        exp_neg_t = ax_L.plot(lambda t: np.exp(-t),
                                x_range=[0, 5, 0.02],
                                color=BLUE, stroke_width=2.5)
        neg_exp_neg_2t = ax_L.plot(lambda t: -np.exp(-2 * t),
                                      x_range=[0, 5, 0.02],
                                      color=ORANGE, stroke_width=2.5)
        sum_curve = ax_L.plot(lambda t: np.exp(-t) - np.exp(-2 * t),
                                x_range=[0, 5, 0.02],
                                color=GREEN, stroke_width=3.5)
        b_lbl = MathTex(r"e^{-t}", color=BLUE, font_size=18
                          ).next_to(ax_L.c2p(4, np.exp(-4)), UR, buff=0.05)
        o_lbl = MathTex(r"-e^{-2t}", color=ORANGE, font_size=18
                          ).next_to(ax_L.c2p(4, -np.exp(-8)), DR, buff=0.05)
        g_lbl = MathTex(r"f(t)", color=GREEN, font_size=20
                          ).next_to(ax_L.c2p(2, np.exp(-2) - np.exp(-4)),
                                      UR, buff=0.1)
        self.play(Create(exp_neg_t), Create(neg_exp_neg_2t),
                   Create(sum_curve), Write(b_lbl), Write(o_lbl), Write(g_lbl))

        t_tr = ValueTracker(0.01)

        def rider_sum():
            t = t_tr.get_value()
            f = np.exp(-t) - np.exp(-2 * t)
            return Dot(ax_L.c2p(t, f), color=GREEN, radius=0.1)

        def rider_blue():
            t = t_tr.get_value()
            return Dot(ax_L.c2p(t, np.exp(-t)), color=BLUE, radius=0.08)

        def rider_orange():
            t = t_tr.get_value()
            return Dot(ax_L.c2p(t, -np.exp(-2 * t)),
                        color=ORANGE, radius=0.08)

        self.add(always_redraw(rider_sum),
                  always_redraw(rider_blue),
                  always_redraw(rider_orange))

        # RIGHT: F(s)
        ax_R = Axes(x_range=[0, 4, 1], y_range=[0, 1, 0.25],
                     x_length=4, y_length=3, tips=False,
                     axis_config={"font_size": 12, "include_numbers": True}
                     ).move_to([3.8, 0.5, 0])
        xl_R = MathTex(r"s", font_size=14).next_to(ax_R, DOWN, buff=0.08)
        yl_R = MathTex(r"F(s)", font_size=14).next_to(ax_R, LEFT, buff=0.08)
        F_curve = ax_R.plot(lambda s: 1 / ((s + 1) * (s + 2)),
                              x_range=[0, 4, 0.02],
                              color=RED, stroke_width=3)
        F_lbl = MathTex(r"\tfrac{1}{(s+1)(s+2)}",
                          color=RED, font_size=16
                          ).next_to(ax_R.c2p(1, 1 / 6), UR, buff=0.1)
        self.play(Create(ax_R), Write(xl_R), Write(yl_R),
                   Create(F_curve), Write(F_lbl))

        def info():
            t = t_tr.get_value()
            f = np.exp(-t) - np.exp(-2 * t)
            return VGroup(
                MathTex(rf"t = {t:.2f}", color=GREEN, font_size=22),
                MathTex(rf"f(t) = {f:.4f}", color=GREEN, font_size=20),
                Tex(r"partial fractions:",
                     color=YELLOW, font_size=18),
                MathTex(r"\tfrac{1}{(s+1)(s+2)} = \tfrac{1}{s+1} - \tfrac{1}{s+2}",
                         color=YELLOW, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        self.play(t_tr.animate.set_value(5),
                   run_time=6, rate_func=linear)
        self.wait(0.4)
