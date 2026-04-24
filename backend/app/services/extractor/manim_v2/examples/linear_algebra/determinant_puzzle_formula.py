from manim import *
import numpy as np


class DeterminantPuzzleFormulaExample(Scene):
    """
    2×2 determinant from column parallelogram area:
    det[[a, b], [c, d]] = ad - bc.

    TWO_COLUMN:
      LEFT  — parallelogram spanned by columns (a, c) and (b, d)
              drawn on a NumberPlane; always_redraw via 4 Value-
              Trackers a, b, c, d. Shaded area colored GREEN for
              positive det, RED for negative.
      RIGHT — live matrix + computation ad - bc, and an annotated
              formula.
    """

    def construct(self):
        title = Tex(r"Determinant of a $2\times 2$: $\det\,A = ad - bc = $ (signed) area",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-3, 4, 1], y_range=[-3, 4, 1],
                             x_length=6, y_length=6,
                             background_line_style={"stroke_opacity": 0.3}
                             ).move_to([-3, -0.3, 0])
        self.play(Create(plane))

        a_tr = ValueTracker(2.0)
        b_tr = ValueTracker(1.0)
        c_tr = ValueTracker(0.5)
        d_tr = ValueTracker(2.0)

        def col_arrow(vec_fn, color):
            def f():
                v = vec_fn()
                return Arrow(plane.c2p(0, 0),
                               plane.c2p(v[0], v[1]),
                               color=color, buff=0,
                               stroke_width=5,
                               max_tip_length_to_length_ratio=0.15)
            return f

        def v1():
            return np.array([a_tr.get_value(), c_tr.get_value()])

        def v2():
            return np.array([b_tr.get_value(), d_tr.get_value()])

        def para():
            a, c = v1()
            b, d = v2()
            det = a * d - b * c
            color = GREEN if det >= 0 else RED
            return Polygon(
                plane.c2p(0, 0),
                plane.c2p(a, c),
                plane.c2p(a + b, c + d),
                plane.c2p(b, d),
                color=color, fill_opacity=0.35, stroke_width=2)

        self.add(always_redraw(para),
                  always_redraw(col_arrow(v1, BLUE)),
                  always_redraw(col_arrow(v2, ORANGE)))

        def info():
            a, c = v1()
            b, d = v2()
            det = a * d - b * c
            color = GREEN if det >= 0 else RED
            return VGroup(
                MathTex(rf"A = \begin{{pmatrix}} {a:.2f} & {b:.2f} \\ {c:.2f} & {d:.2f} \end{{pmatrix}}",
                         color=WHITE, font_size=24),
                MathTex(rf"\det A = ad - bc", color=WHITE, font_size=22),
                MathTex(rf"= {a:.2f} \cdot {d:.2f} - {b:.2f} \cdot {c:.2f}",
                         color=WHITE, font_size=22),
                MathTex(rf"= {det:+.3f}",
                         color=color, font_size=28),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.8, 0.0, 0])

        self.add(always_redraw(info))

        tour = [(2, 1, 0.5, 2),
                (2, 0.5, 1.5, 1),  # smaller det
                (3, -1, 1, 2),
                (2, 2, 1, 1),  # det near zero (nearly parallel)
                (1, 2, 2, 1),  # det = -3 negative
                (2, 0, 0, 2)]  # diagonal, det = 4
        for (a, b, c, d) in tour:
            self.play(a_tr.animate.set_value(a),
                       b_tr.animate.set_value(b),
                       c_tr.animate.set_value(c),
                       d_tr.animate.set_value(d),
                       run_time=1.6, rate_func=smooth)
            self.wait(0.35)
        self.wait(0.4)
