from manim import *
import numpy as np


class HarmonicDivergenceExample(Scene):
    """
    The harmonic series Σ 1/n diverges logarithmically: partial sums
    grow like ln(N) + γ. Adapted from diffyq / various sources.

    TWO_COLUMN:
      LEFT  — axes plotting partial sums S_N = Σ_{n=1}^{N} 1/n
              growing with ValueTracker N_tr; compare to ln(N) + γ
              reference curve.
      RIGHT — live N, S_N, ln(N) + γ, gap S_N - ln(N) → γ.
    """

    def construct(self):
        title = Tex(r"Harmonic series diverges: $S_N \sim \ln N + \gamma$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        gamma = 0.5772

        ax = Axes(x_range=[0, 200, 40], y_range=[0, 6.5, 1],
                   x_length=7, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-2.8, -0.3, 0])
        xl = MathTex(r"N", font_size=20).next_to(ax, DOWN, buff=0.1)
        yl = MathTex(r"S_N", font_size=20).next_to(ax, LEFT, buff=0.1)
        self.play(Create(ax), Write(xl), Write(yl))

        # ln(N) + γ reference
        ref_curve = ax.plot(lambda n: np.log(n) + gamma if n > 0 else 0,
                              x_range=[1, 200, 0.5],
                              color=GREEN, stroke_width=2.5,
                              stroke_opacity=0.7)
        ref_lbl = MathTex(r"\ln N + \gamma",
                            color=GREEN, font_size=22
                            ).next_to(ax.c2p(160, np.log(160) + gamma),
                                        UP, buff=0.1)
        self.play(Create(ref_curve), Write(ref_lbl))

        N_tr = ValueTracker(1)

        # Precompute partial sums
        N_max = 200
        partials = np.cumsum(1.0 / np.arange(1, N_max + 1))

        def partial_curve():
            N = int(round(N_tr.get_value()))
            N = max(1, min(N, N_max))
            pts = []
            for n in range(1, N + 1):
                pts.append(ax.c2p(n, partials[n - 1]))
            m = VMobject(color=YELLOW, stroke_width=3)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        def rider():
            N = int(round(N_tr.get_value()))
            N = max(1, min(N, N_max))
            return Dot(ax.c2p(N, partials[N - 1]),
                        color=RED, radius=0.1)

        self.add(always_redraw(partial_curve), always_redraw(rider))

        def info():
            N = int(round(N_tr.get_value()))
            N = max(1, min(N, N_max))
            S_N = partials[N - 1]
            ln_N = np.log(N) + gamma if N > 0 else 0
            gap = S_N - np.log(N) if N > 0 else 0
            return VGroup(
                MathTex(rf"N = {N}", color=WHITE, font_size=22),
                MathTex(rf"S_N = {S_N:.4f}",
                         color=YELLOW, font_size=22),
                MathTex(rf"\ln N + \gamma = {ln_N:.4f}",
                         color=GREEN, font_size=22),
                MathTex(rf"S_N - \ln N = {gap:.4f}",
                         color=RED, font_size=22),
                MathTex(rf"\to \gamma = {gamma}",
                         color=ORANGE, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([4.3, 0.0, 0])

        self.add(always_redraw(info))

        self.play(N_tr.animate.set_value(N_max),
                   run_time=9, rate_func=linear)
        self.wait(0.4)
