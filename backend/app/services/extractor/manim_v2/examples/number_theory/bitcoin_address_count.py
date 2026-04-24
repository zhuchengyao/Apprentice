from manim import *
import numpy as np


class BitcoinAddressCountExample(Scene):
    """
    A Bitcoin address is a 160-bit hash; total distinct addresses
    ≈ 2^160 ≈ 1.46 × 10⁴⁸. Visualize this magnitude via a log-scale
    comparison chart.

    SINGLE_FOCUS:
      Log10 scale 0..55 along a number line. Fixed labels for atoms
      in a person (10^27), stars in a galaxy (10^11), etc. ValueTracker
      k_tr sweeps a cursor; always_redraw moving marker and reading.
      Bitcoin marker at log10(2^160) ≈ 48.16.
    """

    def construct(self):
        title = Tex(r"Bitcoin addresses: $2^{160} \approx 1.46 \times 10^{48}$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        nl = NumberLine(x_range=[0, 55, 10], length=12,
                         include_numbers=True,
                         decimal_number_config={"num_decimal_places": 0,
                                                 "font_size": 16}
                         ).move_to([0, -0.5, 0])
        scale_lbl = MathTex(r"\log_{10}(\#)",
                              color=WHITE, font_size=22
                              ).next_to(nl, DOWN, buff=0.35)
        self.play(Create(nl), Write(scale_lbl))

        markers = [
            (4, r"10^4 \approx 10,\!000 \text{ people}", BLUE),
            (9, r"10^9 \approx \text{seconds in 30y}", GREEN),
            (11, r"10^{11} \approx \text{stars in galaxy}", GREEN),
            (22, r"10^{22} \approx \text{all stars in universe}", PURPLE),
            (27, r"10^{27} \approx \text{atoms in person}", PURPLE),
            (48.16, r"2^{160} \approx 1.46 \times 10^{48}", YELLOW),
            (50, r"10^{50} \approx \text{atoms in Earth}", RED),
        ]

        for (k, lbl, color) in markers:
            p = nl.n2p(k)
            tick = Line(p + UP * 0.2, p + DOWN * 0.2,
                          color=color, stroke_width=3)
            txt = MathTex(lbl, font_size=18, color=color).next_to(
                p, UP, buff=0.3)
            self.add(tick, txt)

        k_tr = ValueTracker(0.0)

        def cursor():
            k = k_tr.get_value()
            p = nl.n2p(k)
            return VGroup(
                Line(p + UP * 0.35, p + DOWN * 0.35,
                      color=YELLOW_E, stroke_width=4),
                Dot(p, color=YELLOW_E, radius=0.1),
            )

        def reading():
            k = k_tr.get_value()
            val = 10 ** k
            return MathTex(rf"\log_{{10}} = {k:.1f},\ \text{{value}} \approx {val:.3g}",
                             color=YELLOW, font_size=24
                             ).to_edge(DOWN, buff=0.4)

        self.add(always_redraw(cursor), always_redraw(reading))

        self.play(k_tr.animate.set_value(55),
                   run_time=8, rate_func=linear)
        self.wait(0.5)
