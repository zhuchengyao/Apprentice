from manim import *
import math
import numpy as np


def beta_pdf(x, a, b):
    if x <= 0 or x >= 1:
        return 0.0
    log_B = math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)
    log_pdf = (a - 1) * math.log(x) + (b - 1) * math.log(1 - x) - log_B
    if log_pdf < -50:
        return 0.0
    return math.exp(log_pdf)


class BetaDistributionExample(Scene):
    """
    Beta(α, β) family swept by two ValueTrackers.

    TWO_COLUMN layout:
      LEFT  — Axes plotting the Beta pdf for current (α, β) via always_redraw.
              The mean μ = α/(α+β) is marked by a red vertical dashed line
              that moves with the parameters.
      RIGHT — live α, β, μ, mode (where defined) readouts and the formula.

    Tour through five canonical shapes:
      (1, 1)   uniform
      (2, 2)   bell on [0,1]
      (5, 2)   left-skewed
      (2, 5)   right-skewed
      (0.5, 0.5) U-shape
      back to (2, 2)
    """

    def construct(self):
        title = Tex(r"Beta$(\alpha, \beta)$: two parameters reshape a density on $[0, 1]$",
                    font_size=30).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # LEFT: pdf plot
        axes = Axes(
            x_range=[0, 1, 0.2], y_range=[0, 5, 1],
            x_length=7.5, y_length=4.6,
            axis_config={"include_tip": True, "include_numbers": True, "font_size": 20},
        ).move_to([-2.0, -0.4, 0])
        x_lbl = MathTex("x", font_size=24).next_to(axes, DOWN, buff=0.1)
        y_lbl = MathTex(r"f(x;\alpha,\beta)", font_size=22).next_to(axes, LEFT, buff=0.1)
        self.play(Create(axes), Write(x_lbl), Write(y_lbl))

        alpha = ValueTracker(1.0)
        beta = ValueTracker(1.0)

        def pdf_curve():
            a = alpha.get_value()
            b = beta.get_value()
            return axes.plot(lambda x: beta_pdf(x, a, b),
                             x_range=[0.001, 0.999, 0.005],
                             color=BLUE, stroke_width=3)

        def mean_line():
            a = alpha.get_value()
            b = beta.get_value()
            mu = a / (a + b)
            top_y = beta_pdf(mu, a, b)
            return DashedLine(axes.c2p(mu, 0),
                              axes.c2p(mu, max(top_y, 0.5)),
                              color=RED, stroke_width=3)

        def mean_dot():
            a = alpha.get_value()
            b = beta.get_value()
            mu = a / (a + b)
            return Dot(axes.c2p(mu, 0), color=RED, radius=0.08)

        self.add(always_redraw(pdf_curve), always_redraw(mean_line), always_redraw(mean_dot))

        # RIGHT COLUMN
        rcol_x = +4.6

        def info_panel():
            a = alpha.get_value()
            b = beta.get_value()
            mu = a / (a + b)
            if a > 1 and b > 1:
                mode_str = f"{(a - 1) / (a + b - 2):.3f}"
            elif a < 1 and b < 1:
                mode_str = "0 and 1"
            elif a >= 1 and b < 1:
                mode_str = "1"
            else:
                mode_str = "0"
            return VGroup(
                MathTex(rf"\alpha = {a:.2f}", color=GREEN, font_size=28),
                MathTex(rf"\beta = {b:.2f}", color=ORANGE, font_size=28),
                MathTex(rf"\mu = \tfrac{{\alpha}}{{\alpha+\beta}} = {mu:.3f}",
                        color=RED, font_size=24),
                Text(f"mode: {mode_str}", color=GREY_B, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([rcol_x, +1.4, 0])

        self.add(always_redraw(info_panel))

        formula = MathTex(
            r"f(x) = \frac{x^{\alpha-1}(1-x)^{\beta-1}}{B(\alpha,\beta)}",
            font_size=24, color=YELLOW,
        ).move_to([rcol_x, -1.5, 0])
        self.play(Write(formula))

        # Tour through canonical shapes
        for label, (a, b) in [
            ("uniform (1, 1)", (1.0, 1.0)),
            ("bell (2, 2)", (2.0, 2.0)),
            ("left-skewed (5, 2)", (5.0, 2.0)),
            ("right-skewed (2, 5)", (2.0, 5.0)),
            ("U-shape (0.5, 0.5)", (0.5, 0.5)),
            ("bell again (2, 2)", (2.0, 2.0)),
        ]:
            self.play(alpha.animate.set_value(a),
                      beta.animate.set_value(b),
                      run_time=2.0, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.5)
