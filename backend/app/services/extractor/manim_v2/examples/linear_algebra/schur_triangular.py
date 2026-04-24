from manim import *
import numpy as np


class SchurTriangularExample(Scene):
    """
    Schur decomposition: every real square matrix A is orthogonally
    similar to an upper quasi-triangular matrix T (2×2 blocks for
    complex eigenvalues). If A is symmetric: T is diagonal.

    Example A = [[4, -2, 1], [-2, 5, -3], [1, -3, 6]] (symmetric).
    Compute Q such that Qᵀ A Q = D diagonal.

    SINGLE_FOCUS: reveal matrix A, then rotate its entries via
    ValueTracker s_tr ∈ [0, 1] from A → (1-s)A + s·D morphing via
    orthogonal change of basis.
    """

    def construct(self):
        A = np.array([[4.0, -2.0, 1.0],
                      [-2.0, 5.0, -3.0],
                      [1.0, -3.0, 6.0]])
        evals, Q = np.linalg.eigh(A)
        D = np.diag(evals)

        title = Tex(r"Schur: $A = Q T Q^T$ with $T$ upper triangular",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        s_tr = ValueTracker(0.0)

        def current_matrix():
            s = s_tr.get_value()
            return (1 - s) * A + s * D

        def matrix_str():
            M = current_matrix()
            rows = []
            for i in range(3):
                cells = [f"{M[i, j]:+.2f}" for j in range(3)]
                rows.append(" & ".join(cells))
            return r"$\begin{pmatrix}" + r"\\".join(rows) + r"\end{pmatrix}$"

        mat_tex = Tex(matrix_str(), font_size=42)
        mat_tex.shift(LEFT * 2.5)
        self.add(mat_tex)

        def update_mat(mob, dt):
            new = Tex(matrix_str(), font_size=42).move_to(mat_tex)
            mat_tex.become(new)
            return mat_tex
        mat_tex.add_updater(update_mat)

        # Right: show Q and eigenvalues
        info = VGroup(
            Tex(r"symmetric $\Rightarrow T$ diagonal",
                color=YELLOW, font_size=22),
            Tex(r"$\lambda_i$ (eigenvalues):", font_size=22),
            Tex(rf"$\lambda_1={evals[0]:.3f}$", color=RED, font_size=22),
            Tex(rf"$\lambda_2={evals[1]:.3f}$", color=ORANGE, font_size=22),
            Tex(rf"$\lambda_3={evals[2]:.3f}$", color=GREEN, font_size=22),
            VGroup(Tex(r"morph $s=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"off-diagonals $\to 0$",
                color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.3)
        info[5][1].add_updater(lambda m: m.set_value(s_tr.get_value()))
        self.add(info)

        # Off-diagonal sum
        off_tex = Tex(r"$\sum_{i\ne j}|M_{ij}|=$",
                      font_size=22).next_to(mat_tex, DOWN, buff=0.5)
        off_val = DecimalNumber(0.0, num_decimal_places=4, font_size=22).set_color(
            RED).next_to(off_tex, RIGHT, buff=0.1)

        def off_diag_sum():
            M = current_matrix()
            return float(sum(abs(M[i, j]) for i in range(3) for j in range(3) if i != j))
        off_val.add_updater(lambda m: m.set_value(off_diag_sum()))
        self.add(off_tex, off_val)

        self.play(s_tr.animate.set_value(1.0),
                  run_time=5, rate_func=smooth)
        self.wait(0.8)
        self.play(s_tr.animate.set_value(0.0),
                  run_time=3, rate_func=smooth)
        self.wait(0.5)
