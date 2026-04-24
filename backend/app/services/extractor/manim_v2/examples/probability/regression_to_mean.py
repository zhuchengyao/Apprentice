from manim import *
import numpy as np


class RegressionToMeanExample(Scene):
    """
    Regression to the mean: extreme observations tend to be less
    extreme on subsequent measurements. Illustrate with bivariate
    normal (X, Y) with correlation ρ; E[Y | X = x] = ρ x (< x for
    extreme x).

    SINGLE_FOCUS:
      Scatter of (X_1, X_2) pairs from bivariate normal with ρ=0.6;
      regression line y = ρ x; ValueTracker x_tr moves on x-axis,
      conditional mean shown always_redraw.
    """

    def construct(self):
        title = Tex(r"Regression to the mean: $E[Y|X=x] = \rho x$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-3, 3, 1], y_range=[-3, 3, 1],
                             x_length=7, y_length=5.5,
                             background_line_style={"stroke_opacity": 0.3}
                             ).move_to([-2, -0.3, 0])
        self.play(Create(plane))

        # Correlation
        rho = 0.6

        # Sample bivariate
        rng = np.random.default_rng(12)
        n = 200
        z1 = rng.normal(size=n)
        z2 = rng.normal(size=n)
        X = z1
        Y = rho * z1 + np.sqrt(1 - rho ** 2) * z2

        scatter = VGroup()
        for i in range(n):
            scatter.add(Dot(plane.c2p(X[i], Y[i]),
                              color=BLUE_D, radius=0.04))
        self.play(FadeIn(scatter))

        # Regression line y = ρ x
        reg_line = Line(plane.c2p(-3, -3 * rho), plane.c2p(3, 3 * rho),
                          color=RED, stroke_width=3)
        reg_lbl = MathTex(rf"y = {rho} x", color=RED, font_size=20
                            ).next_to(reg_line.get_end(), UP, buff=0.1)
        # Diagonal y = x reference
        diag_line = DashedLine(plane.c2p(-3, -3), plane.c2p(3, 3),
                                 color=GREY_B, stroke_width=2)
        diag_lbl = MathTex(r"y = x", color=GREY_B, font_size=18
                             ).next_to(diag_line.get_end(), UR, buff=0.1)
        self.play(Create(reg_line), Create(diag_line),
                   Write(reg_lbl), Write(diag_lbl))

        x_tr = ValueTracker(0.0)

        def x_vertical():
            x = x_tr.get_value()
            return DashedLine(plane.c2p(x, -3), plane.c2p(x, 3),
                               color=YELLOW, stroke_width=2)

        def cond_mean_dot():
            x = x_tr.get_value()
            return Dot(plane.c2p(x, rho * x),
                        color=YELLOW, radius=0.12)

        def x_dot():
            x = x_tr.get_value()
            return Dot(plane.c2p(x, x), color=ORANGE, radius=0.1)

        self.add(always_redraw(x_vertical),
                  always_redraw(cond_mean_dot),
                  always_redraw(x_dot))

        def info():
            x = x_tr.get_value()
            cond = rho * x
            return VGroup(
                MathTex(rf"x = {x:+.2f}", color=YELLOW, font_size=22),
                MathTex(rf"E[Y|X=x] = {cond:+.3f}",
                         color=YELLOW, font_size=20),
                MathTex(rf"\text{{regress toward 0 by }} (1 - \rho) = {1 - rho:.2f}",
                         color=ORANGE, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for xv in [2.0, -2.5, 1.5, -1.0, 2.5]:
            self.play(x_tr.animate.set_value(xv),
                       run_time=1.4, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
