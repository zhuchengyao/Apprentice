from manim import *
import numpy as np


class FermatLittleTheoremExample(Scene):
    """
    Fermat's little theorem: for prime p and gcd(a, p) = 1,
    a^(p-1) ≡ 1 (mod p). Equivalently a^p ≡ a (mod p).

    SINGLE_FOCUS:
      Grid showing a^k mod p for a = 1..p-1 and k = 0..p-1 for p=7.
      ValueTracker highlights the column k = p-1 where all entries
      equal 1.
    """

    def construct(self):
        title = Tex(r"Fermat's little theorem: $a^{p-1} \equiv 1 \pmod p$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        p = 7
        table = np.zeros((p, p), dtype=int)
        for a in range(1, p):
            for k in range(p):
                table[a, k] = pow(a, k, p)

        cell = 0.65
        origin = np.array([-cell * (p - 1) / 2, cell * (p - 1) / 2 - 0.3, 0])

        # Grid
        def cell_center(i, j):
            return origin + np.array([j * cell, -i * cell, 0])

        grid_group = VGroup()
        # Header row: k = 0, 1, ..., p-1
        for j in range(p):
            lbl = MathTex(rf"k={j}", font_size=16, color=WHITE
                            ).move_to(cell_center(-1, j))
            grid_group.add(lbl)
        # Column a = 1, 2, ..., p-1 header
        for i in range(1, p):
            lbl = MathTex(rf"a={i}", font_size=16, color=WHITE
                            ).move_to(cell_center(i, -1))
            grid_group.add(lbl)

        # Cells
        for i in range(1, p):
            for j in range(p):
                val = table[i, j]
                sq = Square(side_length=cell * 0.95,
                              color=WHITE, stroke_width=1,
                              fill_opacity=0.15)
                sq.move_to(cell_center(i, j))
                grid_group.add(sq)
                lbl = MathTex(rf"{val}", font_size=20, color=WHITE
                                ).move_to(cell_center(i, j))
                grid_group.add(lbl)

        self.play(FadeIn(grid_group))

        k_tr = ValueTracker(0)

        def column_highlight():
            k = int(round(k_tr.get_value())) % p
            grp = VGroup()
            for i in range(1, p):
                # Fill column k in yellow if k == p-1 else blue
                col = YELLOW if k == p - 1 else BLUE
                sq = Square(side_length=cell * 0.95,
                              color=col, fill_opacity=0.55,
                              stroke_width=1.5)
                sq.move_to(cell_center(i, k))
                grp.add(sq)
                lbl = MathTex(rf"{table[i, k]}",
                                color=BLACK if k == p - 1 else WHITE,
                                font_size=22).move_to(cell_center(i, k))
                grp.add(lbl)
            return grp

        self.add(always_redraw(column_highlight))

        def info():
            k = int(round(k_tr.get_value())) % p
            return VGroup(
                MathTex(rf"p = {p}", color=WHITE, font_size=24),
                MathTex(rf"k = {k}", color=BLUE, font_size=24),
                MathTex(rf"\text{{column}} a^{{{k}}} \bmod {p}",
                         color=BLUE, font_size=20),
                MathTex(r"a^{p-1} \equiv 1 \pmod p",
                         color=YELLOW, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for kv in range(1, p):
            self.play(k_tr.animate.set_value(kv),
                       run_time=1.0, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.5)
