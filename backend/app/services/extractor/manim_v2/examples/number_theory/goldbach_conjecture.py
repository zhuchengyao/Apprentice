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


class GoldbachConjectureExample(Scene):
    """
    Goldbach's conjecture: every even integer > 2 is the sum of two
    primes. Show Goldbach's comet: count of decompositions for each
    even n up to 200.

    SINGLE_FOCUS:
      Scatter of (n, G(n)) where G(n) = # pairs (p, q) with p+q=n,
      p≤q, both prime. ValueTracker n_tr reveals points; visible
      "comet" shape.
    """

    def construct(self):
        title = Tex(r"Goldbach's conjecture: every even $n > 2$ = prime + prime",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        N_MAX = 200

        def G(n):
            """Count pairs (p, q) with p+q=n, p<=q, both prime."""
            count = 0
            for p in range(2, n // 2 + 1):
                if is_prime(p) and is_prime(n - p):
                    count += 1
            return count

        evens = list(range(4, N_MAX + 1, 2))
        G_vals = [G(n) for n in evens]

        ax = Axes(x_range=[0, N_MAX, 40], y_range=[0, 15, 3],
                   x_length=9, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([0, -0.3, 0])
        xl = MathTex(r"n", font_size=20).next_to(ax, DOWN, buff=0.1)
        yl = MathTex(r"G(n)", font_size=18).next_to(ax, LEFT, buff=0.1)
        self.play(Create(ax), Write(xl), Write(yl))

        n_tr = ValueTracker(4)

        def comet_points():
            n_cur = int(round(n_tr.get_value()))
            n_cur = max(4, min(n_cur, N_MAX))
            grp = VGroup()
            for n, g in zip(evens, G_vals):
                if n > n_cur:
                    break
                grp.add(Dot(ax.c2p(n, g), color=YELLOW, radius=0.04))
            return grp

        self.add(always_redraw(comet_points))

        def info():
            n_cur = int(round(n_tr.get_value()))
            n_cur = max(4, min(n_cur, N_MAX))
            # Find largest even ≤ n_cur
            largest_even = n_cur - (n_cur % 2)
            if largest_even >= 4:
                g = G(largest_even)
            else:
                g = 0
            return VGroup(
                MathTex(rf"n = {largest_even}", color=YELLOW, font_size=22),
                MathTex(rf"G(n) = {g}", color=GREEN, font_size=22),
                Tex(r"all checked up to $n = 10^{18}$",
                     color=WHITE, font_size=18),
                Tex(r"open in general (Goldbach 1742)",
                     color=ORANGE, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        self.play(n_tr.animate.set_value(N_MAX),
                   run_time=8, rate_func=linear)
        self.wait(0.4)
