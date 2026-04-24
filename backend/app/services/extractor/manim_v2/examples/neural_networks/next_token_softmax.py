from manim import *
import numpy as np


class NextTokenSoftmaxExample(Scene):
    """
    Next-token prediction with temperature (from _2024/transformers/
    generation): logits from the final layer are scaled by 1/T
    before softmax. Low T → peaked, high T → uniform.

    TWO_COLUMN:
      LEFT  — bar chart of softmax probabilities over 8 candidate
              tokens; ValueTracker T_tr sweeps temperature 0.3 → 3.0;
              always_redraw bars update.
      RIGHT — live T, argmax token, entropy H = -Σ p log p.
    """

    def construct(self):
        title = Tex(r"Next-token softmax: $p_i = \dfrac{\exp(z_i/T)}{\sum_j \exp(z_j/T)}$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        tokens = ["the", "cat", "sat", "on", "a", "mat", "!", "</s>"]
        logits = np.array([2.5, 1.8, 0.3, 2.2, 1.5, 2.0, -0.5, -1.0])

        ax = Axes(x_range=[0, 8.5, 1], y_range=[0, 1.0, 0.25],
                   x_length=7, y_length=4, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-2.8, -0.3, 0])
        self.play(Create(ax))

        T_tr = ValueTracker(1.0)

        def softmax(T):
            z = logits / T
            z -= z.max()
            e = np.exp(z)
            return e / e.sum()

        def bars():
            T = T_tr.get_value()
            p = softmax(T)
            grp = VGroup()
            for i, pi in enumerate(p):
                h_scene = ax.c2p(0, pi)[1] - ax.c2p(0, 0)[1]
                if h_scene < 0.005:
                    continue
                bar = Rectangle(width=0.5, height=h_scene,
                                 color=BLUE, fill_opacity=0.7,
                                 stroke_width=1)
                bar.move_to([ax.c2p(i + 0.5, 0)[0],
                             ax.c2p(0, 0)[1] + h_scene / 2, 0])
                grp.add(bar)
                # Token label
                lbl = Tex(tokens[i], font_size=16,
                           color=WHITE).next_to(
                    ax.c2p(i + 0.5, 0), DOWN, buff=0.15)
                grp.add(lbl)
            return grp

        self.add(always_redraw(bars))

        def info():
            T = T_tr.get_value()
            p = softmax(T)
            argmax_i = int(np.argmax(p))
            H = -float(np.sum(p * np.log2(np.maximum(p, 1e-12))))
            return VGroup(
                MathTex(rf"T = {T:.2f}", color=YELLOW, font_size=26),
                Tex(rf"argmax: \"{tokens[argmax_i]}\" ({p[argmax_i]:.3f})",
                     color=GREEN, font_size=22),
                MathTex(rf"H = {H:.3f}\,\text{{bits}}",
                         color=RED, font_size=22),
                Tex(r"low $T$: greedy", color=BLUE, font_size=20),
                Tex(r"high $T$: diverse", color=ORANGE, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.3, 0.0, 0])

        self.add(always_redraw(info))

        for T_target in [0.3, 0.5, 1.0, 2.0, 3.0, 1.0]:
            self.play(T_tr.animate.set_value(T_target),
                       run_time=1.5, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
