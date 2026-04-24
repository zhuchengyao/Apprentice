from manim import *
import numpy as np


class IntegralAsAreaExample(Scene):
    """
    Riemann sum converging to the integral.

    A ValueTracker n drives the number of rectangles from 4 to 80.
    The rectangles are drawn with always_redraw using
    axes.get_riemann_rectangles. A live numeric readout of the
    approximate area compares to the exact analytic value
    ∫₀.₅^4.5 (0.2 x² + 0.3) dx.
    """

    def construct(self):
        title = Tex(r"Riemann sum $\to$ integral as rectangles narrow", font_size=34).to_edge(UP)
        self.play(Write(title))

        axes = Axes(
            x_range=[0, 5, 1], y_range=[0, 5, 1],
            x_length=8, y_length=4, tips=False,
            axis_config={"include_numbers": True, "font_size": 22},
        ).shift(0.2 * DOWN)
        labels = axes.get_axis_labels("x", "f(x)")
        f = lambda x: 0.2 * x * x + 0.3
        graph = axes.plot(f, color=BLUE)
        self.play(Create(axes), Write(labels), Create(graph))

        a, b = 0.5, 4.5
        exact = 0.2 * (b ** 3 - a ** 3) / 3 + 0.3 * (b - a)

        # Permanent reference area shading
        true_area = axes.get_area(graph, x_range=[a, b], color=GREEN, opacity=0.25)
        self.play(FadeIn(true_area))

        n_tracker = ValueTracker(4)

        def riemann():
            n = max(1, int(n_tracker.get_value()))
            dx = (b - a) / n
            rects = axes.get_riemann_rectangles(
                graph, x_range=[a, b], dx=dx,
                input_sample_type="center",
                stroke_width=0.5, fill_opacity=0.55, stroke_color=WHITE,
            )
            rects.set_color(ORANGE)
            return rects

        def approx_area():
            n = max(1, int(n_tracker.get_value()))
            dx = (b - a) / n
            s = sum(f(a + (k + 0.5) * dx) for k in range(n)) * dx
            return s

        rects = always_redraw(riemann)
        self.add(rects)

        readout = VGroup(
            MathTex(r"n", color=WHITE, font_size=28),
            MathTex("=", font_size=28),
            DecimalNumber(4, num_decimal_places=0, font_size=28, color=WHITE),
        ).arrange(RIGHT, buff=0.12).to_corner(UR).shift(LEFT * 0.3 + DOWN * 0.4)

        approx_readout = VGroup(
            MathTex(r"\text{approx}", color=ORANGE, font_size=26),
            MathTex("=", font_size=26),
            DecimalNumber(approx_area(), num_decimal_places=4, font_size=26, color=ORANGE),
        ).arrange(RIGHT, buff=0.12).next_to(readout, DOWN, buff=0.15)

        exact_readout = VGroup(
            MathTex(r"\text{exact}", color=GREEN, font_size=26),
            MathTex("=", font_size=26),
            DecimalNumber(exact, num_decimal_places=4, font_size=26, color=GREEN),
        ).arrange(RIGHT, buff=0.12).next_to(approx_readout, DOWN, buff=0.1)

        readout[2].add_updater(lambda d: d.set_value(int(n_tracker.get_value())))
        approx_readout[2].add_updater(lambda d: d.set_value(approx_area()))
        self.add(readout, approx_readout, exact_readout)

        self.play(n_tracker.animate.set_value(80), run_time=6, rate_func=linear)
        self.wait(0.4)

        readout[2].clear_updaters()
        approx_readout[2].clear_updaters()

        formula = MathTex(
            r"\int_a^b f(x)\, dx = \lim_{n\to\infty} \sum_{k=1}^{n} f(x_k^*)\,\Delta x",
            font_size=30, color=YELLOW,
        ).to_edge(DOWN)
        self.play(Write(formula))
        self.wait(1.0)
