from manim import *
import numpy as np


class LaplaceTransformExample(Scene):
    """
    Laplace transform of f(t) = e^(at) shown as a parameterized integral.

    TWO_COLUMN:
      LEFT  — Axes with f(t) = e^(at) for a small a (fixed), and the
              damped integrand e^(-st)·f(t). ValueTracker s sweeps;
              when s ≤ a the integrand grows unboundedly, when s > a
              the integrand decays — and the shaded area under it is
              the Laplace value F(s) = 1/(s − a).
      RIGHT — live readouts s, F(s) numerical (only valid when s > a),
              the F(s) closed form, and a small bottom plot of F(s)
              vs s with a vertical asymptote at s = a marked.
    """

    def construct(self):
        title = Tex(r"Laplace transform of $f(t) = e^{at}$: $F(s) = \dfrac{1}{s - a}$",
                    font_size=28).to_edge(UP, buff=0.4)
        self.play(Write(title))

        a = 0.5

        axes = Axes(
            x_range=[0, 6, 1], y_range=[0, 4, 1],
            x_length=6.4, y_length=3.6,
            axis_config={"include_tip": True, "include_numbers": True, "font_size": 18},
        ).move_to([-2.6, +0.4, 0])
        self.play(Create(axes))

        f_curve = axes.plot(lambda t: np.exp(a * t), x_range=[0, 5.9], color=BLUE)
        f_lbl = MathTex(rf"f(t) = e^{{{a}t}}", color=BLUE,
                        font_size=22).next_to(axes.c2p(5.9, np.exp(a * 5.9)),
                                              UR, buff=0.05)
        self.play(Create(f_curve), Write(f_lbl))

        s_tr = ValueTracker(2.0)

        def integrand(t, s):
            return np.exp(-s * t) * np.exp(a * t)

        def integrand_curve():
            s = s_tr.get_value()
            return axes.plot(lambda t: integrand(t, s),
                             x_range=[0, 5.9, 0.05], color=ORANGE)

        def integrand_area():
            s = s_tr.get_value()
            curve = axes.plot(lambda t: integrand(t, s),
                              x_range=[0, 5.9, 0.05])
            return axes.get_area(curve, x_range=[0, 5.9],
                                 color=ORANGE, opacity=0.4)

        self.add(always_redraw(integrand_area), always_redraw(integrand_curve))

        # RIGHT COLUMN
        rcol_x = +4.0

        def info_panel():
            s = s_tr.get_value()
            valid = s > a + 1e-3
            if valid:
                fs = 1 / (s - a)
                fs_str = f"{fs:.4f}"
            else:
                fs_str = r"\text{diverges}"
            return VGroup(
                MathTex(rf"a = {a}", color=BLUE, font_size=22),
                MathTex(rf"s = {s:.2f}", color=ORANGE, font_size=24),
                MathTex(r"e^{-st}f(t) = e^{(a-s)t}",
                        color=ORANGE, font_size=22),
                MathTex(rf"F(s) = \int_0^\infty e^{{-st}} f(t)\,dt",
                        color=YELLOW, font_size=20),
                MathTex(rf"= \frac{{1}}{{s - a}} = {fs_str}",
                        color=YELLOW if valid else RED, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([rcol_x, +1.6, 0])

        self.add(always_redraw(info_panel))

        # Mini-axes for F(s) vs s
        mini_axes = Axes(
            x_range=[0, 4, 1], y_range=[0, 4, 1],
            x_length=2.6, y_length=1.6,
            axis_config={"include_tip": False, "include_numbers": False, "font_size": 14},
        ).move_to([rcol_x, -1.8, 0])
        F_curve = mini_axes.plot(
            lambda s: 1 / (s - a) if s > a + 0.1 else 8,
            x_range=[a + 0.1, 3.95, 0.02],
            color=YELLOW,
        )
        asymptote = DashedLine(mini_axes.c2p(a, 0), mini_axes.c2p(a, 4),
                                color=RED, stroke_width=2)
        F_lbl = Tex(r"$F(s)$ for $s > a$", color=YELLOW,
                    font_size=18).next_to(mini_axes, UP, buff=0.08)
        self.play(Create(mini_axes), Create(F_curve), Create(asymptote), Write(F_lbl))

        def cursor():
            s = s_tr.get_value()
            if s > a + 0.05:
                return Dot(mini_axes.c2p(s, 1 / (s - a)),
                           color=YELLOW, radius=0.07)
            return Dot([0, 0, 0], color=BLACK, radius=0.001)

        self.add(always_redraw(cursor))

        # Sweep s through several values
        for tgt in [3.5, 1.5, 0.7, 2.5]:
            self.play(s_tr.animate.set_value(tgt),
                      run_time=2.0, rate_func=smooth)
            self.wait(0.4)

        self.wait(0.5)
