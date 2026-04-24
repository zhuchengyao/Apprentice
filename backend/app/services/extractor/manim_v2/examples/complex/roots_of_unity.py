from manim import *
import numpy as np


class RootsOfUnityExample(Scene):
    """
    Sweep n from 2 to 12: each step shows the n-th roots of unity as
    vertices of a regular n-gon inscribed in the unit circle.

    TWO_COLUMN layout:
      LEFT  — ComplexPlane with the unit circle and an always_redraw
              VGroup of n dots + a regular n-gon connecting them.
              Integer ValueTracker n_idx steps through 2..12.
      RIGHT — live n value, equation z^n = 1, the explicit root list
              z_k = exp(2πi k / n), and the angle 2π/n in degrees.
    """

    def construct(self):
        title = Tex(r"$n$-th roots of unity: solutions of $z^n = 1$",
                    font_size=32).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # LEFT: complex plane + unit circle
        plane = ComplexPlane(
            x_range=[-1.8, 1.8, 1], y_range=[-1.8, 1.8, 1],
            x_length=5.4, y_length=5.4,
            background_line_style={"stroke_opacity": 0.3},
        ).move_to([-3.0, -0.2, 0])
        unit_circle = Circle(
            radius=plane.n2p(complex(1, 0))[0] - plane.n2p(0)[0],
            color=BLUE, stroke_width=2, stroke_opacity=0.7,
        ).move_to(plane.n2p(0))
        self.play(Create(plane), Create(unit_circle))

        n_tracker = ValueTracker(2.0)

        def n_value() -> int:
            return max(2, int(round(n_tracker.get_value())))

        def roots_group():
            n = n_value()
            roots = [np.exp(2j * PI * k / n) for k in range(n)]
            pts = [plane.n2p(r) for r in roots]
            dots = VGroup(*[Dot(p, color=YELLOW, radius=0.10) for p in pts])
            polygon = Polygon(*pts, color=YELLOW, stroke_width=3,
                              fill_color=YELLOW, fill_opacity=0.18)
            return VGroup(polygon, dots)

        self.add(always_redraw(roots_group))

        # RIGHT COLUMN: live readouts
        rcol_x = +3.5

        def info_panel():
            n = n_value()
            return VGroup(
                MathTex(rf"n = {n}", color=YELLOW, font_size=44),
                MathTex(rf"z^{{{n}}} = 1", color=WHITE, font_size=32),
                MathTex(rf"z_k = e^{{2\pi i k / {n}}},\;k=0,\ldots,{n-1}",
                        color=WHITE, font_size=22),
                MathTex(rf"\frac{{2\pi}}{{n}} = {360 / n:.1f}^\circ",
                        color=GREY_B, font_size=24),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([rcol_x, +0.6, 0])

        self.add(always_redraw(info_panel))

        # Step through n = 2, 3, 4, 5, 6, 7, 8, 9, 10, 12
        for n in [3, 4, 5, 6, 7, 8, 9, 10, 12]:
            self.play(n_tracker.animate.set_value(float(n)),
                      run_time=0.85, rate_func=smooth)
            self.wait(0.25)

        # Then morph back to a small n
        self.play(n_tracker.animate.set_value(5.0),
                  run_time=1.2, rate_func=smooth)
        self.wait(0.3)

        formula = MathTex(
            r"\prod_{k=0}^{n-1}(z - z_k) = z^n - 1",
            font_size=28, color=YELLOW,
        ).move_to([rcol_x, -2.6, 0])
        self.play(Write(formula))
        self.wait(1.0)
