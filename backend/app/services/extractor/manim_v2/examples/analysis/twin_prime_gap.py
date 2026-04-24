from manim import *
import numpy as np
from math import log


def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0: return False
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0: return False
    return True


class TwinPrimeGapExample(Scene):
    """
    Twin prime count π₂(x) vs Hardy-Littlewood prediction.

    TWO_COLUMN:
      LEFT  — Number line 0..N. ValueTracker N_max sweeps 30→1500;
              twin prime pairs (p, p+2) accumulate as YELLOW boxes.
              Density visibly thins.
      RIGHT — Live N, twin pair count π₂(N), and Hardy-Littlewood
              estimate 2C₂·N/(ln N)². Plus the conjecture statement.
    """

    def construct(self):
        title = Tex(r"Twin primes $\{(p, p+2)\}$ vs the Hardy-Littlewood density",
                    font_size=22).to_edge(UP, buff=0.4)
        self.play(Write(title))

        N_GLOBAL = 1500
        C2 = 0.66016

        # Precompute twin pairs up to N_GLOBAL
        twin_pairs = []
        for p in range(3, N_GLOBAL):
            if is_prime(p) and is_prime(p + 2):
                twin_pairs.append((p, p + 2))

        # Number line
        nl = NumberLine(
            x_range=[0, N_GLOBAL, 250], length=10,
            include_numbers=True,
            decimal_number_config={"num_decimal_places": 0, "font_size": 18},
        ).move_to([0, -1.0, 0])
        self.play(Create(nl))

        N_tr = ValueTracker(30)

        def twin_dots():
            N_max = max(30, int(round(N_tr.get_value())))
            grp = VGroup()
            for (p, q) in twin_pairs:
                if p <= N_max:
                    grp.add(Dot(nl.n2p(p), color=YELLOW, radius=0.05))
                    grp.add(Dot(nl.n2p(q), color=ORANGE, radius=0.05))
                else:
                    break
            return grp

        self.add(always_redraw(twin_dots))

        # RIGHT COLUMN
        rcol_x = +4.0

        def info_panel():
            N_max = max(30, int(round(N_tr.get_value())))
            count = sum(1 for (p, q) in twin_pairs if p <= N_max)
            if N_max > 2:
                hl = 2 * C2 * N_max / (log(N_max) ** 2)
            else:
                hl = 0
            return VGroup(
                MathTex(rf"N = {N_max}", color=WHITE, font_size=24),
                MathTex(rf"\pi_2(N) = {count}",
                        color=YELLOW, font_size=24),
                MathTex(rf"2C_2 \tfrac{{N}}{{(\ln N)^2}} \approx {hl:.1f}",
                        color=GREEN, font_size=20),
                MathTex(rf"C_2 \approx {C2:.4f}",
                        color=GREY_B, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([rcol_x, +1.4, 0])

        self.add(always_redraw(info_panel))

        conj = Tex(r"Twin Prime Conjecture: $\pi_2(x) \to \infty$ (open since 1849)",
                   color=YELLOW, font_size=22).to_edge(DOWN, buff=0.3)
        self.play(Write(conj))

        self.play(N_tr.animate.set_value(N_GLOBAL),
                  run_time=10, rate_func=linear)
        self.wait(0.6)
