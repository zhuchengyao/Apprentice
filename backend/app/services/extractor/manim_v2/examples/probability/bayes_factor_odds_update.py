from manim import *
import numpy as np


class BayesFactorOddsUpdate(Scene):
    """Bayes' rule in odds form.  Instead of tracking probabilities, track
    the ODDS O(H) = P(H) / P(not H).  New evidence multiplies the odds
    by the Bayes factor (likelihood ratio):
        O(H | E) = O(H) * [P(E|H) / P(E|not H)].
    Example: medical test with 90% sensitivity, 9% false-positive rate
    (Bayes factor = 10), starting from 1% disease prior."""

    def construct(self):
        title = Tex(
            r"Bayes in odds form: multiply by the Bayes factor",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        rule = MathTex(
            r"\text{posterior odds} = \text{prior odds} \times "
            r"\underbrace{\tfrac{P(E|H)}{P(E|\neg H)}}_{\text{Bayes factor}}",
            font_size=30,
        ).next_to(title, DOWN, buff=0.4)
        self.play(Write(rule))

        sensitivity = 0.9
        false_pos = 0.09
        bf = sensitivity / false_pos
        prior_p = 0.01
        prior_odds = prior_p / (1 - prior_p)
        post_odds = prior_odds * bf
        post_p = post_odds / (1 + post_odds)

        table = VGroup()
        header = VGroup(
            Tex("", font_size=22),
            Tex("odds", font_size=22, color=YELLOW),
            Tex("probability", font_size=22, color=YELLOW),
        ).arrange(RIGHT, buff=1.5)
        header.move_to([0, 1.2, 0])
        table.add(header)
        rows_data = [
            ("prior", prior_odds, prior_p, BLUE),
            (r"$\times$ Bayes factor (10)", None, None, GREEN),
            ("posterior", post_odds, post_p, PURPLE),
        ]
        y = 0.5
        for i, (name, odds, p, color) in enumerate(rows_data):
            if odds is None:
                row = Tex(name, font_size=24, color=color).move_to(
                    [0, y, 0]
                )
            else:
                row = VGroup(
                    Tex(name, font_size=24, color=color),
                    MathTex(
                        rf"\approx {odds:.4f}",
                        font_size=24, color=color,
                    ),
                    MathTex(
                        rf"\approx {p*100:.2f}\%",
                        font_size=24, color=color,
                    ),
                ).arrange(RIGHT, buff=1.2)
                row.move_to([0, y, 0])
            table.add(row)
            y -= 0.55

        self.play(FadeIn(table[0]))
        self.play(FadeIn(table[1]))
        self.play(Write(table[2]))
        self.play(Write(table[3]))

        arrow = Arrow(
            [3.5, 0.5, 0], [3.5, -0.6, 0],
            buff=0.1, color=GREEN, stroke_width=3,
            max_tip_length_to_length_ratio=0.15,
        )
        arrow_lab = MathTex(
            r"\times 10",
            font_size=30, color=GREEN,
        ).next_to(arrow, RIGHT, buff=0.1)
        self.play(GrowArrow(arrow), Write(arrow_lab))

        compare = VGroup(
            Tex(r"Prior: 1 in 100 have the disease.",
                font_size=22, color=BLUE),
            Tex(r"Bayes factor: a positive test is 10$\times$ more likely\\"
                r"in a sick person (sensitivity 90\%) than healthy (FPR 9\%).",
                font_size=22, color=GREEN),
            Tex(rf"Posterior: $\approx {post_p*100:.1f}\%$ — not the 90\% most people guess.",
                font_size=22, color=PURPLE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        compare.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(compare))
        self.wait(1.5)
