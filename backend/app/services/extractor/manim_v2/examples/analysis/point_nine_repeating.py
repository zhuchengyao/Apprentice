from manim import *
import numpy as np


class PointNineRepeatingExample(Scene):
    """
    0.999... = 1 demonstrated by partial sums S_n = 1 - 10^(-n).

    TWO_COLUMN:
      LEFT  — number line [0, 1] with always_redraw markers at S_n
              for n = 1..N. ValueTracker N steps 1..15; each time N
              advances, a new dot appears at S_n with label "0.99..9".
              All dots cluster ever closer to 1.
      RIGHT — geometric-series derivation: 0.999... = 9/10 + 9/100 + ...
              = (9/10) / (1 - 1/10) = 1.
    """

    def construct(self):
        title = Tex(r"$0.999\ldots = 1$ — partial sums make it visible",
                    font_size=28).to_edge(UP, buff=0.4)
        self.play(Write(title))

        line = NumberLine(
            x_range=[0.9, 1.0, 0.01], length=8.0,
            include_numbers=True,
            decimal_number_config={"num_decimal_places": 2, "font_size": 18},
        ).move_to([-1.4, -0.6, 0])
        self.play(Create(line))

        N_max = 15

        N_tr = ValueTracker(0)

        def dots():
            n = int(round(N_tr.get_value()))
            grp = VGroup()
            for k in range(1, n + 1):
                S = 1 - 10 ** (-k)
                color = interpolate_color(BLUE, YELLOW, k / N_max)
                d = Dot(line.n2p(S), color=color, radius=0.10)
                grp.add(d)
            return grp

        self.add(always_redraw(dots))

        # Highlight the limit at 1
        one_marker = Line(line.n2p(1.0) + DOWN * 0.4,
                          line.n2p(1.0) + UP * 0.4,
                          color=GREEN, stroke_width=4)
        one_lbl = Tex(r"$1$", color=GREEN, font_size=28).next_to(
            one_marker, UP, buff=0.05)
        self.play(Create(one_marker), Write(one_lbl))

        # RIGHT COLUMN
        rcol_x = +4.4

        def info_panel():
            n = max(0, int(round(N_tr.get_value())))
            if n == 0:
                S = 0
                S_str = "—"
            else:
                S = 1 - 10 ** (-n)
                S_str = f"{S:.{n}f}"
            gap_str = f"10^(-{n})" if n > 0 else "1"
            return VGroup(
                MathTex(rf"n = {n}", color=WHITE, font_size=24),
                MathTex(rf"S_n = 1 - 10^{{-n}}", color=YELLOW, font_size=22),
                MathTex(rf"S_n = {S_str}", color=YELLOW, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([rcol_x, +1.6, 0])

        self.add(always_redraw(info_panel))

        derivation = VGroup(
            MathTex(r"0.999\ldots = \tfrac{9}{10} + \tfrac{9}{100} + \tfrac{9}{1000} + \cdots",
                    color=YELLOW, font_size=22),
            MathTex(r"= \tfrac{9/10}{1 - 1/10}", color=GREEN, font_size=24),
            MathTex(r"= \tfrac{9/10}{9/10} = 1", color=GREEN, font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([rcol_x, -1.4, 0])
        self.play(Write(derivation))

        # Step N up
        for n in range(1, N_max + 1):
            self.play(N_tr.animate.set_value(n),
                      run_time=0.4, rate_func=smooth)

        self.wait(0.8)
        conclusion = Tex(r"Limit of $S_n$ is exactly $1$",
                         color=YELLOW, font_size=24).to_edge(DOWN, buff=0.4)
        self.play(Write(conclusion))
        self.wait(0.6)
