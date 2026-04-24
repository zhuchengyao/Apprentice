from manim import *
import numpy as np


class SymmetriesOfSquareExample(Scene):
    def construct(self):
        title = Text("Dihedral group D₄: 8 symmetries of a square", font_size=28).to_edge(UP)
        self.play(Write(title))

        def square_with_markers(scale=0.9):
            sq = Square(side_length=1.4, color=BLUE, stroke_width=4).scale(scale)
            # Put colored corner dots so rotations/reflections are visible
            corners = sq.get_vertices()
            colors = [RED, GREEN, YELLOW, ORANGE]
            dots = VGroup(*[Dot(p, color=c, radius=0.09) for p, c in zip(corners, colors)])
            return VGroup(sq, dots)

        grid_entries = []
        grid_labels = ["e", "r", "r²", "r³", "s", "sr", "sr²", "sr³"]

        for idx, (label, op) in enumerate(zip(
            grid_labels,
            [
                lambda m: m,
                lambda m: m.rotate(PI / 2),
                lambda m: m.rotate(PI),
                lambda m: m.rotate(3 * PI / 2),
                lambda m: m.flip(RIGHT),
                lambda m: m.flip(RIGHT).rotate(PI / 2),
                lambda m: m.flip(RIGHT).rotate(PI),
                lambda m: m.flip(RIGHT).rotate(3 * PI / 2),
            ],
        )):
            cell = square_with_markers()
            op(cell)
            col = idx % 4
            row = idx // 4
            cell.move_to(np.array([-3.75 + col * 2.5, 0.9 - row * 2.2, 0]))
            lbl = MathTex(label, font_size=28).next_to(cell, DOWN, buff=0.1)
            grid_entries.append(VGroup(cell, lbl))

        self.play(LaggedStart(*[FadeIn(g) for g in grid_entries], lag_ratio=0.1))
        self.wait(0.3)

        caption = MathTex(r"|D_4| = 8 = 4\text{ rotations} + 4\text{ reflections}",
                          font_size=30, color=YELLOW).to_edge(DOWN)
        self.play(Write(caption))
        self.wait(0.6)
