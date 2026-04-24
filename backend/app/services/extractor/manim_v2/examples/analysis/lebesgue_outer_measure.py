from manim import *
import numpy as np


class LebesgueOuterMeasureExample(Scene):
    """
    Lebesgue outer measure: m*(E) = inf{Σ |I_k| : E ⊂ ∪I_k, I_k open
    intervals}. Demonstrate for E = [0.2, 0.7]:
      N=1 covers: |I_1| ≥ 0.5
      Refined: approach 0.5 via Σ = 0.5 + ε.
    Cantor set has m* = 0 (can be covered by arbitrarily small total).

    TWO_COLUMN: LEFT number line with E highlighted + covering
    intervals shown; ValueTracker n_tr refines cover. RIGHT shows
    total measure → |E|.
    """

    def construct(self):
        title = Tex(r"Lebesgue outer measure: $m^*(E)=\inf \sum|I_k|$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        line = NumberLine(x_range=[0, 1, 0.1], length=10,
                          include_numbers=True,
                          font_size=18).shift(DOWN * 1.5)
        self.play(Create(line))

        # E = [0.2, 0.7]
        E = Line(line.n2p(0.2), line.n2p(0.7),
                 color=BLUE, stroke_width=8)
        E_lbl = Tex(r"$E=[0.2, 0.7]$", color=BLUE, font_size=24).next_to(E, UP, buff=0.15)
        self.play(Create(E), Write(E_lbl))

        n_tr = ValueTracker(1.0)

        def cover_intervals():
            n = int(round(n_tr.get_value()))
            n = max(1, min(20, n))
            # Split E = [0.2, 0.7] into n subintervals plus slight margin
            margin = 0.5 / n
            grp = VGroup()
            step = 0.5 / n
            for k in range(n):
                a = 0.2 + k * step - margin * 0.3
                b = 0.2 + (k + 1) * step + margin * 0.3
                y = 0.9 + k * 0.08 / n
                seg = Line(line.n2p(max(0, a)) + UP * y,
                            line.n2p(min(1, b)) + UP * y,
                            color=YELLOW, stroke_width=5)
                grp.add(seg)
                grp.add(Line(line.n2p(max(0, a)) + UP * (y - 0.05),
                              line.n2p(max(0, a)) + UP * (y + 0.05),
                              color=YELLOW, stroke_width=2))
                grp.add(Line(line.n2p(min(1, b)) + UP * (y - 0.05),
                              line.n2p(min(1, b)) + UP * (y + 0.05),
                              color=YELLOW, stroke_width=2))
            return grp

        self.add(always_redraw(cover_intervals))

        def total_measure():
            n = int(round(n_tr.get_value()))
            n = max(1, min(20, n))
            margin = 0.5 / n
            step = 0.5 / n
            return n * (step + 0.6 * margin)

        info = VGroup(
            VGroup(Tex(r"pieces $n=$", font_size=24),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=24).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\sum|I_k|=$", font_size=24),
                   DecimalNumber(0.8, num_decimal_places=4,
                                 font_size=24).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"$m^*(E)=|E|=0.5$", color=BLUE, font_size=24),
            Tex(r"$m^*$ attained as $n\to\infty$, margin $\to 0$",
                color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(UP, buff=1.5).shift(LEFT * 3.5)
        info[0][1].add_updater(lambda m: m.set_value(
            max(1, min(20, int(round(n_tr.get_value()))))))
        info[1][1].add_updater(lambda m: m.set_value(total_measure()))
        self.add(info)

        self.play(n_tr.animate.set_value(20.0),
                  run_time=6, rate_func=linear)
        self.wait(0.8)
