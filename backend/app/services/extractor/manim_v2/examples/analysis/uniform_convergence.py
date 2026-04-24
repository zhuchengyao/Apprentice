from manim import *
import numpy as np


class UniformConvergenceExample(Scene):
    """
    Pointwise vs uniform convergence: f_n(x) = x^n on [0, 1]
    converges pointwise to f(x) = 0 on [0, 1) and 1 at x = 1, but
    NOT uniformly. Sup norm ‖f_n - f‖_∞ = 1 for all n.

    TWO_COLUMN:
      LEFT  — curves f_n for n = 1, 2, 5, 20, 100 stacked; ValueTracker
              n_tr grows.
      RIGHT — axes of sup norm ‖f_n - f‖ over [0, 1]; stays at 1.
    """

    def construct(self):
        title = Tex(r"Pointwise vs uniform convergence",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # LEFT: x^n curves
        ax_L = Axes(x_range=[0, 1, 0.25], y_range=[0, 1.1, 0.25],
                     x_length=6, y_length=4, tips=False,
                     axis_config={"font_size": 14, "include_numbers": True}
                     ).move_to([-3, -0.3, 0])
        self.play(Create(ax_L))

        # Limit function f (0 on [0, 1), 1 at x=1)
        limit_pts = [ax_L.c2p(x, 0) for x in np.linspace(0, 0.999, 40)]
        limit_pts.append(ax_L.c2p(1, 1))  # jump
        limit_curve = VMobject(color=GREEN, stroke_width=3)
        limit_curve.set_points_as_corners(limit_pts)
        self.play(Create(limit_curve))
        lim_lbl = Tex(r"limit $f$", color=GREEN, font_size=18
                       ).next_to(ax_L.c2p(0.7, 0), UP, buff=0.15)
        self.play(Write(lim_lbl))

        n_tr = ValueTracker(1)

        def fn_curve():
            n = int(round(n_tr.get_value()))
            n = max(1, min(n, 200))
            return ax_L.plot(lambda x: x ** n,
                              x_range=[0, 1, 0.005],
                              color=BLUE, stroke_width=3)

        self.add(always_redraw(fn_curve))

        # RIGHT: sup norm plot (constant 1)
        ax_R = Axes(x_range=[0, 200, 50], y_range=[0, 1.2, 0.25],
                     x_length=5, y_length=3, tips=False,
                     axis_config={"font_size": 14, "include_numbers": True}
                     ).move_to([3.5, -0.5, 0])
        xl = MathTex(r"n", font_size=18).next_to(ax_R, DOWN, buff=0.1)
        yl = MathTex(r"\|f_n - f\|_\infty", font_size=18
                      ).next_to(ax_R, LEFT, buff=0.1)
        self.play(Create(ax_R), Write(xl), Write(yl))

        sup_line = DashedLine(ax_R.c2p(0, 1), ax_R.c2p(200, 1),
                                color=RED, stroke_width=3)
        sup_lbl = MathTex(r"\|f_n - f\|_\infty = 1",
                            color=RED, font_size=20
                            ).next_to(ax_R.c2p(100, 1), UP, buff=0.1)
        self.play(Create(sup_line), Write(sup_lbl))

        def rider():
            n = int(round(n_tr.get_value()))
            n = max(1, min(n, 200))
            return Dot(ax_R.c2p(n, 1), color=YELLOW, radius=0.1)

        self.add(always_redraw(rider))

        def info():
            n = int(round(n_tr.get_value()))
            n = max(1, min(n, 200))
            # Pointwise at x=0.9: 0.9^n → 0
            ptwise_09 = 0.9 ** n
            return VGroup(
                MathTex(rf"n = {n}", color=BLUE, font_size=24),
                MathTex(rf"f_n(0.9) = 0.9^n = {ptwise_09:.5f}",
                         color=BLUE, font_size=20),
                Tex(r"pointwise: $f_n(x) \to 0$ for $x<1$",
                     color=GREEN, font_size=18),
                Tex(r"sup norm stays $= 1$ (no uniform conv.)",
                     color=RED, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        for nv in [3, 10, 30, 100, 200]:
            self.play(n_tr.animate.set_value(nv),
                       run_time=1.3, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
