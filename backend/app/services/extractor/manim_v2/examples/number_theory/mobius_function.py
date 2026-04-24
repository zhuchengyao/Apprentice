from manim import *
import numpy as np


class MobiusFunctionExample(Scene):
    """
    Möbius μ(n): 0 if n has a squared prime factor; (-1)^k if n is
    a product of k distinct primes. Visualize μ for n = 1..30.

    SINGLE_FOCUS:
      Row of 30 colored cells by μ(n) value: YELLOW +1, BLUE -1,
      GREY_B 0. ValueTracker n_tr highlights each n in sequence with
      factorization shown.
    """

    def construct(self):
        title = Tex(r"Möbius $\mu(n)$: $+1, -1, 0$ by prime factorization",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        def mu(n):
            if n == 1:
                return 1
            # Factor n
            factors = {}
            x = n
            for p in range(2, int(np.sqrt(n)) + 2):
                while x % p == 0:
                    factors[p] = factors.get(p, 0) + 1
                    x //= p
            if x > 1:
                factors[x] = factors.get(x, 0) + 1
            # If any prime has exponent >= 2, mu = 0
            for exp in factors.values():
                if exp >= 2:
                    return 0
            # Else mu = (-1)^k where k = number of prime factors
            return (-1) ** len(factors)

        N = 30
        cell = 0.4
        origin = np.array([-N * cell / 2 + cell / 2, 0, 0])

        # Pre-compute colors
        def mu_color(val):
            if val == 1:
                return YELLOW
            elif val == -1:
                return BLUE
            else:
                return GREY_B

        # Base cells
        cells_grp = VGroup()
        for n in range(1, N + 1):
            mv = mu(n)
            sq = Square(side_length=cell * 0.9,
                          color=mu_color(mv), fill_opacity=0.7,
                          stroke_width=1)
            sq.move_to(origin + np.array([(n - 1) * cell, 0, 0]))
            cells_grp.add(sq)
            # Value label inside
            lbl = MathTex(rf"{mv:+d}" if mv != 0 else "0",
                           color=BLACK if mv != 0 else WHITE,
                           font_size=14).move_to(sq.get_center())
            cells_grp.add(lbl)
            # n label below
            n_lbl = MathTex(rf"{n}", color=WHITE, font_size=12
                              ).move_to(sq.get_center() + DOWN * 0.4)
            cells_grp.add(n_lbl)
        self.play(FadeIn(cells_grp))

        n_tr = ValueTracker(1)

        def highlight_n():
            n = int(round(n_tr.get_value()))
            n = max(1, min(n, N))
            sq = Square(side_length=cell * 0.9,
                          color=RED, stroke_width=3,
                          fill_opacity=0)
            sq.move_to(origin + np.array([(n - 1) * cell, 0, 0]))
            return sq

        self.add(always_redraw(highlight_n))

        def factorize(n):
            factors = {}
            x = n
            for p in range(2, int(np.sqrt(n)) + 2):
                while x % p == 0:
                    factors[p] = factors.get(p, 0) + 1
                    x //= p
            if x > 1:
                factors[x] = factors.get(x, 0) + 1
            return factors

        def info():
            n = int(round(n_tr.get_value()))
            n = max(1, min(n, N))
            mv = mu(n)
            factors = factorize(n)
            fact_str = "·".join(f"{p}^{e}" if e > 1 else str(p)
                                 for p, e in factors.items())
            if n == 1:
                fact_str = "1"
            return VGroup(
                MathTex(rf"n = {n}", color=RED, font_size=24),
                MathTex(rf"n = {fact_str}",
                         color=WHITE, font_size=22),
                MathTex(rf"\mu(n) = {mv:+d}" if mv != 0 else rf"\mu(n) = 0",
                         color=mu_color(mv), font_size=26),
                Tex(r"$\sum_{d | n} \mu(d) = [n = 1]$",
                     color=GREEN, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        for nv in [2, 4, 6, 8, 10, 12, 15, 20, 25, 30]:
            self.play(n_tr.animate.set_value(nv),
                       run_time=0.9, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.4)
