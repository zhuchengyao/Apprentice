from manim import *
import numpy as np


class ChiModFourMultiplicative(Scene):
    """The non-principal Dirichlet character mod 4:
    chi(n) = 0 if n even, +1 if n ≡ 1 mod 4, -1 if n ≡ 3 mod 4.
    Show a long strip of values; then verify multiplicativity chi(mn) =
    chi(m) chi(n) on a 3 x 3 table with m, n in {1, 3, 5, 7, 9}."""

    def construct(self):
        title = Tex(
            r"$\chi$ mod 4 and the identity $\chi(mn)=\chi(m)\chi(n)$",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        def chi(n):
            if n % 2 == 0:
                return 0
            return 1 if n % 4 == 1 else -1

        color_of = {0: GREY_B, 1: GREEN, -1: RED}
        sym_of = {0: "0", 1: "+1", -1: "-1"}

        strip = VGroup()
        for n in range(1, 17):
            cell = VGroup(
                Square(side_length=0.55, color=WHITE, stroke_width=1.5),
                Tex(str(n), font_size=22),
                MathTex(sym_of[chi(n)], font_size=22,
                        color=color_of[chi(n)]),
            )
            cell[1].next_to(cell[0], UP, buff=0.05)
            cell[2].move_to(cell[0])
            strip.add(cell)
        strip.arrange(RIGHT, buff=0.08).next_to(title, DOWN, buff=0.6)
        self.play(LaggedStart(*[FadeIn(c) for c in strip], lag_ratio=0.04,
                              run_time=1.8))

        ms = [1, 3, 5, 7, 9]
        ns = [1, 3, 5, 7, 9]
        cells = {}
        grid = VGroup()
        for i, m in enumerate(ms):
            for j, n in enumerate(ns):
                val = chi(m * n)
                cell = VGroup(
                    Square(side_length=0.5, color=WHITE, stroke_width=1),
                    MathTex(sym_of[val], font_size=22, color=color_of[val]),
                )
                cell[1].move_to(cell[0])
                cell.move_to([j * 0.55 - 1.2, -i * 0.55 - 0.4, 0])
                cells[(m, n)] = cell
                grid.add(cell)

        row_headers = VGroup(*[
            MathTex(f"m={m}", font_size=22).move_to(
                [-1.85, -i * 0.55 - 0.4, 0]
            )
            for i, m in enumerate(ms)
        ])
        col_headers = VGroup(*[
            MathTex(f"n={n}", font_size=22).move_to(
                [j * 0.55 - 1.2, 0.25, 0]
            )
            for j, n in enumerate(ns)
        ])
        table_block = VGroup(grid, row_headers, col_headers)
        table_block.shift(DOWN * 1.2 + LEFT * 1.5)
        self.play(FadeIn(row_headers), FadeIn(col_headers))
        self.play(LaggedStart(*[FadeIn(c) for c in grid], lag_ratio=0.02,
                              run_time=1.6))

        verify_box = VGroup(
            Tex(r"Spot-check: $\chi(3 \cdot 7) = \chi(21) = \chi(1)$?",
                font_size=26),
            MathTex(r"\chi(21) = +1 = (-1)(-1) = \chi(3)\chi(7) \ \checkmark",
                    font_size=26, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        verify_box.to_corner(DR, buff=0.4).shift(UP * 0.2)
        self.play(FadeIn(verify_box[0]))
        self.play(Indicate(cells[(3, 7)], color=YELLOW, scale_factor=1.4))
        self.play(Write(verify_box[1]))
        self.wait(1.3)
