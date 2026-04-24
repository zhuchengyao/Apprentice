from manim import *
import numpy as np


class PerfectNumbersExample(Scene):
    """
    A perfect number equals the sum of its proper divisors.
    First few: 6, 28, 496, 8128.

    Euclid-Euler: if 2^p − 1 is prime (Mersenne), then
    2^(p-1) · (2^p − 1) is perfect.

    SINGLE_FOCUS: for each of n=6, 28, 496, step through divisors
    one by one via ValueTracker d_tr; always_redraw highlights
    current divisor in grid + running sum.
    """

    def construct(self):
        title = Tex(r"Perfect number: $n=\sum_{d|n,\ d<n} d$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Use n = 28 for primary demo
        n = 28
        divisors = [d for d in range(1, n + 1) if n % d == 0 and d < n]
        # = [1, 2, 4, 7, 14] → sum 28

        # Grid of integers 1..n
        cell_s = 0.55
        origin = np.array([-3.5, 1.8, 0])
        cells = {}
        for k in range(1, n + 1):
            col = (k - 1) % 7
            row = (k - 1) // 7
            pos = origin + RIGHT * col * cell_s + DOWN * row * cell_s
            c = Square(side_length=cell_s * 0.9, color=GREY_B,
                       stroke_width=1.0,
                       fill_color=GREY_B, fill_opacity=0.1).move_to(pos)
            l = Tex(str(k), font_size=18).move_to(pos)
            cells[k] = (c, l, pos)
            self.add(c, l)

        # Highlight self
        self.play(cells[n][0].animate.set_color(RED)
                  .set_fill(RED, opacity=0.3),
                  cells[n][1].animate.set_color(RED),
                  run_time=0.4)

        d_tr = ValueTracker(0.0)

        def k_now():
            return max(0, min(len(divisors), int(round(d_tr.get_value()))))

        def highlighted_divisors():
            k = k_now()
            grp = VGroup()
            for i in range(k):
                d = divisors[i]
                grp.add(Square(side_length=cell_s * 0.9, color=GREEN,
                                stroke_width=2.5,
                                fill_color=GREEN,
                                fill_opacity=0.4).move_to(cells[d][2]))
            return grp

        self.add(always_redraw(highlighted_divisors))

        # Sum strip
        def sum_str():
            k = k_now()
            parts = [str(divisors[i]) for i in range(k)]
            if not parts:
                return r"$\sum = 0$"
            return r"$" + "+".join(parts) + rf"= {sum(divisors[:k])}$"

        sum_tex = Tex(sum_str(), font_size=26, color=GREEN).to_edge(DOWN, buff=0.6)
        self.add(sum_tex)

        def update_sum(mob, dt):
            new = Tex(sum_str(), font_size=26, color=GREEN).move_to(sum_tex)
            sum_tex.become(new)
            return sum_tex
        sum_tex.add_updater(update_sum)

        info = VGroup(
            Tex(rf"$n={n}$", color=RED, font_size=24),
            VGroup(Tex(r"divisor $k=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"running sum $=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"Euclid–Euler: $p=2\Rightarrow 6$",
                color=YELLOW, font_size=20),
            Tex(r"$p=3\Rightarrow 28$",
                color=YELLOW, font_size=20),
            Tex(r"$p=5\Rightarrow 496$, $p=7\Rightarrow 8128$",
                color=YELLOW, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR, buff=0.3)
        info[1][1].add_updater(lambda m: m.set_value(k_now()))
        info[2][1].add_updater(lambda m: m.set_value(sum(divisors[:k_now()])))
        self.add(info)

        for k in range(1, len(divisors) + 1):
            self.play(d_tr.animate.set_value(float(k)),
                      run_time=0.8, rate_func=smooth)
            self.wait(0.3)

        final_stamp = Tex(rf"$\sum = n = {n}$ ✓ (perfect!)",
                          color=YELLOW, font_size=32).to_corner(DR, buff=0.3)
        self.play(Write(final_stamp))
        self.wait(1.0)
