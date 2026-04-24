from manim import *
import numpy as np


class RolleTheoremExample(Scene):
    """
    Rolle's theorem: if f continuous on [a, b], differentiable on
    (a, b), and f(a) = f(b), then ∃ c ∈ (a, b) with f'(c) = 0.

    SINGLE_FOCUS: f(x) = sin(πx) + x(1−x) on [0, 1] (deforms on
    ValueTracker s_tr). f(0) = f(1) = 0 always. always_redraw
    horizontal tangent at critical point c where f'(c) = 0.
    """

    def construct(self):
        title = Tex(r"Rolle: $f(a)=f(b)\Rightarrow\exists c:\ f'(c)=0$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[0, 1.05, 0.2], y_range=[-0.3, 1.3, 0.3],
                    x_length=8, y_length=4.5,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(DOWN * 0.3)
        self.play(Create(axes))

        s_tr = ValueTracker(1.0)

        def f(x, s):
            return s * np.sin(PI * x) + (1 - s * 0.5) * x * (1 - x) * 2

        def fp(x, s):
            eps = 1e-4
            return (f(x + eps, s) - f(x - eps, s)) / (2 * eps)

        def curve():
            s = s_tr.get_value()
            return axes.plot(lambda x: float(f(x, s)),
                             x_range=[0, 1], color=BLUE, stroke_width=3)

        # endpoints
        self.add(Dot(axes.c2p(0, 0), color=GREEN, radius=0.1))
        self.add(Dot(axes.c2p(1, 0), color=GREEN, radius=0.1))
        self.add(Tex(r"$f(0)=f(1)=0$", color=GREEN, font_size=22).next_to(
            axes.c2p(0.5, -0.22), DOWN, buff=0.1))

        self.add(always_redraw(curve))

        # Find critical point via numeric root of f'
        def find_critical():
            s = s_tr.get_value()
            xs = np.linspace(0.05, 0.95, 200)
            derivs = [fp(x, s) for x in xs]
            for i in range(len(derivs) - 1):
                if derivs[i] * derivs[i + 1] < 0:
                    return float(xs[i])
            # fallback: midpoint with zero derivative
            return 0.5

        def tangent_line():
            c = find_critical()
            s = s_tr.get_value()
            y = f(c, s)
            return Line(axes.c2p(c - 0.2, y),
                         axes.c2p(c + 0.2, y),
                         color=RED, stroke_width=4)

        def c_dot():
            c = find_critical()
            s = s_tr.get_value()
            return Dot(axes.c2p(c, f(c, s)), color=RED, radius=0.13)

        def c_lbl():
            c = find_critical()
            return Tex(rf"$c\approx {c:.3f}$", color=RED,
                        font_size=22).move_to(axes.c2p(c, -0.2))

        self.add(always_redraw(tangent_line), always_redraw(c_dot),
                 always_redraw(c_lbl))

        info = VGroup(
            VGroup(Tex(r"deform $s=$", font_size=22),
                   DecimalNumber(1.0, num_decimal_places=2,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$f'(c)=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=5,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
            Tex(r"tangent horizontal at $c$",
                color=RED, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(s_tr.get_value()))
        info[1][1].add_updater(lambda m: m.set_value(fp(find_critical(), s_tr.get_value())))
        self.add(info)

        for sval in [0.3, 0.6, 1.0, 0.0, 0.8]:
            self.play(s_tr.animate.set_value(sval),
                      run_time=1.8, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.5)
