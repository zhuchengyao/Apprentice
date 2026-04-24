from manim import *
import numpy as np


class NumberlineDerivativeExample(Scene):
    """
    Derivative as a stretching factor: a tiny dx-interval at x maps to
    f'(x)·dx on the output line.

    THREE_ROW:
      TOP    — input number line for x; ValueTracker x_tr drives a
               BLUE marker and an orange sub-interval [x-dx, x+dx].
      MIDDLE — labels for f(x) = x² mapping notation, with f' = 2x annotation.
      BOTTOM — output number line for f(x); always_redraw shows the
               YELLOW marker at f(x) and the corresponding orange
               output interval [f(x-dx), f(x+dx)].
    Live readout: x, dx (constant 0.1), output interval length, and 2x
    for comparison. As x sweeps, the output interval visibly stretches
    and shrinks proportional to 2x.
    """

    def construct(self):
        title = Tex(r"$f'(x_0)$ = local stretch factor on the number line",
                    font_size=28).to_edge(UP, buff=0.4)
        self.play(Write(title))

        in_line = NumberLine(
            x_range=[0, 3, 0.5], length=10,
            include_numbers=True,
            decimal_number_config={"num_decimal_places": 1, "font_size": 18},
        ).move_to([0, +1.5, 0])
        in_lbl = MathTex(r"x", font_size=24).next_to(in_line, LEFT, buff=0.15)
        self.play(Create(in_line), Write(in_lbl))

        out_line = NumberLine(
            x_range=[0, 9, 1], length=10,
            include_numbers=True,
            decimal_number_config={"num_decimal_places": 0, "font_size": 18},
        ).move_to([0, -1.8, 0])
        out_lbl = MathTex(r"f(x) = x^2", font_size=24).next_to(out_line, LEFT, buff=0.15)
        self.play(Create(out_line), Write(out_lbl))

        x_tr = ValueTracker(0.5)
        dx = 0.1

        def x_marker():
            x = x_tr.get_value()
            return Dot(in_line.n2p(x), color=BLUE, radius=0.10)

        def x_interval():
            x = x_tr.get_value()
            return Line(in_line.n2p(x - dx), in_line.n2p(x + dx),
                        color=ORANGE, stroke_width=8)

        def y_marker():
            x = x_tr.get_value()
            return Dot(out_line.n2p(x * x), color=YELLOW, radius=0.10)

        def y_interval():
            x = x_tr.get_value()
            return Line(out_line.n2p((x - dx) ** 2),
                        out_line.n2p((x + dx) ** 2),
                        color=ORANGE, stroke_width=8)

        def connector():
            x = x_tr.get_value()
            return DashedLine(x_marker().get_center(),
                              y_marker().get_center(),
                              color=GREY_B, stroke_width=2, stroke_opacity=0.6)

        self.add(always_redraw(x_marker), always_redraw(x_interval),
                 always_redraw(y_marker), always_redraw(y_interval),
                 always_redraw(connector))

        # Live readout (right side)
        rcol_x = +5.4

        def info_panel():
            x = x_tr.get_value()
            in_len = 2 * dx
            out_len = (x + dx) ** 2 - (x - dx) ** 2  # = 4·x·dx
            ratio = out_len / in_len
            return VGroup(
                MathTex(rf"x = {x:.2f}", color=BLUE, font_size=22),
                MathTex(rf"\Delta x = {2*dx:.2f}", color=ORANGE, font_size=20),
                MathTex(rf"\Delta y = {out_len:.3f}", color=YELLOW, font_size=22),
                MathTex(rf"\tfrac{{\Delta y}}{{\Delta x}} = {ratio:.2f}",
                        color=YELLOW, font_size=22),
                MathTex(rf"f'(x) = 2x = {2*x:.2f}",
                        color=GREEN, font_size=24),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([rcol_x, 0, 0])

        self.add(always_redraw(info_panel))

        # Sweep
        for tgt in [2.5, 0.5, 1.5]:
            self.play(x_tr.animate.set_value(tgt),
                      run_time=2.5, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.5)
