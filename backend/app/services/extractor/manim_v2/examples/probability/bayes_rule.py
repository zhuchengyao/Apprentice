from manim import *
import numpy as np


class BayesRuleExample(Scene):
    """
    Bayesian update visualized as rectangle proportions.

    A unit square is split vertically by the prior P(H) and horizontally
    within each column by the conditional P(+|H) or P(+|¬H). The yellow
    regions are where the test comes back positive; the posterior
    P(H|+) is the fraction of that yellow area inside the sick column.

    A ValueTracker sweeps the prior from 0.01 → 0.40 → 0.01 so you can
    watch the posterior transform as base rate changes — the point of
    the whole rule.
    """

    def construct(self):
        title = Text("Bayes' rule: posterior as a fraction of positive area",
                     font_size=26).to_edge(UP)
        self.play(Write(title))

        # Fixed test characteristics
        tpr = 0.9   # P(+ | sick)
        fpr = 0.1   # P(+ | healthy)

        prior = ValueTracker(0.05)

        # Axes/frame for the proportion diagram
        total_w, total_h = 6.0, 3.2
        frame = Rectangle(width=total_w, height=total_h, color=GREY_B, stroke_width=2)
        frame.shift(0.3 * DOWN + LEFT * 1.2)

        # Persistent column outlines that redraw each frame based on prior
        def sick_col():
            p = prior.get_value()
            rect = Rectangle(width=total_w * p, height=total_h,
                             color=RED, fill_opacity=0.15, stroke_width=1.5)
            rect.align_to(frame, LEFT).align_to(frame, DOWN)
            return rect

        def healthy_col():
            p = prior.get_value()
            rect = Rectangle(width=total_w * (1 - p), height=total_h,
                             color=BLUE, fill_opacity=0.15, stroke_width=1.5)
            rect.align_to(frame, RIGHT).align_to(frame, DOWN)
            return rect

        def sick_pos():
            p = prior.get_value()
            rect = Rectangle(width=total_w * p, height=total_h * tpr,
                             color=YELLOW, fill_opacity=0.75, stroke_width=0)
            rect.align_to(frame, LEFT).align_to(frame, UP)
            return rect

        def healthy_pos():
            p = prior.get_value()
            rect = Rectangle(width=total_w * (1 - p), height=total_h * fpr,
                             color=YELLOW, fill_opacity=0.5, stroke_width=0)
            rect.align_to(frame, RIGHT).align_to(frame, UP)
            return rect

        self.play(Create(frame))
        self.add(
            always_redraw(sick_col),
            always_redraw(healthy_col),
            always_redraw(sick_pos),
            always_redraw(healthy_pos),
        )

        # Axis labels
        prior_brace = always_redraw(lambda: Brace(
            Line(
                frame.get_corner(DL),
                frame.get_corner(DL) + RIGHT * total_w * prior.get_value(),
            ),
            DOWN, color=RED,
        ))
        prior_lbl = always_redraw(lambda: MathTex(
            rf"P(H) = {prior.get_value():.2f}", color=RED, font_size=24
        ).next_to(prior_brace, DOWN, buff=0.1))

        self.add(prior_brace, prior_lbl)

        # Right-side stats panel
        def stats_panel():
            p = prior.get_value()
            tp = p * tpr
            fp = (1 - p) * fpr
            post = tp / (tp + fp) if (tp + fp) > 0 else 0
            return VGroup(
                MathTex(rf"P(+ | H) = {tpr:.1f}", color=RED, font_size=24),
                MathTex(rf"P(+ | \neg H) = {fpr:.1f}", color=BLUE, font_size=24),
                MathTex(rf"P(+) = {tp + fp:.3f}", color=YELLOW, font_size=24),
                MathTex(rf"P(H | +) = {post:.3f}", color=GREEN, font_size=28),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT).shift(LEFT * 0.2)

        panel = always_redraw(stats_panel)
        self.add(panel)

        self.wait(0.6)

        # Sweep the prior so the viewer watches the posterior climb
        self.play(prior.animate.set_value(0.40), run_time=4, rate_func=smooth)
        self.wait(0.5)
        self.play(prior.animate.set_value(0.01), run_time=4, rate_func=smooth)
        self.wait(0.5)
        self.play(prior.animate.set_value(0.15), run_time=2, rate_func=smooth)
        self.wait(0.5)

        formula = MathTex(
            r"P(H \mid +) = \tfrac{P(+\mid H)\,P(H)}{P(+\mid H)\,P(H) + P(+\mid \neg H)\,P(\neg H)}",
            font_size=26, color=YELLOW,
        ).to_edge(DOWN)
        self.play(Write(formula))
        self.wait(1.0)
