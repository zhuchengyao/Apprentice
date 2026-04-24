from manim import *
import numpy as np


class JacobianTransformationExample(Scene):
    """
    Change of variables for 2D integrals: dA' = |det J| dA. Visualize
    with polar coordinates (r, θ) → (x, y) = (r cos θ, r sin θ),
    |det J| = r. A uniform rectangular grid in (r, θ) maps to an
    angular-radial grid in (x, y) whose cell area grows with r.

    COMPARISON:
      LEFT (r, θ) plane with uniform grid cells; RIGHT (x, y) plane
      showing the image. ValueTracker s_tr morphs smoothly.
    """

    def construct(self):
        title = Tex(r"Jacobian: $dA = r\,dr\,d\theta$ for polar",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        left = NumberPlane(x_range=[0, 2.5, 0.5],
                             y_range=[0, 2 * PI, PI / 4],
                             x_length=5, y_length=5,
                             background_line_style={"stroke_opacity": 0.3}
                             ).move_to([-3.5, -0.3, 0])
        right = NumberPlane(x_range=[-2.5, 2.5, 0.5],
                              y_range=[-2.5, 2.5, 0.5],
                              x_length=5, y_length=5,
                              background_line_style={"stroke_opacity": 0.3}
                              ).move_to([3.5, -0.3, 0])
        self.play(Create(left), Create(right))

        left_lbl = MathTex(r"(r, \theta)", font_size=22
                             ).next_to(left, UP, buff=0.1)
        right_lbl = MathTex(r"(x, y) = (r\cos\theta, r\sin\theta)",
                              font_size=20
                              ).next_to(right, UP, buff=0.1)
        self.play(Write(left_lbl), Write(right_lbl))

        s_tr = ValueTracker(0.0)

        def grid_cells():
            s = s_tr.get_value()
            grp = VGroup()
            r_vals = np.arange(0.2, 2.3, 0.4)
            th_vals = np.arange(0, 2 * PI + 0.01, PI / 6)
            for i, r0 in enumerate(r_vals):
                for j, th0 in enumerate(th_vals[:-1]):
                    r1 = r0 + 0.4
                    th1 = th_vals[j + 1]
                    # 4 corners
                    corners_rth = [(r0, th0), (r1, th0), (r1, th1), (r0, th1)]
                    pts = []
                    for (rr, tt) in corners_rth:
                        # Source (left plane): (rr, tt)
                        src = left.c2p(rr, tt)
                        # Target (right plane): (rr cos tt, rr sin tt)
                        tgt = right.c2p(rr * np.cos(tt), rr * np.sin(tt))
                        # Interpolate between left and right positions
                        p = (1 - s) * np.array(src) + s * np.array(tgt)
                        pts.append(p)
                    # Color: darker for small r, lighter for large r
                    intensity = min(1.0, r0 / 2.2)
                    col = interpolate_color(BLUE, RED, intensity)
                    poly = Polygon(*pts, color=col, fill_opacity=0.4,
                                     stroke_width=1)
                    grp.add(poly)
            return grp

        self.add(always_redraw(grid_cells))

        def info():
            s = s_tr.get_value()
            return VGroup(
                MathTex(rf"s = {s:.2f}", color=YELLOW, font_size=22),
                MathTex(r"J = \begin{pmatrix}\cos\theta & -r\sin\theta \\ \sin\theta & r\cos\theta\end{pmatrix}",
                         color=WHITE, font_size=18),
                MathTex(r"|\det J| = r", color=GREEN, font_size=24),
                Tex(r"$r=0.2$ cells shrink, $r=2.2$ expand",
                     color=YELLOW, font_size=16),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        self.play(s_tr.animate.set_value(1.0),
                   run_time=5, rate_func=smooth)
        self.wait(0.5)
        self.play(s_tr.animate.set_value(0.0),
                   run_time=3, rate_func=smooth)
        self.wait(0.4)
