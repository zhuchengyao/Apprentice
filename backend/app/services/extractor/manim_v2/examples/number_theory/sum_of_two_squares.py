from manim import *
import numpy as np


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


class SumOfTwoSquaresExample(Scene):
    """
    Fermat: a prime p is sum of two squares iff p = 2 or p ≡ 1 (mod 4).
    Show primes 2..100 classified: (p ≡ 1 mod 4 or p = 2) → GREEN,
    else RED.

    SINGLE_FOCUS:
      Row of primes up to 100. ValueTracker step_tr reveals and
      classifies each with its two-squares decomposition if possible.
    """

    def construct(self):
        title = Tex(r"Fermat: $p = a^2 + b^2 \Leftrightarrow p = 2$ or $p \equiv 1 \pmod 4$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        primes = [p for p in range(2, 101) if is_prime(p)]

        # Find two-squares decomposition for primes ≡ 1 mod 4 or p = 2
        def two_sq(p):
            if p == 2:
                return (1, 1)
            if p % 4 == 3:
                return None
            for a in range(1, int(np.sqrt(p)) + 1):
                b2 = p - a * a
                b = int(round(np.sqrt(b2)))
                if b * b == b2:
                    return (a, b)
            return None

        decomps = [(p, two_sq(p)) for p in primes]

        N = len(primes)
        cell = 0.38
        # Two rows
        x_start = -5.5
        row1_y = 1.0
        row2_y = -0.5
        y_by_idx = [row1_y if i < N // 2 + 1 else row2_y for i in range(N)]

        step_tr = ValueTracker(0)

        def prime_cells():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, N))
            grp = VGroup()
            for i in range(s):
                p, decomp = decomps[i]
                col = GREEN if decomp else RED
                # Position on one of two rows
                row_y = row1_y if i < N / 2 else row2_y
                row_idx = i if i < N / 2 else i - int(N / 2)
                x = x_start + row_idx * cell
                sq = Square(side_length=cell * 0.9, color=col,
                              fill_opacity=0.7, stroke_width=1)
                sq.move_to([x, row_y, 0])
                grp.add(sq)
                grp.add(MathTex(rf"{p}", font_size=10,
                                  color=BLACK).move_to(sq.get_center()))
            return grp

        self.add(always_redraw(prime_cells))

        def info():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, N))
            if s == 0:
                return VGroup()
            p, decomp = decomps[s - 1]
            if decomp:
                a, b = decomp
                txt = MathTex(rf"{p} = {a}^2 + {b}^2",
                                color=GREEN, font_size=24)
            else:
                txt = MathTex(rf"{p} \equiv 3 \pmod 4: \text{{no decomposition}}",
                                color=RED, font_size=22)
            return VGroup(
                MathTex(rf"\text{{prime }} #{s}/{N}: p = {p}",
                         color=WHITE, font_size=22),
                txt,
                Tex(r"GREEN: sum of 2 squares; RED: not",
                     color=YELLOW, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        for i in range(1, N + 1, 2):  # step by 2 for speed
            self.play(step_tr.animate.set_value(i),
                       run_time=0.3, rate_func=smooth)
        self.play(step_tr.animate.set_value(N), run_time=0.5)
        self.wait(0.5)
