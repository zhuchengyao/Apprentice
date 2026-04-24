from manim import *
import numpy as np


class TotalVarianceDecompExample(Scene):
    """
    Total variance decomposition (law of total variance):
    Var(Y) = E[Var(Y|X)] + Var(E[Y|X]).
    Explain via two groups with different means and variances.

    SINGLE_FOCUS:
      Two Gaussian "clusters" at different means; within-cluster
      variance (blue) + between-cluster variance of means (green).
      ValueTracker gap_tr separates the clusters; always_redraw
      verifies identity.
    """

    def construct(self):
        title = Tex(r"Var$(Y) = E[\text{Var}(Y|X)] + \text{Var}(E[Y|X])$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ax = Axes(x_range=[-5, 5, 1], y_range=[0, 0.6, 0.2],
                   x_length=10, y_length=4, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([0, -0.3, 0])
        self.play(Create(ax))

        sigma_in = 0.8  # within-cluster SD
        gap_tr = ValueTracker(0.0)  # distance of cluster means

        def gaussian(x, mu, sigma):
            return np.exp(-(x - mu) ** 2 / (2 * sigma ** 2)) / (sigma * np.sqrt(2 * PI))

        def density_curve():
            gap = gap_tr.get_value()
            mu1 = -gap / 2
            mu2 = gap / 2
            return ax.plot(lambda x: 0.5 * gaussian(x, mu1, sigma_in)
                                         + 0.5 * gaussian(x, mu2, sigma_in),
                            x_range=[-5, 5, 0.02],
                            color=BLUE, stroke_width=3)

        def cluster_curves():
            gap = gap_tr.get_value()
            mu1 = -gap / 2
            mu2 = gap / 2
            grp = VGroup()
            grp.add(ax.plot(lambda x: 0.5 * gaussian(x, mu1, sigma_in),
                              x_range=[-5, 5, 0.02],
                              color=GREEN, stroke_width=2,
                              stroke_opacity=0.55))
            grp.add(ax.plot(lambda x: 0.5 * gaussian(x, mu2, sigma_in),
                              x_range=[-5, 5, 0.02],
                              color=ORANGE, stroke_width=2,
                              stroke_opacity=0.55))
            # Cluster-mean markers
            grp.add(DashedLine(ax.c2p(mu1, 0), ax.c2p(mu1, 0.5),
                                 color=GREEN, stroke_width=2))
            grp.add(DashedLine(ax.c2p(mu2, 0), ax.c2p(mu2, 0.5),
                                 color=ORANGE, stroke_width=2))
            return grp

        self.add(always_redraw(cluster_curves), always_redraw(density_curve))

        def info():
            gap = gap_tr.get_value()
            within = sigma_in ** 2  # E[Var(Y|X)] = σ² (constant)
            between = (gap ** 2) / 4  # Var(E[Y|X]) = Var(X·μ) with 50/50
            # Actually for Bernoulli(0.5): Var of (μ1, μ2) each with prob 1/2 = (μ1 - μ2)²/4
            total = within + between
            return VGroup(
                MathTex(rf"\text{{gap}} = {gap:.2f}",
                         color=YELLOW, font_size=22),
                MathTex(rf"E[\text{{Var}}(Y|X)] = \sigma^2 = {within:.3f}",
                         color=GREEN, font_size=18),
                MathTex(rf"\text{{Var}}(E[Y|X]) = {between:.3f}",
                         color=ORANGE, font_size=18),
                MathTex(rf"\text{{total Var}}(Y) = {total:.3f}",
                         color=BLUE, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.3).shift(UP * 0.5)

        self.add(always_redraw(info))

        self.play(gap_tr.animate.set_value(3.0),
                   run_time=4, rate_func=smooth)
        self.wait(0.5)
        self.play(gap_tr.animate.set_value(0.5),
                   run_time=2, rate_func=smooth)
        self.wait(0.4)
