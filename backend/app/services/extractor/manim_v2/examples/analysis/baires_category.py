from manim import *
import numpy as np


class BairesCategoryExample(Scene):
    """
    Baire category theorem: in a complete metric space, a countable
    intersection of open dense sets is dense.

    Visualize: U_n = [0, 1] minus rational numbers p/q with q ≤ n
    (each thinned set is open & dense). The intersection is the
    irrationals — dense in [0, 1].

    SINGLE_FOCUS: horizontal [0, 1] number line. ValueTracker n_tr
    steps n=1..12; always_redraw removes rationals with denom ≤ n
    (punctures shown as RED holes of shrinking radius 0.02/q).
    Live count of removed rationals + note that result is still dense.
    """

    def construct(self):
        title = Tex(r"Baire: $\bigcap_n U_n$ dense. $U_n=[0,1]\setminus \{p/q : q\le n\}$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        line = NumberLine(x_range=[0, 1, 0.1], length=11,
                          include_numbers=True,
                          font_size=18).shift(DOWN * 0.2)
        self.play(Create(line))

        green_line = Line(line.n2p(0), line.n2p(1),
                          color=GREEN, stroke_width=6)
        self.play(Create(green_line))

        n_tr = ValueTracker(1.0)

        def rationals_up_to(n):
            from math import gcd
            out = []
            for q in range(1, n + 1):
                for p in range(0, q + 1):
                    if gcd(p, q) == 1 or (p == 0 and q == 1) or (p == q and q == 1):
                        out.append((p / q, q))
            # Deduplicate (p/q could repeat)
            seen = set()
            unique = []
            for v, q in out:
                if round(v, 8) not in seen:
                    seen.add(round(v, 8))
                    unique.append((v, q))
            return unique

        def holes():
            n = int(round(n_tr.get_value()))
            n = max(1, min(12, n))
            rats = rationals_up_to(n)
            grp = VGroup()
            for v, q in rats:
                radius_units = 0.35 / q
                left_x = max(0, v - radius_units / 11)  # radius in number-line units
                right_x = min(1, v + radius_units / 11)
                seg = Line(line.n2p(left_x), line.n2p(right_x),
                            color=RED, stroke_width=6)
                grp.add(seg)
                if q <= 5:  # label for small q only
                    grp.add(Dot(line.n2p(v), color=RED, radius=0.04))
                    grp.add(Tex(f"${int(round(v*q))}/{q}$", font_size=14,
                                 color=RED).next_to(line.n2p(v), DOWN, buff=0.2))
            return grp

        self.add(always_redraw(holes))

        # Info
        def n_now():
            return max(1, min(12, int(round(n_tr.get_value()))))

        info = VGroup(
            VGroup(Tex(r"$n=$", font_size=22),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"rationals removed $=$", font_size=22),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
            Tex(r"$U_n$ open (each hole open)", color=YELLOW, font_size=20),
            Tex(r"$U_n$ dense (between holes)", color=YELLOW, font_size=20),
            Tex(r"$\bigcap U_n=\mathbb{Q}^c\cap[0,1]$ dense (Baire)",
                color=GREEN, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)

        info[0][1].add_updater(lambda m: m.set_value(n_now()))
        info[1][1].add_updater(lambda m: m.set_value(len(rationals_up_to(n_now()))))
        self.add(info)

        for n in range(2, 13):
            self.play(n_tr.animate.set_value(float(n)),
                      run_time=0.6, rate_func=smooth)
            self.wait(0.2)
        self.wait(0.8)
