from manim import *
import numpy as np


class PCAGaussianCloudExample(Scene):
    """
    PCA on 2D Gaussian cloud: compute principal axes via
    eigendecomposition of sample covariance; largest eigenvalue
    direction captures most variance.

    SINGLE_FOCUS: 200 sample points + both PC axes. Variance along
    each axis shown as colored band. ValueTracker s_tr rotates a
    probe direction and compares variance projected onto it.
    """

    def construct(self):
        title = Tex(r"PCA: maximize variance of $u^T X$ over unit $u$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-3, 3, 1], y_range=[-2.5, 2.5, 1],
                            x_length=8, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.2)
        self.play(Create(plane))

        np.random.seed(3)
        N = 200
        # Anisotropic Gaussian with eigenvalues 1.5, 0.4
        L = np.array([[1.5, 0], [0, 0.4]])
        theta_rot = PI / 6
        R_rot = np.array([[np.cos(theta_rot), -np.sin(theta_rot)],
                           [np.sin(theta_rot), np.cos(theta_rot)]])
        cov = R_rot @ L @ R_rot.T
        data = np.random.multivariate_normal([0, 0], cov, N)

        # Plot points
        for pt in data:
            self.add(Dot(plane.c2p(pt[0], pt[1]), color=BLUE, radius=0.04))

        # Sample covariance
        data_centered = data - data.mean(axis=0)
        S_cov = (data_centered.T @ data_centered) / (N - 1)
        evals, evecs = np.linalg.eigh(S_cov)
        # Largest first
        idx_sort = np.argsort(-evals)
        evals = evals[idx_sort]
        evecs = evecs[:, idx_sort]

        # Draw PC axes
        pc1 = evecs[:, 0] * np.sqrt(evals[0]) * 2
        pc2 = evecs[:, 1] * np.sqrt(evals[1]) * 2
        self.add(Line(plane.c2p(-pc1[0] * 1.5, -pc1[1] * 1.5),
                       plane.c2p(pc1[0] * 1.5, pc1[1] * 1.5),
                       color=RED, stroke_width=4))
        self.add(Line(plane.c2p(-pc2[0] * 1.5, -pc2[1] * 1.5),
                       plane.c2p(pc2[0] * 1.5, pc2[1] * 1.5),
                       color=GREEN, stroke_width=3))

        theta_tr = ValueTracker(0.0)

        def probe_line():
            t = theta_tr.get_value()
            u = np.array([np.cos(t), np.sin(t)])
            return Line(plane.c2p(-u[0] * 2.5, -u[1] * 2.5),
                         plane.c2p(u[0] * 2.5, u[1] * 2.5),
                         color=YELLOW, stroke_width=3)

        def probe_arrow():
            t = theta_tr.get_value()
            u = np.array([np.cos(t), np.sin(t)])
            return Arrow(plane.c2p(0, 0),
                          plane.c2p(u[0] * 2.0, u[1] * 2.0),
                          color=YELLOW, buff=0, stroke_width=4)

        self.add(always_redraw(probe_line), always_redraw(probe_arrow))

        def variance_proj():
            t = theta_tr.get_value()
            u = np.array([np.cos(t), np.sin(t)])
            proj = data_centered @ u
            return float(np.var(proj))

        info = VGroup(
            VGroup(Tex(r"$\theta=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=1,
                                 font_size=22).set_color(YELLOW),
                   Tex(r"$^\circ$", font_size=22)).arrange(RIGHT, buff=0.05),
            VGroup(Tex(r"Var$(u^TX)=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(rf"$\lambda_1={evals[0]:.3f}$ (RED)",
                color=RED, font_size=22),
            Tex(rf"$\lambda_2={evals[1]:.3f}$ (GREEN)",
                color=GREEN, font_size=22),
            Tex(r"PC1 direction maximizes variance",
                color=RED, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.3).shift(LEFT * 2)
        info[0][1].add_updater(lambda m: m.set_value(np.degrees(theta_tr.get_value())))
        info[1][1].add_updater(lambda m: m.set_value(variance_proj()))
        self.add(info)

        self.play(theta_tr.animate.set_value(PI),
                  run_time=8, rate_func=linear)
        self.wait(0.8)
