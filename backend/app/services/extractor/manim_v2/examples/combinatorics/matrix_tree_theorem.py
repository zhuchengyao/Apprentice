from manim import *
import numpy as np


class MatrixTreeTheoremExample(Scene):
    """
    Matrix-tree theorem (Kirchhoff): the number of spanning trees of
    a graph equals any cofactor of the Laplacian matrix L = D - A.

    SINGLE_FOCUS:
      4-vertex complete graph K_4; compute L, display, strike out
      one row+column, compute determinant. Cayley's formula says
      K_n has n^(n-2) spanning trees = 16 for n=4.
    """

    def construct(self):
        title = Tex(r"Matrix-tree theorem: $\det L_{ii} = \#$ spanning trees",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # K_4 graph on left
        n = 4
        positions = [
            np.array([-4, 1, 0]),
            np.array([-3, -1, 0]),
            np.array([-5, -1, 0]),
            np.array([-4, -2.5, 0]),
        ]

        edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
        edge_group = VGroup()
        for (i, j) in edges:
            edge_group.add(Line(positions[i], positions[j],
                                  color=BLUE, stroke_width=2))
        vertex_group = VGroup()
        for i, p in enumerate(positions):
            c = Circle(radius=0.22, color=YELLOW,
                         fill_opacity=0.6, stroke_width=1.5
                         ).move_to(p)
            lbl = MathTex(rf"{i + 1}", font_size=18, color=BLACK
                            ).move_to(p)
            vertex_group.add(c, lbl)
        self.play(Create(edge_group), FadeIn(vertex_group))

        graph_lbl = Tex(r"$K_4$", color=YELLOW, font_size=24
                         ).move_to([-4, 2, 0])
        self.play(Write(graph_lbl))

        # Laplacian L = D - A; for K_n, D = (n-1)I, A = J - I, so
        # L = nI - J (where J is all-1s matrix).
        L = n * np.eye(n) - np.ones((n, n))

        # Display L as a matrix on right
        cell = 0.7
        L_origin = np.array([3.5, 0.5, 0])

        def matrix_cells(L_mat, origin, highlight_row=None, highlight_col=None):
            grp = VGroup()
            for r in range(L_mat.shape[0]):
                for c in range(L_mat.shape[1]):
                    if highlight_row is not None and r == highlight_row:
                        col = RED
                        op = 0.4
                    elif highlight_col is not None and c == highlight_col:
                        col = RED
                        op = 0.4
                    else:
                        col = BLUE
                        op = 0.3
                    sq = Square(side_length=cell * 0.9, color=col,
                                  fill_opacity=op, stroke_width=0.8)
                    sq.move_to(origin + np.array([c * cell - 1.5 * cell,
                                                       -r * cell + 1.5 * cell, 0]))
                    grp.add(sq)
                    v = L_mat[r, c]
                    lbl = MathTex(rf"{int(v) if v == int(v) else v:.0f}",
                                    color=WHITE, font_size=20
                                    ).move_to(sq.get_center())
                    grp.add(lbl)
            return grp

        L_grid = matrix_cells(L, L_origin)
        L_lbl = MathTex(r"L = D - A", color=BLUE, font_size=22
                          ).move_to(L_origin + np.array([0, 1.8 * cell, 0]))
        self.play(Write(L_lbl), FadeIn(L_grid))

        step_tr = ValueTracker(0)

        def struck_grid():
            s = int(round(step_tr.get_value()))
            if s < 1:
                return VGroup()
            # Strike out row 0 and col 0
            return matrix_cells(L, L_origin, highlight_row=0, highlight_col=0)

        self.add(always_redraw(struck_grid))

        # Cofactor = det of 3x3 remaining submatrix
        L_sub = L[1:, 1:]
        det_val = int(round(np.linalg.det(L_sub)))

        def result_text():
            s = int(round(step_tr.get_value()))
            if s < 2:
                return VGroup()
            return VGroup(
                MathTex(rf"\det L_{{11}} = {det_val}",
                         color=YELLOW, font_size=24),
                MathTex(r"\text{Cayley: } n^{n-2} = 4^2 = 16",
                         color=GREEN, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(result_text))

        self.play(step_tr.animate.set_value(1), run_time=1.0)
        self.wait(1.0)
        self.play(step_tr.animate.set_value(2), run_time=1.0)
        self.wait(1.0)
