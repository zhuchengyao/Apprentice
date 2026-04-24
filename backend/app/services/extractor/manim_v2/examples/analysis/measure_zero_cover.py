from manim import *
import numpy as np


class MeasureZeroCoverExample(Scene):
    """
    The rationals can be covered by intervals of arbitrarily small total
    length. Animate ε shrinking and the cover intervals tightening.

    TWO_COLUMN:
      LEFT  — number line [0, 1] with 8 rationals shown as yellow dots,
              each surrounded by a blue rectangle of width
              ε / 2^k (k = enumeration index). ValueTracker eps sweeps
              from 1.0 down to 0.05; each interval shrinks proportionally.
      RIGHT — live ε, total cover length (= ε), and the conclusion
              that ℚ ∩ [0,1] has Lebesgue measure 0.
    """

    def construct(self):
        title = Tex(r"$\mathbb{Q} \cap [0, 1]$ has Lebesgue measure $0$",
                    font_size=28).to_edge(UP, buff=0.4)
        self.play(Write(title))

        line = NumberLine(
            x_range=[0, 1, 0.25], length=8.0,
            include_numbers=True,
            decimal_number_config={"num_decimal_places": 2, "font_size": 18},
        ).move_to([-1.4, -0.8, 0])
        self.play(Create(line))

        # 8 rationals
        rationals = [(1 / 2, 1), (1 / 3, 2), (2 / 3, 3), (1 / 4, 4),
                     (3 / 4, 5), (2 / 5, 6), (3 / 5, 7), (1 / 6, 8)]

        eps_tr = ValueTracker(1.0)

        rat_dots = VGroup(*[
            Dot(line.n2p(x), color=YELLOW, radius=0.08) for x, _ in rationals
        ])
        self.play(FadeIn(rat_dots))

        def covers():
            eps = eps_tr.get_value()
            grp = VGroup()
            for (x, k) in rationals:
                w_fraction = eps / (2 ** k)
                # Width on the number line in screen units
                left_world = max(0, x - w_fraction / 2)
                right_world = min(1, x + w_fraction / 2)
                left = line.n2p(left_world)
                right = line.n2p(right_world)
                w = abs(right[0] - left[0])
                rect = Rectangle(width=w, height=0.4, color=BLUE,
                                 fill_opacity=0.45, stroke_width=1)
                rect.move_to([(left[0] + right[0]) / 2, line.get_center()[1], 0])
                grp.add(rect)
            return grp

        self.add(always_redraw(covers))

        # RIGHT COLUMN
        rcol_x = +4.4

        def info_panel():
            eps = eps_tr.get_value()
            return VGroup(
                MathTex(rf"\varepsilon = {eps:.3f}", color=YELLOW, font_size=28),
                MathTex(r"\sum_k \tfrac{\varepsilon}{2^k} = \varepsilon",
                        color=BLUE, font_size=24),
                MathTex(rf"\text{{total cover}} = {eps:.3f}",
                        color=BLUE, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([rcol_x, +0.6, 0])

        self.add(always_redraw(info_panel))

        principle = Tex(r"$\forall \varepsilon > 0$ — measure zero",
                        color=GREEN, font_size=24).move_to([rcol_x, -1.6, 0])
        self.play(Write(principle))

        # Sweep ε down
        for tgt in [0.5, 0.2, 0.05, 0.5]:
            self.play(eps_tr.animate.set_value(tgt),
                      run_time=2.0, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.5)
