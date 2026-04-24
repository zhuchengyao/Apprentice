from manim import *
import numpy as np


class SingularValueDecompositionExample(Scene):
    """
    SVD geometric interpretation: A = UΣV^T decomposes any linear
    map into rotation V^T, scaling Σ, rotation U. A unit circle is
    mapped to an ellipse with axes σ_1, σ_2.

    SINGLE_FOCUS:
      2D plane; ValueTracker s_tr morphs identity → V^T → ΣV^T → UΣV^T.
      Unit circle transformed stage by stage; singular values shown.
    """

    def construct(self):
        title = Tex(r"SVD: $A = U \Sigma V^\top$ (rotate, scale, rotate)",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 4, 1], y_range=[-3, 3, 1],
                             x_length=9, y_length=6,
                             background_line_style={"stroke_opacity": 0.25}
                             ).move_to([0, -0.3, 0])
        self.play(Create(plane))

        # Specific matrix A = [[2, 1], [0, 1]]
        A = np.array([[2.0, 1.0], [0.0, 1.0]])
        U, S, Vt = np.linalg.svd(A)

        s_tr = ValueTracker(0.0)

        def stage_matrix():
            s = s_tr.get_value()
            if s <= 1.0:
                # Interpolate identity → V^T
                return (1 - s) * np.eye(2) + s * Vt
            elif s <= 2.0:
                # Apply scaling from Σ on top of V^T
                t = s - 1
                Sigma = np.diag([1 + t * (S[0] - 1), 1 + t * (S[1] - 1)])
                return Sigma @ Vt
            else:
                # Apply U rotation on top of ΣV^T
                t = s - 2
                U_interp = (1 - t) * np.eye(2) + t * U
                return U_interp @ np.diag(S) @ Vt

        def transformed_shape():
            M = stage_matrix()
            pts_out = []
            for theta in np.linspace(0, 2 * PI, 100):
                v = np.array([np.cos(theta), np.sin(theta)])
                w = M @ v
                pts_out.append(plane.c2p(w[0], w[1]))
            m = VMobject(color=YELLOW, stroke_width=3)
            m.set_points_as_corners(pts_out + [pts_out[0]])
            return m

        def basis_arrows():
            M = stage_matrix()
            e1 = M[:, 0]
            e2 = M[:, 1]
            grp = VGroup()
            grp.add(Arrow(plane.c2p(0, 0),
                            plane.c2p(e1[0], e1[1]),
                            color=RED, buff=0, stroke_width=5,
                            max_tip_length_to_length_ratio=0.15))
            grp.add(Arrow(plane.c2p(0, 0),
                            plane.c2p(e2[0], e2[1]),
                            color=BLUE, buff=0, stroke_width=5,
                            max_tip_length_to_length_ratio=0.15))
            return grp

        self.add(always_redraw(transformed_shape),
                  always_redraw(basis_arrows))

        def info():
            s = s_tr.get_value()
            if s <= 1.0:
                stage = r"1. V^\top (rotate)"
                col = BLUE
            elif s <= 2.0:
                stage = r"2. \Sigma (scale)"
                col = GREEN
            else:
                stage = r"3. U (rotate)"
                col = RED
            return VGroup(
                MathTex(rf"s = {s:.2f}", color=YELLOW, font_size=24),
                MathTex(stage, color=col, font_size=22),
                MathTex(rf"\sigma_1 = {S[0]:.3f}",
                         color=GREEN, font_size=22),
                MathTex(rf"\sigma_2 = {S[1]:.3f}",
                         color=GREEN, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.3).shift(UP * 0.5)

        self.add(always_redraw(info))

        self.play(s_tr.animate.set_value(1.0),
                   run_time=2.5, rate_func=smooth)
        self.wait(0.4)
        self.play(s_tr.animate.set_value(2.0),
                   run_time=2.5, rate_func=smooth)
        self.wait(0.4)
        self.play(s_tr.animate.set_value(3.0),
                   run_time=2.5, rate_func=smooth)
        self.wait(0.4)
