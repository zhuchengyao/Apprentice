from manim import *
import numpy as np


class CauchySequenceCompletenessExample(Scene):
    """
    Cauchy sequence → convergent in complete space. ℝ is complete;
    ℚ is not. Visualize x_n = (1 + 1/n)^n Cauchy in ℚ converging to
    e ∉ ℚ, so ℚ is incomplete.

    TWO_COLUMN: LEFT number line with x_n dots accumulating at e;
    shrinking ε-balls around each x_n illustrate Cauchy condition.
    RIGHT panel shows live n, |x_n − x_m| for m=n+1 (shrinking),
    and |x_n − e| → 0.
    """

    def construct(self):
        title = Tex(r"Cauchy: $|x_n-x_m|\to 0 \Rightarrow$ convergent in $\mathbb{R}$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[2.0, 3.0, 0.2], y_range=[0, 1, 0.5],
                    x_length=8, y_length=1.5,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(DOWN * 1.2)
        self.play(Create(axes))

        # e reference
        e_line = DashedLine(axes.c2p(np.e, 0), axes.c2p(np.e, 1),
                            color=RED, stroke_width=2)
        e_lbl = Tex(r"$e\approx 2.71828$", color=RED, font_size=22).next_to(
            axes.c2p(np.e, 1.1), UP, buff=0.1)
        self.play(Create(e_line), Write(e_lbl))

        n_tr = ValueTracker(1.0)

        def x_n(n):
            return (1 + 1 / n) ** n

        def dots():
            n = int(round(n_tr.get_value()))
            n = max(1, min(200, n))
            grp = VGroup()
            for k in range(1, n + 1):
                grp.add(Dot(axes.c2p(x_n(k), 0.3),
                             color=YELLOW, radius=0.04,
                             fill_opacity=min(1.0, 0.3 + 0.02 * (n - k))))
            # current dot emphasized
            grp.add(Dot(axes.c2p(x_n(n), 0.3),
                         color=ORANGE, radius=0.1))
            return grp

        def eps_ball():
            n = int(round(n_tr.get_value()))
            n = max(1, min(200, n))
            eps = abs(x_n(n + 1) - x_n(n)) + 0.005
            return VGroup(
                Line(axes.c2p(x_n(n) - eps, 0.3),
                      axes.c2p(x_n(n) + eps, 0.3),
                      color=GREEN, stroke_width=6),
                Dot(axes.c2p(x_n(n), 0.3), color=ORANGE, radius=0.1),
            )

        self.add(always_redraw(dots), always_redraw(eps_ball))

        info = VGroup(
            VGroup(Tex(r"$n=$", font_size=22),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$x_n=(1+1/n)^n=$", font_size=22),
                   DecimalNumber(2.0, num_decimal_places=6,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$|x_{n+1}-x_n|=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=6,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$|x_n-e|=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=6,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
            Tex(r"$\{x_n\}\subset \mathbb{Q}$ but $e\notin \mathbb{Q}$",
                color=RED, font_size=20),
            Tex(r"$\mathbb{Q}$ incomplete, $\mathbb{R}$ complete",
                color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(UP, buff=1.6).shift(LEFT * 4)

        def n_now():
            return max(1, min(200, int(round(n_tr.get_value()))))

        info[0][1].add_updater(lambda m: m.set_value(n_now()))
        info[1][1].add_updater(lambda m: m.set_value(x_n(n_now())))
        info[2][1].add_updater(lambda m: m.set_value(abs(x_n(n_now() + 1) - x_n(n_now()))))
        info[3][1].add_updater(lambda m: m.set_value(abs(x_n(n_now()) - np.e)))
        self.add(info)

        self.play(n_tr.animate.set_value(200.0),
                  run_time=8, rate_func=linear)
        self.wait(0.8)
