from manim import *
import numpy as np


class GaussianConcentrationExample(Scene):
    """
    Gaussian concentration inequality: for X ~ N(0, 1),
    P(|X| > t) ≤ 2 exp(-t²/2). Empirically the tail is tight.

    TWO_COLUMN:
      LEFT  — standard normal pdf + shaded tail ±t; ValueTracker
              t_tr sweeps t.
      RIGHT — running empirical tail vs theoretical bound.
    """

    def construct(self):
        title = Tex(r"Gaussian concentration: $P(|X| > t) \le 2 e^{-t^2/2}$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ax_L = Axes(x_range=[-4, 4, 1], y_range=[0, 0.5, 0.1],
                     x_length=6, y_length=3.5, tips=False,
                     axis_config={"font_size": 14, "include_numbers": True}
                     ).move_to([-3, 0, 0])
        self.play(Create(ax_L))

        pdf_curve = ax_L.plot(lambda x: np.exp(-x ** 2 / 2) / np.sqrt(2 * PI),
                                x_range=[-4, 4, 0.02],
                                color=BLUE, stroke_width=3)
        self.play(Create(pdf_curve))

        t_tr = ValueTracker(0.5)

        def tail_shades():
            t = t_tr.get_value()
            # Left tail [-4, -t]
            pts_L = [ax_L.c2p(-4, 0)]
            for x in np.linspace(-4, -t, 40):
                pts_L.append(ax_L.c2p(x, np.exp(-x ** 2 / 2) / np.sqrt(2 * PI)))
            pts_L.append(ax_L.c2p(-t, 0))
            left_poly = Polygon(*pts_L, color=RED, fill_opacity=0.5,
                                  stroke_width=0)
            # Right tail [t, 4]
            pts_R = [ax_L.c2p(t, 0)]
            for x in np.linspace(t, 4, 40):
                pts_R.append(ax_L.c2p(x, np.exp(-x ** 2 / 2) / np.sqrt(2 * PI)))
            pts_R.append(ax_L.c2p(4, 0))
            right_poly = Polygon(*pts_R, color=RED, fill_opacity=0.5,
                                   stroke_width=0)
            return VGroup(left_poly, right_poly)

        def t_lines():
            t = t_tr.get_value()
            return VGroup(
                DashedLine(ax_L.c2p(-t, 0), ax_L.c2p(-t, 0.5),
                             color=RED, stroke_width=2),
                DashedLine(ax_L.c2p(t, 0), ax_L.c2p(t, 0.5),
                             color=RED, stroke_width=2),
            )

        self.add(always_redraw(tail_shades), always_redraw(t_lines))

        # RIGHT: tail vs bound
        ax_R = Axes(x_range=[0, 4, 1], y_range=[-8, 1, 2],
                     x_length=5, y_length=3.5, tips=False,
                     axis_config={"font_size": 12, "include_numbers": True}
                     ).move_to([3.5, 0, 0])
        xl = MathTex(r"t", font_size=16).next_to(ax_R, DOWN, buff=0.08)
        yl = MathTex(r"\log_{10} P", font_size=16).next_to(ax_R, LEFT, buff=0.08)
        self.play(Create(ax_R), Write(xl), Write(yl))

        # True tail curve
        from scipy.stats import norm
        true_curve = ax_R.plot(
            lambda t: np.log10(2 * (1 - norm.cdf(t))) if 2 * (1 - norm.cdf(t)) > 1e-8 else -8,
            x_range=[0.1, 4, 0.02],
            color=BLUE, stroke_width=3)
        bound_curve = ax_R.plot(
            lambda t: np.log10(2 * np.exp(-t ** 2 / 2)),
            x_range=[0.1, 4, 0.02],
            color=GREEN, stroke_width=3)
        true_lbl = Tex(r"true tail", color=BLUE, font_size=16
                        ).next_to(ax_R.c2p(2.5, np.log10(2 * (1 - norm.cdf(2.5)))),
                                    UP, buff=0.15)
        bound_lbl = Tex(r"bound $2 e^{-t^2/2}$",
                         color=GREEN, font_size=16
                         ).next_to(ax_R.c2p(3.5, np.log10(2 * np.exp(-3.5 ** 2 / 2))),
                                     UP, buff=0.15)
        self.play(Create(true_curve), Create(bound_curve),
                   Write(true_lbl), Write(bound_lbl))

        def rider_true():
            t = t_tr.get_value()
            v = 2 * (1 - norm.cdf(t))
            ly = np.log10(max(v, 1e-8))
            return Dot(ax_R.c2p(t, ly), color=BLUE, radius=0.09)

        def rider_bound():
            t = t_tr.get_value()
            v = 2 * np.exp(-t ** 2 / 2)
            ly = np.log10(v)
            return Dot(ax_R.c2p(t, ly), color=GREEN, radius=0.09)

        self.add(always_redraw(rider_true), always_redraw(rider_bound))

        def info():
            t = t_tr.get_value()
            true_v = 2 * (1 - norm.cdf(t))
            bound_v = 2 * np.exp(-t ** 2 / 2)
            return VGroup(
                MathTex(rf"t = {t:.2f}", color=RED, font_size=22),
                MathTex(rf"P(|X|>t) = {true_v:.2e}",
                         color=BLUE, font_size=18),
                MathTex(rf"2e^{{-t^2/2}} = {bound_v:.2e}",
                         color=GREEN, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        for tv in [1.0, 2.0, 3.0, 0.5]:
            self.play(t_tr.animate.set_value(tv),
                       run_time=1.3, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
