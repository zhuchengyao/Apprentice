from manim import *
import numpy as np


class ImportanceSamplingExample(Scene):
    """
    Importance sampling: estimate E_p[f(X)] using samples from
    proposal q, with weights w_i = p(x_i)/q(x_i).

    Target p = Normal(0, 1). Proposal q = Normal(1.5, 1). Function
    f(x) = x² (true E_p[f] = 1).

    TWO_COLUMN: LEFT axes show BLUE p density and ORANGE q density;
    400 pre-drawn samples from q shown as dots at varying heights
    colored by weight w_i (YELLOW high → RED low).
    ValueTracker n_tr reveals samples one-by-one; always_redraw
    updates running weighted-average estimator converging to 1.
    """

    def construct(self):
        title = Tex(r"Importance sampling: $E_p[X^2]\approx \frac{1}{N}\sum \frac{p(x_i)}{q(x_i)} x_i^2$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        np.random.seed(0)
        xs = 1.5 + np.random.randn(400)  # samples from q
        p_den = np.exp(-xs ** 2 / 2) / np.sqrt(TAU)
        q_den = np.exp(-(xs - 1.5) ** 2 / 2) / np.sqrt(TAU)
        weights = p_den / q_den

        axes = Axes(x_range=[-4, 5, 1], y_range=[0, 0.45, 0.1],
                    x_length=5.8, y_length=3.8,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(LEFT * 2.5 + DOWN * 0.2)
        self.play(Create(axes))

        p_curve = axes.plot(lambda x: np.exp(-x ** 2 / 2) / np.sqrt(TAU),
                            x_range=[-4, 5], color=BLUE, stroke_width=3)
        q_curve = axes.plot(lambda x: np.exp(-(x - 1.5) ** 2 / 2) / np.sqrt(TAU),
                            x_range=[-4, 5], color=ORANGE, stroke_width=3)
        p_lbl = Tex(r"$p=\mathcal{N}(0,1)$", color=BLUE,
                    font_size=22).next_to(axes, UP, buff=0.1).shift(LEFT * 1.5)
        q_lbl = Tex(r"$q=\mathcal{N}(1.5,1)$", color=ORANGE,
                    font_size=22).next_to(axes, UP, buff=0.1).shift(RIGHT * 1.5)
        self.play(Create(p_curve), Create(q_curve), Write(p_lbl), Write(q_lbl))

        n_tr = ValueTracker(0.0)

        def sample_dots():
            n = int(round(n_tr.get_value()))
            n = max(0, min(400, n))
            grp = VGroup()
            for i in range(n):
                x = xs[i]
                w = weights[i]
                # color from RED (w→0) to YELLOW (w large)
                col = interpolate_color(RED, YELLOW, np.clip(w, 0, 1))
                y = q_den[i]
                grp.add(Dot(axes.c2p(x, y),
                             color=col, radius=0.035))
            return grp

        self.add(always_redraw(sample_dots))

        # Right column
        def estimator():
            n = max(1, min(400, int(round(n_tr.get_value()))))
            return float(np.mean(weights[:n] * xs[:n] ** 2))

        info = VGroup(
            Tex(r"$f(x)=x^2$, true $E_p[X^2]=1$",
                color=BLUE, font_size=22),
            VGroup(Tex(r"$N=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"estimator $=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=4,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"error $=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=4,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"YELLOW dots: $p>q$ (upweight)", color=YELLOW, font_size=20),
            Tex(r"RED dots: $p<q$ (downweight)", color=RED, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.2)

        info[1][1].add_updater(lambda m: m.set_value(int(round(n_tr.get_value()))))
        info[2][1].add_updater(lambda m: m.set_value(estimator()))
        info[3][1].add_updater(lambda m: m.set_value(abs(estimator() - 1.0)))
        self.add(info)

        self.play(n_tr.animate.set_value(400.0),
                  run_time=7, rate_func=linear)
        self.wait(0.8)
