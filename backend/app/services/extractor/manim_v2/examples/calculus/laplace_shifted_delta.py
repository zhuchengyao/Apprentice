from manim import *
import numpy as np


class LaplaceShiftedDeltaExample(Scene):
    """
    Laplace transform of a shifted delta: L{δ(t - a)} = e^{-as}.

    TWO_COLUMN:
      LEFT  — time axes with a narrow spike ("δ(t-a)") placed at
              t = a; ValueTracker a_tr slides the spike from 0.5 → 4.
      RIGHT — Laplace-domain axes showing F(s) = e^{-as} as a curve
              always_redraw; ValueTracker s marked with a cursor to
              sample specific s values.
    """

    def construct(self):
        title = Tex(r"Laplace of shifted delta: $\mathcal L\{\delta(t - a)\} = e^{-a s}$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # LEFT: time domain
        ax_t = Axes(x_range=[0, 5, 1], y_range=[0, 3, 1],
                     x_length=6, y_length=3.0, tips=False,
                     axis_config={"font_size": 14, "include_numbers": True}
                     ).move_to([-3.2, 1.3, 0])
        t_lbl = MathTex(r"t", font_size=22).next_to(ax_t, DOWN, buff=0.1)
        f_lbl = MathTex(r"\delta(t - a)", color=YELLOW, font_size=22
                         ).next_to(ax_t, LEFT, buff=0.1)
        self.play(Create(ax_t), Write(t_lbl), Write(f_lbl))

        a_tr = ValueTracker(1.0)

        def delta_spike():
            a = a_tr.get_value()
            return VGroup(
                Line(ax_t.c2p(a, 0), ax_t.c2p(a, 2.7),
                      color=YELLOW, stroke_width=6),
                Triangle(color=YELLOW, fill_opacity=1.0
                          ).scale(0.12).move_to(ax_t.c2p(a, 2.7)),
                MathTex(rf"a = {a:.2f}", color=YELLOW, font_size=18
                          ).next_to(ax_t.c2p(a, 0), DOWN, buff=0.15),
            )

        self.add(always_redraw(delta_spike))

        # RIGHT: Laplace domain
        ax_s = Axes(x_range=[0, 3, 0.5], y_range=[0, 1.1, 0.25],
                     x_length=6, y_length=3.0, tips=False,
                     axis_config={"font_size": 14, "include_numbers": True}
                     ).move_to([-3.2, -1.8, 0])
        s_lbl = MathTex(r"s", font_size=22).next_to(ax_s, DOWN, buff=0.1)
        F_lbl = MathTex(r"F(s) = e^{-a s}", color=GREEN, font_size=22
                         ).next_to(ax_s, LEFT, buff=0.1)
        self.play(Create(ax_s), Write(s_lbl), Write(F_lbl))

        def F_curve():
            a = a_tr.get_value()
            return ax_s.plot(lambda s: np.exp(-a * s),
                              x_range=[0, 3, 0.02],
                              color=GREEN, stroke_width=4)

        self.add(always_redraw(F_curve))

        # Cursor at s = 1 showing F(1) = e^-a
        s_probe = 1.0

        def cursor():
            a = a_tr.get_value()
            val = np.exp(-a * s_probe)
            return VGroup(
                DashedLine(ax_s.c2p(s_probe, 0),
                            ax_s.c2p(s_probe, val),
                            color=RED, stroke_width=1.5),
                Dot(ax_s.c2p(s_probe, val),
                     color=RED, radius=0.09),
            )

        self.add(always_redraw(cursor))

        def info():
            a = a_tr.get_value()
            F1 = np.exp(-a * s_probe)
            return VGroup(
                MathTex(rf"a = {a:.3f}", color=YELLOW, font_size=24),
                MathTex(rf"F(s) = e^{{-a s}}", color=GREEN, font_size=22),
                MathTex(rf"F(1) = e^{{-a}} = {F1:.4f}",
                         color=RED, font_size=22),
                Tex(r"shifting $a$ $\Leftrightarrow$ scaling $F$",
                     color=WHITE, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.0, 0.0, 0])

        self.add(always_redraw(info))

        for a in [0.5, 2.0, 3.5, 1.0, 2.5]:
            self.play(a_tr.animate.set_value(a),
                       run_time=1.8, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.3)
