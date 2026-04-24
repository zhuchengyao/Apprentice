from manim import *
import numpy as np


class MedicalTestBayesExample(Scene):
    """
    Bayesian update on a 100-person population: prior sweeps via tracker.

    TWO_COLUMN:
      LEFT  — 10×10 grid of dots representing 100 people. ValueTracker
              prior_pct sweeps from 1% to 30%; each frame the dots are
              recolored: the bottom-left "prior_pct" dots are RED
              (sick), the rest are BLUE; among the BLUE dots, exactly
              5% (rounded) become ORANGE (false positives). Among the
              RED dots, all are also "positive" — drawn as RED with a
              thicker stroke for "positive test".
      RIGHT — live readouts: prior P(sick), TP count, FP count, total
              positive, posterior P(sick | +). A small bar chart on the
              far right shows posterior climbing as prior climbs.
    """

    def construct(self):
        title = Tex(r"Bayes update: posterior $P(\text{sick} \mid +)$ as the base rate changes",
                    font_size=26).to_edge(UP, buff=0.4)
        self.play(Write(title))

        rows, cols = 10, 10
        spacing = 0.42
        # Persistent dot positions
        positions = []
        for r in range(rows):
            for c in range(cols):
                positions.append([c * spacing - cols * spacing / 2,
                                  r * spacing - rows * spacing / 2, 0])

        prior_pct = ValueTracker(0.01)  # fraction sick
        TPR = 1.0   # P(+ | sick)
        FPR = 0.05  # P(+ | healthy)

        # Anchor the dots in the LEFT column
        anchor = np.array([-3.4, -0.4, 0])

        def dots_group():
            p = prior_pct.get_value()
            n_sick = int(round(p * 100))
            n_healthy = 100 - n_sick
            n_fp = int(round(FPR * n_healthy))
            grp = VGroup()
            # Pseudo-random but deterministic: false positives spread among healthy slots
            # Sick = first n_sick indices; FP = next n_fp indices wrapped
            for i, pos in enumerate(positions):
                world_pos = [pos[0] + anchor[0], pos[1] + anchor[1], 0]
                if i < n_sick:
                    color = RED
                    stroke_w = 2.5  # positive test (TPR=1)
                elif i < n_sick + n_fp:
                    color = ORANGE
                    stroke_w = 2.5  # false positive
                else:
                    color = BLUE_E
                    stroke_w = 0
                d = Dot(world_pos, color=color, radius=0.13, stroke_width=stroke_w,
                        stroke_color=YELLOW)
                grp.add(d)
            return grp

        self.add(always_redraw(dots_group))

        legend = VGroup(
            VGroup(Dot(color=RED, radius=0.12), Tex(r"sick (positive)", font_size=20, color=RED)).arrange(RIGHT, buff=0.15),
            VGroup(Dot(color=ORANGE, radius=0.12), Tex(r"false positive", font_size=20, color=ORANGE)).arrange(RIGHT, buff=0.15),
            VGroup(Dot(color=BLUE_E, radius=0.12), Tex(r"healthy", font_size=20, color=BLUE)).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([anchor[0], -3.0, 0])
        self.play(FadeIn(legend))

        # RIGHT COLUMN: live readouts
        rcol_x = +3.6

        def stats_panel():
            p = prior_pct.get_value()
            tp = p * TPR
            fp = (1 - p) * FPR
            posterior = tp / (tp + fp) if (tp + fp) > 0 else 0
            return VGroup(
                MathTex(rf"P(\text{{sick}}) = {p:.2%}", color=RED, font_size=28),
                MathTex(rf"P(+\,|\,\text{{sick}}) = {TPR:.2f}", color=GREY_B, font_size=22),
                MathTex(rf"P(+\,|\,\text{{healthy}}) = {FPR:.2f}",
                        color=GREY_B, font_size=22),
                MathTex(rf"P(+) = {tp + fp:.4f}", color=YELLOW, font_size=24),
                MathTex(rf"P(\text{{sick}}\,|\,+) = {posterior:.3f}",
                        color=GREEN, font_size=32),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([rcol_x, +1.6, 0])

        self.add(always_redraw(stats_panel))

        # Mini bar showing posterior on a 0-1 scale
        bar_axes = Axes(
            x_range=[0, 0.3, 0.05], y_range=[0, 1, 0.25],
            x_length=2.6, y_length=1.6,
            axis_config={"include_tip": False, "include_numbers": True, "font_size": 14},
        ).move_to([rcol_x, -1.7, 0])
        # Posterior as function of prior, fixed TPR/FPR
        post_curve = bar_axes.plot(
            lambda x: x * TPR / (x * TPR + (1 - x) * FPR) if x > 0 else 0,
            x_range=[0.001, 0.295, 0.005],
            color=GREEN,
        )
        bar_lbl = Tex(r"$P(\text{sick}|+)$ vs prior", color=GREEN,
                      font_size=18).next_to(bar_axes, UP, buff=0.05)
        self.play(Create(bar_axes), Create(post_curve), Write(bar_lbl))

        def bar_cursor():
            p = prior_pct.get_value()
            posterior = p * TPR / (p * TPR + (1 - p) * FPR) if p > 0 else 0
            return Dot(bar_axes.c2p(p, posterior), color=GREEN, radius=0.07)

        self.add(always_redraw(bar_cursor))

        # Sweep prior up
        for tgt in [0.01, 0.05, 0.10, 0.20, 0.30, 0.05]:
            self.play(prior_pct.animate.set_value(tgt),
                      run_time=2.0, rate_func=smooth)
            self.wait(0.4)

        formula = MathTex(
            r"P(\text{sick}\,|\,+) = \frac{P(+\,|\,\text{sick})\,P(\text{sick})}"
            r"{P(+\,|\,\text{sick})\,P(\text{sick}) + P(+\,|\,\text{healthy})\,P(\text{healthy})}",
            font_size=22, color=YELLOW,
        ).move_to([rcol_x, -3.4, 0])
        self.play(Write(formula))
        self.wait(1.0)
