from manim import *
import numpy as np


class CarmichaelNumbersExample(Scene):
    """
    Carmichael numbers n are composite but pass Fermat's primality
    test: a^(n-1) ≡ 1 (mod n) for all a coprime to n. Smallest is 561.

    SINGLE_FOCUS: test n=561 across coprime bases. For each a in
    {2, 4, 5, 7, 8, 10, 11, 13}, compute a^560 mod 561; all = 1.
    ValueTracker idx_tr walks bases; always_redraw current test +
    running table.
    """

    def construct(self):
        n = 561
        title = Tex(rf"Carmichael $n={n}=3\cdot 11\cdot 17$: fools Fermat test",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        bases = [2, 4, 5, 7, 8, 10, 11, 13]
        # Some of these share factor with 561 (3, 11, 17); filter
        coprime = [b for b in bases if np.gcd(b, n) == 1]
        # Compute Fermat test
        results = [(a, pow(a, n - 1, n)) for a in coprime]

        idx_tr = ValueTracker(0.0)

        def k_now():
            return max(0, min(len(results) - 1, int(round(idx_tr.get_value()))))

        # Table layout
        origin = np.array([-3.5, 1.8, 0])
        row_h = 0.5
        col_w_a = 1.5
        col_w_r = 2.5

        # Header
        self.add(Tex(r"$a$", font_size=22, color=BLUE).move_to(origin + UP * 0.5))
        self.add(Tex(rf"$a^{{{n-1}}}\bmod {n}$", font_size=22, color=GREEN).move_to(
            origin + UP * 0.5 + RIGHT * col_w_a))

        def rows():
            k = k_now()
            grp = VGroup()
            for i in range(k + 1):
                a, r = results[i]
                grp.add(Tex(str(a), font_size=22, color=BLUE).move_to(
                    origin + DOWN * i * row_h))
                grp.add(Tex(str(r), font_size=22, color=GREEN if r == 1 else RED).move_to(
                    origin + DOWN * i * row_h + RIGHT * col_w_a))
                check = "✓" if r == 1 else "✗"
                col_check = GREEN if r == 1 else RED
                grp.add(Tex(check, font_size=26, color=col_check).move_to(
                    origin + DOWN * i * row_h + RIGHT * col_w_a + RIGHT * col_w_r))
            return grp

        self.add(always_redraw(rows))

        # Current test panel
        def current():
            k = k_now()
            return results[k]

        info = VGroup(
            Tex(rf"$n={n}$ composite ($=3\cdot 11\cdot 17$)",
                color=YELLOW, font_size=22),
            VGroup(Tex(r"base $a=$", font_size=22),
                   DecimalNumber(2, num_decimal_places=0,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(rf"$a^{{{n-1}}}\bmod {n}=$", font_size=22),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"Fermat says: if composite, usually $\neq 1$",
                color=GREY_B, font_size=20),
            Tex(r"But for Carmichael: ALWAYS $=1$ if $\gcd(a,n)=1$",
                color=RED, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(DR, buff=0.3)
        info[1][1].add_updater(lambda m: m.set_value(current()[0]))
        info[2][1].add_updater(lambda m: m.set_value(current()[1]))
        self.add(info)

        for k in range(1, len(results)):
            self.play(idx_tr.animate.set_value(float(k)),
                      run_time=0.9, rate_func=smooth)
            self.wait(0.3)
        self.wait(0.8)
