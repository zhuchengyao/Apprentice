from manim import *
import numpy as np


class KnightsTourExample(Scene):
    def construct(self):
        title = Text("Knight's tour: 64 L-shaped moves covering the board",
                     font_size=22).to_edge(UP)
        self.play(Write(title))

        board = VGroup()
        for r in range(8):
            for c in range(8):
                sq = Square(side_length=0.6).set_fill(
                    GREY_D if (r + c) % 2 == 0 else GREY_B, opacity=1,
                ).set_stroke(WHITE, width=1)
                sq.move_to([(c - 3.5) * 0.6, (3.5 - r) * 0.6, 0])
                board.add(sq)
        self.play(Create(board))

        tour = [(0, 0), (2, 1), (0, 2), (1, 0), (2, 2), (0, 1), (1, 3), (3, 2),
                (2, 0), (0, 3), (2, 4), (4, 3), (3, 1), (1, 2), (3, 3), (1, 4)]
        points = [np.array([(c - 3.5) * 0.6, (3.5 - r) * 0.6, 0]) for r, c in tour]
        path = VMobject(stroke_color=YELLOW, stroke_width=3)
        path.set_points_as_corners(points)
        knight = Dot(points[0], color=YELLOW, radius=0.12)

        self.play(FadeIn(knight))
        self.play(Create(path), MoveAlongPath(knight, path), run_time=5)
        self.wait(0.4)
