from manim import *
import numpy as np


class BayesDiseaseProportionsExample(Scene):
    """
    Bayesian update for a disease test: P(D|+) = (P(+|D) P(D)) /
    (P(+|D) P(D) + P(+|¬D) P(¬D)). ValueTracker prior_tr sweeps
    prior P(D) from 0.1% → 20%; unit square recolors showing the
    4 outcome regions; posterior P(D|+) plotted.

    TWO_COLUMN:
      LEFT  — unit square split into 4 regions (TP, FN, FP, TN) by
              two ValueTrackers prior_tr and sens=0.99, spec=0.95.
              Sizes update via always_redraw.
      RIGHT — live prior, P(+), posterior, and a small posterior-
              vs-prior plot with a cursor.
    """

    def construct(self):
        title = Tex(r"Bayesian disease test: $P(D \mid +)$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Unit square area: 4 cells arranged as [D, +] [D, -] [¬D, +] [¬D, -]
        sq_center = np.array([-3.5, -0.5, 0])
        W, H = 3.0, 3.0
        sens = 0.99
        spec = 0.95

        prior_tr = ValueTracker(0.01)

        def outer_box():
            return Rectangle(width=W, height=H, color=WHITE,
                              stroke_width=2, fill_opacity=0
                              ).move_to(sq_center)

        def cells():
            p = prior_tr.get_value()
            # Left column: D (width = W * p)
            # Right column: ¬D (width = W * (1-p))
            # Top row: + (height ∝ conditional)
            # Bottom row: -
            d_w = W * p
            nd_w = W * (1 - p)
            tp_h = H * sens
            fn_h = H * (1 - sens)
            fp_h = H * (1 - spec)
            tn_h = H * spec
            x_left = sq_center[0] - W / 2
            y_top = sq_center[1] + H / 2
            grp = VGroup()
            # TP (top-left)
            tp = Rectangle(width=d_w, height=tp_h, color=RED,
                            fill_opacity=0.6, stroke_width=1
                            ).move_to(np.array([x_left + d_w / 2,
                                                   y_top - tp_h / 2, 0]))
            grp.add(tp)
            # FN (bottom-left, height fn_h = H * (1 - sens))
            fn = Rectangle(width=d_w, height=fn_h, color=ORANGE,
                            fill_opacity=0.6, stroke_width=1
                            ).move_to(np.array([x_left + d_w / 2,
                                                   y_top - tp_h - fn_h / 2, 0]))
            grp.add(fn)
            # FP (top-right, height fp_h = H * (1 - spec))
            fp = Rectangle(width=nd_w, height=fp_h, color=YELLOW,
                            fill_opacity=0.6, stroke_width=1
                            ).move_to(np.array([x_left + d_w + nd_w / 2,
                                                   y_top - fp_h / 2, 0]))
            grp.add(fp)
            # TN (bottom-right, height tn_h = H * spec)
            tn = Rectangle(width=nd_w, height=tn_h, color=GREEN,
                            fill_opacity=0.6, stroke_width=1
                            ).move_to(np.array([x_left + d_w + nd_w / 2,
                                                   y_top - fp_h - tn_h / 2, 0]))
            grp.add(tn)
            return grp

        self.add(outer_box(), always_redraw(cells))

        def info():
            p = prior_tr.get_value()
            p_plus = sens * p + (1 - spec) * (1 - p)
            post = (sens * p) / p_plus if p_plus > 0 else 0.0
            return VGroup(
                MathTex(rf"P(D) = {p:.4f}", color=WHITE, font_size=22),
                MathTex(rf"P(+\mid D) = {sens:.2f}",
                         color=RED, font_size=22),
                MathTex(rf"P(-\mid \lnot D) = {spec:.2f}",
                         color=GREEN, font_size=22),
                MathTex(rf"P(+) = {p_plus:.4f}", color=YELLOW, font_size=22),
                MathTex(rf"P(D\mid +) = {post:.4f}",
                         color=ORANGE, font_size=24),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.5, 0.8, 0])

        self.add(always_redraw(info))

        # Small posterior vs prior plot
        ax = Axes(x_range=[0, 0.25, 0.05], y_range=[0, 1, 0.25],
                   x_length=3.2, y_length=2.0, tips=False,
                   axis_config={"font_size": 14}
                   ).move_to([3.5, -2.4, 0])

        def post_curve():
            return ax.plot(lambda p: sens * p / (sens * p + (1 - spec) * (1 - p)),
                            x_range=[0.001, 0.25, 0.005],
                            color=ORANGE, stroke_width=3)

        def cursor_dot():
            p = prior_tr.get_value()
            p_plus = sens * p + (1 - spec) * (1 - p)
            post = (sens * p) / p_plus if p_plus > 0 else 0.0
            return Dot(ax.c2p(min(p, 0.25), post),
                        color=YELLOW, radius=0.08)

        self.play(Create(ax), Create(post_curve()))
        self.add(always_redraw(cursor_dot))

        self.play(prior_tr.animate.set_value(0.20),
                   run_time=8, rate_func=linear)
        self.wait(0.5)
