from manim import *
import numpy as np


class EulerPhiProductExample(Scene):
    """
    Euler's totient function formula: for n = Π p_i^{a_i},
       φ(n) = n · Π (1 − 1/p_i).

    Demo for n = 360 = 2³ · 3² · 5. Then φ(360) = 360·½·⅔·⅘ = 96.

    SINGLE_FOCUS: 12×30 grid of integers 1..360; coprime-to-360 cells
    colored YELLOW (φ total), others GREY. Three sequential sieving
    steps (remove multiples of 2, then 3, then 5) via ValueTracker
    step_tr ∈ {0, 1, 2, 3}; count shrinks from 360 → 180 → 120 → 96.
    """

    def construct(self):
        from math import gcd
        n = 360
        primes = [2, 3, 5]
        title = Tex(rf"Euler totient: $\varphi(360) = 360\cdot(1-\tfrac12)(1-\tfrac13)(1-\tfrac15)=96$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        rows, cols = 12, 30
        cell_s = 0.38
        origin = np.array([-5.5, 2.0, 0])

        step_tr = ValueTracker(0.0)

        def state_of(k):  # k = 1..n
            s = int(round(step_tr.get_value()))
            if s == 0:
                return "all"
            if any(k % primes[i] == 0 for i in range(s)):
                return "removed"
            return "kept"

        def cell(i, k):
            r = (k - 1) // cols
            c = (k - 1) % cols
            state = state_of(k)
            if state == "all":
                col = BLUE; op = 0.3
            elif state == "removed":
                col = GREY_D; op = 0.25
            else:
                col = YELLOW; op = 0.85
            return Square(side_length=cell_s * 0.88,
                          color=col, stroke_width=0.5,
                          fill_color=col, fill_opacity=op).move_to(
                origin + RIGHT * c * cell_s - DOWN * r * cell_s - DOWN * 0.0)

        def grid():
            grp = VGroup()
            for k in range(1, n + 1):
                grp.add(cell(0, k))
            return grp

        self.add(always_redraw(grid))

        def kept_count():
            s = int(round(step_tr.get_value()))
            cnt = 0
            for k in range(1, n + 1):
                if not any(k % primes[i] == 0 for i in range(s)):
                    cnt += 1
            return cnt

        info = VGroup(
            VGroup(Tex(r"step $=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"kept $=$", color=YELLOW, font_size=22),
                   DecimalNumber(360, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"expected $n\cdot\prod(1-1/p)=$", font_size=20),
                   DecimalNumber(360, num_decimal_places=0,
                                 font_size=20).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"$\gcd(k, 360)=1$ iff YELLOW",
                color=YELLOW, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.3)

        def expected():
            s = int(round(step_tr.get_value()))
            val = 360.0
            for i in range(s):
                val = val * (1 - 1 / primes[i])
            return int(round(val))

        info[0][1].add_updater(lambda m: m.set_value(int(round(step_tr.get_value()))))
        info[1][1].add_updater(lambda m: m.set_value(kept_count()))
        info[2][1].add_updater(lambda m: m.set_value(expected()))
        self.add(info)

        # Sieve steps
        for s in [1, 2, 3]:
            self.play(step_tr.animate.set_value(float(s)),
                      run_time=2.5, rate_func=smooth)
            self.wait(0.6)

        # Verify analytic
        import math
        phi_val = n
        for p in primes:
            phi_val = phi_val * (p - 1) // p
        verify = Tex(rf"$\varphi(360)={phi_val}$ ✓",
                     color=GREEN, font_size=28).to_corner(UR, buff=0.4)
        self.play(Write(verify))
        self.wait(0.8)
