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


class DirichletAPPrimesExample(Scene):
    """
    Dirichlet's theorem: for gcd(a, d) = 1, there are infinitely
    many primes in the AP a + nd. Visualize with AP 1 mod 4 and
    3 mod 4 up to 200.

    TWO_COLUMN:
      LEFT  — number line 0..200 with primes marked; ValueTracker
              N_tr advances; colored by residue class 1 mod 4 (GREEN)
              or 3 mod 4 (RED).
      RIGHT — running counts π(N; 4, 1) vs π(N; 4, 3) (both grow
              without bound, slight Chebyshev bias).
    """

    def construct(self):
        title = Tex(r"Dirichlet: primes in AP $\{4n+1\}$ and $\{4n+3\}$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        N_MAX = 200

        primes_1 = [n for n in range(2, N_MAX + 1) if is_prime(n) and n % 4 == 1]
        primes_3 = [n for n in range(2, N_MAX + 1) if is_prime(n) and n % 4 == 3]

        # Precompute cumulative counts
        cum_1 = np.zeros(N_MAX + 1, dtype=int)
        cum_3 = np.zeros(N_MAX + 1, dtype=int)
        for i in range(1, N_MAX + 1):
            cum_1[i] = cum_1[i - 1] + (i % 4 == 1 and is_prime(i))
            cum_3[i] = cum_3[i - 1] + (i % 4 == 3 and is_prime(i))

        nl = NumberLine(x_range=[0, N_MAX, 50], length=6,
                         include_numbers=True,
                         decimal_number_config={"num_decimal_places": 0,
                                                 "font_size": 12}
                         ).move_to([-3.5, -0.5, 0])
        self.play(Create(nl))

        N_tr = ValueTracker(0)

        def prime_marks():
            N = int(round(N_tr.get_value()))
            N = max(0, min(N, N_MAX))
            grp = VGroup()
            for p in primes_1:
                if p > N:
                    break
                grp.add(Dot(nl.n2p(p), color=GREEN, radius=0.05))
            for p in primes_3:
                if p > N:
                    break
                grp.add(Dot(nl.n2p(p), color=RED, radius=0.05))
            return grp

        self.add(always_redraw(prime_marks))

        # RIGHT: running counts
        ax = Axes(x_range=[0, N_MAX, 50], y_range=[0, 25, 5],
                   x_length=5.5, y_length=4, tips=False,
                   axis_config={"font_size": 12, "include_numbers": True}
                   ).move_to([3, 0, 0])
        xl = MathTex(r"N", font_size=18).next_to(ax, DOWN, buff=0.1)
        yl = MathTex(r"\pi(N; 4, a)", font_size=18).next_to(ax, LEFT, buff=0.1)
        self.play(Create(ax), Write(xl), Write(yl))

        def curve_1():
            N = int(round(N_tr.get_value()))
            N = max(1, min(N, N_MAX))
            pts = [ax.c2p(i, cum_1[i]) for i in range(1, N + 1)]
            m = VMobject(color=GREEN, stroke_width=2.5)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        def curve_3():
            N = int(round(N_tr.get_value()))
            N = max(1, min(N, N_MAX))
            pts = [ax.c2p(i, cum_3[i]) for i in range(1, N + 1)]
            m = VMobject(color=RED, stroke_width=2.5)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        self.add(always_redraw(curve_1), always_redraw(curve_3))

        def info():
            N = int(round(N_tr.get_value()))
            N = max(0, min(N, N_MAX))
            return VGroup(
                MathTex(rf"N = {N}", color=WHITE, font_size=20),
                MathTex(rf"\pi(N; 4, 1) = {cum_1[N]}",
                         color=GREEN, font_size=20),
                MathTex(rf"\pi(N; 4, 3) = {cum_3[N]}",
                         color=RED, font_size=20),
                Tex(r"both $\to \infty$ (Dirichlet)",
                     color=YELLOW, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        self.play(N_tr.animate.set_value(N_MAX),
                   run_time=8, rate_func=linear)
        self.wait(0.4)
