from manim import *
import numpy as np


class EverywhereScalesBySameFactorExample(Scene):
    """
    Apply A = [[1, -1], [0.5, 1]] (det = 1.5) to a plane tiled with
    6 squares of various sizes and positions. Each square's area
    scales by the SAME factor 1.5 — so this property doesn't depend
    on the square's size or location.

    SINGLE_FOCUS: ValueTracker t_tr applies transformation.
    """

    def construct(self):
        title = Tex(r"All shapes scale by same factor (the determinant)",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 5, 1], y_range=[-3, 3, 1],
                            x_length=9, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.1)
        self.play(Create(plane))

        A = np.array([[1.0, -1.0], [0.5, 1.0]])
        det_A = float(np.linalg.det(A))

        # 6 squares with positions and side lengths
        squares_info = [
            (np.array([2.0, 1.0]), 1.0, BLUE),
            (np.array([-2.5, 0.5]), 2.0, GREEN),
            (np.array([-1.8, -1.0]), 0.5, ORANGE),
            (np.array([3.0, 2.0]), 1.5, RED),
            (np.array([1.0, -1.5]), 0.25, PURPLE),
            (np.array([-2.5, -2.0]), 1.0, TEAL),
        ]

        t_tr = ValueTracker(0.0)

        def M_of():
            t = t_tr.get_value()
            return (1 - t) * np.eye(2) + t * A

        def squares():
            M = M_of()
            grp = VGroup()
            for pos, side, col in squares_info:
                corners = [pos + np.array([dx * side / 2, dy * side / 2])
                            for dx, dy in [(-1, -1), (1, -1), (1, 1), (-1, 1)]]
                corners_after = [plane.c2p(*(M @ c)) for c in corners]
                grp.add(Polygon(*corners_after, color=col,
                                 stroke_width=2,
                                 fill_color=col, fill_opacity=0.5))
            return grp

        self.add(always_redraw(squares))

        info = VGroup(
            Tex(r"$A=\begin{pmatrix}1&-1\\0.5&1\end{pmatrix}$", font_size=24),
            Tex(rf"$\det A={det_A:.1f}$", color=YELLOW, font_size=24),
            Tex(r"every shape area $\to 1.5\cdot$(original)",
                color=GREEN, font_size=22),
            VGroup(Tex(r"$t=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22).set_color(BLUE)
                   ).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.3)
        info[3][1].add_updater(lambda m: m.set_value(t_tr.get_value()))
        self.add(info)

        self.play(t_tr.animate.set_value(1.0), run_time=3.5, rate_func=smooth)
        self.wait(0.8)
