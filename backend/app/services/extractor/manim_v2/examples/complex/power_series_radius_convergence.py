from manim import *
import numpy as np


class PowerSeriesRadiusConvergenceExample(Scene):
    """
    Power series f(z) = Σ a_n z^n has radius of convergence R =
    1 / limsup |a_n|^(1/n). Series converges absolutely for |z|<R,
    diverges for |z|>R.

    Example: Σ n z^n has R = 1. Show partial sums S_N(z) on various
    |z| values: |z|=0.5 converges rapidly, |z|=0.95 slowly, |z|=1.1
    diverges.
    """

    def construct(self):
        title = Tex(r"Radius of convergence $R=1$ for $\sum n z^n$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = ComplexPlane(x_range=[-1.5, 1.5, 0.5], y_range=[-1.5, 1.5, 0.5],
                             x_length=5.0, y_length=5.0,
                             background_line_style={"stroke_opacity": 0.3}
                             ).shift(LEFT * 3.3)

        # Unit circle (boundary)
        boundary = Circle(radius=plane.x_length / (plane.x_range[1] - plane.x_range[0]),
                          color=YELLOW, stroke_width=3).move_to(plane.n2p(0))
        self.play(Create(plane), Create(boundary))
        self.add(Tex(r"$|z|=R=1$", color=YELLOW, font_size=20).next_to(boundary, UR, buff=0.1))

        # RIGHT: partial sums plot
        axes = Axes(x_range=[0, 50, 10], y_range=[-30, 30, 10],
                    x_length=5.0, y_length=4.5,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(RIGHT * 2.5 + DOWN * 0.3)
        self.play(Create(axes))

        z_tr = ValueTracker(0.5)  # tour |z| values

        def z_val():
            t = z_tr.get_value()
            return t  # real for simplicity

        def z_dot():
            z = z_val()
            return Dot(plane.n2p(z + 0j), color=RED, radius=0.13)

        def z_label():
            z = z_val()
            return Tex(rf"$z={z:.2f}$", color=RED, font_size=22).move_to(
                plane.n2p(z + 0j) + UP * 0.3)

        self.add(always_redraw(z_dot), always_redraw(z_label))

        # Compute partial sums
        def S_N(z, N):
            return sum(n * z ** n for n in range(N + 1))

        def partial_curve():
            z = z_val()
            N_max = 50
            pts = []
            for N in range(N_max + 1):
                val = S_N(z, N)
                if abs(val) < 30:
                    pts.append(axes.c2p(N, val))
            if len(pts) < 2:
                return VMobject()
            col = GREEN if abs(z) < 1 else RED
            return VMobject().set_points_as_corners(pts).set_color(col).set_stroke(width=3)

        self.add(always_redraw(partial_curve))

        # True limit 1/(1-z)^2 for |z|<1
        def limit_line():
            z = z_val()
            if abs(z) >= 1:
                return VMobject()
            L = 1 / (1 - z) ** 2
            return DashedLine(axes.c2p(0, L), axes.c2p(50, L),
                              color=BLUE, stroke_width=2)
        self.add(always_redraw(limit_line))

        info = VGroup(
            VGroup(Tex(r"$|z|=$", font_size=22),
                   DecimalNumber(0.5, num_decimal_places=3,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$S_N(z)$ as $N\to\infty$:", font_size=22),
                    ).arrange(RIGHT, buff=0.1),
            Tex(r"$|z|<1$: converges to $1/(1-z)^2$",
                color=GREEN, font_size=20),
            Tex(r"$|z|>1$: diverges",
                color=RED, font_size=20),
            Tex(r"$|z|=1$: boundary (case-by-case)",
                color=YELLOW, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(DL, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(z_val()))
        self.add(info)

        for z_val_target in [0.8, 0.95, 1.05, 1.1, 0.3]:
            self.play(z_tr.animate.set_value(z_val_target),
                      run_time=2.0, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.5)
