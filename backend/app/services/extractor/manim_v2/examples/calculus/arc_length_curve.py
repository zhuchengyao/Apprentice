from manim import *
import numpy as np


class ArcLengthCurveExample(Scene):
    """
    Arc length L = ∫ √(1 + (dy/dx)²) dx. Approximate as a polygonal
    path and refine; polygonal length converges to the arc length.

    TWO_COLUMN:
      LEFT  — axes with f(x) = x·sin(x) + 1 on [0, 4]; ValueTracker
              N_tr grows number of polygon segments 2 → 40.
      RIGHT — live polygon length vs exact arc length (numerical).
    """

    def construct(self):
        title = Tex(r"Arc length: $L = \int \sqrt{1 + (f')^2}\,dx$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        def f(x):
            return x * np.sin(x) + 1

        def fp(x):
            return np.sin(x) + x * np.cos(x)

        ax = Axes(x_range=[0, 4, 1], y_range=[-3, 5, 2],
                   x_length=7, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-2.8, -0.3, 0])
        self.play(Create(ax))

        curve = ax.plot(f, x_range=[0, 4], color=BLUE, stroke_width=3)
        self.play(Create(curve))

        a, b = 0.0, 4.0
        # Exact arc length via fine numerical integration
        xs_fine = np.linspace(a, b, 5000)
        exact_L = float(np.trapz(np.sqrt(1 + fp(xs_fine) ** 2), xs_fine))

        N_tr = ValueTracker(2)

        def polygon():
            N = int(round(N_tr.get_value()))
            N = max(2, min(N, 60))
            xs = np.linspace(a, b, N + 1)
            pts = [ax.c2p(x, f(x)) for x in xs]
            m = VMobject(color=YELLOW, stroke_width=3)
            m.set_points_as_corners(pts)
            return m

        def polygon_dots():
            N = int(round(N_tr.get_value()))
            N = max(2, min(N, 60))
            xs = np.linspace(a, b, N + 1)
            grp = VGroup()
            for x in xs:
                grp.add(Dot(ax.c2p(x, f(x)), color=YELLOW, radius=0.05))
            return grp

        self.add(always_redraw(polygon), always_redraw(polygon_dots))

        def poly_length(N):
            xs = np.linspace(a, b, N + 1)
            ys = f(xs)
            return float(np.sum(np.sqrt(np.diff(xs) ** 2 + np.diff(ys) ** 2)))

        def info():
            N = int(round(N_tr.get_value()))
            N = max(2, min(N, 60))
            L_poly = poly_length(N)
            err = abs(L_poly - exact_L)
            return VGroup(
                MathTex(rf"N = {N}", color=YELLOW, font_size=24),
                MathTex(rf"L_{{\text{{poly}}}} = {L_poly:.5f}",
                         color=YELLOW, font_size=22),
                MathTex(rf"L_{{\text{{exact}}}} = {exact_L:.5f}",
                         color=GREEN, font_size=22),
                MathTex(rf"|\text{{err}}| = {err:.2e}",
                         color=RED, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for nv in [4, 8, 16, 40]:
            self.play(N_tr.animate.set_value(nv),
                       run_time=1.4, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
