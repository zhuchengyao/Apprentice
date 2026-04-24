from manim import *
import numpy as np


class SchwarzLemmaExample(Scene):
    """
    Schwarz lemma: if f: 𝔻 → 𝔻 is holomorphic with f(0) = 0, then
    |f(z)| ≤ |z| on 𝔻 and |f'(0)| ≤ 1.

    TWO_COLUMN:
      LEFT unit disk; trace a test point z at radius r; RIGHT image
      disk showing |f(z)|. Bound |f(z)| ≤ |z| as dashed line.
      Example: f(z) = z² satisfies the bound.
    """

    def construct(self):
        title = Tex(r"Schwarz lemma: $|f(z)| \le |z|$ for $f: \mathbb D \to \mathbb D$, $f(0) = 0$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Axes: |z| vs |f(z)|
        ax = Axes(x_range=[0, 1, 0.25], y_range=[0, 1, 0.25],
                   x_length=6, y_length=5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-2.5, -0.3, 0])
        xl = MathTex(r"|z|", font_size=20).next_to(ax, DOWN, buff=0.1)
        yl = MathTex(r"|f(z)|", font_size=20).next_to(ax, LEFT, buff=0.1)
        self.play(Create(ax), Write(xl), Write(yl))

        # Bound y = x
        bound_line = ax.plot(lambda x: x, x_range=[0, 1],
                               color=RED, stroke_width=3)
        bound_lbl = MathTex(r"y = |z|", color=RED, font_size=20
                              ).next_to(ax.c2p(0.8, 0.8), UR, buff=0.1)
        self.play(Create(bound_line), Write(bound_lbl))

        # For f(z) = z²: |f(z)| = |z|²
        fz2_curve = ax.plot(lambda x: x ** 2, x_range=[0, 1],
                              color=BLUE, stroke_width=3)
        fz2_lbl = MathTex(r"f(z) = z^2: |f| = |z|^2",
                            color=BLUE, font_size=18
                            ).next_to(ax.c2p(0.7, 0.49), DR, buff=0.1)
        self.play(Create(fz2_curve), Write(fz2_lbl))

        r_tr = ValueTracker(0.01)

        def rider_z():
            r = r_tr.get_value()
            return Dot(ax.c2p(r, r), color=RED, radius=0.09)

        def rider_fz():
            r = r_tr.get_value()
            return Dot(ax.c2p(r, r ** 2), color=BLUE, radius=0.11)

        def drop():
            r = r_tr.get_value()
            return DashedLine(ax.c2p(r, 0), ax.c2p(r, max(r, r ** 2)),
                               color=GREY_B, stroke_width=1.5)

        self.add(always_redraw(drop),
                  always_redraw(rider_z),
                  always_redraw(rider_fz))

        # RIGHT: visualize unit disk with a spiral trajectory under f
        plane = ComplexPlane(x_range=[-1.2, 1.2, 0.5], y_range=[-1.2, 1.2, 0.5],
                               x_length=3.5, y_length=3.5,
                               background_line_style={"stroke_opacity": 0.25}
                               ).move_to([3.5, 0.5, 0])
        unit_c = Circle(radius=plane.c2p(1, 0)[0] - plane.c2p(0, 0)[0],
                          color=YELLOW, stroke_width=2
                          ).move_to(plane.c2p(0, 0))
        self.play(Create(plane), Create(unit_c))

        def z_dot_on_disk():
            r = r_tr.get_value()
            theta = PI / 3  # fixed angle for visualization
            return Dot(plane.c2p(r * np.cos(theta),
                                    r * np.sin(theta)),
                        color=RED, radius=0.1)

        def fz_dot_on_disk():
            r = r_tr.get_value()
            theta = PI / 3
            z = r * np.exp(1j * theta)
            w = z ** 2
            return Dot(plane.c2p(w.real, w.imag),
                        color=BLUE, radius=0.1)

        self.add(always_redraw(z_dot_on_disk),
                  always_redraw(fz_dot_on_disk))

        def info():
            r = r_tr.get_value()
            return VGroup(
                MathTex(rf"|z| = {r:.3f}", color=RED, font_size=22),
                MathTex(rf"|f(z)| = {r ** 2:.3f}",
                         color=BLUE, font_size=22),
                MathTex(rf"|f(z)| \le |z|? \ {'yes' if r ** 2 <= r + 1e-8 else 'no'}",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        self.play(r_tr.animate.set_value(1.0),
                   run_time=6, rate_func=linear)
        self.wait(0.4)
