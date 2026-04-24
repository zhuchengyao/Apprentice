from manim import *
import numpy as np


class AddingWavesSuperpositionExample(Scene):
    """
    Wave superposition (from _2023/optics_puzzles/adding_waves):
    y = cos(k x - ωt) + cos(k x - ωt + φ) shows constructive and
    destructive interference as relative phase φ varies.

    TWO_COLUMN:
      LEFT  — 3 stacked axes: wave A, wave B, their sum. ValueTracker
              phi_tr sweeps φ 0 → 2π via always_redraw.
      RIGHT — live φ, amplitude of sum 2|cos(φ/2)|, interference mode
              label.
    """

    def construct(self):
        title = Tex(r"Superposition: $A + B = 2\cos(\phi/2)$ amplitude",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ax_A = Axes(x_range=[0, 6, 1], y_range=[-1.2, 1.2, 0.5],
                     x_length=7, y_length=1.6, tips=False,
                     axis_config={"font_size": 12, "include_numbers": True}
                     ).move_to([-2, 2.0, 0])
        ax_B = Axes(x_range=[0, 6, 1], y_range=[-1.2, 1.2, 0.5],
                     x_length=7, y_length=1.6, tips=False,
                     axis_config={"font_size": 12, "include_numbers": True}
                     ).move_to([-2, 0.2, 0])
        ax_S = Axes(x_range=[0, 6, 1], y_range=[-2.2, 2.2, 1],
                     x_length=7, y_length=2.2, tips=False,
                     axis_config={"font_size": 12, "include_numbers": True}
                     ).move_to([-2, -1.7, 0])

        A_lbl = MathTex(r"A", color=BLUE, font_size=20).next_to(ax_A, LEFT, buff=0.1)
        B_lbl = MathTex(r"B", color=ORANGE, font_size=20).next_to(ax_B, LEFT, buff=0.1)
        S_lbl = MathTex(r"A+B", color=GREEN, font_size=22).next_to(ax_S, LEFT, buff=0.1)

        self.play(Create(ax_A), Create(ax_B), Create(ax_S),
                   Write(A_lbl), Write(B_lbl), Write(S_lbl))

        # Static A curve: cos(πx)
        A_curve = ax_A.plot(lambda x: np.cos(PI * x),
                              x_range=[0, 6], color=BLUE, stroke_width=2.5)
        self.play(Create(A_curve))

        phi_tr = ValueTracker(0.0)

        def B_curve():
            phi = phi_tr.get_value()
            return ax_B.plot(lambda x: np.cos(PI * x + phi),
                              x_range=[0, 6], color=ORANGE, stroke_width=2.5)

        def sum_curve():
            phi = phi_tr.get_value()
            return ax_S.plot(
                lambda x: np.cos(PI * x) + np.cos(PI * x + phi),
                x_range=[0, 6], color=GREEN, stroke_width=3)

        # Envelope |2cos(φ/2)| as dashed bounds
        def env_upper():
            phi = phi_tr.get_value()
            env = 2 * abs(np.cos(phi / 2))
            return DashedLine(ax_S.c2p(0, env), ax_S.c2p(6, env),
                               color=YELLOW, stroke_width=2)

        def env_lower():
            phi = phi_tr.get_value()
            env = 2 * abs(np.cos(phi / 2))
            return DashedLine(ax_S.c2p(0, -env), ax_S.c2p(6, -env),
                               color=YELLOW, stroke_width=2)

        self.add(always_redraw(B_curve),
                  always_redraw(sum_curve),
                  always_redraw(env_upper),
                  always_redraw(env_lower))

        def info():
            phi = phi_tr.get_value()
            amp = 2 * abs(np.cos(phi / 2))
            if abs(amp - 2) < 0.05:
                mode = "constructive"
                col = GREEN
            elif amp < 0.1:
                mode = "destructive"
                col = RED
            else:
                mode = "partial"
                col = YELLOW
            return VGroup(
                MathTex(rf"\phi = {np.degrees(phi):.0f}^\circ",
                         color=ORANGE, font_size=22),
                MathTex(rf"\text{{amp}} = 2|\cos(\phi/2)| = {amp:.3f}",
                         color=YELLOW, font_size=22),
                Tex(mode, color=col, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.3).shift(DOWN * 0.5)

        self.add(always_redraw(info))

        self.play(phi_tr.animate.set_value(2 * PI),
                   run_time=8, rate_func=linear)
        self.wait(0.5)
