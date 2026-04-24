from manim import *
import numpy as np


class GeometricSeriesFormulaExample(Scene):
    """
    Geometric series sum: vary r and watch the partial sums and limit.

    TWO_COLUMN:
      LEFT  — Axes plotting partial sums S_N = (1 − r^(N+1))/(1−r) as N
              grows; horizontal dashed limit line at 1/(1-r). For
              |r| < 1 the curve approaches the limit; for r = 0.5
              the limit is 2; for r = -0.5 the limit is 2/3 with
              alternating zigzag; for r = 0.9 it climbs slowly toward 10.
      RIGHT — live r, S_N, limit, gap.

    Three phases — sweep N to 30 at r=0.5, then morph r to -0.5 and
    sweep again, then to 0.9.
    """

    def construct(self):
        title = Tex(r"Geometric series: $\sum_{n=0}^{\infty} r^n = \dfrac{1}{1-r}$ for $|r| < 1$",
                    font_size=26).to_edge(UP, buff=0.4)
        self.play(Write(title))

        N_max = 30

        axes = Axes(
            x_range=[0, N_max + 1, 5], y_range=[-2, 11, 2],
            x_length=7.2, y_length=4.8,
            axis_config={"include_tip": True, "include_numbers": True, "font_size": 18},
        ).move_to([-2.4, -0.4, 0])
        x_lbl = Tex(r"$N$", font_size=22).next_to(axes, DOWN, buff=0.1)
        y_lbl = Tex(r"$S_N$", font_size=22).next_to(axes, LEFT, buff=0.1)
        self.play(Create(axes), Write(x_lbl), Write(y_lbl))

        r_tr = ValueTracker(0.5)
        N_tr = ValueTracker(0.0)

        def partial_sum(r, N):
            if abs(r - 1) < 1e-9:
                return float(N + 1)
            return (1 - r ** (N + 1)) / (1 - r)

        def limit(r):
            if abs(r) >= 1:
                return float('inf')
            return 1 / (1 - r)

        def partial_curve():
            r = r_tr.get_value()
            n_max = max(0, int(N_tr.get_value()))
            pts = [axes.c2p(k, partial_sum(r, k)) for k in range(n_max + 1)]
            curve = VMobject(color=YELLOW, stroke_width=3)
            if len(pts) >= 2:
                curve.set_points_as_corners(pts)
            else:
                curve.set_points_as_corners([pts[0], pts[0]])
            return curve

        def head_dot():
            r = r_tr.get_value()
            n = max(0, int(N_tr.get_value()))
            return Dot(axes.c2p(n, partial_sum(r, n)),
                       color=YELLOW, radius=0.10)

        def limit_line():
            L = limit(r_tr.get_value())
            if not np.isfinite(L) or L < -1.5 or L > 10.5:
                return DashedLine([0, 0, 0], [0, 0, 0],
                                  color=BLACK, stroke_width=0.001)
            return DashedLine(axes.c2p(0, L), axes.c2p(N_max, L),
                              color=GREEN, stroke_width=2)

        def limit_lbl():
            L = limit(r_tr.get_value())
            if not np.isfinite(L) or L < -1.5 or L > 10.5:
                return MathTex(r"", color=BLACK, font_size=1)
            return MathTex(rf"\tfrac{{1}}{{1-r}} = {L:.3f}",
                           color=GREEN, font_size=22).next_to(
                axes.c2p(N_max, L), RIGHT, buff=0.05)

        self.add(always_redraw(limit_line), always_redraw(limit_lbl),
                 always_redraw(partial_curve), always_redraw(head_dot))

        # RIGHT COLUMN
        rcol_x = +4.4

        def info_panel():
            r = r_tr.get_value()
            n = max(0, int(N_tr.get_value()))
            S = partial_sum(r, n)
            L = limit(r)
            return VGroup(
                MathTex(rf"r = {r:+.2f}", color=WHITE, font_size=26),
                MathTex(rf"N = {n}", color=WHITE, font_size=24),
                MathTex(rf"S_N = {S:+.4f}", color=YELLOW, font_size=22),
                MathTex(rf"\tfrac{{1}}{{1-r}} = {L:+.4f}",
                        color=GREEN, font_size=22),
                MathTex(rf"\text{{gap}} = {L - S:+.4f}",
                        color=ORANGE, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([rcol_x, +0.4, 0])

        self.add(always_redraw(info_panel))

        # Phase 1: r=0.5, sweep N
        self.play(N_tr.animate.set_value(N_max), run_time=4, rate_func=linear)
        self.wait(0.4)

        # Phase 2: morph r to -0.5
        N_tr.set_value(0.0)
        self.play(r_tr.animate.set_value(-0.5),
                  N_tr.animate.set_value(N_max),
                  run_time=4, rate_func=linear)
        self.wait(0.4)

        # Phase 3: morph r to 0.9 (slower convergence)
        N_tr.set_value(0.0)
        self.play(r_tr.animate.set_value(0.9),
                  N_tr.animate.set_value(N_max),
                  run_time=5, rate_func=linear)
        self.wait(1.0)
