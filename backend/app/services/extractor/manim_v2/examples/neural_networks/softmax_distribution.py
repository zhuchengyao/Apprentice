from manim import *
import numpy as np


class SoftmaxDistributionExample(Scene):
    def construct(self):
        title = Text("Softmax turns logits into a probability distribution",
                     font_size=26).to_edge(UP)
        self.play(Write(title))

        logits = np.array([2.0, 1.0, 0.1, -0.5, 3.2])
        exps = np.exp(logits)
        probs = exps / exps.sum()

        axes = Axes(
            x_range=[0, 6, 1], y_range=[0, 1, 0.25],
            x_length=8, y_length=3.3,
            axis_config={"include_tip": True, "include_numbers": True},
        ).shift(DOWN * 0.5)
        self.play(Create(axes))

        # Logit bars (raw)
        logit_bars = VGroup()
        for i, z in enumerate(logits):
            # Display raw logits by shifting up by 1 so that negatives still show
            base = axes.c2p(i + 0.7, 0)
            top_y = 0.2 + 0.15 * (z + 1)
            top = axes.c2p(i + 0.7, top_y)
            bar = Rectangle(width=0.35, height=np.linalg.norm(np.array(top) - np.array(base)),
                            color=BLUE, fill_opacity=0.5, stroke_width=1)
            bar.move_to((np.array(top) + np.array(base)) / 2)
            lbl = MathTex(f"{z:.1f}", font_size=20, color=BLUE).next_to(bar, UP, buff=0.05)
            logit_bars.add(VGroup(bar, lbl))
        self.play(FadeIn(logit_bars))

        logits_title = Text("logits zᵢ", color=BLUE, font_size=22).to_corner(UL).shift(DOWN * 0.6 + RIGHT * 0.4)
        self.play(Write(logits_title))
        self.wait(0.5)

        # Transform to softmax probabilities
        prob_bars = VGroup()
        for i, p in enumerate(probs):
            base = axes.c2p(i + 0.7, 0)
            top = axes.c2p(i + 0.7, p)
            bar = Rectangle(width=0.35, height=np.linalg.norm(np.array(top) - np.array(base)),
                            color=YELLOW, fill_opacity=0.7, stroke_width=1)
            bar.move_to((np.array(top) + np.array(base)) / 2)
            lbl = MathTex(f"{p:.2f}", font_size=20, color=YELLOW).next_to(bar, UP, buff=0.05)
            prob_bars.add(VGroup(bar, lbl))

        self.play(Transform(logit_bars, prob_bars), run_time=1.5)
        probs_title = Text("softmax probs p_i", color=YELLOW, font_size=22).next_to(logits_title, DOWN, aligned_edge=LEFT, buff=0.15)
        self.play(Transform(logits_title, probs_title))

        formula = MathTex(
            r"p_i = \frac{e^{z_i}}{\sum_j e^{z_j}}\quad \sum_i p_i = 1",
            font_size=30, color=YELLOW,
        ).to_edge(DOWN)
        self.play(Write(formula))
        self.wait(0.6)
