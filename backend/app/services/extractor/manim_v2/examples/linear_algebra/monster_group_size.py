from manim import *
import numpy as np


class MonsterGroupSizeExample(Scene):
    """
    The Monster group: 808017424794512875886459904961710757005754368000000000
    ≈ 8 × 10⁵³ elements. Visualize the magnitude via a 10^k scale
    bar with the Monster's exponent and other touchstones.

    SINGLE_FOCUS:
      Horizontal log-scale from 10⁰ to 10⁸⁰. ValueTracker k_tr moves
      a YELLOW cursor across the scale; always_redraw the marker +
      reading; fixed labels for Z₁₂, S_{10}, atoms in universe, etc.;
      the Monster sits at 10^53.8.
    """

    def construct(self):
        title = Tex(r"The Monster group: $|M| \approx 8 \times 10^{53}$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Log scale number line 0..80
        nl = NumberLine(x_range=[0, 80, 10], length=12,
                         include_numbers=True,
                         decimal_number_config={"num_decimal_places": 0,
                                                 "font_size": 16}
                         ).move_to([0, -0.5, 0])
        scale_lbl = MathTex(r"\log_{10}(\,\text{group size}\,)",
                              color=WHITE, font_size=22
                              ).next_to(nl, DOWN, buff=0.4)
        self.play(Create(nl), Write(scale_lbl))

        markers = [
            (np.log10(12), r"\mathbb Z_{12}", BLUE, "clock group"),
            (np.log10(720), r"S_5 = 120", GREEN, "perm. of 5"),
            (np.log10(362880), r"S_9 \approx 3.6 \times 10^5",
             GREEN, "perm. of 9"),
            (23, r"\text{sec. in } 30\text{y} \approx 10^9",
             GREY_B, ""),
            (50, r"M_{24} \approx 2.4 \times 10^8", PURPLE, "Mathieu M_{24}"),
            (25, r"10^{25} \approx \text{Avogadro}", GREY_B, ""),
            (80, r"10^{80} \approx \text{atoms in universe}",
             RED, ""),
            (np.log10(8.08 * 10**53), r"|M| \approx 8 \times 10^{53}",
             YELLOW, "Monster"),
        ]

        for (k, lbl, color, _) in markers:
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
            return MathTex(rf"\text{{value}} \approx 10^{{{k:.1f}}} \approx {val:.3g}",
                             color=YELLOW, font_size=24
                             ).to_edge(DOWN, buff=0.4)

        self.add(always_redraw(cursor), always_redraw(reading))

        self.play(k_tr.animate.set_value(80),
                   run_time=8, rate_func=linear)
        self.wait(0.5)
