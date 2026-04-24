from manim import *
import numpy as np


class StirlingSecondKindExample(Scene):
    """
    Stirling numbers of the 2nd kind S(n, k): number of ways to
    partition an n-element set into k non-empty subsets.
    Recurrence: S(n, k) = k·S(n-1, k) + S(n-1, k-1).

    SINGLE_FOCUS: Stirling triangle for n=1..7, k=1..7 as cell grid;
    ValueTracker reveals rows one by one.
    """

    def construct(self):
        title = Tex(r"Stirling 2nd kind: $S(n,k)=k\,S(n-1,k)+S(n-1,k-1)$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        N = 7
        cell_s = 0.7

        # Compute Stirling numbers
        S = [[0] * (N + 1) for _ in range(N + 1)]
        S[0][0] = 1
        for n in range(1, N + 1):
            for k in range(1, n + 1):
                S[n][k] = k * S[n - 1][k] + S[n - 1][k - 1]

        origin = np.array([-3.5, 2.2, 0])

        n_tr = ValueTracker(1.0)

        def n_now():
            return max(1, min(N, int(round(n_tr.get_value()))))

        def triangle():
            nmax = n_now()
            grp = VGroup()
            for n in range(1, nmax + 1):
                for k in range(1, n + 1):
                    val = S[n][k]
                    pos = origin + RIGHT * (k - 1) * cell_s - DOWN * (n - 1) * cell_s
                    col = interpolate_color(BLUE, YELLOW, min(1, np.log10(val + 1) / 3))
                    cell = Square(side_length=cell_s * 0.9,
                                   color=col, stroke_width=1,
                                   fill_color=col, fill_opacity=0.5).move_to(pos)
                    lbl = Tex(str(val), font_size=18).move_to(pos)
                    grp.add(cell, lbl)
                # n, k labels
                grp.add(Tex(rf"$n={n}$", font_size=16, color=BLUE).move_to(
                    origin + LEFT * cell_s - DOWN * (n - 1) * cell_s))
            return grp

        self.add(always_redraw(triangle))

        # Column headers (once)
        for k in range(1, N + 1):
            self.add(Tex(rf"$k={k}$", font_size=16, color=GREEN).move_to(
                origin + RIGHT * (k - 1) * cell_s - DOWN * (-1) * cell_s))

        # Special values
        info = VGroup(
            VGroup(Tex(r"up to $n=$", font_size=22),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$S(n,1)=1$ always", color=BLUE, font_size=20),
                    ).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$S(n,n)=1$ always", color=BLUE, font_size=20),
                    ).arrange(RIGHT, buff=0.1),
            Tex(r"Bell $B_n = \sum_k S(n,k)$",
                color=GREEN, font_size=20),
            VGroup(Tex(r"$B_n=$", font_size=20),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=20).set_color(GREEN)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(DR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(n_now()))
        info[4][1].add_updater(lambda m: m.set_value(sum(S[n_now()][k] for k in range(1, n_now() + 1))))
        self.add(info)

        for n in range(2, N + 1):
            self.play(n_tr.animate.set_value(float(n)),
                      run_time=0.9, rate_func=smooth)
            self.wait(0.3)
        self.wait(0.5)
