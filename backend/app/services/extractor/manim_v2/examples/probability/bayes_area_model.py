from manim import *
import numpy as np


class BayesAreaModelExample(Scene):
    """
    Bayes via area model (from _2018/eop/chapter1/area_model_bayes):
    a 100-dot grid partitioned by prior P(H) and likelihood P(E|H);
    posterior P(H|E) = area of (H ∩ E) / area of E.

    SINGLE_FOCUS:
      10×10 dot grid; ValueTracker prior_tr slides prior boundary
      1% → 50%; always_redraw recolors cells: BLUE=H∩E (TP),
      YELLOW=H∩¬E (FN), RED=¬H∩E (FP), GREY=¬H∩¬E (TN). Live
      posterior panel.
    """

    def construct(self):
        title = Tex(r"Bayes by area: $P(H|E) = \dfrac{P(H \cap E)}{P(E)}$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # 10×10 grid
        rows, cols = 10, 10
        dx = 0.55
        origin = np.array([-dx * 4.5, -dx * 4.5 + 0.3, 0])

        # Likelihoods: sens = 0.9, fpr = 0.2
        sens = 0.9
        fpr = 0.2

        prior_tr = ValueTracker(0.10)

        def cells():
            p = prior_tr.get_value()
            grp = VGroup()
            # Split grid: leftmost 100*p columns are H, rest are ¬H
            h_cols = p * cols
            for r in range(rows):
                for c in range(cols):
                    x = origin[0] + c * dx
                    y = origin[1] + r * dx
                    # Is this cell in H?
                    in_H = (c + 0.5) < h_cols
                    # In E (given H or ¬H)?
                    if in_H:
                        # Top sens fraction of this column in E
                        in_E = (r + 0.5) / rows > (1 - sens)
                    else:
                        # Top fpr fraction
                        in_E = (r + 0.5) / rows > (1 - fpr)

                    if in_H and in_E:
                        color = BLUE  # TP
                    elif in_H and not in_E:
                        color = YELLOW  # FN
                    elif not in_H and in_E:
                        color = RED  # FP
                    else:
                        color = GREY_B  # TN

                    sq = Square(side_length=dx * 0.9,
                                 color=color, fill_opacity=0.7,
                                 stroke_width=0.5)
                    sq.move_to([x, y, 0])
                    grp.add(sq)
            return grp

        self.add(always_redraw(cells))

        # Legend
        legend = VGroup(
            Tex(r"BLUE: $H \cap E$ (TP)", color=BLUE, font_size=20),
            Tex(r"YELLOW: $H \cap \neg E$ (FN)", color=YELLOW, font_size=20),
            Tex(r"RED: $\neg H \cap E$ (FP)", color=RED, font_size=20),
            Tex(r"GREY: $\neg H \cap \neg E$ (TN)", color=GREY_B, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(RIGHT, buff=0.3).shift(UP * 1.3)
        self.play(Write(legend))

        def info():
            p = prior_tr.get_value()
            p_e = sens * p + fpr * (1 - p)
            post = sens * p / p_e if p_e > 0 else 0
            return VGroup(
                MathTex(rf"P(H) = {p:.3f}", color=WHITE, font_size=22),
                MathTex(rf"P(E|H) = {sens}", color=BLUE, font_size=20),
                MathTex(rf"P(E|\neg H) = {fpr}", color=RED, font_size=20),
                MathTex(rf"P(E) = {p_e:.3f}", color=YELLOW, font_size=20),
                MathTex(rf"P(H|E) = {post:.4f}",
                         color=GREEN, font_size=24),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.3).shift(DOWN * 1.4)

        self.add(always_redraw(info))

        self.play(prior_tr.animate.set_value(0.01),
                   run_time=3, rate_func=smooth)
        self.play(prior_tr.animate.set_value(0.5),
                   run_time=4, rate_func=smooth)
        self.play(prior_tr.animate.set_value(0.1),
                   run_time=2, rate_func=smooth)
        self.wait(0.5)
