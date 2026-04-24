from manim import *
import numpy as np


class SimpsonRuleIntegrationExample(Scene):
    """
    Simpson's rule approximates ∫f dx by parabolic segments:
      ∫_a^b f ≈ (h/3)·[f_0 + 4f_1 + 2f_2 + 4f_3 + ... + f_N]
    where h = (b - a)/N and f_i = f(a + ih), N even.

    SINGLE_FOCUS:
      Axes with f(x) = e^(-x²/2)·(1 + sin(2x)); ValueTracker N_tr
      increases number of subintervals (multiples of 2). always_redraw
      parabolic segments + live Simpson approximation vs true integral.
    """

    def construct(self):
        title = Tex(r"Simpson's rule: parabolic approximation of $\int f$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        def f(x):
            return np.exp(-x ** 2 / 2) * (1 + np.sin(2 * x))

        ax = Axes(x_range=[-2.5, 2.5, 1], y_range=[0, 2, 0.5],
                   x_length=9, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-0.5, -0.3, 0])
        self.play(Create(ax))

        curve = ax.plot(f, x_range=[-2.5, 2.5, 0.02],
                          color=BLUE, stroke_width=3)
        self.play(Create(curve))

        a, b = -2.0, 2.0
        # True integral via fine grid
        xs_fine = np.linspace(a, b, 2000)
        true_int = float(np.trapz(f(xs_fine), xs_fine))

        N_tr = ValueTracker(2)

        def simpson_approx(N):
            N = int(N)
            if N % 2 == 1:
                N += 1
            h = (b - a) / N
            xs = np.linspace(a, b, N + 1)
            ys = f(xs)
            weights = np.ones(N + 1)
            weights[1:-1:2] = 4
            weights[2:-1:2] = 2
            return (h / 3) * np.sum(weights * ys)

        def parabolic_segments():
            N = int(round(N_tr.get_value()))
            if N % 2 == 1:
                N += 1
            N = max(2, min(N, 20))
            h = (b - a) / N
            grp = VGroup()
            # Each parabola spans 2h
            for i in range(0, N, 2):
                x0 = a + i * h
                x1 = a + (i + 1) * h
                x2 = a + (i + 2) * h
                y0, y1, y2 = f(x0), f(x1), f(x2)
                # Fit parabola through (x0, y0), (x1, y1), (x2, y2)
                pts_para = []
                for xi in np.linspace(x0, x2, 25):
                    # Lagrange
                    l0 = ((xi - x1) * (xi - x2)) / ((x0 - x1) * (x0 - x2))
                    l1 = ((xi - x0) * (xi - x2)) / ((x1 - x0) * (x1 - x2))
                    l2 = ((xi - x0) * (xi - x1)) / ((x2 - x0) * (x2 - x1))
                    yi = y0 * l0 + y1 * l1 + y2 * l2
                    pts_para.append(ax.c2p(xi, yi))
                # Shade area under parabola
                shade_pts = [ax.c2p(x0, 0)]
                shade_pts.extend(pts_para)
                shade_pts.append(ax.c2p(x2, 0))
                shade = Polygon(*shade_pts, color=YELLOW,
                                  fill_opacity=0.3, stroke_width=0)
                grp.add(shade)
                para = VMobject(color=YELLOW, stroke_width=2)
                para.set_points_as_corners(pts_para)
                grp.add(para)
                # Vertical lines at x0, x1, x2
                for xp in [x0, x1, x2]:
                    grp.add(Line(ax.c2p(xp, 0), ax.c2p(xp, f(xp)),
                                   color=GREY_B, stroke_width=0.8,
                                   stroke_opacity=0.6))
            return grp

        self.add(always_redraw(parabolic_segments))

        def info():
            N = int(round(N_tr.get_value()))
            if N % 2 == 1:
                N += 1
            N = max(2, min(N, 20))
            approx = simpson_approx(N)
            err = abs(approx - true_int)
            return VGroup(
                MathTex(rf"N = {N}", color=YELLOW, font_size=24),
                MathTex(rf"\text{{Simpson}} = {approx:.5f}",
                         color=GREEN, font_size=22),
                MathTex(rf"\text{{true}} = {true_int:.5f}",
                         color=BLUE, font_size=22),
                MathTex(rf"|\text{{err}}| = {err:.2e}",
                         color=RED, font_size=22),
                Tex(r"error $\sim 1/N^4$",
                     color=GREY_B, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for target in [4, 6, 10, 20]:
            self.play(N_tr.animate.set_value(target),
                       run_time=1.5, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
