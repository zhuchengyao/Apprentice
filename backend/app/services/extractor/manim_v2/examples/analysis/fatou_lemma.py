from manim import *
import numpy as np


class FatouLemmaExample(Scene):
    """
    Fatou's lemma: ∫ liminf f_n ≤ liminf ∫ f_n for non-negative
    measurable f_n. Strict inequality possible: f_n(x) = n·𝟙_{[0, 1/n]}
    has ∫f_n = 1 for all n, but liminf f_n = 0 (a.e.), so
    ∫ liminf = 0 < 1 = liminf ∫.

    TWO_COLUMN:
      LEFT  — f_n(x) = n·𝟙_{[0, 1/n]} on [0, 1]; ValueTracker n_tr
              grows. Curves get taller and narrower but integral = 1.
      RIGHT — liminf f_n(x) = 0 almost everywhere (just 0 axis).
    """

    def construct(self):
        title = Tex(r"Fatou: $\int \liminf f_n \le \liminf \int f_n$ (strict here)",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ax_L = Axes(x_range=[0, 1, 0.25], y_range=[0, 20, 5],
                     x_length=6, y_length=4, tips=False,
                     axis_config={"font_size": 14, "include_numbers": True}
                     ).move_to([-3.5, -0.3, 0])
        self.play(Create(ax_L))

        L_lbl = MathTex(r"f_n = n\cdot \mathbf{1}_{[0, 1/n]}",
                          color=BLUE, font_size=22
                          ).next_to(ax_L, UP, buff=0.1)
        self.play(Write(L_lbl))

        n_tr = ValueTracker(1)

        def f_n_curve():
            n = int(round(n_tr.get_value()))
            n = max(1, min(n, 20))
            # Height n from x=0 to 1/n, then 0 beyond
            return ax_L.plot(lambda x: n if x < 1 / n else 0,
                              x_range=[0, 1, 0.002],
                              color=BLUE, stroke_width=3)

        def f_n_shade():
            n = int(round(n_tr.get_value()))
            n = max(1, min(n, 20))
            # Rectangle area (= always 1)
            return Rectangle(
                width=ax_L.c2p(1 / n, 0)[0] - ax_L.c2p(0, 0)[0],
                height=ax_L.c2p(0, n)[1] - ax_L.c2p(0, 0)[1],
                color=BLUE, fill_opacity=0.3, stroke_width=0
            ).move_to([(ax_L.c2p(0, 0)[0] + ax_L.c2p(1 / n, 0)[0]) / 2,
                         (ax_L.c2p(0, 0)[1] + ax_L.c2p(0, n)[1]) / 2, 0])

        self.add(always_redraw(f_n_shade), always_redraw(f_n_curve))

        # RIGHT: liminf f_n = 0 everywhere (in the limit)
        ax_R = Axes(x_range=[0, 1, 0.25], y_range=[0, 20, 5],
                     x_length=6, y_length=4, tips=False,
                     axis_config={"font_size": 14, "include_numbers": True}
                     ).move_to([3.3, -0.3, 0])
        self.play(Create(ax_R))

        R_lbl = MathTex(r"\liminf f_n = 0 \text{ a.e.}",
                          color=RED, font_size=22
                          ).next_to(ax_R, UP, buff=0.1)
        self.play(Write(R_lbl))

        zero_line = Line(ax_R.c2p(0, 0), ax_R.c2p(1, 0),
                           color=RED, stroke_width=4)
        self.play(Create(zero_line))

        def info():
            n = int(round(n_tr.get_value()))
            n = max(1, min(n, 20))
            return VGroup(
                MathTex(rf"n = {n}", color=BLUE, font_size=22),
                MathTex(r"\int f_n = 1 \text{ for all } n",
                         color=BLUE, font_size=20),
                MathTex(r"\int \liminf f_n = 0",
                         color=RED, font_size=22),
                MathTex(r"0 \le 1 \text{ (strict!)}",
                         color=YELLOW, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        for nv in [2, 5, 10, 20, 1]:
            self.play(n_tr.animate.set_value(nv),
                       run_time=1.4, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
