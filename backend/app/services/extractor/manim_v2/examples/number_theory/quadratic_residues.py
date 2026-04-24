from manim import *
import numpy as np


class QuadraticResiduesExample(Scene):
    """
    Quadratic residues mod p: the values a² mod p for a = 1..p-1.
    Exactly (p-1)/2 distinct residues. ValueTracker p_tr steps
    through several odd primes.

    SINGLE_FOCUS:
      Grid of residues {0, 1, ..., p-1} colored GREEN (QR) or GREY
      (non-QR). always_redraw as p_tr changes. Quadratic character
      χ(a) = ±1 visualized.
    """

    def construct(self):
        title = Tex(r"Quadratic residues mod $p$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        primes = [5, 7, 11, 13, 17, 19, 23]
        p_idx_tr = ValueTracker(0)

        def cells():
            i = int(round(p_idx_tr.get_value())) % len(primes)
            p = primes[i]
            # Compute QR set
            qr_set = set()
            for a in range(1, p):
                qr_set.add((a * a) % p)
            # Display 0..p-1 in a row of cells
            cell_w = 0.55
            grp = VGroup()
            total_w = p * cell_w
            x_start = -total_w / 2
            for val in range(p):
                color = GREEN if val in qr_set else GREY_B
                fill = 0.7 if val in qr_set else 0.2
                sq = Square(side_length=cell_w * 0.92,
                              color=color, fill_opacity=fill,
                              stroke_width=1)
                sq.move_to([x_start + (val + 0.5) * cell_w, 0, 0])
                grp.add(sq)
                lbl = MathTex(rf"{val}", font_size=18,
                                color=BLACK if val in qr_set else WHITE
                                ).move_to(sq.get_center())
                grp.add(lbl)
            return grp

        self.add(always_redraw(cells))

        def info():
            i = int(round(p_idx_tr.get_value())) % len(primes)
            p = primes[i]
            qr_set = set()
            for a in range(1, p):
                qr_set.add((a * a) % p)
            return VGroup(
                MathTex(rf"p = {p}", color=YELLOW, font_size=28),
                MathTex(rf"|\text{{QR}}| = {len(qr_set - {0})}",
                         color=GREEN, font_size=22),
                MathTex(rf"(p-1)/2 = {(p-1)//2}",
                         color=WHITE, font_size=22),
                Tex(r"GREEN: $a^2 \equiv $ val", color=GREEN, font_size=20),
                Tex(r"GREY: non-residue", color=GREY_B, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        for i in range(1, len(primes)):
            self.play(p_idx_tr.animate.set_value(i),
                       run_time=1.2, rate_func=smooth)
            self.wait(0.6)
        self.wait(0.4)
