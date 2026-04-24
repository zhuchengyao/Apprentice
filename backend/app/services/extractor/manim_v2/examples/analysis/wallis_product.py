from manim import *
import numpy as np


class WallisProductExample(Scene):
    """
    Wallis product: partial product P_N = ∏_{n=1}^{N} (2n)²/((2n-1)(2n+1)) → π/2.

    TWO_COLUMN:
      LEFT  — Axes plotting P_N vs N. ValueTracker N sweeps 1→100 with
              an always_redraw curve growing toward the dashed π/2
              limit line.
      RIGHT — live N, partial product, π/2, gap, plus the formula
              and an alternating-product written out.

    Convergence is slow (logarithmic), so the curve climbs noticeably
    but never quite hits the line.
    """

    def construct(self):
        title = Tex(r"Wallis: $\dfrac{\pi}{2} = \prod_{n=1}^{\infty} \dfrac{(2n)^2}{(2n-1)(2n+1)}$",
                    font_size=28).to_edge(UP, buff=0.4)
        self.play(Write(title))

        target = PI / 2
        N_max = 100

        # Precompute partial products
        partials = [1.0]
        p = 1.0
        for n in range(1, N_max + 1):
            p *= (2 * n) ** 2 / ((2 * n - 1) * (2 * n + 1))
            partials.append(p)

        axes = Axes(
            x_range=[0, N_max + 5, 20], y_range=[1.0, 1.7, 0.1],
            x_length=7.0, y_length=4.4,
            axis_config={"include_tip": True, "include_numbers": True, "font_size": 18},
        ).move_to([-2.4, -0.4, 0])
        x_lbl = Tex(r"$N$", font_size=22).next_to(axes, DOWN, buff=0.1)
        y_lbl = Tex(r"$P_N$", font_size=22).next_to(axes, LEFT, buff=0.1)
        self.play(Create(axes), Write(x_lbl), Write(y_lbl))

        target_line = DashedLine(axes.c2p(0, target), axes.c2p(N_max, target),
                                 color=GREEN, stroke_width=2)
        target_lbl = MathTex(r"\pi/2", color=GREEN, font_size=22).next_to(
            axes.c2p(N_max, target), RIGHT, buff=0.05)
        self.play(Create(target_line), Write(target_lbl))

        N_tr = ValueTracker(0.0)

        def partial_curve():
            n = max(0, int(N_tr.get_value()))
            pts = [axes.c2p(k, partials[k]) for k in range(n + 1)]
            curve = VMobject(color=YELLOW, stroke_width=3)
            if len(pts) >= 2:
                curve.set_points_as_corners(pts)
            else:
                curve.set_points_as_corners([pts[0], pts[0]])
            return curve

        def head_dot():
            n = max(0, int(N_tr.get_value()))
            n = min(n, N_max)
            return Dot(axes.c2p(n, partials[n]), color=YELLOW, radius=0.10)

        self.add(always_redraw(partial_curve), always_redraw(head_dot))

        rcol_x = +4.0

        def info_panel():
            n = max(0, int(N_tr.get_value()))
            P = partials[min(n, N_max)]
            return VGroup(
                MathTex(rf"N = {n}", color=WHITE, font_size=24),
                MathTex(rf"P_N = {P:.6f}", color=YELLOW, font_size=22),
                MathTex(rf"\pi/2 = {target:.6f}", color=GREEN, font_size=22),
                MathTex(rf"\pi/2 - P_N = {target - P:+.6f}",
                        color=ORANGE, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([rcol_x, +1.4, 0])

        self.add(always_redraw(info_panel))

        expansion = MathTex(
            r"\tfrac{2 \cdot 2}{1 \cdot 3} \cdot \tfrac{4 \cdot 4}{3 \cdot 5} \cdot"
            r"\tfrac{6 \cdot 6}{5 \cdot 7} \cdots",
            color=YELLOW, font_size=24,
        ).move_to([rcol_x, -1.6, 0])
        self.play(Write(expansion))

        self.play(N_tr.animate.set_value(N_max), run_time=8, rate_func=linear)
        self.wait(1.0)
