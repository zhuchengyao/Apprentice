from manim import *
import numpy as np


class BanachFixedPointExample(Scene):
    """
    Banach fixed-point theorem: if T: X → X is a contraction on a
    complete metric space (|T(x) - T(y)| ≤ k|x - y|, k < 1), then T
    has a unique fixed point, reached by iteration from any start.

    TWO_COLUMN:
      LEFT  — axes with y = T(x) = 0.7 x + 0.3 (a contraction with
              fixed point x* = 1); ValueTracker step_tr applies T
              iteratively from x_0 = 3.5; cobweb plot.
      RIGHT — live iterates and convergence.
    """

    def construct(self):
        title = Tex(r"Banach fixed-point: iteration converges at rate $k < 1$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        k = 0.7
        b = 0.3
        fixed = b / (1 - k)  # = 1.0

        def T(x):
            return k * x + b

        ax = Axes(x_range=[0, 4, 1], y_range=[0, 4, 1],
                   x_length=5.5, y_length=5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-3.2, -0.3, 0])
        self.play(Create(ax))

        # y = x line (identity)
        identity = ax.plot(lambda x: x, x_range=[0, 4],
                             color=GREY_B, stroke_width=2)
        # y = T(x) line
        T_line = ax.plot(T, x_range=[0, 4],
                           color=BLUE, stroke_width=3)
        self.play(Create(identity), Create(T_line))

        # Fixed point
        fp_dot = Dot(ax.c2p(fixed, fixed), color=RED, radius=0.12)
        fp_lbl = MathTex(r"x^* = 1", color=RED, font_size=22
                           ).next_to(fp_dot, UR, buff=0.1)
        self.play(FadeIn(fp_dot), Write(fp_lbl))

        x_0 = 3.5
        # Precompute iterates
        iterates = [x_0]
        for _ in range(15):
            iterates.append(T(iterates[-1]))

        step_tr = ValueTracker(0)

        def cobweb():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, 15))
            pts = [ax.c2p(iterates[0], 0)]
            for i in range(s):
                x = iterates[i]
                y = iterates[i + 1]  # = T(x)
                pts.append(ax.c2p(x, y))
                pts.append(ax.c2p(y, y))
            m = VMobject(color=YELLOW, stroke_width=2.5)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        def rider():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, 15))
            return Dot(ax.c2p(iterates[s], iterates[s]),
                        color=ORANGE, radius=0.1)

        self.add(always_redraw(cobweb), always_redraw(rider))

        def info():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, 15))
            x_s = iterates[s]
            err = abs(x_s - fixed)
            return VGroup(
                MathTex(rf"n = {s}", color=WHITE, font_size=22),
                MathTex(rf"x_n = {x_s:.6f}",
                         color=YELLOW, font_size=22),
                MathTex(rf"|x_n - x^*| = {err:.4f}",
                         color=RED, font_size=22),
                MathTex(rf"\le k^n |x_0 - x^*| = {k ** s * abs(x_0 - fixed):.4f}",
                         color=GREEN, font_size=20),
                Tex(r"geometric convergence",
                     color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for s in [1, 2, 4, 8, 15]:
            self.play(step_tr.animate.set_value(s),
                       run_time=1.3, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
