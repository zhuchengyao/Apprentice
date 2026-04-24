from manim import *
import numpy as np


class WordleEntropyExample(Scene):
    """
    Wordle-style information gain (from _2022/wordle): the expected
    information gained from a guess is H = -Σ p_i log₂ p_i where
    p_i is the fraction of remaining words falling in each feedback
    pattern (grey / yellow / green).

    TWO_COLUMN:
      LEFT  — histogram of feedback-pattern sizes for 3 candidate
              guesses; always_redraw rebuilt as ValueTracker guess_idx
              steps through.
      RIGHT — information content -log₂ p_i per bin, with expected
              info H = Σ p_i · (-log₂ p_i) highlighted.
    """

    def construct(self):
        title = Tex(r"Wordle information: $H = -\sum p_i \log_2 p_i$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # 3 candidate guesses with their feedback-pattern distributions
        # over a hypothetical 200-word remaining list
        dists = {
            "TARES":  [50, 30, 28, 25, 20, 18, 15, 10, 4],
            "RAISE":  [42, 35, 28, 24, 21, 16, 14, 12, 8],
            "SLATE":  [46, 32, 30, 22, 21, 19, 14, 10, 6],
        }
        guesses = list(dists.keys())

        guess_idx = ValueTracker(0)

        ax = Axes(x_range=[0, 10, 1], y_range=[0, 60, 10],
                   x_length=6, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-3.3, -0.3, 0])
        xlbl = Tex("feedback pattern index",
                    font_size=18).next_to(ax, DOWN, buff=0.1)
        ylbl = Tex("count", font_size=18).next_to(ax, LEFT, buff=0.1)
        self.play(Create(ax), Write(xlbl), Write(ylbl))

        def hist():
            idx = int(round(guess_idx.get_value())) % len(guesses)
            g = guesses[idx]
            counts = dists[g]
            grp = VGroup()
            for i, c in enumerate(counts):
                bar = Rectangle(width=0.5, height=c * 0.07,
                                 color=BLUE, fill_opacity=0.6,
                                 stroke_width=1)
                bar.move_to(ax.c2p(i + 0.5, c * 0.5))
                # Height is c scaled
                bar.stretch_to_fit_height((ax.c2p(0, c)[1]
                                              - ax.c2p(0, 0)[1]))
                bar.move_to(ax.c2p(i + 0.5,
                                     (ax.c2p(0, c)[1] - ax.c2p(0, 0)[1]) / 2 /
                                     (ax.c2p(0, 1)[1] - ax.c2p(0, 0)[1])))
                # Easier: use the y-length directly
                h_scene = ax.c2p(0, c)[1] - ax.c2p(0, 0)[1]
                bar = Rectangle(width=0.5, height=h_scene,
                                 color=BLUE, fill_opacity=0.6,
                                 stroke_width=1)
                x_scene = ax.c2p(i + 0.5, 0)[0]
                bar.move_to([x_scene, ax.c2p(0, 0)[1] + h_scene / 2, 0])
                grp.add(bar)
            return grp

        self.add(always_redraw(hist))

        def title_guess():
            idx = int(round(guess_idx.get_value())) % len(guesses)
            return Tex(rf"guess: {guesses[idx]}",
                        color=YELLOW, font_size=24
                        ).move_to([-3.3, 2.3, 0])

        self.add(always_redraw(title_guess))

        def info_panel():
            idx = int(round(guess_idx.get_value())) % len(guesses)
            g = guesses[idx]
            counts = dists[g]
            total = sum(counts)
            probs = [c / total for c in counts]
            H = -sum(p * np.log2(p) for p in probs if p > 0)
            return VGroup(
                MathTex(rf"\text{{total words}} = {total}",
                         color=WHITE, font_size=22),
                MathTex(rf"H({guesses[idx]}) = {H:.3f}\,\text{{bits}}",
                         color=GREEN, font_size=24),
                MathTex(r"\text{higher}\ H \Rightarrow \text{more info}",
                         color=GREEN, font_size=20),
                MathTex(r"\log_2 |\text{buckets}| \approx 3.17",
                         color=GREY_B, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.8, 0.0, 0])

        self.add(always_redraw(info_panel))

        for target in [1, 2, 0, 1]:
            self.play(guess_idx.animate.set_value(target),
                       run_time=1.6, rate_func=smooth)
            self.wait(0.6)
        self.wait(0.4)
