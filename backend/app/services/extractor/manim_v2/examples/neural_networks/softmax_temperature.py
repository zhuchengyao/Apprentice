from manim import *
import numpy as np


class SoftmaxTemperatureExample(Scene):
    """
    Softmax with temperature: softmax_T(x_i) = exp(x_i/T) / Σ_j exp(x_j/T).
    T → 0: argmax becomes 1-hot. T → ∞: distribution becomes uniform.

    TWO_COLUMN: LEFT bars showing softmax output for 8 logits
    [2.1, -1.3, 0.5, 3.0, 1.2, -0.4, 2.4, -2.5]; ValueTracker T_tr
    sweeps T ∈ {2.0, 0.5, 0.15, 0.05, 1.0, 5.0, 20.0}; always_redraw
    recomputes bar heights. RIGHT shows entropy and current T.
    """

    def construct(self):
        title = Tex(r"Softmax temperature: $p_i(T)=e^{x_i/T}/\sum_j e^{x_j/T}$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        logits = np.array([2.1, -1.3, 0.5, 3.0, 1.2, -0.4, 2.4, -2.5])
        n = len(logits)

        axes = Axes(x_range=[0, n + 0.5, 1], y_range=[0, 1.0, 0.2],
                    x_length=6.0, y_length=3.8,
                    axis_config={"include_numbers": False,
                                 "font_size": 16}).shift(LEFT * 2.3 + DOWN * 0.2)
        self.play(Create(axes))

        T_tr = ValueTracker(2.0)

        def softmax(x, T):
            z = x / T
            z = z - z.max()  # numeric stability
            e = np.exp(z)
            return e / e.sum()

        colors = [BLUE, GREEN, ORANGE, RED, YELLOW, PURPLE, TEAL, PINK]

        def bars():
            p = softmax(logits, T_tr.get_value())
            grp = VGroup()
            for i in range(n):
                rect = Rectangle(width=0.4,
                                  height=p[i] * axes.y_length / 1.0,
                                  color=colors[i],
                                  fill_color=colors[i],
                                  fill_opacity=0.7)
                rect.move_to(axes.c2p(i + 1, p[i] / 2))
                grp.add(rect)
            return grp

        self.add(always_redraw(bars))

        # Labels (logits under bars)
        for i, v in enumerate(logits):
            self.add(Tex(f"${v:+.1f}$", font_size=16,
                         color=colors[i]).move_to(axes.c2p(i + 1, -0.08)))

        def entropy():
            p = softmax(logits, T_tr.get_value())
            p = np.where(p > 1e-12, p, 1e-12)
            return float(-np.sum(p * np.log(p)))

        info = VGroup(
            VGroup(Tex(r"$T=$", font_size=26),
                   DecimalNumber(2.0, num_decimal_places=3,
                                 font_size=26).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$H(p)=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\log n = \log 8=$", font_size=22),
                   DecimalNumber(float(np.log(n)), num_decimal_places=3,
                                 font_size=22).set_color(GREY_B)).arrange(RIGHT, buff=0.1),
            Tex(r"$T\to 0$: argmax, $T\to\infty$: uniform",
                color=YELLOW, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.2)
        info[0][1].add_updater(lambda m: m.set_value(T_tr.get_value()))
        info[1][1].add_updater(lambda m: m.set_value(entropy()))
        self.add(info)

        for T_val in [0.5, 0.15, 0.05, 1.0, 5.0, 20.0, 1.0]:
            self.play(T_tr.animate.set_value(T_val),
                      run_time=1.7, rate_func=smooth)
            self.wait(0.3)
        self.wait(0.5)
