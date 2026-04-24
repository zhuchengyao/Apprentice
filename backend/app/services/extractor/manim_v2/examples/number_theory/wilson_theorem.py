from manim import *
import numpy as np


class WilsonTheoremExample(Scene):
    """
    Wilson's theorem: p is prime iff (p − 1)! ≡ −1 (mod p).

    SINGLE_FOCUS: for p = 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
    compute (p − 1)! mod p and compare with p − 1. Primes get GREEN,
    composites get RED.
    """

    def construct(self):
        title = Tex(r"Wilson's theorem: $p$ prime iff $(p-1)!\equiv -1\pmod p$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ns = list(range(2, 14))
        # compute (n-1)! mod n
        def is_prime(n):
            if n < 2: return False
            if n == 2: return True
            if n % 2 == 0: return False
            for i in range(3, int(np.sqrt(n)) + 1, 2):
                if n % i == 0: return False
            return True

        from math import factorial
        results = [(n, factorial(n - 1) % n, is_prime(n)) for n in ns]

        # Layout: table with 4 columns
        origin = np.array([-5.0, 2.2, 0])
        row_h = 0.55

        # Headers
        self.add(Tex(r"$n$", font_size=22, color=BLUE).move_to(origin + UP * 0.3))
        self.add(Tex(r"$(n-1)!\bmod n$", font_size=22, color=GREEN).move_to(origin + UP * 0.3 + RIGHT * 2.0))
        self.add(Tex(r"$\equiv n-1$?", font_size=22, color=YELLOW).move_to(origin + UP * 0.3 + RIGHT * 4.5))
        self.add(Tex(r"prime?", font_size=22, color=ORANGE).move_to(origin + UP * 0.3 + RIGHT * 6.8))

        idx_tr = ValueTracker(0.0)

        def k_now():
            return max(0, min(len(results) - 1, int(round(idx_tr.get_value()))))

        def rows():
            k = k_now()
            grp = VGroup()
            for i in range(k + 1):
                n, fact_mod, prime = results[i]
                y = origin[1] - i * row_h
                grp.add(Tex(str(n), font_size=22).move_to(np.array([origin[0], y, 0])))
                grp.add(Tex(str(fact_mod), font_size=22,
                             color=GREEN if fact_mod == n - 1 else RED).move_to(
                    np.array([origin[0] + 2.0, y, 0])))
                wilson_ok = (fact_mod == n - 1)
                symbol = "✓" if wilson_ok else "✗"
                grp.add(Tex(symbol, font_size=26,
                             color=GREEN if wilson_ok else RED).move_to(
                    np.array([origin[0] + 4.5, y, 0])))
                prime_sym = "prime" if prime else "comp."
                grp.add(Tex(prime_sym, font_size=20,
                             color=GREEN if prime else RED).move_to(
                    np.array([origin[0] + 6.8, y, 0])))
            return grp

        self.add(always_redraw(rows))

        # Current cell highlight
        def scanner():
            k = k_now()
            y = origin[1] - k * row_h
            return Rectangle(width=8.2, height=row_h * 0.9,
                             color=YELLOW, stroke_width=3).move_to(
                np.array([origin[0] + 3.4, y, 0]))

        self.add(always_redraw(scanner))

        info = VGroup(
            VGroup(Tex(r"$n=$", font_size=22),
                   DecimalNumber(2, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"biconditional: Wilson $\iff$ prime",
                color=YELLOW, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.4)
        info[0][1].add_updater(lambda m: m.set_value(results[k_now()][0]))
        self.add(info)

        for k in range(1, len(results)):
            self.play(idx_tr.animate.set_value(float(k)),
                      run_time=0.6, rate_func=smooth)
            self.wait(0.2)
        self.wait(0.8)
