from manim import *
import numpy as np


class ColumnSpaceRankTourExample(Scene):
    """
    Column space = span of A's columns. Rank = dimension of col space.
    Tour 4 matrices with rank 3, 2, 1, 0 showing column-space dim.

    Example: 3×3 matrices chosen to have each rank.
    """

    def construct(self):
        title = Tex(r"Column space = span of columns; rank = its dimension",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        configs = [
            ("Rank 3 (full)", BLUE,
             np.array([[1, 1, 0], [0, 1, 1], [1, 0, 1]], dtype=float)),
            ("Rank 2 (plane)", GREEN,
             np.array([[1, 1, 0], [0, 1, 1], [-1, -2, -1]], dtype=float)),
            ("Rank 1 (line)", ORANGE,
             np.array([[1, 1, 0], [2, 2, 0], [3, 3, 0]], dtype=float)),
            ("Rank 0 (point)", RED,
             np.zeros((3, 3))),
        ]

        # Display matrix + rank annotation; cycle through with ValueTracker
        idx_tr = ValueTracker(0.0)

        def k_now():
            return max(0, min(3, int(round(idx_tr.get_value()))))

        def matrix_display():
            k = k_now()
            name, col, A = configs[k]
            entries = [[int(A[i, j]) for j in range(3)] for i in range(3)]
            m = Matrix(entries).set_color(col)
            return m

        def title_display():
            k = k_now()
            name, col, _ = configs[k]
            return Tex(name, color=col, font_size=32).move_to(UP * 2)

        mat_tex = matrix_display().shift(LEFT * 3)
        self.add(mat_tex)
        def update_mat(mob, dt):
            new = matrix_display().move_to(mat_tex)
            mat_tex.become(new)
            return mat_tex
        mat_tex.add_updater(update_mat)

        title_tex = title_display()
        self.add(title_tex)
        def update_title(mob, dt):
            new = title_display().move_to(title_tex)
            title_tex.become(new)
            return title_tex
        title_tex.add_updater(update_title)

        # Description
        def desc_str():
            k = k_now()
            descs = [
                r"columns span all of $\mathbb{R}^3$",
                r"columns span a 2D plane in $\mathbb{R}^3$",
                r"columns span a 1D line in $\mathbb{R}^3$",
                r"all columns are zero $\Rightarrow$ span $\{\vec 0\}$",
            ]
            return descs[k]

        desc = Tex(desc_str(), color=WHITE, font_size=24).shift(RIGHT * 2 + DOWN * 0.3)
        self.add(desc)
        def update_desc(mob, dt):
            new = Tex(desc_str(), color=WHITE, font_size=24).move_to(desc)
            desc.become(new)
            return desc
        desc.add_updater(update_desc)

        # Rank panel on right
        rank_tex = VGroup(
            Tex(r"rank = dim(col space)", font_size=22),
            Tex(r"full rank $\Leftrightarrow$ invertible",
                color=GREEN, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.4).shift(LEFT * 3)
        self.add(rank_tex)

        for k in range(1, 4):
            self.play(idx_tr.animate.set_value(float(k)),
                      run_time=1.8, rate_func=smooth)
            self.wait(0.6)
        self.wait(0.8)
