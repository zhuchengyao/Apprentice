from manim import *
import numpy as np


class HadamardThreeCirclesExample(Scene):
    """
    Hadamard's three-circle theorem: for f holomorphic on annulus
    a < |z| < b, M(r) = max_{|z|=r} |f(z)| is logarithmically convex,
    i.e., log M is convex in log r.

    TWO_COLUMN:
      LEFT  — complex plane with 3 circles of increasing radii; f(z)
              = z² sample; value shown.
      RIGHT — plot of log M(r) vs log r — concave up (convex).
    """

    def construct(self):
        title = Tex(r"Hadamard: $\log M(r)$ is convex in $\log r$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = ComplexPlane(x_range=[-3, 3, 1], y_range=[-3, 3, 1],
                               x_length=5, y_length=5,
                               background_line_style={"stroke_opacity": 0.25}
                               ).move_to([-3.5, -0.3, 0])
        self.play(Create(plane))

        # Three static circles at r = 0.5, 1.5, 2.5
        r_values = [0.5, 1.5, 2.5]
        colors_r = [BLUE, GREEN, ORANGE]
        for rv, col in zip(r_values, colors_r):
            c = Circle(radius=plane.c2p(rv, 0)[0] - plane.c2p(0, 0)[0],
                         color=col, stroke_width=2,
                         fill_opacity=0).move_to(plane.c2p(0, 0))
            self.add(c)

        # Sweep a max-modulus indicator
        r_tr = ValueTracker(0.6)

        def current_circle():
            r = r_tr.get_value()
            return Circle(radius=plane.c2p(r, 0)[0] - plane.c2p(0, 0)[0],
                            color=YELLOW, stroke_width=3,
                            fill_opacity=0).move_to(plane.c2p(0, 0))

        self.add(always_redraw(current_circle))

        # RIGHT: log M(r) vs log r for f(z) = z²
        # M(r) = r², so log M = 2 log r (linear, hence convex).
        # Also show f(z) = z² + z (non-trivial)
        ax = Axes(x_range=[-1, 1.2, 0.5], y_range=[-1, 2.5, 0.5],
                   x_length=5, y_length=4, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([3, -0.3, 0])
        xl = MathTex(r"\log_{10} r", font_size=18).next_to(ax, DOWN, buff=0.1)
        yl = MathTex(r"\log_{10} M(r)", font_size=18).next_to(ax, LEFT, buff=0.1)
        self.play(Create(ax), Write(xl), Write(yl))

        # For f(z) = z²: M(r) = r², so log M = 2 log r
        curve_1 = ax.plot(lambda lr: 2 * lr, x_range=[-1, 1.2],
                            color=BLUE, stroke_width=3)
        lbl_1 = MathTex(r"z^2", color=BLUE, font_size=18
                          ).next_to(ax.c2p(1.2, 2.4), LEFT, buff=0.1)
        # For f(z) = z² + z: M(r) = r² + r, log M = log(r² + r) = log r + log(r + 1)
        curve_2 = ax.plot(lambda lr: np.log10(10 ** (2 * lr) + 10 ** lr),
                            x_range=[-1, 1.2, 0.02],
                            color=RED, stroke_width=3)
        lbl_2 = MathTex(r"z^2 + z", color=RED, font_size=18
                          ).next_to(ax.c2p(0.5, np.log10(10 ** 1 + 10 ** 0.5)),
                                      RIGHT, buff=0.1)
        self.play(Create(curve_1), Create(curve_2),
                   Write(lbl_1), Write(lbl_2))

        def rider():
            r = r_tr.get_value()
            lr = np.log10(r)
            # z² rider
            M1 = r ** 2
            # z² + z rider
            M2 = r ** 2 + r
            return VGroup(
                Dot(ax.c2p(lr, np.log10(M1)), color=BLUE, radius=0.09),
                Dot(ax.c2p(lr, np.log10(M2)), color=RED, radius=0.09),
            )

        self.add(always_redraw(rider))

        def info():
            r = r_tr.get_value()
            return VGroup(
                MathTex(rf"r = {r:.2f}", color=YELLOW, font_size=22),
                MathTex(rf"M_{{z^2}}(r) = {r ** 2:.3f}",
                         color=BLUE, font_size=20),
                MathTex(rf"M_{{z^2+z}}(r) = {r ** 2 + r:.3f}",
                         color=RED, font_size=20),
                Tex(r"both log-convex (Hadamard)",
                     color=GREEN, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        self.play(r_tr.animate.set_value(2.5),
                   run_time=6, rate_func=linear)
        self.wait(0.4)
