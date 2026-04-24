from manim import *
import numpy as np


class RossCentralLimitExample(Scene):
    """
    CLT convergence rate: for X_i i.i.d. Uniform(0, 1), the
    standardized sum S_n = (Σ X_i − n/2)·√(12/n) converges in
    distribution to 𝒩(0, 1). Berry-Esseen: the sup-distance to
    the standard normal CDF is O(1/√n).

    TWO_COLUMN: LEFT histogram of S_n with n driven by ValueTracker
    n_tr through {1, 2, 3, 5, 10, 30}; always_redraw re-samples and
    bins 5000 realizations. RIGHT shows standard normal reference
    and live Kolmogorov-Smirnov distance.
    """

    def construct(self):
        title = Tex(r"CLT: $(S_n-n/2)\sqrt{12/n}\to \mathcal{N}(0,1)$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[-4, 4, 1], y_range=[0, 0.5, 0.1],
                    x_length=6.0, y_length=4.0,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(LEFT * 2.5 + DOWN * 0.2)
        self.play(Create(axes))

        # Standard normal reference curve
        ref = axes.plot(lambda x: np.exp(-x * x / 2) / np.sqrt(TAU),
                        x_range=[-4, 4], color=BLUE, stroke_width=3)
        ref_lbl = Tex(r"$\mathcal{N}(0,1)$", color=BLUE,
                      font_size=22).next_to(axes, UR, buff=0.1)
        self.play(Create(ref), Write(ref_lbl))

        np.random.seed(7)
        # Precompute normalized sums for each n
        n_values = [1, 2, 3, 5, 10, 30]
        N_sample = 5000
        precomputed = {}
        for n in n_values:
            uni = np.random.random((N_sample, n))
            s = uni.sum(axis=1)
            z = (s - n / 2) * np.sqrt(12 / n)
            precomputed[n] = z

        n_tr = ValueTracker(0.0)  # index into n_values

        def hist_bars():
            idx = max(0, min(len(n_values) - 1, int(round(n_tr.get_value()))))
            n = n_values[idx]
            z = precomputed[n]
            bin_edges = np.linspace(-4, 4, 33)
            hist, _ = np.histogram(z, bins=bin_edges)
            hist = hist / (N_sample * (bin_edges[1] - bin_edges[0]))
            grp = VGroup()
            for i in range(len(hist)):
                x_c = (bin_edges[i] + bin_edges[i + 1]) / 2
                h = hist[i]
                rect = Rectangle(width=0.22, height=h * axes.y_length / 0.5,
                                 color=YELLOW, stroke_width=1,
                                 fill_color=YELLOW, fill_opacity=0.5)
                rect.move_to(axes.c2p(x_c, h / 2))
                grp.add(rect)
            return grp

        self.add(always_redraw(hist_bars))

        # KS distance via empirical CDF
        def ks_distance():
            idx = max(0, min(len(n_values) - 1, int(round(n_tr.get_value()))))
            n = n_values[idx]
            z = np.sort(precomputed[n])
            from scipy.stats import norm as sp_norm
            emp = np.arange(1, N_sample + 1) / N_sample
            return float(np.max(np.abs(emp - sp_norm.cdf(z))))

        def n_now():
            idx = max(0, min(len(n_values) - 1, int(round(n_tr.get_value()))))
            return n_values[idx]

        info = VGroup(
            VGroup(Tex(r"$n=$", font_size=22),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$5000$ samples each", font_size=20),
                   ).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"KS distance $=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=4,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$1/\sqrt{n}=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=4,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            Tex(r"Berry-Esseen: KS $\le C/\sqrt{n}$",
                color=ORANGE, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.2)

        info[0][1].add_updater(lambda m: m.set_value(n_now()))
        info[2][1].add_updater(lambda m: m.set_value(ks_distance()))
        info[3][1].add_updater(lambda m: m.set_value(1 / np.sqrt(n_now())))
        self.add(info)

        for target in range(1, len(n_values)):
            self.play(n_tr.animate.set_value(float(target)),
                      run_time=1.5, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.8)
