from manim import *
import numpy as np


class ContinuedFractionsSqrtExample(Scene):
    """
    Continued fraction expansion of √N is eventually periodic.
    Example √23 = [4; 1, 3, 1, 8, 1, 3, 1, 8, ...] with period 4.

    TWO_COLUMN: LEFT axes show convergents p_k/q_k (YELLOW dots) approaching √23 (dashed RED line). ValueTracker k_tr advances
    index; always_redraw partial path + current p_k/q_k live readout.
    RIGHT shows the expansion [4; 1, 3, 1, 8, ...] with active index
    highlighted GREEN; live |p_k/q_k − √23| shrinks.
    """

    def construct(self):
        title = Tex(r"Continued fraction: $\sqrt{23}=[4;\overline{1,3,1,8}]$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Compute CF and convergents
        N = 23
        a = [4, 1, 3, 1, 8, 1, 3, 1, 8, 1, 3, 1, 8, 1, 3, 1, 8]  # more terms
        # convergents p/q via recursion
        p = [1, a[0]]
        q = [0, 1]
        for k in range(1, len(a)):
            p.append(a[k] * p[-1] + p[-2])
            q.append(a[k] * q[-1] + q[-2])
        p = p[1:]  # drop leading seed
        q = q[1:]
        convs = [pi / qi for pi, qi in zip(p, q)]

        axes = Axes(x_range=[0, len(a), 2], y_range=[4.65, 4.90, 0.05],
                    x_length=5.5, y_length=3.6,
                    axis_config={"include_numbers": True,
                                 "font_size": 18}).shift(LEFT * 2.5 + DOWN * 0.2)
        self.play(Create(axes))

        # Horizontal dashed line at √23
        true_val = np.sqrt(N)
        hline = DashedLine(axes.c2p(0, true_val), axes.c2p(len(a), true_val),
                           color=RED, stroke_width=2)
        hline_lbl = Tex(r"$\sqrt{23}\approx 4.7958$", color=RED, font_size=22).next_to(
            hline, UR, buff=0.1)
        self.play(Create(hline), Write(hline_lbl))

        k_tr = ValueTracker(0.0)

        def conv_dots():
            k = int(round(k_tr.get_value()))
            k = max(0, min(len(a) - 1, k))
            dots = VGroup()
            for i in range(k + 1):
                dots.add(Dot(axes.c2p(i + 1, convs[i]),
                              color=YELLOW, radius=0.08))
            return dots

        def conv_path():
            k = int(round(k_tr.get_value()))
            k = max(1, min(len(a) - 1, k))
            pts = [axes.c2p(i + 1, convs[i]) for i in range(k + 1)]
            return VMobject().set_points_as_corners(pts).set_color(YELLOW).set_stroke(width=2.5)

        self.add(always_redraw(conv_dots), always_redraw(conv_path))

        # Right column: expansion strip
        exp_label = Tex(r"$\sqrt{23}=$", font_size=22)
        exp_terms = VGroup(*[
            Tex(str(a[i]), font_size=22, color=GREY_B)
            for i in range(10)
        ]).arrange(RIGHT, buff=0.25)
        expansion = VGroup(exp_label, exp_terms).arrange(RIGHT, buff=0.3).to_edge(RIGHT, buff=0.3).shift(UP * 1.5)
        self.play(Write(expansion))

        def highlight_term():
            k = int(round(k_tr.get_value()))
            k = max(0, min(9, k))
            grp = VGroup()
            for i, t in enumerate(exp_terms):
                if i == k:
                    grp.add(Square(side_length=0.5, color=GREEN,
                                   stroke_width=2, fill_opacity=0.15).move_to(t.get_center()))
            return grp
        self.add(always_redraw(highlight_term))

        def k_now():
            return max(0, min(len(a) - 1, int(round(k_tr.get_value()))))

        info = VGroup(
            VGroup(Tex(r"$k=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$p_k=$", font_size=22),
                   DecimalNumber(4, num_decimal_places=0,
                                 font_size=22)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$q_k=$", font_size=22),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=22)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$p_k/q_k=$", font_size=22),
                   DecimalNumber(4.0, num_decimal_places=6,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$|p_k/q_k-\sqrt{23}|=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=7,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.2).shift(DOWN * 1.3)

        info[0][1].add_updater(lambda m: m.set_value(k_now()))
        info[1][1].add_updater(lambda m: m.set_value(p[k_now()]))
        info[2][1].add_updater(lambda m: m.set_value(q[k_now()]))
        info[3][1].add_updater(lambda m: m.set_value(convs[k_now()]))
        info[4][1].add_updater(lambda m: m.set_value(abs(convs[k_now()] - true_val)))
        self.add(info)

        self.play(k_tr.animate.set_value(9.0),
                  run_time=6, rate_func=linear)
        self.wait(0.8)
