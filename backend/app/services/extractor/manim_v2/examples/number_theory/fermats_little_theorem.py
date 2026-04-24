from manim import *
import numpy as np


class FermatsLittleTheoremExample(Scene):
    """
    Fermat's little theorem: for prime p and gcd(a, p)=1,
       a^(p-1) ≡ 1 (mod p).
    Visualize for p=7: the sequence a, 2a, 3a, 4a, 5a, 6a mod 7 is
    a permutation of {1, 2, ..., 6}. Product = 6! ⇒ a^6·6! ≡ 6! ⇒
    a^6 ≡ 1.

    SINGLE_FOCUS: table of a=1..6 and columns j=1..6 showing j·a mod 7.
    Each row is a permutation of 1..6. ValueTracker a_tr walks a=1..6;
    always_redraw YELLOW row highlight + final a^6 mod 7 = 1 check.
    """

    def construct(self):
        p = 7
        title = Tex(rf"Fermat: $a^{{{p-1}}}\equiv 1\pmod {{{p}}}$ for $\gcd(a,{p})=1$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        cell_s = 0.7
        origin = np.array([-2.8, 1.4, 0])

        # Header row
        headers = VGroup()
        headers.add(Tex(r"$a\backslash j$", font_size=20, color=GREY_B).move_to(
            origin + LEFT * cell_s))
        for j in range(1, p):
            headers.add(Tex(rf"$j={j}$", font_size=20, color=BLUE).move_to(
                origin + RIGHT * (j - 1) * cell_s))

        rows = VGroup()
        cells = {}
        for a in range(1, p):
            rows.add(Tex(rf"$a={a}$", font_size=20, color=BLUE).move_to(
                origin + LEFT * cell_s + DOWN * a * cell_s))
            for j in range(1, p):
                v = (j * a) % p
                cell = Square(side_length=cell_s * 0.9, color=GREY_B,
                              stroke_width=1.0,
                              fill_color=GREY_B,
                              fill_opacity=0.05).move_to(
                    origin + RIGHT * (j - 1) * cell_s + DOWN * a * cell_s)
                val = Tex(str(v), font_size=22).move_to(cell.get_center())
                cells[(a, j)] = (cell, val)
                rows.add(cell, val)

        self.play(Write(headers), Write(rows))

        a_tr = ValueTracker(1.0)

        def a_now():
            return max(1, min(p - 1, int(round(a_tr.get_value()))))

        def highlight():
            a = a_now()
            return Rectangle(width=cell_s * (p - 1),
                             height=cell_s * 0.95,
                             color=YELLOW,
                             stroke_width=3).move_to(
                origin + RIGHT * (p - 2) * cell_s / 2 + DOWN * a * cell_s)

        self.add(always_redraw(highlight))

        # Verification panel
        info = VGroup(
            VGroup(Tex(r"$a=$", font_size=22),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(rf"$a^{{{p-1}}}\bmod{p}=$", font_size=22),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"always $=1$ for prime modulus",
                color=GREEN, font_size=22),
            Tex(r"proof: $\{ja\bmod p\}_{j=1}^{p-1}$ is permutation",
                color=YELLOW, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(a_now()))
        info[1][1].add_updater(lambda m: m.set_value(pow(a_now(), p - 1, p)))
        self.add(info)

        for a in range(2, p):
            self.play(a_tr.animate.set_value(float(a)),
                      run_time=1.2, rate_func=smooth)
            self.wait(0.35)
        self.wait(0.8)
