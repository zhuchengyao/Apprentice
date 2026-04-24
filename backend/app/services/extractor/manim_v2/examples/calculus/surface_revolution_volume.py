from manim import *
import numpy as np


class SurfaceRevolutionVolumeExample(Scene):
    """
    Solid of revolution about the x-axis: V = π ∫ f(x)² dx.
    Demonstrates with f(x) = x² + 1 on [0, 2].

    TWO_COLUMN:
      LEFT  — curve with shaded disc cross-sections stacking up via
              ValueTracker N_tr going 2 → 40 discs.
      RIGHT — live Riemann-sum V_N approaching V = π ∫ (x²+1)² dx =
              π(64/5 + 4 + 8/3).
    """

    def construct(self):
        title = Tex(r"Volume of revolution: $V = \pi \int f(x)^2\,dx$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        def f(x):
            return x ** 2 / 3 + 1

        ax = Axes(x_range=[0, 2.2, 0.5], y_range=[-2.5, 2.5, 1],
                   x_length=7, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-2.5, -0.3, 0])
        self.play(Create(ax))

        # Curve
        curve = ax.plot(f, x_range=[0, 2], color=BLUE, stroke_width=3)
        curve_neg = ax.plot(lambda x: -f(x), x_range=[0, 2],
                              color=BLUE, stroke_width=3)
        self.play(Create(curve), Create(curve_neg))

        # True volume
        xs_fine = np.linspace(0, 2, 5000)
        true_V = float(np.trapz(PI * f(xs_fine) ** 2, xs_fine))

        N_tr = ValueTracker(2)

        def discs():
            N = int(round(N_tr.get_value()))
            N = max(1, min(N, 50))
            h = 2 / N
            grp = VGroup()
            for i in range(N):
                x_c = (i + 0.5) * h
                r = f(x_c)
                # Ellipse approximation of disc (seen from an angle)
                e = Ellipse(width=h * 0.95,
                              height=(ax.c2p(0, r)[1] - ax.c2p(0, -r)[1]),
                              color=YELLOW, fill_opacity=0.35,
                              stroke_width=0.5).move_to(ax.c2p(x_c, 0))
                grp.add(e)
            return grp

        self.add(always_redraw(discs))

        def info():
            N = int(round(N_tr.get_value()))
            N = max(1, min(N, 50))
            h = 2 / N
            V_approx = sum(PI * f((i + 0.5) * h) ** 2 * h for i in range(N))
            err = abs(V_approx - true_V)
            return VGroup(
                MathTex(rf"N = {N}", color=YELLOW, font_size=24),
                MathTex(rf"V_N = \pi \sum f(x_i)^2 \Delta x = {V_approx:.4f}",
                         color=YELLOW, font_size=20),
                MathTex(rf"V = \pi \int_0^2 f^2\,dx = {true_V:.4f}",
                         color=GREEN, font_size=20),
                MathTex(rf"|\text{{err}}| = {err:.4f}",
                         color=RED, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for nv in [5, 10, 20, 40]:
            self.play(N_tr.animate.set_value(nv),
                       run_time=1.5, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
