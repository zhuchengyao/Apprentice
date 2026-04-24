from manim import *
import numpy as np
from math import comb


class SubsetCountingExample(Scene):
    """
    A set of n elements has 2^n subsets — every element either in
    or out, binary choice each.

    SINGLE_FOCUS:
      ValueTracker n_tr steps through n = 1, 2, 3, 4. For each n:
      Transform into a grid showing all 2^n subsets as binary rows
      of colored bits. Live count.
    """

    def construct(self):
        title = Tex(r"A set of $n$ elements has $2^n$ subsets",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        def row_for_subset(bits, n, row_y, x_start):
            grp = VGroup()
            for i, b in enumerate(bits):
                box = Square(side_length=0.36,
                              color=YELLOW if b else GREY_B,
                              fill_opacity=0.55 if b else 0.15,
                              stroke_width=1)
                box.move_to([x_start + i * 0.38, row_y, 0])
                lbl = MathTex(str(b),
                               color=BLACK if b else WHITE,
                               font_size=18).move_to(box.get_center())
                grp.add(box, lbl)
            return grp

        def grid(n):
            count = 2 ** n
            rows_per_col = min(count, 8)
            cols_needed = (count + rows_per_col - 1) // rows_per_col
            grp = VGroup()
            for mask in range(count):
                bits = [(mask >> (n - 1 - i)) & 1 for i in range(n)]
                col = mask // rows_per_col
                r = mask % rows_per_col
                y = 1.7 - r * 0.45
                x_start = -4.5 + col * 2.5
                grp.add(row_for_subset(bits, n, y, x_start))
            return grp, count

        # Start with n = 1
        cur, cnt = grid(1)
        count_lbl = MathTex(rf"n = 1,\ 2^n = {cnt}",
                             color=YELLOW, font_size=30
                             ).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(cur), Write(count_lbl))
        self.wait(0.6)

        for n in [2, 3, 4]:
            new_grp, cnt = grid(n)
            new_lbl = MathTex(rf"n = {n},\ 2^n = {cnt}",
                                color=YELLOW, font_size=30
                                ).to_edge(DOWN, buff=0.7)
            self.play(Transform(cur, new_grp),
                       Transform(count_lbl, new_lbl),
                       run_time=1.6)
            self.wait(0.7)

        # Identity
        id_note = MathTex(r"\sum_{k=0}^{n} \binom{n}{k} = 2^n",
                           color=GREEN, font_size=26
                           ).to_corner(UR, buff=0.5)
        self.play(Write(id_note))
        self.wait(0.5)
