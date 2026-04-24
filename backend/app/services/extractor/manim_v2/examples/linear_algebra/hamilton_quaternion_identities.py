from manim import *
import numpy as np


class HamiltonQuaternionIdentities(Scene):
    """Hamilton's carving on Broom Bridge: i^2 = j^2 = k^2 = ijk = -1.
    Visualize the multiplication table of {1, i, j, k} and highlight the
    cyclic identities ij = k, jk = i, ki = j (and their reverses with
    sign flips).  Show the Broom-Bridge-style summary in a boxed panel."""

    def construct(self):
        title = Tex(
            r"Hamilton's quaternion identities: $i^2 = j^2 = k^2 = ijk = -1$",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        def q_mult(a, b):
            table = {
                ("1", "1"): ("+", "1"), ("1", "i"): ("+", "i"),
                ("1", "j"): ("+", "j"), ("1", "k"): ("+", "k"),
                ("i", "1"): ("+", "i"), ("i", "i"): ("-", "1"),
                ("i", "j"): ("+", "k"), ("i", "k"): ("-", "j"),
                ("j", "1"): ("+", "j"), ("j", "i"): ("-", "k"),
                ("j", "j"): ("-", "1"), ("j", "k"): ("+", "i"),
                ("k", "1"): ("+", "k"), ("k", "i"): ("+", "j"),
                ("k", "j"): ("-", "i"), ("k", "k"): ("-", "1"),
            }
            return table[(a, b)]

        basis = ["1", "i", "j", "k"]
        color_of = {"1": WHITE, "i": GREEN, "j": RED, "k": BLUE}

        cell = 0.9
        grid = VGroup()
        cells = {}
        for r, b in enumerate(basis):
            for c, a in enumerate(basis):
                sign, result = q_mult(b, a)
                color = color_of[result]
                if sign == "-":
                    color = RED
                sq = Square(side_length=cell, stroke_width=1.5,
                            color=WHITE)
                label = MathTex(
                    rf"{'-' if sign=='-' else ''}{result}",
                    font_size=26, color=color,
                )
                sq.move_to([c * cell - 1.5, -r * cell - 0.2, 0])
                label.move_to(sq)
                cells[(b, a)] = VGroup(sq, label)
                grid.add(VGroup(sq, label))

        row_headers = VGroup(*[
            MathTex(b, font_size=28, color=color_of[b]).move_to(
                [-1.5 - cell, -r * cell - 0.2, 0]
            )
            for r, b in enumerate(basis)
        ])
        col_headers = VGroup(*[
            MathTex(a, font_size=28, color=color_of[a]).move_to(
                [c * cell - 1.5, 0.35, 0]
            )
            for c, a in enumerate(basis)
        ])
        mult_sign = Tex(r"$b \cdot a$", font_size=24).move_to(
            [-1.5 - cell, 0.35, 0]
        )
        self.play(FadeIn(mult_sign))
        self.play(FadeIn(row_headers), FadeIn(col_headers))
        self.play(LaggedStart(*[FadeIn(c) for c in grid],
                              lag_ratio=0.03, run_time=2.5))

        cyclic = VGroup(
            MathTex(r"ij = k", font_size=28, color=BLUE),
            MathTex(r"jk = i", font_size=28, color=GREEN),
            MathTex(r"ki = j", font_size=28, color=RED),
            MathTex(r"ji = -k", font_size=28, color=RED),
            MathTex(r"kj = -i", font_size=28, color=RED),
            MathTex(r"ik = -j", font_size=28, color=RED),
        ).arrange_in_grid(rows=2, cols=3, buff=0.4)
        cyclic.to_edge(RIGHT, buff=0.4).shift(UP * 0.5)
        self.play(FadeIn(cyclic))

        for b, a in [("i", "j"), ("j", "k"), ("k", "i")]:
            self.play(Indicate(cells[(b, a)], color=YELLOW,
                               scale_factor=1.3), run_time=0.8)

        carving = MathTex(
            r"i^2 = j^2 = k^2 = ijk = -1",
            font_size=30, color=YELLOW,
        )
        carving.to_edge(DOWN, buff=0.3)
        box = SurroundingRectangle(carving, color=YELLOW,
                                   buff=0.2, stroke_width=3)
        self.play(Write(carving), Create(box))
        self.wait(1.5)
