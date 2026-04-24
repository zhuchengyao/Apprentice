from manim import *
import numpy as np


class TotientFunctionExample(Scene):
    """
    Euler's totient φ(n) = #{k ∈ [1, n] : gcd(k, n) = 1}. Multiplicative
    function. φ(p) = p-1 for prime p; φ(p^k) = p^k - p^(k-1); Euler's
    product formula φ(n) = n · ∏_{p|n} (1 - 1/p).

    SINGLE_FOCUS:
      Row of cells n = 1..30 with φ(n) displayed; ValueTracker
      highlights each n; primes (φ = n-1) colored YELLOW.
    """

    def construct(self):
        title = Tex(r"Euler's totient $\varphi(n)$: count of coprimes $\le n$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        from math import gcd

        def phi(n):
            if n == 1:
                return 1
            return sum(1 for k in range(1, n + 1) if gcd(k, n) == 1)

        def is_prime(n):
            if n < 2:
                return False
            for i in range(2, int(n ** 0.5) + 1):
                if n % i == 0:
                    return False
            return True

        N = 20
        cell = 0.55
        origin = np.array([-N * cell / 2 + cell / 2, 0, 0])

        # Static cells
        cells_grp = VGroup()
        for n in range(1, N + 1):
            p = phi(n)
            col = YELLOW if is_prime(n) else BLUE
            sq = Square(side_length=cell * 0.9, color=col,
                          fill_opacity=0.55, stroke_width=1)
            sq.move_to(origin + np.array([(n - 1) * cell, 0, 0]))
            cells_grp.add(sq)
            lbl_phi = MathTex(rf"{p}", font_size=16,
                                color=WHITE
                                ).move_to(sq.get_center())
            cells_grp.add(lbl_phi)
            lbl_n = MathTex(rf"{n}", font_size=12, color=GREY_B
                              ).next_to(sq, DOWN, buff=0.1)
            cells_grp.add(lbl_n)
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

        def info():
            n = int(round(n_tr.get_value()))
            n = max(1, min(n, N))
            p = phi(n)
            # Coprime list
            from math import gcd
            coprimes = [k for k in range(1, n + 1) if gcd(k, n) == 1]
            return VGroup(
                MathTex(rf"n = {n}", color=RED, font_size=22),
                MathTex(rf"\varphi({n}) = {p}",
                         color=YELLOW, font_size=24),
                MathTex(rf"\varphi(n) = n \prod_{{p|n}} (1 - 1/p)",
                         color=GREEN, font_size=18),
                Tex(r"coprimes: " + ", ".join(str(x) for x in coprimes[:8]) + (r"\ldots" if len(coprimes) > 8 else ""),
                     color=WHITE, font_size=14),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        for nv in [2, 4, 6, 8, 10, 12, 15, 20]:
            self.play(n_tr.animate.set_value(nv),
                       run_time=0.8, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.4)
