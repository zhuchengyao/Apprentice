from manim import *
import numpy as np


class AnalyticContinuationZetaExample(Scene):
    """
    Riemann zeta: ζ(s) = Σ 1/n^s converges only for Re(s) > 1 but
    extends analytically to ℂ \ {1}. Famously ζ(-1) = -1/12.

    SINGLE_FOCUS:
      Axes over real s: BLUE series partial sum (diverges for s ≤ 1);
      ORANGE continued ζ(s) (correct for all s ≠ 1). ValueTracker
      N_tr shows divergence/convergence of partial sum; special
      values marked at s = 2, 4 (convergent) and s = -1 (ζ = -1/12).
    """

    def construct(self):
        title = Tex(r"Analytic continuation: $\zeta(s)$ beyond $\Re(s) > 1$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ax = Axes(x_range=[-3, 4, 1], y_range=[-1, 4, 1],
                   x_length=8, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-0.5, -0.3, 0])
        self.play(Create(ax))

        # Line Re(s) = 1 (pole)
        pole_line = DashedLine(ax.c2p(1, -1), ax.c2p(1, 4),
                                 color=RED, stroke_width=2)
        pole_lbl = MathTex(r"s = 1\ \text{pole}", color=RED, font_size=18
                             ).next_to(ax.c2p(1, 3.7), UR, buff=0.05)
        self.play(Create(pole_line), Write(pole_lbl))

        # Continued ζ(s) — use scipy if available, else numerical table
        def zeta_continued(s):
            # Use Python's zetaq implementation (numerical) — approximate via series for s > 1,
            # and functional equation or Euler-Maclaurin for s ≤ 1.
            # For visualization, use a hardcoded polynomial-like approximation.
            # For s > 1, series converges.
            if s > 1.05:
                return sum(1 / n ** s for n in range(1, 200))
            # For s < 1, use functional equation:
            # ζ(s) = 2^s π^(s-1) sin(πs/2) Γ(1-s) ζ(1-s)
            from math import gamma
            if abs(s - 1) < 0.05:
                return float("inf")
            return (2 ** s * PI ** (s - 1) *
                    np.sin(PI * s / 2) * gamma(1 - s) *
                    sum(1 / n ** (1 - s) for n in range(1, 200)))

        # Draw continued zeta on two sides of the pole
        cont_left = ax.plot(lambda s: min(max(zeta_continued(s), -1), 4),
                              x_range=[-2.9, 0.9, 0.03],
                              color=ORANGE, stroke_width=3)
        cont_right = ax.plot(lambda s: min(max(zeta_continued(s), -1), 4),
                               x_range=[1.1, 4, 0.03],
                               color=ORANGE, stroke_width=3)
        self.play(Create(cont_left), Create(cont_right))

        # Partial sum (diverges for s ≤ 1)
        N_tr = ValueTracker(3)

        def partial_zeta(s, N):
            return sum(1 / n ** s for n in range(1, N + 1))

        def partial_curve():
            N = int(round(N_tr.get_value()))
            N = max(1, min(N, 200))
            return ax.plot(lambda s: min(max(partial_zeta(s, N), -1), 4),
                            x_range=[-0.5, 4, 0.02],
                            color=BLUE, stroke_width=2.5)

        self.add(always_redraw(partial_curve))

        # Special value markers
        z2 = Dot(ax.c2p(2, PI ** 2 / 6), color=GREEN, radius=0.12)
        z4 = Dot(ax.c2p(4, PI ** 4 / 90), color=GREEN, radius=0.12)
        z_neg = Dot(ax.c2p(-1, -1 / 12), color=YELLOW, radius=0.12)
        z2_lbl = MathTex(r"\zeta(2) = \pi^2/6", color=GREEN, font_size=16
                           ).next_to(z2, UR, buff=0.1)
        z_neg_lbl = MathTex(r"\zeta(-1) = -1/12", color=YELLOW, font_size=16
                               ).next_to(z_neg, DOWN, buff=0.1)
        self.play(FadeIn(z2, z4, z_neg), Write(z2_lbl), Write(z_neg_lbl))

        def info():
            N = int(round(N_tr.get_value()))
            N = max(1, min(N, 200))
            return VGroup(
                MathTex(rf"N = {N}", color=BLUE, font_size=22),
                Tex(r"BLUE: partial series $\sum_{n=1}^N 1/n^s$",
                     color=BLUE, font_size=16),
                Tex(r"ORANGE: analytic $\zeta(s)$",
                     color=ORANGE, font_size=16),
                MathTex(rf"S_N(2) = {partial_zeta(2, N):.4f}",
                         color=BLUE, font_size=18),
                MathTex(rf"S_N(-1) = {partial_zeta(-1, N):.1f} \to \infty",
                         color=RED, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.13).to_edge(RIGHT, buff=0.3).shift(DOWN * 0.5)

        self.add(always_redraw(info))

        for nv in [10, 30, 80, 200]:
            self.play(N_tr.animate.set_value(nv),
                       run_time=1.5, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
