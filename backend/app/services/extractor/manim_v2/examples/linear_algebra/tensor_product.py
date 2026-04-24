from manim import *
import numpy as np


class TensorProductExample(Scene):
    """
    Tensor (Kronecker) product: A ⊗ B is a block matrix where each
    a_ij is replaced by a_ij·B. For 2×2 matrices, result is 4×4.

    SINGLE_FOCUS:
      Matrices A (2×2), B (2×2), then A ⊗ B (4×4). ValueTracker
      step_tr reveals block-by-block construction.
    """

    def construct(self):
        title = Tex(r"Kronecker product: $A \otimes B$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        A = np.array([[1, 2], [3, 4]], dtype=float)
        B = np.array([[0, 1], [1, 0]], dtype=float)
        AB = np.kron(A, B)

        cell = 0.55

        # A matrix on left
        A_origin = np.array([-5, 1, 0])
        A_grid = VGroup()
        for r in range(2):
            for c in range(2):
                sq = Square(side_length=cell * 0.9, color=BLUE,
                              fill_opacity=0.4, stroke_width=1.5)
                sq.move_to(A_origin + np.array([c * cell, -r * cell, 0]))
                A_grid.add(sq)
                A_grid.add(MathTex(rf"{int(A[r, c])}", color=WHITE,
                                      font_size=22
                                      ).move_to(A_origin + np.array([c * cell, -r * cell, 0])))
        A_lbl = MathTex(r"A", color=BLUE, font_size=26
                          ).move_to(A_origin + np.array([cell * 0.5, cell * 1.2, 0]))
        self.play(FadeIn(A_grid), Write(A_lbl))

        # B matrix
        B_origin = np.array([-2, 1, 0])
        B_grid = VGroup()
        for r in range(2):
            for c in range(2):
                sq = Square(side_length=cell * 0.9, color=ORANGE,
                              fill_opacity=0.4, stroke_width=1.5)
                sq.move_to(B_origin + np.array([c * cell, -r * cell, 0]))
                B_grid.add(sq)
                B_grid.add(MathTex(rf"{int(B[r, c])}", color=WHITE,
                                      font_size=22
                                      ).move_to(B_origin + np.array([c * cell, -r * cell, 0])))
        B_lbl = MathTex(r"B", color=ORANGE, font_size=26
                          ).move_to(B_origin + np.array([cell * 0.5, cell * 1.2, 0]))
        self.play(FadeIn(B_grid), Write(B_lbl))

        otimes = MathTex(r"\otimes", color=WHITE, font_size=32
                           ).move_to([-3.5, 1 - cell * 0.5, 0])
        equals = MathTex(r"=", color=WHITE, font_size=32
                           ).move_to([-0.5, 1 - cell * 0.5, 0])
        self.play(Write(otimes), Write(equals))

        # A⊗B matrix on right, built block by block
        AB_origin = np.array([3, 1.5, 0])

        step_tr = ValueTracker(0)

        def AB_blocks():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, 4))  # 4 blocks
            grp = VGroup()
            for block_idx in range(s):
                block_r = block_idx // 2
                block_c = block_idx % 2
                a_ij = A[block_r, block_c]
                # Fill the 2×2 block at (block_r, block_c)
                for r in range(2):
                    for c in range(2):
                        global_r = block_r * 2 + r
                        global_c = block_c * 2 + c
                        v = a_ij * B[r, c]
                        sq = Square(side_length=cell * 0.9,
                                      color=GREEN, fill_opacity=0.45,
                                      stroke_width=1.5)
                        sq.move_to(AB_origin + np.array([
                            global_c * cell - cell * 1.5,
                            -global_r * cell + cell * 1.5, 0]))
                        grp.add(sq)
                        grp.add(MathTex(rf"{int(v)}", color=WHITE,
                                          font_size=20
                                          ).move_to(AB_origin + np.array([
                            global_c * cell - cell * 1.5,
                            -global_r * cell + cell * 1.5, 0])))
                # Outline block
                block_outline = Rectangle(
                    width=cell * 2, height=cell * 2,
                    color=YELLOW, stroke_width=3, fill_opacity=0
                ).move_to(AB_origin + np.array([
                    block_c * 2 * cell + cell * 0.5 - cell * 1.5,
                    -block_r * 2 * cell - cell * 0.5 + cell * 1.5, 0]))
                grp.add(block_outline)
            return grp

        self.add(always_redraw(AB_blocks))

        AB_lbl = MathTex(r"A \otimes B", color=GREEN, font_size=26
                            ).move_to(AB_origin + np.array([cell, cell * 1.8, 0]))
        self.play(Write(AB_lbl))

        def step_label():
            s = int(round(step_tr.get_value()))
            return MathTex(rf"\text{{block}} = {s}/4",
                             color=YELLOW, font_size=22
                             ).to_edge(DOWN, buff=0.4)

        self.add(always_redraw(step_label))

        for s in range(1, 5):
            self.play(step_tr.animate.set_value(s),
                       run_time=1.0, rate_func=smooth)
            self.wait(0.7)
        self.wait(0.5)
