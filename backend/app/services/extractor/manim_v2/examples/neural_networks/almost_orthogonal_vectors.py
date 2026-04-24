from manim import *
import numpy as np


class AlmostOrthogonalVectorsExample(Scene):
    """
    In high dimensions, random unit vectors are almost orthogonal
    (adapted from _2024/transformers/almost_orthogonal): for
    v, w ~ Uniform(S^{d-1}), E[cos²(angle)] = 1/d, so angles cluster
    near 90°.

    TWO_COLUMN:
      LEFT  — histogram of angles between 200 random unit vectors in
              dimension d; ValueTracker d_tr steps d = 2, 3, 5, 10, 50, 200.
              Curve narrows around 90° as d grows.
      RIGHT — live d, mean angle, stdev, and the √(1/d) rule.
    """

    def construct(self):
        title = Tex(r"High-dim random unit vectors are nearly orthogonal",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ax = Axes(x_range=[0, 180, 30], y_range=[0, 0.2, 0.05],
                   x_length=7, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-2.8, -0.3, 0])
        xlbl = MathTex(r"\text{angle (deg)}",
                         font_size=20).next_to(ax, DOWN, buff=0.15)
        ylbl = Tex(r"density", font_size=20).next_to(ax, LEFT, buff=0.15)
        self.play(Create(ax), Write(xlbl), Write(ylbl))

        # Vertical dashed line at 90°
        ninety = DashedLine(ax.c2p(90, 0), ax.c2p(90, 0.2),
                              color=YELLOW, stroke_width=2)
        ninety_lbl = MathTex(r"90^\circ", color=YELLOW,
                               font_size=20).next_to(ax.c2p(90, 0.2),
                                                       UP, buff=0.1)
        self.play(Create(ninety), Write(ninety_lbl))

        d_tr = ValueTracker(2)

        rng = np.random.default_rng(11)
        N = 200

        def sample_angles(d):
            V = rng.normal(size=(N, d))
            V /= np.linalg.norm(V, axis=1, keepdims=True) + 1e-10
            angles = []
            for i in range(0, min(N, 80)):
                for j in range(i + 1, min(N, 80)):
                    cos_ij = np.dot(V[i], V[j])
                    cos_ij = max(-1.0, min(1.0, cos_ij))
                    angles.append(np.degrees(np.arccos(cos_ij)))
            return np.array(angles)

        def hist_curve():
            d = int(round(d_tr.get_value()))
            angles = sample_angles(max(d, 2))
            bins = np.arange(0, 181, 10)
            hist, _ = np.histogram(angles, bins=bins)
            hist = hist / hist.sum() / 10  # density
            pts = []
            for i in range(len(hist)):
                x = (bins[i] + bins[i + 1]) / 2
                y = hist[i]
                pts.append(ax.c2p(x, y))
            m = VMobject(color=BLUE, stroke_width=4)
            m.set_points_smoothly(pts)
            return m

        self.add(always_redraw(hist_curve))

        def info():
            d = int(round(d_tr.get_value()))
            angles = sample_angles(max(d, 2))
            mean_ang = float(np.mean(angles))
            std_ang = float(np.std(angles))
            # E[cos²] = 1/d → angle stdev ≈ (180/π)·1/√d
            predicted_std = np.degrees(1.0 / np.sqrt(d))
            return VGroup(
                MathTex(rf"d = {d}", color=WHITE, font_size=26),
                MathTex(rf"\overline{{\theta}} = {mean_ang:.1f}^\circ",
                         color=YELLOW, font_size=24),
                MathTex(rf"\sigma = {std_ang:.1f}^\circ",
                         color=RED, font_size=22),
                MathTex(rf"\sqrt{{1/d}} \cdot \tfrac{{180}}{{\pi}} \approx {predicted_std:.1f}^\circ",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.2, 0.0, 0])

        self.add(always_redraw(info))

        for d_target in [3, 5, 10, 50, 200]:
            self.play(d_tr.animate.set_value(d_target),
                       run_time=1.7, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
