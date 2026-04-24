from manim import *
import numpy as np


class HoeffdingInequalityExample(Scene):
    """
    Hoeffding's inequality: for X_1, ..., X_n iid in [0, 1] with mean μ,
      P(|X̄_n − μ| ≥ t) ≤ 2 exp(−2 n t²).

    TWO_COLUMN: LEFT axes show n grows from 5 to 2000; plot
    empirical tail via 1000 Monte Carlo simulations each, YELLOW.
    Overlay Hoeffding bound 2 exp(-2nt²) in RED (dashed). t=0.1 fixed.
    RIGHT shows live n, empirical tail prob, and bound.
    """

    def construct(self):
        title = Tex(r"Hoeffding: $P(|\bar X_n-\mu|\ge t)\le 2e^{-2nt^2}$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[0, 2000, 400], y_range=[0, 1.05, 0.2],
                    x_length=6.0, y_length=4.0,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(LEFT * 2.3 + DOWN * 0.2)
        self.play(Create(axes))

        np.random.seed(3)
        t = 0.1
        n_values = [5, 10, 20, 50, 100, 200, 500, 1000, 1500, 2000]
        # For each n, simulate 1000 runs, measure |X̄-μ|>=t proportion.
        empirical = []
        bound = []
        for n in n_values:
            samples = np.random.random((1000, n))
            means = samples.mean(axis=1)
            p_emp = np.mean(np.abs(means - 0.5) >= t)
            empirical.append(p_emp)
            bound.append(min(2 * np.exp(-2 * n * t * t), 1.0))

        # Pre-draw bound curve
        bound_curve = axes.plot(lambda n: min(2 * np.exp(-2 * n * t * t), 1.0),
                                 x_range=[5, 2000], color=RED, stroke_width=3)
        self.play(Create(bound_curve))
        bound_lbl = Tex(r"$2e^{-2nt^2}$ bound", color=RED,
                        font_size=22).next_to(axes, UP, buff=0.1)
        self.play(Write(bound_lbl))

        idx_tr = ValueTracker(0.0)

        def emp_dots():
            k = int(round(idx_tr.get_value()))
            k = max(0, min(len(n_values) - 1, k))
            grp = VGroup()
            for i in range(k + 1):
                grp.add(Dot(axes.c2p(n_values[i], empirical[i]),
                             color=YELLOW, radius=0.07))
            return grp

        def emp_line():
            k = int(round(idx_tr.get_value()))
            k = max(0, min(len(n_values) - 1, k))
            if k < 1:
                return VMobject()
            pts = [axes.c2p(n_values[i], empirical[i]) for i in range(k + 1)]
            return VMobject().set_points_as_corners(pts).set_color(YELLOW).set_stroke(width=3)

        self.add(always_redraw(emp_dots), always_redraw(emp_line))

        def idx_now():
            return max(0, min(len(n_values) - 1, int(round(idx_tr.get_value()))))

        info = VGroup(
            Tex(rf"$t={t}$, $\mu=0.5$", font_size=22),
            VGroup(Tex(r"$n=$", font_size=22),
                   DecimalNumber(5, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"empirical tail $=$", color=YELLOW, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=4,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"Hoeffding bound $=$", color=RED, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=4,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
            Tex(r"tail decays exponentially",
                color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.2)

        info[1][1].add_updater(lambda m: m.set_value(n_values[idx_now()]))
        info[2][1].add_updater(lambda m: m.set_value(empirical[idx_now()]))
        info[3][1].add_updater(lambda m: m.set_value(bound[idx_now()]))
        self.add(info)

        self.play(idx_tr.animate.set_value(float(len(n_values) - 1)),
                  run_time=7, rate_func=linear)
        self.wait(0.8)
