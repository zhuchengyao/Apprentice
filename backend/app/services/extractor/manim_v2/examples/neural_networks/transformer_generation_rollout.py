from manim import *
import numpy as np


class TransformerGenerationRolloutExample(Scene):
    """
    Autoregressive transformer generation (from _2024/transformers/
    auto_regression): each step, the model sees previous tokens and
    predicts the next via softmax; sampled token appended to context.

    SINGLE_FOCUS:
      Token-box row grows as ValueTracker step_tr steps; each step
      shows the current softmax distribution bar chart + sampled
      token (BLUE highlight).
    """

    def construct(self):
        title = Tex(r"Autoregressive generation: $p(x_t \mid x_{<t})$ $\to$ sample $\to$ append",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Generated sequence (precomputed)
        sentence = ["The", "cat", "sat", "on", "the", "mat", "."]
        probs = [
            [0.7, 0.15, 0.05, 0.05, 0.03, 0.02, 0.0],  # "The"
            [0.6, 0.2, 0.1, 0.05, 0.03, 0.02, 0.0],   # "cat"
            [0.5, 0.3, 0.1, 0.05, 0.03, 0.02, 0.0],   # "sat"
            [0.4, 0.3, 0.15, 0.08, 0.04, 0.03, 0.0],  # "on"
            [0.5, 0.2, 0.15, 0.08, 0.04, 0.03, 0.0],  # "the"
            [0.55, 0.2, 0.1, 0.08, 0.04, 0.03, 0.0],  # "mat"
            [0.7, 0.1, 0.08, 0.05, 0.04, 0.02, 0.01],  # "."
        ]

        # Candidate tokens shown in the softmax (top 7 options per step)
        candidates = [
            ["The", "A", "An", "One", "Every", "The_", "Some"],
            ["cat", "dog", "man", "boy", "fish", "bird", "bear"],
            ["sat", "ran", "was", "stood", "slept", "ate", "fell"],
            ["on", "in", "under", "beside", "near", "atop", "by"],
            ["the", "a", "his", "my", "their", "our", "one"],
            ["mat", "floor", "chair", "box", "lawn", "rug", "sofa"],
            [".", ",", "!", "?", ";", ":", "..."],
        ]

        box_y = 2.0
        box_w = 0.8

        step_tr = ValueTracker(0)

        def token_boxes():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, len(sentence)))
            grp = VGroup()
            for i in range(s):
                # Box
                b = Rectangle(width=box_w, height=0.6,
                                color=BLUE, fill_opacity=0.3, stroke_width=1.5)
                b.move_to([-3.5 + i * (box_w + 0.1), box_y, 0])
                lbl = Tex(sentence[i], font_size=18,
                           color=WHITE).move_to(b.get_center())
                grp.add(b, lbl)
            # Next-token placeholder (at step s)
            if s < len(sentence):
                b_next = Rectangle(width=box_w, height=0.6,
                                     color=ORANGE, fill_opacity=0.15,
                                     stroke_width=2)
                b_next.move_to([-3.5 + s * (box_w + 0.1), box_y, 0])
                lbl_q = Tex(r"?", font_size=20, color=ORANGE
                             ).move_to(b_next.get_center())
                grp.add(b_next, lbl_q)
            return grp

        def bar_chart():
            s = int(round(step_tr.get_value())) % len(sentence)
            if s >= len(sentence):
                return VGroup()
            p = probs[s]
            cands = candidates[s]
            grp = VGroup()
            bar_base_y = -2.0
            bar_base_x = -4.5
            for i, (pi, cand) in enumerate(zip(p, cands)):
                if pi < 0.001:
                    continue
                w = pi * 9
                y = bar_base_y + (6 - i) * 0.35
                color = BLUE if cand == sentence[s] else GREY_B
                bar = Rectangle(width=w, height=0.3, color=color,
                                 fill_opacity=0.7, stroke_width=0.8)
                bar.move_to([bar_base_x + w / 2, y, 0])
                grp.add(bar)
                c_lbl = Tex(cand, font_size=16, color=color).next_to(
                    bar, LEFT, buff=0.1)
                p_lbl = MathTex(rf"{pi:.2f}", font_size=14, color=WHITE
                                  ).next_to(bar, RIGHT, buff=0.05)
                grp.add(c_lbl, p_lbl)
            return grp

        self.add(always_redraw(token_boxes),
                  always_redraw(bar_chart))

        def info():
            s = int(round(step_tr.get_value())) % len(sentence)
            if s >= len(sentence):
                sample_txt = "done"
            else:
                sample_txt = rf"sample: ``{sentence[s]}''"
            return VGroup(
                MathTex(rf"\text{{step}} = {s}", color=YELLOW, font_size=24),
                Tex(sample_txt, color=BLUE, font_size=22),
                Tex(r"softmax probabilities (BLUE = sampled)",
                     color=WHITE, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.5, 1.0, 0])

        self.add(always_redraw(info))

        for target in range(1, len(sentence) + 1):
            self.play(step_tr.animate.set_value(target),
                       run_time=1.0, rate_func=smooth)
            self.wait(0.6)
        self.wait(0.4)
