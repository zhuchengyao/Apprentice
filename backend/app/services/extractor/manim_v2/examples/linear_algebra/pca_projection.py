from manim import *
import numpy as np


class PCAProjectionExample(Scene):
    """
    PCA of 2D correlated data: 1st principal axis = direction of
    max variance; 2nd axis orthogonal. Projecting onto PC1 gives a
    1D approximation.

    SINGLE_FOCUS:
      Scatter of 80 points with covariance; PC1 + PC2 axes drawn.
      ValueTracker s_tr morphs each point along -PC2 direction until
      it lies on the PC1 axis (rank-1 reconstruction).
    """

    def construct(self):
        title = Tex(r"PCA: project onto max-variance axis",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 4, 1], y_range=[-3, 3, 1],
                             x_length=9, y_length=6,
                             background_line_style={"stroke_opacity": 0.25}
                             ).move_to([0, -0.3, 0])
        self.play(Create(plane))

        # Generate correlated 2D data
        rng = np.random.default_rng(11)
        N = 80
        cov = np.array([[3.0, 1.8], [1.8, 1.3]])
        L = np.linalg.cholesky(cov)
        raw = rng.normal(size=(N, 2))
        data = raw @ L.T

        # Compute PCA
        cov_emp = np.cov(data.T)
        evals, evecs = np.linalg.eigh(cov_emp)
        # sort descending
        order = np.argsort(evals)[::-1]
        evals = evals[order]
        evecs = evecs[:, order]
        pc1 = evecs[:, 0]
        pc2 = evecs[:, 1]

        # Project each point onto PC1: new = (data · pc1) * pc1
        proj = data @ pc1[:, None] * pc1[None, :]
        # Residual = data - proj (this direction is along PC2)

        s_tr = ValueTracker(0.0)

        def scatter():
            s = s_tr.get_value()
            grp = VGroup()
            for i in range(N):
                p = (1 - s) * data[i] + s * proj[i]
                grp.add(Dot(plane.c2p(p[0], p[1]),
                              color=YELLOW, radius=0.06))
            return grp

        self.add(always_redraw(scatter))

        # PC1 axis line (magenta)
        lim = 3.5
        pc1_line = Line(plane.c2p(-lim * pc1[0], -lim * pc1[1]),
                          plane.c2p(lim * pc1[0], lim * pc1[1]),
                          color=BLUE, stroke_width=3)
        pc2_line = Line(plane.c2p(-lim * pc2[0], -lim * pc2[1]),
                          plane.c2p(lim * pc2[0], lim * pc2[1]),
                          color=RED, stroke_width=2, stroke_opacity=0.5)
        self.play(Create(pc1_line), Create(pc2_line))

        # Labels
        pc1_lbl = Tex(r"PC$_1$", color=BLUE, font_size=20).move_to(
            plane.c2p(lim * pc1[0], lim * pc1[1]) + 0.25 * np.array([pc1[0], pc1[1], 0]))
        pc2_lbl = Tex(r"PC$_2$", color=RED, font_size=20).move_to(
            plane.c2p(lim * pc2[0], lim * pc2[1]) + 0.25 * np.array([pc2[0], pc2[1], 0]))
        self.play(Write(pc1_lbl), Write(pc2_lbl))

        def info():
            s = s_tr.get_value()
            return VGroup(
                MathTex(rf"s = {s:.2f}", color=YELLOW, font_size=22),
                MathTex(rf"\lambda_1 = {evals[0]:.2f}",
                         color=BLUE, font_size=22),
                MathTex(rf"\lambda_2 = {evals[1]:.2f}",
                         color=RED, font_size=22),
                MathTex(rf"\text{{var retained}} = {evals[0]/(evals[0]+evals[1]):.3f}",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UR, buff=0.5).shift(DOWN * 0.5)

        self.add(always_redraw(info))

        self.play(s_tr.animate.set_value(1.0),
                   run_time=4, rate_func=smooth)
        self.wait(0.4)
