from manim import *
import numpy as np


class RankNullityTheoremExample(Scene):
    """
    Rank-nullity theorem: for T: V → W, dim(ker T) + dim(im T) = dim V.
    Illustrate with 3×3 matrix of rank 2.

    SINGLE_FOCUS:
      A 3×3 matrix shown; compute rank = 2, so nullity = 1. Show a
      vector in ker (null space) and show its image = 0.
    """

    def construct(self):
        title = Tex(r"Rank-nullity: $\dim \ker T + \dim \text{im } T = \dim V$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Matrix A = [[1, 1, 0], [1, 0, 1], [0, -1, 1]] (rank 2)
        # Null vector: (1, 1, 1) → [1+1+0, 1+0+1, 0-1+1] = (2, 2, 0)?
        # Let me pick rank 2 matrix:
        # A = [[1, 2, 3], [2, 4, 6], [1, 1, 1]]
        # Row 2 = 2·Row 1, so rank ≤ 2. Row 1 and Row 3 independent, rank = 2.
        # Null space: Av = 0. Row echelon: [[1, 2, 3], [0, 0, 0], [0, -1, -2]]
        # So -y - 2z = 0 → y = -2z; x + 2y + 3z = 0 → x + 2(-2z) + 3z = 0 → x = z
        # So null space = span((1, -2, 1)).
        A = np.array([[1, 2, 3], [2, 4, 6], [1, 1, 1]], dtype=float)
        null_v = np.array([1, -2, 1], dtype=float)

        # Verify
        assert np.allclose(A @ null_v, 0)

        # Display matrix
        cell = 0.8
        M_origin = np.array([-4, 1.2, 0])

        def matrix_grid(M, origin, color, fs=22):
            grp = VGroup()
            for r in range(3):
                for c in range(3):
                    v = M[r, c]
                    sq = Square(side_length=cell * 0.9, color=color,
                                  fill_opacity=0.3, stroke_width=1.5)
                    sq.move_to(origin + np.array([c * cell, -r * cell, 0]))
                    grp.add(sq)
                    grp.add(MathTex(rf"{int(v)}", color=WHITE, font_size=fs
                                      ).move_to(sq.get_center()))
            return grp

        def vector_col(V, origin, color, fs=22):
            grp = VGroup()
            for r in range(3):
                sq = Square(side_length=cell * 0.9, color=color,
                              fill_opacity=0.3, stroke_width=1.5)
                sq.move_to(origin + np.array([0, -r * cell, 0]))
                grp.add(sq)
                grp.add(MathTex(rf"{int(V[r])}", color=WHITE, font_size=fs
                                  ).move_to(sq.get_center()))
            return grp

        A_grid = matrix_grid(A, M_origin, BLUE)
        A_lbl = MathTex(r"A", color=BLUE, font_size=24
                          ).move_to(M_origin + np.array([cell, 1.0, 0]))
        self.play(FadeIn(A_grid), Write(A_lbl))

        # Show A · null_v = 0
        v_origin = np.array([-0.5, 1.2, 0])
        v_grid = vector_col(null_v, v_origin, ORANGE)
        v_lbl = MathTex(r"v", color=ORANGE, font_size=24
                          ).move_to(v_origin + np.array([0, 1.0, 0]))
        self.play(FadeIn(v_grid), Write(v_lbl))

        eq_sign = MathTex(r"=", color=WHITE, font_size=30
                            ).move_to(np.array([1.2, 0.4, 0]))
        Av_grid = vector_col(A @ null_v, np.array([2.2, 1.2, 0]), GREEN)
        Av_lbl = MathTex(r"Av = 0", color=GREEN, font_size=22
                            ).move_to(np.array([2.2, 2.2, 0]))
        self.play(Write(eq_sign), FadeIn(Av_grid), Write(Av_lbl))

        step_tr = ValueTracker(0)

        def summary():
            s = int(round(step_tr.get_value()))
            grp = VGroup()
            if s >= 1:
                grp.add(MathTex(r"\text{rank}(A) = 2",
                                  color=BLUE, font_size=24))
            if s >= 2:
                grp.add(MathTex(r"\text{null}(A) = \text{span}\{(1, -2, 1)\} \Rightarrow \dim = 1",
                                  color=ORANGE, font_size=22))
            if s >= 3:
                grp.add(MathTex(r"2 + 1 = 3 = \dim V\ \checkmark",
                                  color=GREEN, font_size=26))
            if len(grp) > 0:
                grp.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
                grp.to_edge(DOWN, buff=0.3)
            return grp

        self.add(always_redraw(summary))

        for s in range(1, 4):
            self.play(step_tr.animate.set_value(s),
                       run_time=1.0, rate_func=smooth)
            self.wait(0.8)
        self.wait(0.4)
