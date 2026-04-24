from manim import *
import numpy as np


class LayerNormExample(Scene):
    """
    Layer normalization: for each sample, normalize across features
    (not across batch like BatchNorm). y = (x - μ) / √(σ² + ε), μ and
    σ computed per-sample across the feature dim.

    TWO_COLUMN:
      LEFT  — 4 samples (rows) × 8 features (cols); ValueTracker
              s_tr morphs raw values to per-sample normalized.
      RIGHT  — live per-sample μ, σ before vs after.
    """

    def construct(self):
        title = Tex(r"LayerNorm: normalize across features per sample",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        rng = np.random.default_rng(11)
        N_samples, D_features = 4, 8
        raw = rng.normal(loc=2.0, scale=1.5, size=(N_samples, D_features))
        # Add different per-sample shifts to make normalization visible
        for i in range(N_samples):
            raw[i] += i * 1.5

        # Normalize per row
        normalized = (raw - raw.mean(axis=1, keepdims=True)) / (raw.std(axis=1, keepdims=True) + 1e-6)

        s_tr = ValueTracker(0.0)

        cell = 0.5
        grid_origin = np.array([-3.5, 1.3, 0])

        def grid_cells():
            s = s_tr.get_value()
            grp = VGroup()
            for r in range(N_samples):
                for c in range(D_features):
                    v = (1 - s) * raw[r, c] + s * normalized[r, c]
                    norm_v = np.tanh(v / 2)
                    col = interpolate_color(BLUE_E, RED, (norm_v + 1) / 2)
                    sq = Square(side_length=cell * 0.9, color=col,
                                  fill_opacity=0.85, stroke_width=0.5)
                    sq.move_to(grid_origin + np.array([c * cell,
                                                           -r * cell, 0]))
                    grp.add(sq)
            return grp

        self.add(always_redraw(grid_cells))

        # Row labels
        for i in range(N_samples):
            lbl = MathTex(rf"x_{i + 1}", font_size=16, color=WHITE
                            ).move_to(grid_origin + np.array([-0.7, -i * cell, 0]))
            self.add(lbl)
        # Column header
        col_hdr = Tex(r"features", font_size=18
                       ).move_to(grid_origin + np.array([(D_features - 1) * cell / 2, 0.6, 0]))
        self.add(col_hdr)

        def info():
            s = s_tr.get_value()
            cur = (1 - s) * raw + s * normalized
            mu_by_row = cur.mean(axis=1)
            sigma_by_row = cur.std(axis=1)
            return VGroup(
                MathTex(rf"s = {s:.2f}", color=YELLOW, font_size=22),
                MathTex(rf"\mu_1 = {mu_by_row[0]:+.2f},\ \sigma_1 = {sigma_by_row[0]:.2f}",
                         color=WHITE, font_size=18),
                MathTex(rf"\mu_2 = {mu_by_row[1]:+.2f},\ \sigma_2 = {sigma_by_row[1]:.2f}",
                         color=WHITE, font_size=18),
                Tex(r"target: $\mu=0$, $\sigma=1$ per row",
                     color=GREEN, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        self.play(s_tr.animate.set_value(1.0),
                   run_time=4, rate_func=smooth)
        self.wait(0.4)
        self.play(s_tr.animate.set_value(0.0),
                   run_time=3, rate_func=smooth)
        self.wait(0.4)
