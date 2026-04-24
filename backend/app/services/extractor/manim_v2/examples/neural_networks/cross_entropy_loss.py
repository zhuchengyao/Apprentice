from manim import *
import numpy as np


class CrossEntropyLossExample(Scene):
    """
    Cross-entropy loss for classification:
        L = −Σ_i y_i log p_i
    where y is one-hot true label and p is predicted distribution.

    TWO_COLUMN: LEFT shows predicted p over 5 classes (bars) vs
    true one-hot (star markers). ValueTracker conf_tr moves probability
    toward the correct class; always_redraw rebuilds bars + current
    CE loss curve. RIGHT plots CE vs confidence of correct class.
    """

    def construct(self):
        title = Tex(r"Cross-entropy: $L=-\sum y_i\log p_i$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # 5 classes, true label = class 2
        n_classes = 5
        true_label = 2

        axes = Axes(x_range=[0, n_classes + 0.5, 1], y_range=[0, 1.0, 0.2],
                    x_length=5.0, y_length=3.5,
                    axis_config={"include_numbers": False}).shift(LEFT * 3.2 + DOWN * 0.3)
        self.play(Create(axes))

        # True label marker
        star = Star(n=5, color=YELLOW, fill_color=YELLOW,
                     fill_opacity=0.8).scale(0.18).move_to(axes.c2p(true_label + 1, 1.05))
        self.add(star)

        p_tr = ValueTracker(0.2)

        def probs():
            # Correct class prob = p_tr, others share remainder
            p_true = p_tr.get_value()
            p_other = (1 - p_true) / (n_classes - 1)
            p = [p_other] * n_classes
            p[true_label] = p_true
            return np.array(p)

        colors = [BLUE, GREEN, ORANGE, RED, PURPLE]

        def bars():
            p = probs()
            grp = VGroup()
            for i in range(n_classes):
                rect = Rectangle(width=0.55,
                                 height=p[i] * axes.y_length / 1.0,
                                 color=colors[i],
                                 fill_color=colors[i],
                                 fill_opacity=0.7)
                rect.move_to(axes.c2p(i + 1, p[i] / 2))
                grp.add(rect)
            return grp

        self.add(always_redraw(bars))

        # RIGHT: CE plot vs p_true
        ax_right = Axes(x_range=[0, 1.05, 0.2], y_range=[0, 4, 1],
                        x_length=4.8, y_length=3.5,
                        axis_config={"include_numbers": True,
                                     "font_size": 16}).shift(RIGHT * 3.0 + DOWN * 0.3)
        self.add(ax_right)

        ce_curve = ax_right.plot(lambda p: -np.log(p) if p > 0.005 else 5,
                                  x_range=[0.01, 1], color=BLUE, stroke_width=3)
        self.add(ce_curve)

        def ce_dot():
            p = p_tr.get_value()
            ce_val = -np.log(p) if p > 0.01 else 5
            return Dot(ax_right.c2p(p, min(4, ce_val)),
                        color=RED, radius=0.1)

        self.add(always_redraw(ce_dot))

        # Info
        def ce_val():
            p = probs()
            return float(-np.log(p[true_label]))

        info = VGroup(
            VGroup(Tex(r"$p_{\rm true}=$", color=ORANGE, font_size=22),
                   DecimalNumber(0.2, num_decimal_places=3,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$L=-\log p_{\rm true}=$", font_size=22),
                   DecimalNumber(1.609, num_decimal_places=4,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
            Tex(r"$L\to 0$ as $p_{\rm true}\to 1$",
                color=GREEN, font_size=20),
            Tex(r"$L\to\infty$ as $p_{\rm true}\to 0$",
                color=RED, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(p_tr.get_value()))
        info[1][1].add_updater(lambda m: m.set_value(ce_val()))
        self.add(info)

        for pval in [0.5, 0.8, 0.95, 0.05, 0.2]:
            self.play(p_tr.animate.set_value(pval),
                      run_time=1.8, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.5)
