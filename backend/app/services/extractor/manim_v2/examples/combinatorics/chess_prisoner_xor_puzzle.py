from manim import *
import numpy as np
from functools import reduce
import operator


class ChessPrisonerXorPuzzle(Scene):
    """Two prisoners + 8x8 chessboard + one coin on each square.  Jailer
    picks a 'key' square (0..63).  Prisoner A sees the key, may flip
    exactly one coin, then leaves.  Prisoner B sees only the final board
    and must name the key square.  Solution: XOR of all 'heads' indices.
    Flipping the right coin nudges the board's XOR to equal the key."""

    def construct(self):
        title = Tex(
            r"Prisoner-coin puzzle: flip one coin to encode any of 64 keys",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        n = 8
        cell = 0.55
        rng = np.random.default_rng(3)
        initial = rng.integers(0, 2, size=(n, n))

        board = VGroup()
        cells = {}
        for i in range(n):
            for j in range(n):
                sq = Square(
                    side_length=cell, stroke_width=1,
                    stroke_color=GREY_B,
                    fill_color=GREY_D if (i + j) % 2 else GREY_B,
                    fill_opacity=0.8,
                )
                sq.move_to([
                    j * cell - n * cell / 2 + cell / 2,
                    -i * cell + n * cell / 2 - cell / 2,
                    0,
                ])
                idx_text = Tex(str(i * n + j), font_size=10,
                               color=GREY_A).move_to(sq)
                coin_color = GOLD if initial[i][j] else GREY_C
                coin = Circle(
                    radius=0.18,
                    color=coin_color,
                    fill_opacity=0.9,
                    stroke_width=1,
                ).move_to(sq)
                cells[(i, j)] = {"sq": sq, "coin": coin,
                                 "state": int(initial[i][j]),
                                 "idx_text": idx_text}
                board.add(sq, idx_text, coin)
        board.shift(LEFT * 3.0 + DOWN * 0.2)
        self.play(FadeIn(board))

        def heads_indices():
            return [i * n + j for i in range(n) for j in range(n)
                    if cells[(i, j)]["state"] == 1]

        def board_xor():
            return reduce(operator.xor, heads_indices(), 0)

        key = 42
        key_i, key_j = key // n, key % n
        key_sq = cells[(key_i, key_j)]["sq"]
        key_rect = SurroundingRectangle(
            key_sq, color=YELLOW, buff=0.01, stroke_width=3,
        )
        key_lab = Tex(rf"Key: square {key}", font_size=24,
                      color=YELLOW).move_to([3.2, 2.5, 0])
        self.play(Create(key_rect), Write(key_lab))

        initial_xor = board_xor()
        diff = initial_xor ^ key
        diff_i, diff_j = diff // n, diff % n

        panel = VGroup(
            MathTex(rf"\text{{XOR(heads)}} = {initial_xor}",
                    font_size=26, color=BLUE),
            MathTex(rf"\text{{key}} = {key}",
                    font_size=26, color=YELLOW),
            MathTex(
                rf"\text{{flip square: XOR}} \oplus \text{{key}} = {diff}",
                font_size=26, color=GREEN,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        panel.move_to([3.2, 0.8, 0])
        self.play(FadeIn(panel[0]))
        self.play(FadeIn(panel[1]))
        self.play(Write(panel[2]))

        flip_sq = cells[(diff_i, diff_j)]["sq"]
        flip_rect = SurroundingRectangle(
            flip_sq, color=GREEN, buff=0.02, stroke_width=3,
        )
        self.play(Create(flip_rect))

        coin = cells[(diff_i, diff_j)]["coin"]
        new_state = 1 - cells[(diff_i, diff_j)]["state"]
        new_color = GOLD if new_state else GREY_C
        self.play(coin.animate.set_color(new_color).scale(1.3),
                  run_time=0.6)
        self.play(coin.animate.scale(1 / 1.3), run_time=0.4)
        cells[(diff_i, diff_j)]["state"] = new_state

        final_xor = board_xor()
        verdict = MathTex(
            rf"\text{{new XOR(heads)}} = {final_xor} = \text{{key}}\ \checkmark",
            font_size=28, color=GREEN,
        ).next_to(panel, DOWN, buff=0.4)
        self.play(Write(verdict))
        self.wait(1.3)
