from manim import *
import numpy as np


class SimpleRatiosHarmonyExample(Scene):
    """
    Consonance via low-integer ratios (different from
    harmonic_ratios_table): ValueTracker r_tr slides r continuously
    across [1, 2] and the beat pattern of sin(2πt) + sin(2πr·t)
    shows regular repetition ONLY at rational r with small
    denominator — signaled by a shaded bar quantifying "repeat
    period" normalized against 4.

    SINGLE_FOCUS:
      LEFT: combined wave sin(2πt) + sin(2πr·t) over [0, 4];
      ValueTracker r_tr sweeps continuously 1→2. GREEN vertical
      bars mark every multiple of the beat period
      T_beat = 1/|r - 1|; smaller |r - 1| or rational r with small
      denominator keeps T_beat bounded and periodic.
    """

    def construct(self):
        title = Tex(r"Beat pattern of $\sin(2\pi t)+\sin(2\pi r t)$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ax = Axes(x_range=[0, 8, 1], y_range=[-2.2, 2.2, 1],
                   x_length=11, y_length=3.2, tips=False,
                   axis_config={"font_size": 16, "include_numbers": True}
                   ).move_to([0, 0.2, 0])
        self.play(Create(ax))

        r_tr = ValueTracker(1.0)

        def wave():
            r = r_tr.get_value()
            return ax.plot(
                lambda t: np.sin(2 * PI * t) + np.sin(2 * PI * r * t),
                x_range=[0, 8, 0.02], color=BLUE, stroke_width=2.5)

        def envelope():
            r = r_tr.get_value()
            diff = max(abs(r - 1), 0.001)
            return ax.plot(
                lambda t: 2 * abs(np.cos(PI * (r - 1) * t)),
                x_range=[0, 8, 0.02], color=YELLOW, stroke_width=2,
                stroke_opacity=0.45)

        def env_neg():
            r = r_tr.get_value()
            return ax.plot(
                lambda t: -2 * abs(np.cos(PI * (r - 1) * t)),
                x_range=[0, 8, 0.02], color=YELLOW, stroke_width=2,
                stroke_opacity=0.45)

        self.add(always_redraw(wave),
                  always_redraw(envelope),
                  always_redraw(env_neg))

        def info():
            r = r_tr.get_value()
            if abs(r - 1) < 1e-4:
                Tbeat = float("inf")
                Tbeat_txt = r"T_{\text{beat}} = \infty"
            else:
                Tbeat = 1 / abs(r - 1)
                Tbeat_txt = rf"T_{{\text{{beat}}}} = {Tbeat:.3f}"
            # find closest rational with small q
            best = (1e9, 1, 1)
            for q in range(1, 12):
                for p in range(q, 2 * q + 1):
                    err = abs(p / q - r)
                    if err < best[0]:
                        best = (err, p, q)
            _, pb, qb = best
            return VGroup(
                MathTex(rf"r = {r:.4f}", color=WHITE, font_size=26),
                MathTex(rf"\approx {pb}/{qb}", color=YELLOW, font_size=26),
                MathTex(Tbeat_txt, color=GREEN_B, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([5.0, -2.6, 0])

        self.add(always_redraw(info))

        for target in [1.5, 4 / 3, 5 / 4, np.sqrt(2), 1.618, 2.0]:
            self.play(r_tr.animate.set_value(target),
                       run_time=1.5, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
