from manim import *
import numpy as np


class LaplaceDerivativePropertyExample(Scene):
    """
    Laplace transform of a derivative (from _2025/laplace/derivatives):
    L{f'(t)} = s F(s) − f(0). Verify on f(t) = e^(-at): f'(t) = -a e^(-at),
    F(s) = 1/(s+a), L{f'} = -a/(s+a) = s/(s+a) − 1.

    TWO_COLUMN:
      LEFT  — time-domain axes; always_redraw BLUE f(t) = e^(-at)
              and ORANGE f'(t) = -a e^(-at); ValueTracker a_tr tunes
              decay rate 0.5 → 2.5.
      RIGHT — Laplace-domain axes; GREEN F(s) = 1/(s+a) and RED
              s·F(s) − f(0) = -a/(s+a), both always_redraw. Both
              curves match — verifying the derivative property.
    """

    def construct(self):
        title = Tex(r"$\mathcal L\{f'(t)\} = sF(s) - f(0)$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # LEFT
        ax_t = Axes(x_range=[0, 5, 1], y_range=[-2.2, 1.2, 0.5],
                     x_length=6, y_length=3.0, tips=False,
                     axis_config={"font_size": 14, "include_numbers": True}
                     ).move_to([-3.3, 1.4, 0])
        tl = MathTex(r"t", font_size=20).next_to(ax_t, DOWN, buff=0.1)
        self.play(Create(ax_t), Write(tl))

        a_tr = ValueTracker(1.0)

        def f_curve():
            a = a_tr.get_value()
            return ax_t.plot(lambda t: np.exp(-a * t),
                              x_range=[0, 5, 0.05],
                              color=BLUE, stroke_width=3)

        def fp_curve():
            a = a_tr.get_value()
            return ax_t.plot(lambda t: -a * np.exp(-a * t),
                              x_range=[0, 5, 0.05],
                              color=ORANGE, stroke_width=3)

        self.add(always_redraw(f_curve), always_redraw(fp_curve))

        f_lbl = MathTex(r"f(t) = e^{-at}",
                          color=BLUE, font_size=22
                          ).move_to([-0.5, 2.8, 0])
        fp_lbl = MathTex(r"f'(t) = -a e^{-at}",
                           color=ORANGE, font_size=22
                           ).next_to(f_lbl, DOWN, buff=0.15)
        self.play(Write(f_lbl), Write(fp_lbl))

        # RIGHT
        ax_s = Axes(x_range=[0, 4, 1], y_range=[-2.2, 1.2, 0.5],
                     x_length=6, y_length=3.0, tips=False,
                     axis_config={"font_size": 14, "include_numbers": True}
                     ).move_to([-3.3, -1.8, 0])
        sl = MathTex(r"s", font_size=20).next_to(ax_s, DOWN, buff=0.1)
        self.play(Create(ax_s), Write(sl))

        def F_curve():
            a = a_tr.get_value()
            return ax_s.plot(lambda s: 1 / (s + a),
                              x_range=[0.02, 4, 0.02],
                              color=GREEN, stroke_width=3)

        def sFm1_curve():
            a = a_tr.get_value()
            # s·F(s) - f(0) = s/(s+a) - 1 = -a/(s+a)
            return ax_s.plot(lambda s: -a / (s + a),
                              x_range=[0.02, 4, 0.02],
                              color=RED, stroke_width=3,
                              stroke_opacity=0.7)

        self.add(always_redraw(F_curve), always_redraw(sFm1_curve))

        F_lbl = MathTex(r"F(s) = \frac{1}{s+a}",
                          color=GREEN, font_size=22
                          ).move_to([1.7, -0.9, 0])
        sF_lbl = MathTex(r"sF(s) - f(0) = -\frac{a}{s+a}",
                           color=RED, font_size=22
                           ).next_to(F_lbl, DOWN, buff=0.2)
        self.play(Write(F_lbl), Write(sF_lbl))

        def info():
            a = a_tr.get_value()
            return VGroup(
                MathTex(rf"a = {a:.2f}", color=YELLOW, font_size=24),
                Tex(r"L$\{e^{-at}\}$ = 1/(s+a)",
                     color=GREEN, font_size=20),
                Tex(r"L$\{-ae^{-at}\}$ = -a/(s+a)",
                     color=RED, font_size=20),
                MathTex(r"s \cdot \tfrac{1}{s+a} - 1 = -\tfrac{a}{s+a} \checkmark",
                         color=YELLOW, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.3, -0.5, 0])

        self.add(always_redraw(info))

        for av in [0.5, 1.8, 2.5, 1.0]:
            self.play(a_tr.animate.set_value(av),
                       run_time=1.6, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.4)
