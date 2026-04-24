from manim import *
import numpy as np


class SeriesOfFunctionsUniformExample(Scene):
    """
    Weierstrass M-test: Σ f_n converges uniformly if ∃ M_n with
    |f_n(x)| ≤ M_n ∀x, Σ M_n < ∞.

    f_n(x) = sin(nx)/n² on [0, π]. M_n = 1/n². Σ 1/n² = π²/6.
    Partial sums S_N converge uniformly to continuous limit.

    TWO_COLUMN: LEFT axes show partial sum S_N(x) via always_redraw
    curve. ValueTracker N_tr sweeps 1→60. RIGHT shows sup-norm
    gap + ΣM_n bound.
    """

    def construct(self):
        title = Tex(r"Weierstrass $M$-test: $|f_n|\le M_n$, $\sum M_n<\infty\Rightarrow$ uniform",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[0, PI, PI / 4], y_range=[-0.5, 2.0, 0.5],
                    x_length=6.5, y_length=4.0,
                    axis_config={"include_numbers": False}).shift(LEFT * 2.2 + DOWN * 0.2)
        self.play(Create(axes))

        def S_N(x, N):
            return sum(np.sin(n * x) / (n * n) for n in range(1, N + 1))

        N_tr = ValueTracker(1.0)

        def partial_curve():
            N = int(round(N_tr.get_value()))
            N = max(1, min(60, N))
            return axes.plot(lambda xx: float(S_N(xx, N)),
                             x_range=[0, PI], color=YELLOW, stroke_width=3)

        self.add(always_redraw(partial_curve))

        # Limit via large N
        limit_curve = axes.plot(lambda xx: float(S_N(xx, 100)),
                                 x_range=[0, PI], color=GREY_B,
                                 stroke_width=2, stroke_opacity=0.5)
        self.add(limit_curve)

        # Right panel
        def n_now():
            return max(1, min(60, int(round(N_tr.get_value()))))

        def sup_gap():
            N = n_now()
            xs = np.linspace(0, PI, 60)
            return float(max(abs(S_N(x, N) - S_N(x, 100)) for x in xs))

        def M_tail():
            N = n_now()
            return float(sum(1 / (n * n) for n in range(N + 1, 101)))

        info = VGroup(
            VGroup(Tex(r"$N=$", font_size=22),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"sup $|S_N-S_\infty|=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=5,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\sum_{n>N} 1/n^2=$", color=BLUE, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=5,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            Tex(r"sup-gap $\le \sum_{n>N} M_n$ (M-test)",
                color=GREEN, font_size=20),
            Tex(r"$\sum 1/n^2=\pi^2/6\approx 1.6449$",
                color=BLUE, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.2)
        info[0][1].add_updater(lambda m: m.set_value(n_now()))
        info[1][1].add_updater(lambda m: m.set_value(sup_gap()))
        info[2][1].add_updater(lambda m: m.set_value(M_tail()))
        self.add(info)

        for target in [3, 8, 20, 40, 60]:
            self.play(N_tr.animate.set_value(float(target)),
                      run_time=1.5, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.5)
