from manim import *
import numpy as np
from math import log


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


class PrimesNearMillionExample(Scene):
    """
    Density of primes near 10⁶: π(x) ≈ x / ln x. Zoom into a 200-
    wide window centered at 1,000,000 and see which integers are prime.

    TWO_COLUMN:
      LEFT  — number line [999,900, 1,000,100]; ValueTracker center_tr
              slides the window center; always_redraw dots at each
              integer in the window, colored YELLOW if prime else BLUE.
      RIGHT — live window center, primes in window, expected count
              200/ln(10^6), and cumulative π(10^6) = 78498.
    """

    def construct(self):
        title = Tex(r"Primes near $10^6$: density $\sim 1/\ln x$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        nl = NumberLine(x_range=[-100, 100, 25], length=10,
                         include_numbers=True,
                         decimal_number_config={"num_decimal_places": 0,
                                                 "font_size": 16}
                         ).move_to([-1.5, -0.6, 0])
        self.play(Create(nl))

        center_tr = ValueTracker(1000000)

        def int_dots():
            c = int(round(center_tr.get_value()))
            grp = VGroup()
            for off in range(-100, 101, 1):
                n = c + off
                if is_prime(n):
                    grp.add(Dot(nl.n2p(off), color=YELLOW, radius=0.06))
                else:
                    grp.add(Dot(nl.n2p(off), color=BLUE_D, radius=0.03))
            return grp

        self.add(always_redraw(int_dots))

        center_lbl_anchor = Tex(r"window center $= $",
                                  color=WHITE, font_size=22
                                  ).next_to(nl, DOWN, buff=0.35)
        self.play(Write(center_lbl_anchor))

        def center_lbl():
            c = int(round(center_tr.get_value()))
            return MathTex(rf"{c:,}".replace(",", r"\,"),
                             color=YELLOW, font_size=26
                             ).next_to(center_lbl_anchor, RIGHT, buff=0.2)

        self.add(always_redraw(center_lbl))

        def info():
            c = int(round(center_tr.get_value()))
            primes_in_window = sum(
                1 for n in range(max(2, c - 100), c + 101) if is_prime(n))
            expected = 200 / log(max(c, 2))
            return VGroup(
                MathTex(rf"\text{{primes in window}}: {primes_in_window}",
                         color=YELLOW, font_size=22),
                MathTex(rf"200/\ln(x) \approx {expected:.2f}",
                         color=GREEN, font_size=22),
                MathTex(r"\pi(10^6) = 78,498", color=BLUE, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4).shift(UP * 0.8)

        self.add(always_redraw(info))

        # Sweep center from 1M to 1M+10000, then to 1M-5000, then 1M
        for target in [1005000, 999000, 1003000, 1000000]:
            self.play(center_tr.animate.set_value(target),
                       run_time=2.5, rate_func=linear)
            self.wait(0.3)
        self.wait(0.4)
