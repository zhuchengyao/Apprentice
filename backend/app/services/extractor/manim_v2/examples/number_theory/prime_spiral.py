from manim import *
import numpy as np


def is_prime(n: int) -> bool:
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


class PrimeSpiralExample(Scene):
    """
    Sacks-style prime spiral built up incrementally.

    SINGLE_FOCUS: each integer n placed at radius √n, angle n radians.
    A ValueTracker N_max sweeps from 5 to 800; an always_redraw VGroup
    shows the prime dots whose n ≤ N_max. Patterns (curving rays) emerge
    as N grows. Right-corner panel has live N count, prime count,
    π(N) ≈ N/ln(N) approximation.
    """

    def construct(self):
        title = Tex(r"Sacks spiral: primes at radius $\sqrt{n}$, angle $n$ rad",
                    font_size=24).to_edge(UP, buff=0.4)
        self.play(Write(title))

        N_MAX_GLOBAL = 800
        scale = 0.18

        # Precompute positions
        primes_list = [n for n in range(2, N_MAX_GLOBAL + 1) if is_prime(n)]
        prime_positions = []
        for p in primes_list:
            r = scale * np.sqrt(p)
            theta = p
            prime_positions.append((p, np.array([r * np.cos(theta),
                                                 r * np.sin(theta), 0])))

        N_tr = ValueTracker(5.0)

        def prime_dots():
            n_max = int(N_tr.get_value())
            grp = VGroup()
            for p, pos in prime_positions:
                if p > n_max:
                    break
                grp.add(Dot(pos, color=YELLOW, radius=0.04))
            return grp

        # Background origin marker
        origin_dot = Dot(ORIGIN, color=WHITE, radius=0.08)
        self.add(origin_dot)
        self.add(always_redraw(prime_dots))

        # Right-corner readouts
        rcol_x = +5.4

        def info_panel():
            n_max = int(N_tr.get_value())
            primes_so_far = sum(1 for p in primes_list if p <= n_max)
            approx = n_max / np.log(max(2, n_max))
            return VGroup(
                MathTex(rf"N = {n_max}", color=WHITE, font_size=24),
                MathTex(rf"\pi(N) = {primes_so_far}",
                        color=YELLOW, font_size=24),
                MathTex(rf"N/\ln N \approx {approx:.1f}",
                        color=GREEN, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([rcol_x, +2.4, 0])

        self.add(always_redraw(info_panel))

        caption = Tex(r"Curving rays = $n$-coprime patterns from polynomial primes",
                      color=GREY_B, font_size=20).to_edge(DOWN, buff=0.3)
        self.play(Write(caption))

        self.play(N_tr.animate.set_value(N_MAX_GLOBAL),
                  run_time=10, rate_func=linear)
        self.wait(0.8)
