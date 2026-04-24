from manim import *
import numpy as np


class TwoToThe256Example(Scene):
    """
    2^256 ≈ 1.158 × 10^77 — larger than the estimated number of atoms
    in the observable universe (~10^80, so not quite, but close).

    SINGLE_FOCUS:
      ValueTracker k_tr steps through powers 2^k for k = 1, 2, 4, 8,
      16, 32, 64, 128, 256. A doubling visualization: start with one
      dot, double k times. After a few steps, dots are too many to
      show individually; switch to a log-scale number line overlay.
    """

    def construct(self):
        title = Tex(r"$2^{256}$: doubling until the universe is too small",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Log scale 0..80 number line
        nl = NumberLine(x_range=[0, 80, 10], length=12,
                         include_numbers=True,
                         decimal_number_config={"num_decimal_places": 0,
                                                 "font_size": 16}
                         ).move_to([0, -1.0, 0])
        scale_lbl = MathTex(r"\log_{10}(\#)", color=WHITE, font_size=22
                              ).next_to(nl, DOWN, buff=0.35)
        self.play(Create(nl), Write(scale_lbl))

        # Reference markers
        refs = [
            (9, r"\text{sec. in 30y}", BLUE),
            (22, r"\text{stars in universe}", PURPLE),
            (50, r"\text{atoms in Earth}", ORANGE),
            (80, r"\text{atoms in universe}", RED),
        ]
        for (k, lbl, c) in refs:
            p = nl.n2p(k)
            tick = Line(p + UP * 0.18, p + DOWN * 0.18,
                          color=c, stroke_width=3)
            self.add(tick)
            self.add(MathTex(lbl, font_size=18, color=c).next_to(p, UP, buff=0.2))

        # Doubling ladder visualization at top
        k_tr = ValueTracker(0)

        def ladder_value():
            k = int(round(k_tr.get_value()))
            return 2 ** k

        def cursor():
            k = k_tr.get_value()
            v = 2 ** k
            import math
            if v > 0:
                log10 = math.log10(v)
            else:
                log10 = 0
            p = nl.n2p(min(log10, 80))
            return VGroup(
                Line(p + UP * 0.35, p + DOWN * 0.35,
                      color=YELLOW, stroke_width=4),
                Dot(p, color=YELLOW, radius=0.12),
            )

        def step_info():
            k = int(round(k_tr.get_value()))
            v = 2 ** k
            return VGroup(
                MathTex(rf"k = {k}", color=WHITE, font_size=24),
                MathTex(rf"2^k = {v:.3e}" if v >= 10000 else rf"2^k = {v}",
                         color=YELLOW, font_size=26),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4).shift(UP * 1.8)

        self.add(always_redraw(cursor), always_redraw(step_info))

        doubling_note = Tex(r"Each step doubles. Log stops compressing.",
                              color=GREEN, font_size=20
                              ).to_edge(DOWN, buff=0.4)
        self.play(Write(doubling_note))

        for target in [8, 16, 32, 64, 128, 256]:
            self.play(k_tr.animate.set_value(target),
                       run_time=1.3, rate_func=smooth)
            self.wait(0.4)

        final = MathTex(r"2^{256} \approx 1.158 \times 10^{77}",
                         color=YELLOW, font_size=28
                         ).to_edge(LEFT, buff=0.4).shift(DOWN * 3.2)
        self.play(Write(final))
        self.wait(0.4)
