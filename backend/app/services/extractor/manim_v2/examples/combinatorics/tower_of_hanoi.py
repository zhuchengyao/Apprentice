from manim import *


class TowerOfHanoiExample(Scene):
    """
    3-disk Tower of Hanoi solved in 2^n − 1 = 7 moves via the
    recursive min-strategy. Animation uses Transform on the disk
    positions so the move-count solution is visible end-to-end.
    """

    def construct(self):
        title = Tex(r"Tower of Hanoi, 3 disks: $2^n - 1 = 7$ moves",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        peg_y = -2.2
        peg_xs = [-3.5, 0, 3.5]
        base = Line([-5.5, peg_y, 0], [5.5, peg_y, 0], color=WHITE,
                     stroke_width=3)
        pegs = VGroup(*[Line([x, peg_y, 0], [x, peg_y + 2.2, 0],
                                color=WHITE, stroke_width=4)
                         for x in peg_xs])
        self.play(Create(base), Create(pegs))

        def make_disk(size, color):
            return Rectangle(width=0.6 + 0.6 * size, height=0.42,
                              color=color, fill_opacity=0.85, stroke_width=2)

        disks = {
            3: make_disk(3, BLUE_D).move_to([peg_xs[0], peg_y + 0.21, 0]),
            2: make_disk(2, TEAL).move_to([peg_xs[0], peg_y + 0.63, 0]),
            1: make_disk(1, GREEN).move_to([peg_xs[0], peg_y + 1.05, 0]),
        }
        self.play(*[FadeIn(d) for d in disks.values()])

        # Recursive solution of 3-disk from peg 0 to peg 2
        def moves(n, src, dst, aux):
            if n == 1:
                return [(1 if n == 1 else None, src, dst)]
            return (moves(n - 1, src, aux, dst)
                     + [(n, src, dst)]
                     + moves(n - 1, aux, dst, src))

        move_list = moves(3, 0, 2, 1)
        peg_stacks = {0: [3, 2, 1], 1: [], 2: []}
        move_lbls = VGroup()
        move_counter = MathTex(r"\text{move } 0 / 7",
                                color=YELLOW, font_size=26
                                ).to_edge(RIGHT, buff=0.4).shift(UP * 0.7)
        self.play(Write(move_counter))

        for i, (disk, src, dst) in enumerate(move_list, start=1):
            # Remove from src peg
            peg_stacks[src].remove(disk)
            # Compute new y on dst peg
            new_y = peg_y + 0.21 + len(peg_stacks[dst]) * 0.42
            peg_stacks[dst].append(disk)

            lbl = MathTex(rf"\text{{disk }}{disk}: {src+1} \to {dst+1}",
                           color=ORANGE, font_size=24
                           ).to_edge(RIGHT, buff=0.4).shift(UP * 0.2 + DOWN * i * 0.4 * 0)

            # Raise disk above pegs, move horizontally, drop
            up = np.array([disks[disk].get_center()[0], peg_y + 2.4, 0])
            over = np.array([peg_xs[dst], peg_y + 2.4, 0])
            drop = np.array([peg_xs[dst], new_y, 0])
            self.play(disks[disk].animate.move_to(up), run_time=0.25)
            self.play(disks[disk].animate.move_to(over), run_time=0.35)
            self.play(disks[disk].animate.move_to(drop), run_time=0.25)

            new_counter = MathTex(rf"\text{{move }} {i} / 7",
                                    color=YELLOW, font_size=26
                                    ).to_edge(RIGHT, buff=0.4).shift(UP * 0.7)
            self.play(Transform(move_counter, new_counter), run_time=0.1)

        # Final formula note
        note = MathTex(r"T(n) = 2 T(n-1) + 1 \Rightarrow T(n) = 2^n - 1",
                        color=GREEN, font_size=26
                        ).to_edge(DOWN, buff=0.5)
        self.play(Write(note))
        self.wait(0.5)


import numpy as np
