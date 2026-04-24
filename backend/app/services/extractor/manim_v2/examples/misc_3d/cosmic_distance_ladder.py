from manim import *
import numpy as np


class CosmicDistanceLadderExample(Scene):
    """
    Cosmic distance ladder (from _2025/cosmic_distance): each method
    works only over a limited range, passing the baton to the next.

    SINGLE_FOCUS:
      Horizontal log-scale distance axis (in meters) from 10^0
      (1 m) to 10^26 (observable universe). ValueTracker d_tr moves a
      cursor; always_redraw marker + current method + reading. Six
      stacked method bands (radar, parallax, Cepheid, Type Ia SNe,
      redshift, CMB).
    """

    def construct(self):
        title = Tex(r"Cosmic distance ladder: each rung hands off to the next",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        nl = NumberLine(x_range=[0, 26, 2], length=12,
                         include_numbers=True,
                         decimal_number_config={"num_decimal_places": 0,
                                                 "font_size": 16}
                         ).move_to([0, -1.5, 0])
        scale_lbl = MathTex(r"\log_{10}(d / \text{m})",
                              color=WHITE, font_size=22
                              ).next_to(nl, DOWN, buff=0.35)
        self.play(Create(nl), Write(scale_lbl))

        methods = [
            ("radar", 2, 9, BLUE),
            ("parallax", 9, 18, GREEN),
            ("Cepheid", 17, 22, YELLOW),
            ("Type Ia SNe", 20, 25, ORANGE),
            ("redshift", 22, 26, RED),
            ("CMB", 25, 26, PURPLE),
        ]

        # Draw horizontal bands above the line
        for i, (name, lo, hi, col) in enumerate(methods):
            p_lo = nl.n2p(lo)
            p_hi = nl.n2p(hi)
            y_band = 0.0 + i * 0.45
            bar = Rectangle(width=p_hi[0] - p_lo[0], height=0.35,
                             color=col, fill_opacity=0.4, stroke_width=1.5
                             ).move_to([(p_lo[0] + p_hi[0]) / 2, y_band, 0])
            self.add(bar)
            lbl = Tex(name, color=col, font_size=16).next_to(
                bar, LEFT, buff=0.1)
            self.add(lbl)

        # Fixed marker positions
        markers = [
            (0, "1 m"),
            (7, r"10^7 \text{ m: Earth}$-$radius"),
            (11, r"10^{11}: Sun$-$Earth AU"),
            (16, r"10^{16}: light$-$year"),
            (20, r"10^{20}: Milky Way"),
            (22, r"10^{22}: Andromeda"),
            (26, r"10^{26}: obs. universe"),
        ]
        for (k, lbl) in markers:
            p = nl.n2p(k)
            tick = Line(p + UP * 0.15, p + DOWN * 0.15,
                          color=WHITE, stroke_width=2)
            self.add(tick)
            self.add(Tex(rf"${lbl}$" if "$" in lbl or "{" in lbl else lbl,
                         font_size=16).next_to(p, DOWN, buff=0.2))

        d_tr = ValueTracker(0.0)

        def cursor():
            d = d_tr.get_value()
            p = nl.n2p(d)
            return VGroup(
                Line(p + UP * 0.5, p + DOWN * 0.5,
                      color=YELLOW_E, stroke_width=4),
                Dot(p, color=YELLOW_E, radius=0.12),
            )

        def reading():
            d = d_tr.get_value()
            val = 10 ** d
            # Active method
            active = None
            for (name, lo, hi, col) in methods:
                if lo <= d <= hi:
                    active = name
                    break
            active = active or "(out of range)"
            return VGroup(
                MathTex(rf"\log_{{10}} d = {d:.1f}",
                         color=YELLOW, font_size=24),
                MathTex(rf"d \approx {val:.2e}\,\text{{m}}",
                         color=YELLOW, font_size=22),
                Tex(rf"method: {active}",
                     color=WHITE, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.25)

        self.add(always_redraw(cursor), always_redraw(reading))

        self.play(d_tr.animate.set_value(26),
                   run_time=10, rate_func=linear)
        self.wait(0.5)
