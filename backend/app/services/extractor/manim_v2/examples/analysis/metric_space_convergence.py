from manim import *
import numpy as np


class MetricSpaceConvergenceExample(Scene):
    """
    Convergence in a metric space: x_n → x iff d(x_n, x) → 0.
    Illustrate in ℝ² with Euclidean metric; sequence spirals inward
    to the limit.

    SINGLE_FOCUS:
      2D plane with sequence x_n = (cos(n)/n, sin(n)/n) → (0, 0).
      ValueTracker n_tr advances; dots drawn + concentric ε-balls
      shrinking.
    """

    def construct(self):
        title = Tex(r"Metric space convergence: $d(x_n, x) \to 0$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-1.5, 1.5, 0.5],
                             y_range=[-1.5, 1.5, 0.5],
                             x_length=6, y_length=6,
                             background_line_style={"stroke_opacity": 0.3}
                             ).move_to([-2, -0.3, 0])
        self.play(Create(plane))

        # Limit = (0, 0)
        limit_dot = Dot(plane.c2p(0, 0), color=RED, radius=0.15)
        limit_lbl = MathTex(r"x = 0", color=RED, font_size=22
                              ).next_to(limit_dot, DR, buff=0.1)
        self.play(FadeIn(limit_dot), Write(limit_lbl))

        # ε-ball markers (static, several radii)
        for eps in [0.5, 0.25, 0.1]:
            c = Circle(radius=plane.c2p(eps, 0)[0] - plane.c2p(0, 0)[0],
                         color=YELLOW, stroke_width=1.5,
                         stroke_opacity=0.55, fill_opacity=0
                         ).move_to(plane.c2p(0, 0))
            self.add(c)
            lbl = MathTex(rf"\varepsilon = {eps}", color=YELLOW, font_size=14
                            ).next_to(plane.c2p(eps, 0), UP, buff=0.1)
            self.add(lbl)

        # Sequence x_n = (cos(n)/n, sin(n)/n) for n = 1..30
        n_max = 30

        def x_n(n):
            return np.array([np.cos(n) / n, np.sin(n) / n])

        n_tr = ValueTracker(1)

        def points_and_trail():
            n = int(round(n_tr.get_value()))
            n = max(1, min(n, n_max))
            grp = VGroup()
            pts = []
            for k in range(1, n + 1):
                p = x_n(k)
                pts.append(plane.c2p(p[0], p[1]))
                intensity = k / n_max
                col = interpolate_color(BLUE, YELLOW, intensity)
                grp.add(Dot(plane.c2p(p[0], p[1]), color=col, radius=0.06))
            if len(pts) >= 2:
                m = VMobject(color=BLUE_D, stroke_width=1.5,
                               stroke_opacity=0.55)
                m.set_points_as_corners(pts)
                grp.add(m)
            return grp

        self.add(always_redraw(points_and_trail))

        def info():
            n = int(round(n_tr.get_value()))
            n = max(1, min(n, n_max))
            p = x_n(n)
            d = np.linalg.norm(p)
            return VGroup(
                MathTex(rf"n = {n}", color=BLUE, font_size=22),
                MathTex(rf"x_n = ({p[0]:+.3f}, {p[1]:+.3f})",
                         color=BLUE, font_size=18),
                MathTex(rf"d(x_n, 0) = {d:.4f}",
                         color=RED, font_size=22),
                Tex(r"all $x_n$ with $n > 1/\varepsilon$ inside $\varepsilon$-ball",
                     color=YELLOW, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        self.play(n_tr.animate.set_value(n_max),
                   run_time=8, rate_func=linear)
        self.wait(0.4)
