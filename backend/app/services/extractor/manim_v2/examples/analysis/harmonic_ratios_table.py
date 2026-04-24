from manim import *
import numpy as np


class HarmonicRatiosTableExample(Scene):
    """
    Consonant musical intervals = small-integer frequency ratios.

    TWO_COLUMN:
      LEFT  — two stacked axes: top shows sin(2π·1·t), bottom shows
              sin(2π·r·t) for r = {1, 2, 3/2, 4/3, 5/4, 6/5, 7/6,
              π/2 (irrational comparison)}. Waves drawn via
              ValueTracker r_tr sweeping through the discrete ratios;
              always_redraw shows their product/sum below as combined
              pressure wave.
      RIGHT — live ratio, numerator/denominator, and consonance
              rank (octave, fifth, fourth, major-third, ...).
    """

    def construct(self):
        title = Tex(r"Simple ratios $p/q$: wave reconstructs cleanly $\Leftrightarrow$ small $p, q$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ax_top = Axes(x_range=[0, 4, 1], y_range=[-1.2, 1.2, 1],
                      x_length=7, y_length=1.6, tips=False,
                      axis_config={"font_size": 14}).move_to([-1.5, 1.8, 0])
        ax_bot = Axes(x_range=[0, 4, 1], y_range=[-1.2, 1.2, 1],
                      x_length=7, y_length=1.6, tips=False,
                      axis_config={"font_size": 14}).move_to([-1.5, 0.2, 0])
        ax_sum = Axes(x_range=[0, 4, 1], y_range=[-2.4, 2.4, 1],
                      x_length=7, y_length=1.7, tips=False,
                      axis_config={"font_size": 14}).move_to([-1.5, -1.7, 0])

        base_curve = ax_top.plot(lambda t: np.sin(2 * PI * t),
                                  x_range=[0, 4], color=BLUE)

        top_lbl = Tex(r"base $f$", color=BLUE, font_size=18
                       ).next_to(ax_top, LEFT, buff=0.15)
        bot_lbl = Tex(r"$r\,f$", color=ORANGE, font_size=20
                       ).next_to(ax_bot, LEFT, buff=0.15)
        sum_lbl = Tex(r"sum", color=GREEN, font_size=18
                       ).next_to(ax_sum, LEFT, buff=0.15)

        self.play(Create(ax_top), Create(ax_bot), Create(ax_sum),
                   Create(base_curve),
                   Write(top_lbl), Write(bot_lbl), Write(sum_lbl))

        r_tr = ValueTracker(1.0)

        def rf_curve():
            r = r_tr.get_value()
            return ax_bot.plot(lambda t: np.sin(2 * PI * r * t),
                                x_range=[0, 4], color=ORANGE)

        def sum_curve():
            r = r_tr.get_value()
            return ax_sum.plot(
                lambda t: np.sin(2 * PI * t) + np.sin(2 * PI * r * t),
                x_range=[0, 4], color=GREEN)

        self.add(always_redraw(rf_curve), always_redraw(sum_curve))

        ratios = [
            (1.0, r"1/1", "unison"),
            (2.0, r"2/1", "octave"),
            (1.5, r"3/2", "fifth"),
            (4 / 3, r"4/3", "fourth"),
            (5 / 4, r"5/4", "major 3rd"),
            (6 / 5, r"6/5", "minor 3rd"),
            (np.sqrt(2), r"\sqrt{2}", "tritone (irrational)"),
        ]

        def info():
            r = r_tr.get_value()
            closest = min(ratios, key=lambda x: abs(x[0] - r))
            return VGroup(
                MathTex(rf"r = {r:.4f}", color=WHITE, font_size=24),
                MathTex(rf"\approx {closest[1]}", color=YELLOW, font_size=24),
                Tex(closest[2], color=GREEN_B, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([5.2, -1.0, 0])

        self.add(always_redraw(info))

        for (r, _, _) in ratios:
            self.play(r_tr.animate.set_value(r),
                       run_time=1.2, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
