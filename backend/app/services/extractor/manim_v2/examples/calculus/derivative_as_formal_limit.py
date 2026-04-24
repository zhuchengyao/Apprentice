from manim import *
import numpy as np


class DerivativeAsFormalLimitExample(Scene):
    """
    Formal definition of derivative:
      f'(x) = lim_{h→0} [f(x+h) - f(x)] / h.
    Example: f(x) = x². Compute the limit numerically as h → 0.
    At x = 2: [(2+h)² - 4] / h = 4 + h → 4 as h → 0.
    """

    def construct(self):
        title = Tex(r"$f'(x)=\lim_{h\to 0}\frac{f(x+h)-f(x)}{h}$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[0, 4, 1], y_range=[0, 9, 2],
                    x_length=6.5, y_length=4.2,
                    axis_config={"include_numbers": True, "font_size": 16}
                    ).shift(LEFT * 2.3 + DOWN * 0.2)
        self.play(Create(axes))

        def f(x): return x * x

        self.add(axes.plot(f, x_range=[0, 3], color=BLUE, stroke_width=3))
        self.add(Tex(r"$f(x)=x^2$", color=BLUE, font_size=22).next_to(axes, UP, buff=0.1))

        x0 = 2.0
        h_tr = ValueTracker(1.2)

        def anchor():
            return Dot(axes.c2p(x0, f(x0)), color=GREEN, radius=0.12)

        def probe():
            h = h_tr.get_value()
            return Dot(axes.c2p(x0 + h, f(x0 + h)), color=ORANGE, radius=0.12)

        def secant():
            h = h_tr.get_value()
            return Line(axes.c2p(x0 - 0.3, f(x0) - (f(x0 + h) - f(x0)) / h * 0.3),
                         axes.c2p(x0 + h + 0.3, f(x0 + h) + (f(x0 + h) - f(x0)) / h * 0.3),
                         color=YELLOW, stroke_width=3)

        self.add(always_redraw(anchor), always_redraw(probe), always_redraw(secant))

        def ratio():
            h = h_tr.get_value()
            return (f(x0 + h) - f(x0)) / h

        info = VGroup(
            Tex(r"$x=2, f(x)=4$", color=GREEN, font_size=22),
            VGroup(Tex(r"$h=$", font_size=22),
                   DecimalNumber(1.2, num_decimal_places=4,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\frac{f(2+h)-f(2)}{h}=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=4,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"$\to f'(2)=2\cdot 2=4$",
                color=GREEN, font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.3)
        info[1][1].add_updater(lambda m: m.set_value(h_tr.get_value()))
        info[2][1].add_updater(lambda m: m.set_value(ratio()))
        self.add(info)

        self.play(h_tr.animate.set_value(0.01), run_time=5, rate_func=smooth)
        self.wait(0.8)
