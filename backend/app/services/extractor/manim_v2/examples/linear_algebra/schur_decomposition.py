from manim import *
import numpy as np


class SchurDecompositionExample(Scene):
    """
    Schur decomposition: every square matrix A = Q T Q* with Q
    unitary and T upper-triangular. Visualize via Givens-rotation
    steps zeroing out subdiagonal entries of a specific 4×4 matrix.

    SINGLE_FOCUS:
      4×4 matrix as colored cells; ValueTracker step_tr applies QR-
      style rotations; always_redraw cells; subdiagonal → 0 giving
      upper-triangular T.
    """

    def construct(self):
        title = Tex(r"Schur decomposition: $A = Q T Q^*$, $T$ upper-triangular",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Sample 4x4 matrix and its Schur form (precomputed)
        rng = np.random.default_rng(3)
        A0 = rng.normal(size=(4, 4))
        # Compute Schur via numpy (for the target T)
        T_final, Z = np.linalg.qr(A0)  # QR as a proxy (not Schur, but visually similar)
        # Actually run a few QR iterations for Schur-like decomp:
        M = A0.copy()
        snapshots = [M.copy()]
        for _ in range(15):
            Q, R = np.linalg.qr(M)
            M = R @ Q
            snapshots.append(M.copy())

        cell = 0.8
        origin = np.array([-cell * 2, cell * 1.5, 0])

        def cell_center(r, c):
            return origin + np.array([c * cell, -r * cell, 0])

        step_tr = ValueTracker(0)

        def matrix_cells():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, len(snapshots) - 1))
            M = snapshots[s]
            grp = VGroup()
            for r in range(4):
                for c in range(4):
                    val = M[r, c]
                    # Color subdiagonal by how close to 0
                    if r > c:
                        # Subdiagonal: we want → 0
                        intensity = min(1.0, abs(val) / 2)
                        col = interpolate_color(GREEN, RED, intensity)
                    elif r <= c:
                        col = BLUE
                    sq = Square(side_length=cell * 0.9,
                                  color=col, fill_opacity=0.4 + 0.4 * min(1.0, abs(val) / 2),
                                  stroke_width=1)
                    sq.move_to(cell_center(r, c))
                    grp.add(sq)
                    lbl = MathTex(rf"{val:.2f}", font_size=16,
                                    color=WHITE).move_to(cell_center(r, c))
                    grp.add(lbl)
            return grp

        self.add(always_redraw(matrix_cells))

        def info():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, len(snapshots) - 1))
            M = snapshots[s]
            sub_norm = np.linalg.norm(np.tril(M, -1))
            return VGroup(
                MathTex(rf"\text{{QR iter}} = {s}/{len(snapshots) - 1}",
                         color=YELLOW, font_size=22),
                MathTex(rf"\|\text{{subdiag}}\| = {sub_norm:.4f}",
                         color=RED, font_size=22),
                Tex(r"GREEN: subdiag $\to 0$ (upper-triangular)",
                     color=GREEN, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.3).shift(UP * 0.5)

        self.add(always_redraw(info))

        for s in [3, 6, 10, 15]:
            self.play(step_tr.animate.set_value(s),
                       run_time=1.5, rate_func=smooth)
            self.wait(0.6)
        self.wait(0.4)
