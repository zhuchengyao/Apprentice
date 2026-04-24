from manim import *
import numpy as np


class RiemannZetaSeriesExample(Scene):
    """
    ζ(s) = Σ 1/n^s for real s > 1, with partial sums tracked.

    TWO_COLUMN:
      LEFT  — Axes plotting ζ(s) on real axis, with always_redraw
              moving dot at the current s. ValueTracker s_tr sweeps
              1.05 → 5.0 → 1.05; live ζ(s) computed from a 1000-term
              truncation.
      RIGHT — live readouts s, ζ(s), special values:
                ζ(2) = π²/6, ζ(4) = π⁴/90, ζ(6) = π⁶/945
              plus the partial-sum truncation explanation.
    """

    def construct(self):
        title = Tex(r"Riemann zeta on $s > 1$: $\zeta(s) = \sum_{n=1}^\infty \dfrac{1}{n^s}$",
                    font_size=26).to_edge(UP, buff=0.4)
        self.play(Write(title))

        N_terms = 1000

        def zeta_approx(s):
            return sum(1.0 / k ** s for k in range(1, N_terms + 1))

        axes = Axes(
            x_range=[1, 6, 1], y_range=[0, 6, 1],
            x_length=6.5, y_length=4.4,
            axis_config={"include_tip": True, "include_numbers": True, "font_size": 18},
        ).move_to([-2.4, -0.4, 0])
        x_lbl = MathTex(r"s", font_size=22).next_to(axes, DOWN, buff=0.1)
        y_lbl = MathTex(r"\zeta(s)", font_size=22).next_to(axes, LEFT, buff=0.1)
        self.play(Create(axes), Write(x_lbl), Write(y_lbl))

        graph = axes.plot(zeta_approx, x_range=[1.05, 5.95, 0.05], color=BLUE)
        self.play(Create(graph), run_time=2)

        s_tr = ValueTracker(2.0)

        def moving_dot():
            s = s_tr.get_value()
            return Dot(axes.c2p(s, zeta_approx(s)), color=YELLOW, radius=0.10)

        def vert_line():
            s = s_tr.get_value()
            top = axes.c2p(s, zeta_approx(s))
            bot = axes.c2p(s, 0)
            return DashedLine(bot, top, color=YELLOW, stroke_width=2)

        self.add(always_redraw(moving_dot), always_redraw(vert_line))

        # RIGHT COLUMN
        rcol_x = +3.6

        def info_panel():
            s = s_tr.get_value()
            z = zeta_approx(s)
            return VGroup(
                MathTex(rf"s = {s:.3f}", color=WHITE, font_size=24),
                MathTex(rf"\zeta(s) \approx {z:.4f}",
                        color=YELLOW, font_size=26),
                MathTex(rf"\text{{(}}{N_terms}\text{{ terms)}}",
                        color=GREY_B, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([rcol_x, +2.0, 0])

        self.add(always_redraw(info_panel))

        special = VGroup(
            MathTex(r"\zeta(2) = \tfrac{\pi^2}{6} \approx 1.6449",
                    color=GREEN, font_size=22),
            MathTex(r"\zeta(4) = \tfrac{\pi^4}{90} \approx 1.0823",
                    color=GREEN, font_size=22),
            MathTex(r"\zeta(6) = \tfrac{\pi^6}{945} \approx 1.0173",
                    color=GREEN, font_size=22),
            MathTex(r"\zeta(s) \to 1\ \text{as}\ s \to \infty",
                    color=YELLOW, font_size=22),
            MathTex(r"\zeta(s) \to \infty\ \text{as}\ s \to 1^+",
                    color=ORANGE, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([rcol_x, -1.0, 0])
        self.play(Write(special))

        # Sweep s through several values
        for tgt in [3.0, 5.0, 1.5, 2.0, 1.1]:
            self.play(s_tr.animate.set_value(tgt),
                      run_time=2.0, rate_func=smooth)
            self.wait(0.3)
        self.wait(0.5)
