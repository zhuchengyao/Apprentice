from manim import *
import numpy as np


class QuadraticReciprocityExample(Scene):
    """
    Gauss's quadratic reciprocity: for distinct odd primes p, q,
        (p/q)(q/p) = (-1)^((p-1)/2 · (q-1)/2).

    TWO_COLUMN: LEFT is a 10x10 table of (p, q) for primes
    [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]. Cells colored GREEN if
    both (p/q) and (q/p) agree (=1), RED if they differ.
    ValueTracker k_tr walks through cells with YELLOW highlight;
    always_redraw scanner reveals one (p, q) at a time. Right column
    shows live p, q, (p/q), (q/p), sign.
    """

    def construct(self):
        title = Tex(r"Quadratic reciprocity: $(p/q)(q/p)=(-1)^{\frac{p-1}{2}\frac{q-1}{2}}$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
        n = len(primes)

        def legendre(a, p):
            # (a/p) via Euler's criterion
            a = a % p
            if a == 0:
                return 0
            return 1 if pow(a, (p - 1) // 2, p) == 1 else -1

        # Build grid
        cell_s = 0.44
        origin_x = -3.6
        origin_y = 1.8

        cells = {}
        for i, p in enumerate(primes):
            for j, q in enumerate(primes):
                x = origin_x + j * cell_s
                y = origin_y - i * cell_s
                if p == q:
                    col = GREY_D; op = 0.3
                else:
                    lp = legendre(p, q)
                    lq = legendre(q, p)
                    prod = lp * lq
                    expected = (-1) ** (((p - 1) // 2) * ((q - 1) // 2))
                    if prod == expected:
                        col = GREEN; op = 0.5
                    else:
                        col = RED; op = 0.5
                cell = Square(side_length=cell_s * 0.88,
                              color=col, stroke_width=0.8,
                              fill_color=col, fill_opacity=op).move_to([x, y, 0])
                cells[(i, j)] = cell

        grid = VGroup(*cells.values())
        self.play(FadeIn(grid))

        # Row/column prime labels
        for i, p in enumerate(primes):
            self.add(Tex(str(p), font_size=16, color=BLUE).move_to(
                [origin_x - cell_s * 0.85, origin_y - i * cell_s, 0]))
            self.add(Tex(str(p), font_size=16, color=BLUE).move_to(
                [origin_x + i * cell_s, origin_y + cell_s * 0.85, 0]))

        self.wait(0.5)

        # Scanner
        idx_tr = ValueTracker(0.0)

        def scan():
            k = int(round(idx_tr.get_value()))
            i = k // n
            j = k % n
            i = max(0, min(n - 1, i))
            j = max(0, min(n - 1, j))
            x = origin_x + j * cell_s
            y = origin_y - i * cell_s
            return Square(side_length=cell_s * 0.88,
                          color=YELLOW, stroke_width=3).move_to([x, y, 0])

        self.add(always_redraw(scan))

        # Right column
        def k_pq():
            k = int(round(idx_tr.get_value()))
            i = k // n
            j = k % n
            i = max(0, min(n - 1, i))
            j = max(0, min(n - 1, j))
            return primes[i], primes[j]

        info = VGroup(
            VGroup(Tex(r"$p=$", font_size=22),
                   DecimalNumber(3, num_decimal_places=0, font_size=22).set_color(BLUE)
                   ).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$q=$", font_size=22),
                   DecimalNumber(3, num_decimal_places=0, font_size=22).set_color(BLUE)
                   ).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$(p/q)=$", font_size=22),
                   DecimalNumber(1, num_decimal_places=0, font_size=22).set_color(GREEN)
                   ).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$(q/p)=$", font_size=22),
                   DecimalNumber(1, num_decimal_places=0, font_size=22).set_color(GREEN)
                   ).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$(-1)^{\frac{p-1}{2}\frac{q-1}{2}}=$", font_size=22),
                   DecimalNumber(1, num_decimal_places=0, font_size=22).set_color(YELLOW)
                   ).arrange(RIGHT, buff=0.1),
            Tex(r"GREEN: reciprocity holds", color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.2)

        info[0][1].add_updater(lambda m: m.set_value(k_pq()[0]))
        info[1][1].add_updater(lambda m: m.set_value(k_pq()[1]))

        def lpq():
            p, q = k_pq()
            return legendre(p, q) if p != q else 0
        def lqp():
            p, q = k_pq()
            return legendre(q, p) if p != q else 0
        def sign():
            p, q = k_pq()
            if p == q: return 0
            return (-1) ** (((p - 1) // 2) * ((q - 1) // 2))

        info[2][1].add_updater(lambda m: m.set_value(lpq()))
        info[3][1].add_updater(lambda m: m.set_value(lqp()))
        info[4][1].add_updater(lambda m: m.set_value(sign()))
        self.add(info)

        self.play(idx_tr.animate.set_value(float(n * n - 1)),
                  run_time=8, rate_func=linear)
        self.wait(0.5)
