from manim import *
import numpy as np


class StirlingNumbersExample(Scene):
    """
    Stirling numbers of the 2nd kind S(n, k) count partitions of n
    elements into k non-empty blocks. Relation: B_n = Σ_k S(n, k).

    SINGLE_FOCUS:
      Triangle array built row by row via ValueTracker n_tr. Each
      entry S(n, k) shown with color intensity proportional to size.
      Bottom row sum = Bell number.
    """

    def construct(self):
        title = Tex(r"Stirling S(n, k): partitions of $n$ into $k$ blocks",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Precompute S(n, k) for n = 0..6
        N_MAX = 6
        S = [[0] * (N_MAX + 1) for _ in range(N_MAX + 1)]
        S[0][0] = 1
        for n in range(1, N_MAX + 1):
            for k in range(1, n + 1):
                S[n][k] = k * S[n - 1][k] + S[n - 1][k - 1]

        dx = 1.1
        dy = 0.7
        top_y = 2.5

        n_tr = ValueTracker(0)

        def triangle_entries():
            N = int(round(n_tr.get_value()))
            N = max(0, min(N, N_MAX))
            grp = VGroup()
            for n in range(N + 1):
                row_w = n * dx
                x_start = -row_w / 2
                for k in range(n + 1):
                    x = x_start + k * dx
                    y = top_y - n * dy
                    val = S[n][k]
                    if val == 0:
                        continue
                    intensity = min(1.0, np.log(val + 1) / 5)
                    col = interpolate_color(BLUE_E, YELLOW, intensity)
                    sq = Square(side_length=0.85, color=col,
                                  fill_opacity=0.6, stroke_width=1)
                    sq.move_to([x, y, 0])
                    grp.add(sq)
                    lbl = MathTex(rf"{val}", font_size=18,
                                    color=BLACK if intensity > 0.4 else WHITE
                                    ).move_to([x, y, 0])
                    grp.add(lbl)
            return grp

        self.add(always_redraw(triangle_entries))

        def info():
            N = int(round(n_tr.get_value()))
            N = max(0, min(N, N_MAX))
            row_sum = sum(S[N][k] for k in range(N + 1))
            return VGroup(
                MathTex(rf"n = {N}", color=YELLOW, font_size=26),
                MathTex(r"S(n+1, k) = k\,S(n, k) + S(n, k-1)",
                         color=GREEN, font_size=20),
                MathTex(rf"B_n = \sum_k S(n, k) = {row_sum}",
                         color=ORANGE, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        for n in range(1, N_MAX + 1):
            self.play(n_tr.animate.set_value(n),
                       run_time=0.9, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
