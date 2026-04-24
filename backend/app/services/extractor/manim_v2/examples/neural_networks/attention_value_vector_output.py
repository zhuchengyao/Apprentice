from manim import *
import numpy as np


class AttentionValueVectorOutput(Scene):
    """The final step of attention: multiply each Value vector by its
    attention weight (from softmax of Q·K) and sum.  Show 5 tokens, each
    with a 4D Value vector; softmax weights 0.05, 0.10, 0.60, 0.15, 0.10
    for a query row; output = Σ w_i * v_i."""

    def construct(self):
        title = Tex(
            r"Attention output: $\sum_i w_i\, v_i$",
            font_size=30,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        tokens = ["the", "cat", "sat", "on", "mat"]
        weights = [0.05, 0.10, 0.60, 0.15, 0.10]
        rng = np.random.default_rng(11)
        values = rng.normal(size=(5, 4)) * 0.7

        def vec_col(v, x, color=BLUE):
            col = VGroup()
            for i, val in enumerate(v):
                c = GREEN if val >= 0 else RED
                sq = Square(
                    side_length=0.38, stroke_width=0.8,
                    fill_opacity=min(1.0, abs(val) / 1.2),
                    fill_color=c, stroke_color=GREY_B,
                )
                sq.move_to([x, 0.6 - i * 0.4, 0])
                col.add(sq)
            return col

        token_group = VGroup()
        for i, (tok, v) in enumerate(zip(tokens, values)):
            x = -5.2 + i * 1.2
            lab = Tex(tok, font_size=22, color=BLUE).move_to([x, 1.6, 0])
            wlab = MathTex(
                rf"w={weights[i]:.2f}",
                font_size=20,
                color=YELLOW if weights[i] > 0.3 else GREY_A,
            ).move_to([x, 2.1, 0])
            col = vec_col(v, x)
            token_group.add(VGroup(lab, wlab, col))
        self.play(LaggedStart(*[FadeIn(t) for t in token_group],
                              lag_ratio=0.1))

        weighted_group = VGroup()
        for i in range(5):
            x = -5.2 + i * 1.2
            wv = values[i] * weights[i]
            col = vec_col(wv, x, color=PURPLE)
            wlab = MathTex(
                rf"\times {weights[i]:.2f}", font_size=18, color=YELLOW,
            ).move_to([x, -1.5, 0])
            weighted_group.add(VGroup(col, wlab))
        self.play(TransformFromCopy(
            VGroup(*[t[2] for t in token_group]),
            VGroup(*[w[0] for w in weighted_group]),
        ))
        self.play(FadeIn(VGroup(*[w[1] for w in weighted_group])))

        out = np.sum(values * np.array(weights)[:, None], axis=0)
        plus_signs = VGroup(*[
            MathTex("+", font_size=30).move_to(
                [-5.2 + (i + 0.5) * 1.2, -0.5, 0]
            )
            for i in range(4)
        ])
        equal_sign = MathTex("=", font_size=36).move_to([2.4, -0.5, 0])
        out_col = vec_col(out, 3.3, color=YELLOW)
        out_border = SurroundingRectangle(out_col, color=YELLOW, buff=0.08,
                                          stroke_width=3)
        out_lab = Tex("output", font_size=22, color=YELLOW).move_to(
            [3.3, 1.3, 0]
        )
        self.play(FadeIn(plus_signs), Write(equal_sign))
        self.play(FadeIn(out_col), Create(out_border), FadeIn(out_lab))

        formula = MathTex(
            r"z = \sum_i \text{softmax}(QK^T)_i \cdot V_i",
            font_size=26, color=YELLOW,
        ).to_edge(DOWN, buff=0.25)
        self.play(Write(formula))
        self.wait(1.5)
