from manim import *
import numpy as np


class QuadraticFormulaDerivationExample(Scene):
    """
    Quadratic formula via complete-the-square, with live numeric
    coefficients (a, b, c) sweepable.

    TWO_COLUMN:
      LEFT  — Axes plotting y = ax² + bx + c with always_redraw curve;
              roots (x₁, x₂) marked when real, with vertex shown.
              ValueTrackers a, b, c sweep through several configs.
      RIGHT — algebraic walkthrough of completing-the-square in 6
              steps, with live discriminant Δ = b² - 4ac and the
              two-root formulas updated each frame.
    """

    def construct(self):
        title = Tex(r"Quadratic formula: $x = \dfrac{-b \pm \sqrt{b^2 - 4ac}}{2a}$",
                    font_size=28).to_edge(UP, buff=0.4)
        self.play(Write(title))

        a_tr = ValueTracker(1.0)
        b_tr = ValueTracker(-2.0)
        c_tr = ValueTracker(-3.0)

        axes = Axes(
            x_range=[-5, 5, 1], y_range=[-6, 6, 2],
            x_length=6.5, y_length=4.6,
            axis_config={"include_tip": True, "include_numbers": True, "font_size": 18},
        ).move_to([-2.5, -0.4, 0])
        self.play(Create(axes))

        def parabola():
            a, b, c = a_tr.get_value(), b_tr.get_value(), c_tr.get_value()
            return axes.plot(lambda x: a * x ** 2 + b * x + c,
                             x_range=[-5, 5, 0.05], color=BLUE)

        def vertex_dot():
            a, b, c = a_tr.get_value(), b_tr.get_value(), c_tr.get_value()
            xv = -b / (2 * a)
            yv = c - b ** 2 / (4 * a)
            return Dot(axes.c2p(xv, yv), color=ORANGE, radius=0.10)

        def root_dots():
            a, b, c = a_tr.get_value(), b_tr.get_value(), c_tr.get_value()
            disc = b * b - 4 * a * c
            grp = VGroup()
            if disc >= 0:
                sq = np.sqrt(disc)
                x1 = (-b - sq) / (2 * a)
                x2 = (-b + sq) / (2 * a)
                grp.add(Dot(axes.c2p(x1, 0), color=YELLOW, radius=0.10))
                grp.add(Dot(axes.c2p(x2, 0), color=YELLOW, radius=0.10))
            return grp

        self.add(always_redraw(parabola), always_redraw(vertex_dot),
                 always_redraw(root_dots))

        # RIGHT COLUMN
        rcol_x = +4.0

        def info_panel():
            a, b, c = a_tr.get_value(), b_tr.get_value(), c_tr.get_value()
            disc = b * b - 4 * a * c
            if disc >= 0:
                sq = np.sqrt(disc)
                x1 = (-b - sq) / (2 * a)
                x2 = (-b + sq) / (2 * a)
                roots_str = rf"x_1, x_2 = {x1:+.3f},\ {x2:+.3f}"
                color = GREEN
            else:
                roots_str = r"\text{complex roots}"
                color = ORANGE
            return VGroup(
                MathTex(rf"a = {a:+.2f},\ b = {b:+.2f},\ c = {c:+.2f}",
                        color=WHITE, font_size=22),
                MathTex(rf"\Delta = b^2 - 4ac = {disc:+.3f}",
                        color=YELLOW, font_size=22),
                MathTex(rf"x = \tfrac{{-b \pm \sqrt{{\Delta}}}}{{2a}}",
                        color=YELLOW, font_size=22),
                MathTex(roots_str, color=color, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([rcol_x, +1.6, 0])

        self.add(always_redraw(info_panel))

        # Static derivation steps below
        steps = VGroup(
            MathTex(r"ax^2 + bx + c = 0", font_size=20, color=GREY_B),
            MathTex(r"x^2 + \tfrac{b}{a}x = -\tfrac{c}{a}",
                    font_size=20, color=GREY_B),
            MathTex(r"\left(x + \tfrac{b}{2a}\right)^{\!2} = \tfrac{b^2 - 4ac}{4a^2}",
                    font_size=20, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([rcol_x, -1.6, 0])
        self.play(Write(steps))

        # Sweep through several (a, b, c) triples with different discriminants
        for av, bv, cv in [(1.0, -2.0, -3.0),    # roots -1, 3
                           (1.0, 0.0, -4.0),      # roots ±2
                           (1.0, 4.0, 4.0),       # repeated -2
                           (1.0, 2.0, 5.0),       # complex
                           (-0.5, 1.5, 2.0)]:     # downward parabola
            self.play(a_tr.animate.set_value(av),
                      b_tr.animate.set_value(bv),
                      c_tr.animate.set_value(cv),
                      run_time=2.0, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.5)
