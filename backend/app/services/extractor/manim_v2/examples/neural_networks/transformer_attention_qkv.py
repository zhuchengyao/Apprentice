from manim import *
import numpy as np


class TransformerAttentionQKVExample(Scene):
    """
    Scaled dot-product attention as Q K^T / √d → softmax → weighted V
    (from _2024/transformers/attention): three matrices Q, K, V
    with shapes (n, d). ValueTracker query_idx highlights one
    query row; always_redraw colored attention weights over rows.

    TWO_COLUMN:
      LEFT  — three stacked matrices Q, K, V (5×4 each) with highlighted
              query row.
      RIGHT — attention weights (softmaxed) as a horizontal bar chart;
              live weighted-sum V row.
    """

    def construct(self):
        title = Tex(r"Attention: $\mathrm{softmax}(QK^\top/\sqrt d)\,V$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        n, d = 5, 4
        rng = np.random.default_rng(31)
        Q = rng.normal(scale=0.6, size=(n, d))
        K = rng.normal(scale=0.6, size=(n, d))
        V = rng.normal(scale=0.6, size=(n, d))

        # Draw matrices as colored-cell grids
        cell = 0.4

        def matrix_grid(M, origin, label, color):
            grp = VGroup()
            # Label
            lbl = Tex(label, color=color, font_size=22
                        ).move_to(origin + np.array([-1.0, 0, 0]))
            grp.add(lbl)
            for r in range(M.shape[0]):
                for c in range(M.shape[1]):
                    v = M[r, c]
                    intensity = min(1.0, abs(v) / 2)
                    col = interpolate_color(
                        GREY_B, color,
                        intensity)
                    sq = Square(side_length=cell * 0.9, color=color,
                                  fill_opacity=0.2 + 0.5 * intensity,
                                  stroke_width=0.8)
                    sq.move_to(origin + np.array([c * cell, -r * cell, 0]))
                    grp.add(sq)
            return grp

        Q_origin = np.array([-4.5, 1.5, 0])
        K_origin = np.array([-1.5, 1.5, 0])
        V_origin = np.array([1.5, 1.5, 0])

        Q_grid = matrix_grid(Q, Q_origin, r"$Q$", BLUE)
        K_grid = matrix_grid(K, K_origin, r"$K$", GREEN)
        V_grid = matrix_grid(V, V_origin, r"$V$", RED)
        self.play(FadeIn(Q_grid), FadeIn(K_grid), FadeIn(V_grid))

        query_idx = ValueTracker(0)

        def row_highlight_Q():
            i = int(round(query_idx.get_value())) % n
            return Rectangle(width=d * cell + 0.1, height=cell,
                              color=YELLOW, fill_opacity=0.15,
                              stroke_width=2
                              ).move_to(Q_origin
                                         + np.array([(d - 1) * cell / 2,
                                                        -i * cell, 0]))

        self.add(always_redraw(row_highlight_Q))

        def attn_weights():
            i = int(round(query_idx.get_value())) % n
            scores = K @ Q[i] / np.sqrt(d)
            scores -= scores.max()
            w = np.exp(scores)
            w /= w.sum()
            return w

        def weights_bars():
            w = attn_weights()
            grp = VGroup()
            x0 = 3.5
            bar_base_y = 1.3
            for k in range(n):
                wv = w[k]
                h = cell
                wth = wv * 2.5
                bar = Rectangle(width=wth, height=h * 0.85,
                                 color=YELLOW, fill_opacity=0.75,
                                 stroke_width=0.8)
                bar.move_to(np.array([x0 + wth / 2, bar_base_y - k * cell, 0]))
                grp.add(bar)
                lbl = MathTex(rf"{wv:.2f}",
                                font_size=14,
                                color=WHITE).move_to(
                    np.array([x0 + wth + 0.25,
                               bar_base_y - k * cell, 0]))
                grp.add(lbl)
            return grp

        self.add(always_redraw(weights_bars))

        weights_title = Tex(r"softmax weights",
                              color=YELLOW, font_size=22
                              ).move_to([4.5, 2.2, 0])
        self.play(Write(weights_title))

        def info():
            i = int(round(query_idx.get_value())) % n
            w = attn_weights()
            out = w @ V
            return VGroup(
                MathTex(rf"\text{{query}} = Q_{i}",
                         color=BLUE, font_size=22),
                MathTex(r"\text{output} = \sum_k w_k V_k",
                         color=RED, font_size=20),
                MathTex(rf"= ({out[0]:+.2f}, {out[1]:+.2f}, \ldots)",
                         color=RED, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        for target in [1, 2, 3, 4, 0]:
            self.play(query_idx.animate.set_value(target),
                       run_time=1.4, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.4)
