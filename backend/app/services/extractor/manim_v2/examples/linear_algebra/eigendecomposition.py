from manim import *
import numpy as np


class EigendecompositionExample(Scene):
    """
    Eigendecomposition: A = P D P⁻¹ visualized through the action of A.

    A 2D matrix A has two real eigenvectors v₁ (eigenvalue λ₁) and
    v₂ (eigenvalue λ₂). Apply A to:
      - generic vectors (rotate AND scale — direction changes)
      - eigenvectors (only scale — direction unchanged)

    LEFT plane: NumberPlane that morphs under ApplyMatrix(A) via
    ValueTracker s. Two eigenvector arrows + a generic vector all
    redraw each frame; the eigenvector arrows merely stretch along
    their span lines, while the generic arrow rotates.
    RIGHT column: live Mt = (1−s)·I + s·A matrix readout, plus the
    eigenvalue/eigenvector legend and the A = P D P⁻¹ formula.
    """

    def construct(self):
        title = Tex(r"Eigenvectors keep their direction; $A$ scales them by $\lambda$",
                    font_size=32).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # The matrix and its eigenstructure (chosen so eigenvalues are real and distinct)
        A = np.array([[3.0, 1.0],
                      [0.0, 2.0]])
        # Eigenvalues 3, 2; eigenvectors v1 = (1, 0); v2 = (1, -1)
        v1 = np.array([1.0, 0.0])
        v2 = np.array([1.0, -1.0]) / np.sqrt(2)
        lam1, lam2 = 3.0, 2.0

        # LEFT plane
        plane = NumberPlane(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=6.4, y_length=5.0,
            background_line_style={"stroke_opacity": 0.3},
        ).move_to([-2.6, -0.2, 0])
        self.play(Create(plane))

        s = ValueTracker(0.0)

        def Mt():
            sv = s.get_value()
            return (1 - sv) * np.eye(2) + sv * A

        def transform_pt(p2d: np.ndarray) -> np.ndarray:
            q = Mt() @ p2d
            return plane.c2p(q[0], q[1])

        # Eigenvector arrows (scaled to be visually distinct)
        v1_len_world = 1.6
        v2_len_world = 1.6

        def v1_arrow():
            end = transform_pt(v1_len_world * v1)
            return Arrow(plane.c2p(0, 0), end,
                         buff=0, color=GREEN, stroke_width=6,
                         max_tip_length_to_length_ratio=0.12)

        def v2_arrow():
            end = transform_pt(v2_len_world * v2)
            return Arrow(plane.c2p(0, 0), end,
                         buff=0, color=ORANGE, stroke_width=6,
                         max_tip_length_to_length_ratio=0.12)

        # Span lines (the eigenspace lines stay invariant)
        def span_line(direction: np.ndarray, color):
            far = direction / np.linalg.norm(direction) * 4.0
            return Line(plane.c2p(-far[0], -far[1]), plane.c2p(far[0], far[1]),
                        color=color, stroke_width=1.5, stroke_opacity=0.5)

        v1_span = span_line(v1, GREEN_E)
        v2_span = span_line(v2, ORANGE)
        self.play(Create(v1_span), Create(v2_span))

        # Generic vector (NOT an eigenvector) — rotates and scales
        generic = np.array([0.6, 1.4])

        def generic_arrow():
            end = transform_pt(generic)
            return Arrow(plane.c2p(0, 0), end,
                         buff=0, color=YELLOW, stroke_width=5,
                         max_tip_length_to_length_ratio=0.12)

        self.add(always_redraw(v1_arrow), always_redraw(v2_arrow),
                 always_redraw(generic_arrow))

        # Static labels for the arrows
        v1_lbl = MathTex(r"\vec v_1", color=GREEN, font_size=24).move_to(plane.c2p(0.5, -0.3))
        v2_lbl = MathTex(r"\vec v_2", color=ORANGE, font_size=24).move_to(plane.c2p(-0.5, -1.0))
        gen_lbl = MathTex(r"\vec u\ \text{(non-eigen)}", color=YELLOW,
                          font_size=20).move_to(plane.c2p(-1.3, 1.7))
        self.play(Write(v1_lbl), Write(v2_lbl), Write(gen_lbl))

        # RIGHT COLUMN
        rcol_x = +4.6

        def matrix_readout():
            sv = s.get_value()
            M = Mt()
            return MathTex(
                rf"M(s) = \begin{{bmatrix}} {M[0,0]:.2f} & {M[0,1]:.2f} \\ {M[1,0]:.2f} & {M[1,1]:.2f} \end{{bmatrix}}",
                color=WHITE, font_size=24,
            ).move_to([rcol_x, +2.5, 0])

        eigen_panel = VGroup(
            MathTex(r"\vec v_1 = (1, 0),\;\;\lambda_1 = 3", color=GREEN, font_size=22),
            MathTex(r"\vec v_2 = (1, -1)/\sqrt 2,\;\;\lambda_2 = 2", color=ORANGE, font_size=22),
            MathTex(r"A\vec v_i = \lambda_i \vec v_i", color=WHITE, font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([rcol_x, +1.0, 0])

        decomp_panel = VGroup(
            MathTex(r"A = P D P^{-1}", color=YELLOW, font_size=30),
            MathTex(r"P = [\vec v_1\,\vec v_2]", color=WHITE, font_size=22),
            MathTex(r"D = \mathrm{diag}(\lambda_1, \lambda_2)", color=WHITE, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([rcol_x, -1.5, 0])

        self.add(always_redraw(matrix_readout))
        self.play(Write(eigen_panel))

        # Forward and back so you see the morph clearly
        self.play(s.animate.set_value(1.0), run_time=4, rate_func=smooth)
        self.wait(0.4)
        self.play(s.animate.set_value(0.0), run_time=2, rate_func=smooth)
        self.wait(0.3)
        self.play(s.animate.set_value(0.7), run_time=2, rate_func=smooth)
        self.wait(0.3)

        self.play(Write(decomp_panel))
        self.wait(1.2)
