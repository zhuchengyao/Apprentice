from manim import *
import numpy as np


class UniformContinuityHeineExample(Scene):
    """
    Heine-Cantor: continuous function on compact set is uniformly
    continuous. Contrast f(x) = 1/x on (0, 1] (continuous but NOT
    uniformly continuous) vs f(x) = 1/x on [0.1, 1] (compact,
    uniformly continuous).

    SINGLE_FOCUS: f(x) = 1/x. ValueTracker x_tr places a slider;
    show δ-interval around x_tr and image δ image interval on y-axis
    shrinking as x → 0. Without compactness, no uniform δ works.
    """

    def construct(self):
        title = Tex(r"Heine-Cantor: continuous on compact $\Rightarrow$ uniformly continuous",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[0, 1.1, 0.2], y_range=[0, 11, 2],
                    x_length=8, y_length=4.5,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(DOWN * 0.3)
        self.play(Create(axes))

        f_curve = axes.plot(lambda x: 1 / x, x_range=[0.1, 1],
                             color=BLUE, stroke_width=3)
        self.play(Create(f_curve))

        x_tr = ValueTracker(0.5)
        eps = 1.5

        def x_now():
            return x_tr.get_value()

        def epsilon_band():
            x = x_now()
            y = 1 / x if x > 0.05 else 20
            return VGroup(
                DashedLine(axes.c2p(0, y - eps), axes.c2p(1.1, y - eps),
                           color=YELLOW, stroke_width=1.5),
                DashedLine(axes.c2p(0, y + eps), axes.c2p(1.1, y + eps),
                           color=YELLOW, stroke_width=1.5),
            )

        def delta_interval():
            x = x_now()
            # Compute δ needed for |1/t - 1/x| < ε on a neighborhood
            # |1/t - 1/x| = |x-t|/(xt), want <ε ⇒ |x-t|<εxt
            # For t close to x: δ ≈ εx² / (1 + εx) roughly
            delta = eps * x * x / (1 + eps * x) * 0.9
            a = max(0.02, x - delta)
            b = min(1.1, x + delta)
            return Rectangle(
                width=(b - a) * axes.x_length / 1.1,
                height=0.2,
                color=ORANGE, stroke_width=0,
                fill_color=ORANGE, fill_opacity=0.7,
            ).move_to(axes.c2p((a + b) / 2, 0))

        def current_dot():
            x = x_now()
            return Dot(axes.c2p(x, 1 / x), color=RED, radius=0.11)

        self.add(always_redraw(epsilon_band),
                 always_redraw(delta_interval),
                 always_redraw(current_dot))

        def delta_val():
            x = x_now()
            return float(eps * x * x / (1 + eps * x))

        info = VGroup(
            VGroup(Tex(r"$x=$", font_size=22),
                   DecimalNumber(0.5, num_decimal_places=3,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
            Tex(rf"fixed $\varepsilon={eps}$", color=YELLOW, font_size=22),
            VGroup(Tex(r"required $\delta(x)=$", color=ORANGE, font_size=22),
                   DecimalNumber(0.1, num_decimal_places=4,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            Tex(r"$\delta \to 0$ as $x\to 0^+$",
                color=RED, font_size=20),
            Tex(r"$\Rightarrow$ NOT uniformly continuous on $(0,1]$",
                color=RED, font_size=20),
            Tex(r"on $[0.1, 1]$: $\delta_{\min}\approx 0.012>0$ works $\forall x$",
                color=GREEN, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(x_now()))
        info[2][1].add_updater(lambda m: m.set_value(delta_val()))
        self.add(info)

        for xval in [0.3, 0.15, 0.08, 0.05, 0.6]:
            self.play(x_tr.animate.set_value(xval),
                      run_time=1.8, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.5)
