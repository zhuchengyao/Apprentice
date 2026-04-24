from manim import *
import numpy as np


class LatinSquareExample(Scene):
    """
    Latin square: n×n array filled with n symbols so each row and
    each column contains every symbol exactly once. Count of Latin
    squares of order n is known for small n only.

    SINGLE_FOCUS:
      ValueTracker n_tr steps n=2, 3, 4, 5; show an example Latin
      square of each size with color-coded cells; live count.
    """

    def construct(self):
        title = Tex(r"Latin squares: $n \times n$ with each symbol once per row/col",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Known counts for n = 1..5: 1, 2, 12, 576, 161280
        counts = {1: 1, 2: 2, 3: 12, 4: 576, 5: 161280}

        # Example Latin squares
        squares = {
            2: [[0, 1], [1, 0]],
            3: [[0, 1, 2], [1, 2, 0], [2, 0, 1]],
            4: [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]],
            5: [[0, 1, 2, 3, 4], [1, 2, 3, 4, 0], [2, 3, 4, 0, 1],
                [3, 4, 0, 1, 2], [4, 0, 1, 2, 3]],
        }

        colors = [BLUE, GREEN, ORANGE, PURPLE, PINK]

        n_tr = ValueTracker(2)

        def square_cells():
            n = int(round(n_tr.get_value()))
            n = max(2, min(n, 5))
            sq = squares[n]
            cell = 0.6
            origin = np.array([-cell * (n - 1) / 2 - 1.5, -0.3, 0])
            grp = VGroup()
            for r in range(n):
                for c in range(n):
                    val = sq[r][c]
                    col = colors[val % len(colors)]
                    s = Square(side_length=cell * 0.9, color=col,
                                 fill_opacity=0.7, stroke_width=1.5)
                    s.move_to(origin + np.array([c * cell, -r * cell, 0]))
                    grp.add(s)
                    grp.add(MathTex(rf"{val + 1}", font_size=22,
                                      color=BLACK).move_to(s.get_center()))
            return grp

        self.add(always_redraw(square_cells))

        def info():
            n = int(round(n_tr.get_value()))
            n = max(2, min(n, 5))
            return VGroup(
                MathTex(rf"n = {n}", color=YELLOW, font_size=26),
                MathTex(rf"L(n) = {counts[n]:,}".replace(",", r"\,"),
                         color=GREEN, font_size=24),
                Tex(r"= \# distinct Latin squares",
                     color=GREEN, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for nv in [3, 4, 5, 2]:
            self.play(n_tr.animate.set_value(nv),
                       run_time=1.3, rate_func=smooth)
            self.wait(0.8)
        self.wait(0.4)
