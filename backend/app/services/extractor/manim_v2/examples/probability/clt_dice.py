from manim import *
import numpy as np


class CLTDiceExample(Scene):
    """
    Central Limit Theorem with dice: standardized sum of n d6
    approaches N(0, 1) as n grows.

    TWO_COLUMN:
      LEFT  — histogram of standardized sum (Σ_i X_i - nμ)/√(nσ²)
              for N = 2000 trials; ValueTracker n_tr steps dice
              per trial 1 → 30.
      RIGHT — live n, dice-per-trial, N(0,1) overlay.
    """

    def construct(self):
        title = Tex(r"CLT on dice: standardized sum $\to \mathcal N(0, 1)$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Precompute trials for each n
        rng = np.random.default_rng(19)
        N_trials = 2000
        n_values = [1, 2, 4, 8, 16, 30]
        # Single die: μ = 3.5, σ² = 35/12
        mu = 3.5
        var = 35 / 12

        # For each n, compute standardized sums
        stand_sums = {}
        for n in n_values:
            rolls = rng.integers(1, 7, size=(N_trials, n))
            sums = rolls.sum(axis=1)
            z = (sums - n * mu) / np.sqrt(n * var)
            stand_sums[n] = z

        ax = Axes(x_range=[-4, 4, 1], y_range=[0, 0.5, 0.1],
                   x_length=7, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-2.5, -0.3, 0])
        xl = Tex("standardized sum", font_size=18).next_to(ax, DOWN, buff=0.1)
        yl = Tex("density", font_size=18).next_to(ax, LEFT, buff=0.1)
        self.play(Create(ax), Write(xl), Write(yl))

        # N(0, 1) overlay
        normal_curve = ax.plot(
            lambda x: np.exp(-x ** 2 / 2) / np.sqrt(2 * PI),
            x_range=[-4, 4, 0.02], color=YELLOW, stroke_width=3)
        normal_lbl = MathTex(r"\mathcal N(0, 1)", color=YELLOW, font_size=20
                               ).next_to(ax.c2p(1.5, 0.35), UR, buff=0.1)
        self.play(Create(normal_curve), Write(normal_lbl))

        n_idx_tr = ValueTracker(0)

        def histogram():
            i = int(round(n_idx_tr.get_value())) % len(n_values)
            n = n_values[i]
            z = stand_sums[n]
            bins = np.linspace(-4, 4, 41)
            counts, _ = np.histogram(z, bins=bins)
            density = counts / N_trials / (bins[1] - bins[0])
            grp = VGroup()
            bw = bins[1] - bins[0]
            for k, d in enumerate(density):
                if d < 0.003:
                    continue
                x_c = (bins[k] + bins[k + 1]) / 2
                h_scene = ax.c2p(0, d)[1] - ax.c2p(0, 0)[1]
                bar = Rectangle(
                    width=(ax.c2p(bw, 0)[0] - ax.c2p(0, 0)[0]) * 0.9,
                    height=h_scene,
                    color=BLUE, fill_opacity=0.6, stroke_width=0.5)
                bar.move_to([ax.c2p(x_c, 0)[0],
                             ax.c2p(0, 0)[1] + h_scene / 2, 0])
                grp.add(bar)
            return grp

        self.add(always_redraw(histogram))

        def info():
            i = int(round(n_idx_tr.get_value())) % len(n_values)
            n = n_values[i]
            return VGroup(
                MathTex(rf"n\text{{dice per sum}} = {n}",
                         color=BLUE, font_size=24),
                MathTex(rf"N_{{\text{{trials}}}} = {N_trials}",
                         color=WHITE, font_size=20),
                Tex(r"BLUE $\to$ YELLOW as $n \uparrow$",
                     color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for i in range(1, len(n_values)):
            self.play(n_idx_tr.animate.set_value(i),
                       run_time=1.4, rate_func=smooth)
            self.wait(0.6)
        self.wait(0.4)
