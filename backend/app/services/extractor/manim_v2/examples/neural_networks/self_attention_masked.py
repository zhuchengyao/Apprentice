from manim import *
import numpy as np


class SelfAttentionMaskedExample(Scene):
    """
    Masked self-attention (causal): token i can only attend to tokens
    j ≤ i. Used in autoregressive models (GPT-style). Visualize
    attention matrix with upper triangle masked (set to -∞ pre-softmax).

    SINGLE_FOCUS:
      n × n attention heatmap (n=8); softmax over rows. Upper
      triangle zero due to mask. ValueTracker q_idx_tr highlights
      active query row.
    """

    def construct(self):
        title = Tex(r"Masked self-attention: causal triangular mask",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        n = 8
        rng = np.random.default_rng(17)
        scores = rng.normal(size=(n, n)) * 0.6

        # Apply causal mask: upper triangle → -∞
        mask = np.tril(np.ones((n, n))).astype(bool)
        scores_masked = np.where(mask, scores, -1e9)
        # Row-wise softmax
        attn = np.exp(scores_masked - scores_masked.max(axis=1, keepdims=True))
        attn = np.where(mask, attn, 0)
        attn = attn / (attn.sum(axis=1, keepdims=True) + 1e-10)

        cell = 0.55
        origin = np.array([-cell * (n - 1) / 2, cell * (n - 1) / 2 - 0.3, 0])

        # Matrix cells
        cells = VGroup()
        for r in range(n):
            for c in range(n):
                if c > r:  # upper triangle: masked
                    col = GREY_B
                    op = 0.1
                    val_text = ""
                else:
                    intensity = attn[r, c]
                    col = interpolate_color(BLUE_E, YELLOW, intensity)
                    op = 0.4 + 0.5 * intensity
                    val_text = f"{attn[r, c]:.2f}"
                sq = Square(side_length=cell * 0.95,
                              color=col, fill_opacity=op,
                              stroke_width=0.5)
                sq.move_to(origin + np.array([c * cell, -r * cell, 0]))
                cells.add(sq)
                if val_text:
                    cells.add(Tex(val_text, font_size=10, color=WHITE
                                    ).move_to(sq.get_center()))
        self.play(FadeIn(cells))

        # Row/col labels
        axes_lbl = VGroup()
        for i in range(n):
            axes_lbl.add(MathTex(rf"{i}", font_size=14, color=GREY_B
                                   ).move_to(origin + np.array([-0.55, -i * cell, 0])))
            axes_lbl.add(MathTex(rf"{i}", font_size=14, color=GREY_B
                                   ).move_to(origin + np.array([i * cell, cell * 0.6, 0])))
        self.play(FadeIn(axes_lbl))

        q_idx_tr = ValueTracker(0)

        def row_highlight():
            i = int(round(q_idx_tr.get_value())) % n
            return Rectangle(width=n * cell + 0.1, height=cell,
                               color=RED, fill_opacity=0.15,
                               stroke_width=2
                               ).move_to(origin + np.array([(n - 1) * cell / 2,
                                                                 -i * cell, 0]))

        self.add(always_redraw(row_highlight))

        def info():
            i = int(round(q_idx_tr.get_value())) % n
            return VGroup(
                MathTex(rf"\text{{query}} = {i}",
                         color=RED, font_size=22),
                MathTex(rf"\text{{attends to tokens}} 0..{i}",
                         color=YELLOW, font_size=20),
                Tex(r"upper triangle: masked ($-\infty$ pre-softmax)",
                     color=GREY_B, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        for iv in [2, 4, 6, 7, 0]:
            self.play(q_idx_tr.animate.set_value(iv),
                       run_time=1.0, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
