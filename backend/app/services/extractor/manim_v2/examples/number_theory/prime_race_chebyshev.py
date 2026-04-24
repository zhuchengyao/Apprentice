from manim import *
import numpy as np


def is_prime(n):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


class PrimeRaceChebyshevExample(Scene):
    """
    Chebyshev's prime-race bias (from _2023/numberphile/prime_race):
    π(x; 4, 3) leads π(x; 4, 1) most of the time despite both being
    equal in the prime-counting limit (Dirichlet). Visualize the
    gap over a range of x.

    TWO_COLUMN:
      LEFT  — running π(x; 4, 3) - π(x; 4, 1) curve; ValueTracker
              x_tr grows 0 → 10000.
      RIGHT — live counts and which one leads.
    """

    def construct(self):
        title = Tex(r"Prime race mod 4: $\pi(x; 4, 3)$ vs $\pi(x; 4, 1)$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        X_MAX = 10000
        # Precompute cumulative counts
        count_1 = 0
        count_3 = 0
        checkpoints = []  # (x, count_3 - count_1)
        step_size = 100
        for x in range(2, X_MAX + 1):
            if is_prime(x):
                if x % 4 == 1:
                    count_1 += 1
                elif x % 4 == 3:
                    count_3 += 1
            if x % step_size == 0:
                checkpoints.append((x, count_3 - count_1, count_1, count_3))

        ax = Axes(x_range=[0, X_MAX, X_MAX // 5],
                   y_range=[-5, 20, 5],
                   x_length=7, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-2.8, -0.3, 0])
        xlbl = MathTex(r"x", font_size=20).next_to(ax, DOWN, buff=0.1)
        ylbl = MathTex(r"\pi(x;4,3) - \pi(x;4,1)",
                         font_size=18).next_to(ax, LEFT, buff=0.1)
        self.play(Create(ax), Write(xlbl), Write(ylbl))

        zero_line = DashedLine(ax.c2p(0, 0), ax.c2p(X_MAX, 0),
                                 color=GREY_B, stroke_width=2)
        self.play(Create(zero_line))

        x_tr = ValueTracker(0)

        def gap_curve():
            x_cur = x_tr.get_value()
            pts = []
            for (x, d, _, _) in checkpoints:
                if x > x_cur:
                    break
                pts.append(ax.c2p(x, d))
            m = VMobject(color=YELLOW, stroke_width=3)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        def rider():
            x_cur = x_tr.get_value()
            idx = int(x_cur / step_size)
            idx = max(0, min(idx, len(checkpoints) - 1))
            x, d, _, _ = checkpoints[idx]
            return Dot(ax.c2p(x, d), color=RED, radius=0.1)

        self.add(always_redraw(gap_curve), always_redraw(rider))

        def info():
            x_cur = x_tr.get_value()
            idx = int(x_cur / step_size)
            idx = max(0, min(idx, len(checkpoints) - 1))
            x, d, c1, c3 = checkpoints[idx]
            leader = "mod 3" if d > 0 else ("mod 1" if d < 0 else "tied")
            return VGroup(
                MathTex(rf"x = {x}", color=WHITE, font_size=22),
                MathTex(rf"\pi(x; 4, 1) = {c1}",
                         color=BLUE, font_size=22),
                MathTex(rf"\pi(x; 4, 3) = {c3}",
                         color=RED, font_size=22),
                MathTex(rf"\Delta = {d}", color=YELLOW, font_size=24),
                Tex(rf"leader: {leader}",
                     color=YELLOW, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.3).shift(UP * 0.5)

        self.add(always_redraw(info))

        self.play(x_tr.animate.set_value(X_MAX),
                   run_time=9, rate_func=linear)
        self.wait(0.4)
