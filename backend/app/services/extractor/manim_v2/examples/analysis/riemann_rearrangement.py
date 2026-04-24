from manim import *
import numpy as np


class RiemannRearrangementExample(Scene):
    """
    Riemann rearrangement theorem: a conditionally convergent series
    can be rearranged to sum to any real. Illustrate with Σ (-1)^n/n
    = ln 2 ≈ 0.693, then rearrange (2 positive, 1 negative) to get
    (3/2) ln 2 ≈ 1.039.

    TWO_COLUMN:
      LEFT — axes showing cumulative sum of original alternating
             series.
      RIGHT — cumulative sum of rearranged series. ValueTracker N_tr
              grows N; both partial sums displayed.
    """

    def construct(self):
        title = Tex(r"Riemann: conditionally convergent $\Rightarrow$ any sum via rearrangement",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Original alternating series: (-1)^(n+1) / n for n=1,2,...
        # Sum → ln 2
        N_MAX = 100
        orig_terms = np.array([(-1) ** (n + 1) / n for n in range(1, N_MAX + 1)])
        orig_cum = np.cumsum(orig_terms)

        # Rearrangement: 2 positives then 1 negative.
        # Positives: 1, 1/3, 1/5, ...
        # Negatives: -1/2, -1/4, ...
        rearr = []
        pos_idx = 0
        neg_idx = 0
        for batch in range(N_MAX // 3 + 1):
            for _ in range(2):
                rearr.append(1 / (2 * pos_idx + 1))
                pos_idx += 1
            rearr.append(-1 / (2 * (neg_idx + 1)))
            neg_idx += 1
        rearr = np.array(rearr[:N_MAX])
        rearr_cum = np.cumsum(rearr)

        # LEFT axes
        ax_L = Axes(x_range=[0, N_MAX, 20], y_range=[0.5, 1.2, 0.1],
                     x_length=6, y_length=3.5, tips=False,
                     axis_config={"font_size": 12, "include_numbers": True}
                     ).move_to([-3.5, 0.5, 0])
        tlbl_L = Tex("original", font_size=18).next_to(ax_L, UP, buff=0.1)
        self.play(Create(ax_L), Write(tlbl_L))

        # Reference ln 2
        ln2 = DashedLine(ax_L.c2p(0, np.log(2)), ax_L.c2p(N_MAX, np.log(2)),
                           color=GREEN, stroke_width=2)
        ln2_lbl = MathTex(r"\ln 2", color=GREEN, font_size=18
                            ).next_to(ax_L.c2p(N_MAX, np.log(2)), RIGHT, buff=0.1)
        self.play(Create(ln2), Write(ln2_lbl))

        # RIGHT axes
        ax_R = Axes(x_range=[0, N_MAX, 20], y_range=[0.5, 1.2, 0.1],
                     x_length=6, y_length=3.5, tips=False,
                     axis_config={"font_size": 12, "include_numbers": True}
                     ).move_to([3.5, 0.5, 0])
        tlbl_R = Tex("rearranged (2+, 1-)", font_size=18).next_to(ax_R, UP, buff=0.1)
        self.play(Create(ax_R), Write(tlbl_R))

        # Reference (3/2) ln 2
        target_R = 1.5 * np.log(2)
        tgt_R_line = DashedLine(ax_R.c2p(0, target_R),
                                  ax_R.c2p(N_MAX, target_R),
                                  color=ORANGE, stroke_width=2)
        tgt_R_lbl = MathTex(r"\tfrac{3}{2}\ln 2", color=ORANGE, font_size=18
                              ).next_to(ax_R.c2p(N_MAX, target_R), RIGHT, buff=0.1)
        self.play(Create(tgt_R_line), Write(tgt_R_lbl))

        N_tr = ValueTracker(1)

        def curve_L():
            n = int(round(N_tr.get_value()))
            n = max(1, min(n, N_MAX))
            pts = [ax_L.c2p(k + 1, orig_cum[k]) for k in range(n)]
            m = VMobject(color=BLUE, stroke_width=2.5)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        def curve_R():
            n = int(round(N_tr.get_value()))
            n = max(1, min(n, N_MAX))
            pts = [ax_R.c2p(k + 1, rearr_cum[k]) for k in range(n)]
            m = VMobject(color=RED, stroke_width=2.5)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        self.add(always_redraw(curve_L), always_redraw(curve_R))

        def info():
            n = int(round(N_tr.get_value()))
            n = max(1, min(n, N_MAX))
            S1 = orig_cum[n - 1]
            S2 = rearr_cum[n - 1]
            return VGroup(
                MathTex(rf"N = {n}", color=WHITE, font_size=22),
                MathTex(rf"S^{{\text{{orig}}}}_N = {S1:.4f}",
                         color=BLUE, font_size=20),
                MathTex(rf"\ln 2 = {np.log(2):.4f}",
                         color=GREEN, font_size=20),
                MathTex(rf"S^{{\text{{rearr}}}}_N = {S2:.4f}",
                         color=RED, font_size=20),
                MathTex(rf"\tfrac{{3}}{{2}}\ln 2 = {1.5 * np.log(2):.4f}",
                         color=ORANGE, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        self.play(N_tr.animate.set_value(N_MAX),
                   run_time=8, rate_func=linear)
        self.wait(0.4)
