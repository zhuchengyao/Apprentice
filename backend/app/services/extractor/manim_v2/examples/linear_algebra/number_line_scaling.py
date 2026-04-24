from manim import *
import numpy as np


class NumberLineScalingExample(Scene):
    """
    The 1D linear transformation x ↦ k·x: scaling of ℝ.

    TWO_COLUMN:
      LEFT  — input number line with a BLUE point at x and an
              ORANGE interval around it; output number line with
              the scaled image k·x and the stretched interval.
              ValueTracker k_tr sweeps k through -2, -1, 0, 0.5, 1, 2, 3.
      RIGHT — live k, x, k·x; determinant-of-1x1 panel |k|; formula.
    """

    def construct(self):
        title = Tex(r"1D linear map $T(x) = k\,x$: scale + flip",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        input_nl = NumberLine(x_range=[-5, 5, 1], length=10,
                                include_numbers=True,
                                decimal_number_config={"num_decimal_places": 0,
                                                        "font_size": 16}
                                ).move_to([0, 1.2, 0])
        output_nl = NumberLine(x_range=[-5, 5, 1], length=10,
                                include_numbers=True,
                                decimal_number_config={"num_decimal_places": 0,
                                                        "font_size": 16}
                                ).move_to([0, -1.2, 0])
        in_lbl = Tex(r"input $x$", color=BLUE, font_size=22
                      ).next_to(input_nl, LEFT, buff=0.2)
        out_lbl = Tex(r"output $k x$", color=YELLOW, font_size=22
                       ).next_to(output_nl, LEFT, buff=0.2)
        self.play(Create(input_nl), Create(output_nl),
                   Write(in_lbl), Write(out_lbl))

        k_tr = ValueTracker(1.0)
        x_tr = ValueTracker(1.5)
        dx = 0.4

        def input_dot():
            x = x_tr.get_value()
            return Dot(input_nl.n2p(x), color=BLUE, radius=0.12)

        def input_interval():
            x = x_tr.get_value()
            return Line(input_nl.n2p(x - dx), input_nl.n2p(x + dx),
                          color=ORANGE, stroke_width=6)

        def output_dot():
            x = x_tr.get_value()
            k = k_tr.get_value()
            y = max(-4.9, min(4.9, k * x))
            return Dot(output_nl.n2p(y), color=YELLOW, radius=0.12)

        def output_interval():
            x = x_tr.get_value()
            k = k_tr.get_value()
            lo = max(-4.9, min(4.9, k * (x - dx)))
            hi = max(-4.9, min(4.9, k * (x + dx)))
            return Line(output_nl.n2p(lo), output_nl.n2p(hi),
                          color=ORANGE, stroke_width=6)

        def connector():
            x = x_tr.get_value()
            k = k_tr.get_value()
            y = max(-4.9, min(4.9, k * x))
            return DashedLine(input_nl.n2p(x), output_nl.n2p(y),
                               color=GREY_B, stroke_width=1.5)

        self.add(always_redraw(input_interval),
                  always_redraw(output_interval),
                  always_redraw(connector),
                  always_redraw(input_dot),
                  always_redraw(output_dot))

        def info():
            x = x_tr.get_value()
            k = k_tr.get_value()
            return VGroup(
                MathTex(rf"k = {k:+.2f}", color=YELLOW, font_size=26),
                MathTex(rf"x = {x:+.2f}", color=BLUE, font_size=24),
                MathTex(rf"kx = {k*x:+.2f}",
                         color=GREEN, font_size=24),
                MathTex(rf"|\det\,T| = |k| = {abs(k):.2f}",
                         color=RED, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(LEFT, buff=0.5).shift(DOWN * 3.2)

        self.add(always_redraw(info))

        tour_k = [2.0, -1.0, 0.5, 3.0, 0.0, 1.0]
        for kv in tour_k:
            self.play(k_tr.animate.set_value(kv),
                       run_time=1.4, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.3)
