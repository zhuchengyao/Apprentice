from manim import *
import numpy as np


class LaplaceExponentialExample(Scene):
    """
    Laplace transform of an exponential (from _2025/laplace/
    exponentials): L{e^(at) u(t)} = 1/(s − a) for Re(s) > a.

    TWO_COLUMN:
      LEFT  — time-axes; ValueTracker a_tr sweeps a ∈ [-1.5, 0.5];
              always_redraw e^(at) curve (decaying, constant, or
              growing depending on sign of a).
      RIGHT — Laplace-axes plotting F(s) = 1/(s - a) with
              asymptote at s = a; region Re s > a is GREEN (valid),
              s < a is RED (divergent).
    """

    def construct(self):
        title = Tex(r"$\mathcal L\{e^{at}\} = \dfrac{1}{s - a}$, $\Re(s) > a$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ax_t = Axes(x_range=[0, 5, 1], y_range=[0, 3, 0.5],
                     x_length=6, y_length=3, tips=False,
                     axis_config={"font_size": 14, "include_numbers": True}
                     ).move_to([-3.3, 1.3, 0])
        self.play(Create(ax_t))

        ax_s = Axes(x_range=[-2, 3, 1], y_range=[-3, 3, 1],
                     x_length=6, y_length=3.0, tips=False,
                     axis_config={"font_size": 14, "include_numbers": True}
                     ).move_to([-3.3, -1.8, 0])
        self.play(Create(ax_s))

        a_tr = ValueTracker(-0.8)

        def time_curve():
            a = a_tr.get_value()
            return ax_t.plot(lambda t: np.exp(a * t),
                              x_range=[0, 5, 0.02],
                              color=BLUE, stroke_width=3)

        self.add(always_redraw(time_curve))

        def F_curve():
            a = a_tr.get_value()
            # 1/(s-a) has pole at s=a; plot in two pieces
            eps = 0.05
            left_part = ax_s.plot(lambda s: 1 / (s - a),
                                    x_range=[-2, a - eps, 0.02],
                                    color=RED, stroke_width=3)
            right_part = ax_s.plot(lambda s: 1 / (s - a),
                                     x_range=[a + eps, 3, 0.02],
                                     color=GREEN, stroke_width=3)
            return VGroup(left_part, right_part)

        def pole_line():
            a = a_tr.get_value()
            return DashedLine(ax_s.c2p(a, -3), ax_s.c2p(a, 3),
                               color=YELLOW, stroke_width=2)

        self.add(always_redraw(F_curve), always_redraw(pole_line))

        a_lbl_left = MathTex(r"e^{at}",
                               color=BLUE, font_size=22
                               ).move_to([1.5, 2.3, 0])
        F_lbl = MathTex(r"F(s) = \tfrac{1}{s-a}",
                          color=GREEN, font_size=22
                          ).move_to([1.5, -0.5, 0])
        region_lbl = VGroup(
            Tex(r"$s > a$: valid (GREEN)",
                 color=GREEN, font_size=18),
            Tex(r"$s < a$: divergent (RED)",
                 color=RED, font_size=18),
            Tex(r"pole at $s = a$ (dashed)",
                 color=YELLOW, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15
                    ).next_to(F_lbl, DOWN, buff=0.3)
        self.play(Write(a_lbl_left), Write(F_lbl), Write(region_lbl))

        def info():
            a = a_tr.get_value()
            return VGroup(
                MathTex(rf"a = {a:+.2f}", color=YELLOW, font_size=24),
                Tex(rf"{('decay' if a < 0 else 'growth' if a > 0 else 'constant')}",
                     color=BLUE, font_size=22),
                MathTex(rf"F(0) = -1/a = {-1/(a + 1e-9):.3f}"
                          if abs(a) > 0.01 else r"F(0) \to \infty",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.3, -0.8, 0])

        self.add(always_redraw(info))

        for av in [-1.5, 0, 0.4, -0.5]:
            self.play(a_tr.animate.set_value(av),
                       run_time=1.6, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.4)
