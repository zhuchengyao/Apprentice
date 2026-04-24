from manim import *
import numpy as np


class LeibnizPiFormulaExample(Scene):
    """
    Leibniz partial sums approach π/4 — slowly.

    TWO_COLUMN:
      LEFT  — Axes plotting partial sum S_N = Σ_{k=0}^{N-1} (-1)^k / (2k+1)
              against N, with horizontal dashed line at π/4. ValueTracker
              N sweeps; an always_redraw growing curve traces the partial
              sums. The classic alternating zigzag around π/4 is visible.
      RIGHT — live N, partial sum value, gap π/4 - S_N, plus the formula.
    """

    def construct(self):
        title = Tex(r"Leibniz: $\dfrac{\pi}{4} = 1 - \dfrac{1}{3} + \dfrac{1}{5} - \dfrac{1}{7} + \cdots$",
                    font_size=28).to_edge(UP, buff=0.4)
        self.play(Write(title))

        target = PI / 4
        N_max = 200

        # Precompute partial sums
        partials = []
        s = 0.0
        for k in range(N_max + 1):
            s += (-1) ** k / (2 * k + 1)
            partials.append(s)

        axes = Axes(
            x_range=[0, N_max + 5, 50], y_range=[0.6, 1.0, 0.1],
            x_length=7.0, y_length=4.4,
            axis_config={"include_tip": True, "include_numbers": True, "font_size": 18},
        ).move_to([-2.6, -0.4, 0])
        x_lbl = Tex(r"$N$", font_size=22).next_to(axes, DOWN, buff=0.1)
        y_lbl = Tex(r"$S_N$", font_size=22).next_to(axes, LEFT, buff=0.1)
        self.play(Create(axes), Write(x_lbl), Write(y_lbl))

        # Target line
        target_line = DashedLine(axes.c2p(0, target), axes.c2p(N_max, target),
                                 color=GREEN, stroke_width=2)
        target_lbl = MathTex(r"\pi/4", color=GREEN, font_size=22).next_to(
            axes.c2p(N_max, target), RIGHT, buff=0.1)
        self.play(Create(target_line), Write(target_lbl))

        N_tr = ValueTracker(1.0)

        def partial_curve():
            n_max = max(1, int(N_tr.get_value()))
            pts = [axes.c2p(k, partials[k]) for k in range(1, n_max + 1)]
            curve = VMobject(color=YELLOW, stroke_width=2)
            if len(pts) >= 2:
                curve.set_points_as_corners(pts)
            else:
                curve.set_points_as_corners([pts[0], pts[0]])
            return curve

        def head_dot():
            n = int(N_tr.get_value())
            n = max(1, min(n, N_max))
            return Dot(axes.c2p(n, partials[n]), color=YELLOW, radius=0.09)

        self.add(always_redraw(partial_curve), always_redraw(head_dot))

        # RIGHT COLUMN
        rcol_x = +4.0

        def info_panel():
            n = max(1, int(N_tr.get_value()))
            s = partials[min(n, N_max)]
            gap = target - s
            return VGroup(
                MathTex(rf"N = {n}", color=WHITE, font_size=26),
                MathTex(rf"S_N = {s:.6f}", color=YELLOW, font_size=24),
                MathTex(rf"\pi/4 = {target:.6f}", color=GREEN, font_size=24),
                MathTex(rf"\pi/4 - S_N = {gap:+.6f}",
                        color=ORANGE, font_size=22),
                MathTex(r"|{\rm gap}| < \frac{1}{2N+1}",
                        color=GREY_B, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([rcol_x, +1.2, 0])

        self.add(always_redraw(info_panel))

        formula = MathTex(
            r"\frac{\pi}{4} = \sum_{k=0}^{\infty} \frac{(-1)^k}{2k+1}",
            color=YELLOW, font_size=28,
        ).move_to([rcol_x, -2.4, 0])
        self.play(Write(formula))

        self.play(N_tr.animate.set_value(N_max), run_time=8, rate_func=linear)
        self.wait(1.0)
