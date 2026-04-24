from manim import *
import numpy as np


class JordanNormalFormExample(Scene):
    """
    Jordan normal form: every A can be written as A = P J P^{-1}
    where J is block-diagonal with Jordan blocks. A Jordan block
    J_k(λ) is λ on diagonal and 1 on superdiagonal.

    SINGLE_FOCUS:
      Show matrix A and its Jordan form J for a specific 4×4 matrix
      with eigenvalue λ=2 of algebraic multiplicity 4 but geometric
      multiplicity 2. Two Jordan blocks J_2(2) and J_2(2).
    """

    def construct(self):
        title = Tex(r"Jordan normal form: $A = P J P^{-1}$, $J$ block-diagonal",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Matrix A with Jordan structure
        # J has two 2x2 blocks with eigenvalue 2:
        # J = [[2, 1, 0, 0], [0, 2, 0, 0], [0, 0, 2, 1], [0, 0, 0, 2]]
        J_matrix = np.array([
            [2, 1, 0, 0],
            [0, 2, 0, 0],
            [0, 0, 2, 1],
            [0, 0, 0, 2],
        ], dtype=float)

        # Random P (invertible)
        rng = np.random.default_rng(5)
        P_matrix = rng.normal(size=(4, 4)) + np.eye(4) * 2
        P_inv = np.linalg.inv(P_matrix)
        A_matrix = P_matrix @ J_matrix @ P_inv

        cell = 0.7

        def matrix_grid(M, origin, label, color):
            grp = VGroup()
            # Label
            lbl = Tex(label, color=color, font_size=26
                        ).move_to(origin + np.array([0, cell * 2.5, 0]))
            grp.add(lbl)
            # Cells
            for r in range(4):
                for c in range(4):
                    v = M[r, c]
                    # Highlight Jordan blocks on J
                    intensity = min(1.0, abs(v) / 2)
                    if label.startswith("J"):
                        if (r == 0 and c == 0) or (r == 1 and c == 1) or (r == 2 and c == 2) or (r == 3 and c == 3):
                            col = YELLOW
                            op = 0.7
                        elif (r == 0 and c == 1) or (r == 2 and c == 3):
                            col = ORANGE  # superdiagonal 1s
                            op = 0.85
                        else:
                            col = BLUE
                            op = 0.15
                    else:
                        col = color
                        op = 0.2 + 0.5 * intensity
                    sq = Square(side_length=cell * 0.9,
                                  color=col, fill_opacity=op,
                                  stroke_width=0.8)
                    sq.move_to(origin + np.array([c * cell - 1.5 * cell,
                                                       -r * cell + 1.5 * cell, 0]))
                    grp.add(sq)
                    lbl_v = MathTex(f"{v:.1f}", font_size=14,
                                      color=WHITE).move_to(
                        origin + np.array([c * cell - 1.5 * cell,
                                              -r * cell + 1.5 * cell, 0]))
                    grp.add(lbl_v)
            return grp

        A_grid = matrix_grid(A_matrix, np.array([-3, -0.3, 0]),
                               "A", GREEN)
        J_grid = matrix_grid(J_matrix, np.array([3, -0.3, 0]),
                               "J", YELLOW)
        self.play(FadeIn(A_grid), FadeIn(J_grid))

        # Highlight Jordan blocks
        block_highlight = VGroup(
            Rectangle(width=cell * 2 - 0.05,
                        height=cell * 2 - 0.05,
                        color=GREEN, stroke_width=3,
                        fill_opacity=0
                        ).move_to(J_grid[1].get_center()  # will reset
                                    )
        )
        # Just draw outlined rectangles around the two blocks:
        J_origin = np.array([3, -0.3, 0])
        block1 = Rectangle(width=cell * 2 + 0.05,
                             height=cell * 2 + 0.05,
                             color=GREEN, stroke_width=3,
                             fill_opacity=0
                             ).move_to(J_origin + np.array([cell * (-1.5 + 0.5),
                                                                 -cell * (-1.5 + 0.5), 0]))
        block2 = Rectangle(width=cell * 2 + 0.05,
                             height=cell * 2 + 0.05,
                             color=GREEN, stroke_width=3,
                             fill_opacity=0
                             ).move_to(J_origin + np.array([cell * (-1.5 + 2.5),
                                                                 -cell * (-1.5 + 2.5), 0]))
        self.play(Create(block1), Create(block2))

        # Transform animation: apply P^{-1} then P to show similarity
        s_tr = ValueTracker(0)

        info = VGroup(
            MathTex(r"\lambda = 2 \text{ (algebraic mult.\ 4)}",
                     color=YELLOW, font_size=22),
            MathTex(r"\text{geometric mult.} = 2",
                     color=GREEN, font_size=22),
            MathTex(r"J = J_2(2) \oplus J_2(2)",
                     color=ORANGE, font_size=22),
            Tex(r"superdiagonal 1s couple generalized eigenvectors",
                 color=WHITE, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.3)
        self.play(Write(info))
        self.wait(1.0)

        # Tiny animation: briefly flash the superdiagonal entries
        def flash_super():
            t = s_tr.get_value()
            alpha = 0.5 + 0.5 * np.sin(t * 2 * PI * 3)
            sq1 = Square(side_length=cell * 0.9,
                           color=ORANGE,
                           fill_opacity=alpha,
                           stroke_width=0.8)
            sq1.move_to(J_origin + np.array([cell * (-1.5 + 1),
                                                 -cell * (-1.5 + 0), 0]))
            sq2 = Square(side_length=cell * 0.9,
                           color=ORANGE,
                           fill_opacity=alpha,
                           stroke_width=0.8)
            sq2.move_to(J_origin + np.array([cell * (-1.5 + 3),
                                                 -cell * (-1.5 + 2), 0]))
            return VGroup(sq1, sq2)

        self.add(always_redraw(flash_super))
        self.play(s_tr.animate.set_value(1.0), run_time=3, rate_func=linear)
        self.wait(0.5)
