from manim import *
import numpy as np


class MeanValueTheoremCauchyExample(Scene):
    """
    Cauchy's mean value theorem: for f, g continuous on [a, b] and
    differentiable on (a, b), ∃ c ∈ (a, b) with
        (f(b) − f(a)) g'(c) = (g(b) − g(a)) f'(c).

    Example: f(x) = x², g(x) = x³ on [0, 2].
    (4)(3c²) = (8)(2c) ⇒ c = 4/3.

    TWO_COLUMN: LEFT parametric (g(t), f(t)) curve + secant from
    (g(a), f(a)) to (g(b), f(b)) + tangent at c. RIGHT panel.
    """

    def construct(self):
        title = Tex(r"Cauchy MVT: $\exists c:\ \frac{f(b)-f(a)}{g(b)-g(a)}=\frac{f'(c)}{g'(c)}$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[0, 8.5, 2], y_range=[0, 4.5, 1],
                    x_length=6.5, y_length=4.0,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(LEFT * 2.2 + DOWN * 0.2)
        axes_lbls = VGroup(
            Tex(r"$g(x)=x^3$", font_size=20).next_to(axes, RIGHT, buff=0.2),
            Tex(r"$f(x)=x^2$", font_size=20).next_to(axes, UP, buff=0.15).shift(LEFT * 2),
        )
        self.play(Create(axes), Write(axes_lbls))

        curve = axes.plot_parametric_curve(
            lambda t: np.array([t ** 3, t ** 2, 0]),
            t_range=[0, 2], color=BLUE, stroke_width=3)
        self.play(Create(curve))

        # Endpoints
        a, b = 0.0, 2.0
        A_pt = axes.c2p(a ** 3, a ** 2)
        B_pt = axes.c2p(b ** 3, b ** 2)
        dot_A = Dot(A_pt, color=GREEN, radius=0.1)
        dot_B = Dot(B_pt, color=GREEN, radius=0.1)
        secant = Line(A_pt, B_pt, color=GREEN, stroke_width=3)
        self.play(FadeIn(dot_A), FadeIn(dot_B), Create(secant))

        # Tangent point c
        c_tr = ValueTracker(0.2)

        def P_tan():
            c = c_tr.get_value()
            return axes.c2p(c ** 3, c ** 2)

        def tangent_line():
            c = c_tr.get_value()
            # tangent direction = (g'(c), f'(c)) = (3c², 2c)
            dx, dy = 3 * c ** 2, 2 * c
            norm = np.sqrt(dx * dx + dy * dy)
            if norm < 1e-6:
                return VMobject()
            ux, uy = dx / norm * 2.5, dy / norm * 1.3
            pt = P_tan()
            return Line(axes.c2p(c ** 3 - ux, c ** 2 - uy),
                         axes.c2p(c ** 3 + ux, c ** 2 + uy),
                         color=RED, stroke_width=3)

        def c_dot():
            return Dot(P_tan(), color=RED, radius=0.11)

        self.add(always_redraw(tangent_line), always_redraw(c_dot))

        # Right panel
        def slope_tangent():
            c = c_tr.get_value()
            if c < 1e-6:
                return 0.0
            return 2 * c / (3 * c ** 2)  # f'(c)/g'(c) = 2c/(3c²) = 2/(3c)

        def slope_secant():
            return (b ** 2 - a ** 2) / (b ** 3 - a ** 3)

        info = VGroup(
            Tex(rf"$a={a:.0f},\ b={b:.0f}$", font_size=22),
            VGroup(Tex(r"secant slope $=\frac{f(b)-f(a)}{g(b)-g(a)}=\frac{1}{2}$",
                       color=GREEN, font_size=22),
                    ).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$c=$", font_size=22),
                   DecimalNumber(0.2, num_decimal_places=3,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$f'(c)/g'(c)=\frac{2}{3c}=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=4,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
            Tex(r"match at $c=4/3\approx 1.333$",
                color=YELLOW, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.2)
        info[2][1].add_updater(lambda m: m.set_value(c_tr.get_value()))
        info[3][1].add_updater(lambda m: m.set_value(slope_tangent()))
        self.add(info)

        self.play(c_tr.animate.set_value(4 / 3),
                  run_time=4, rate_func=smooth)
        self.wait(0.8)
        self.play(c_tr.animate.set_value(1.9),
                  run_time=2, rate_func=smooth)
        self.play(c_tr.animate.set_value(4 / 3),
                  run_time=1.5, rate_func=smooth)
        self.wait(0.5)
