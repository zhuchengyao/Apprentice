from manim import *
import numpy as np


class ChainRuleExample(Scene):
    """
    Chain rule via stacked number-line stretches.

    Three horizontal number lines. A tiny interval of width dx at x on
    the top line maps through g to an interval of width g'(x)·dx on the
    middle line, then through f to an interval of width
    f'(g(x))·g'(x)·dx on the bottom line. ValueTracker sweeps x; the
    three orange intervals shrink and stretch in step, and live
    readouts show the local stretch factors. The product of the
    per-stage factors IS the chain-rule derivative.
    """

    def construct(self):
        title = Tex(r"Chain rule as successive stretches", font_size=36).to_edge(UP)
        self.play(Write(title))

        # f(y) = y², g(x) = sin(x)  ⇒  f(g(x)) = sin²(x)
        # g'(x) = cos(x),  f'(y) = 2y  ⇒  (f∘g)'(x) = 2 sin(x) cos(x)

        g = lambda x: np.sin(x)
        gp = lambda x: np.cos(x)
        f = lambda y: y * y
        fp = lambda y: 2 * y

        # Three parallel number lines
        top = NumberLine(x_range=[-PI, PI, PI / 2], length=10, include_numbers=False,
                         color=BLUE).shift(UP * 2)
        mid = NumberLine(x_range=[-1.2, 1.2, 0.5], length=10, include_numbers=False,
                         color=GREEN).shift(UP * 0.0)
        bot = NumberLine(x_range=[0, 1.2, 0.25], length=10, include_numbers=False,
                         color=YELLOW).shift(DOWN * 2)

        tl = MathTex("x", font_size=26, color=BLUE).next_to(top, LEFT, buff=0.2)
        ml = MathTex(r"y = \sin(x)", font_size=24, color=GREEN).next_to(mid, LEFT, buff=0.2)
        bl = MathTex(r"z = \sin^2(x)", font_size=24, color=YELLOW).next_to(bot, LEFT, buff=0.2)

        self.play(Create(top), Create(mid), Create(bot), Write(tl), Write(ml), Write(bl))

        # x sweep
        x_tracker = ValueTracker(-PI / 2 + 0.3)
        dx = 0.25  # visual interval half-width on x axis

        # Three "interval brackets"
        def x_interval():
            x0 = x_tracker.get_value()
            a = top.n2p(x0 - dx)
            b = top.n2p(x0 + dx)
            return Line(a, b, color=ORANGE, stroke_width=8)

        def y_interval():
            x0 = x_tracker.get_value()
            a = mid.n2p(g(x0 - dx))
            b = mid.n2p(g(x0 + dx))
            return Line(a, b, color=ORANGE, stroke_width=8)

        def z_interval():
            x0 = x_tracker.get_value()
            a = bot.n2p(f(g(x0 - dx)))
            b = bot.n2p(f(g(x0 + dx)))
            return Line(a, b, color=ORANGE, stroke_width=8)

        def x_dot():
            return Dot(top.n2p(x_tracker.get_value()), color=BLUE, radius=0.08)

        def y_dot():
            return Dot(mid.n2p(g(x_tracker.get_value())), color=GREEN, radius=0.08)

        def z_dot():
            return Dot(bot.n2p(f(g(x_tracker.get_value()))), color=YELLOW, radius=0.08)

        # Connecting arrows between dots
        def arrow_top_mid():
            return Arrow(x_dot().get_center(), y_dot().get_center(),
                         buff=0.1, color=GREY_B, stroke_width=2,
                         max_tip_length_to_length_ratio=0.08)

        def arrow_mid_bot():
            return Arrow(y_dot().get_center(), z_dot().get_center(),
                         buff=0.1, color=GREY_B, stroke_width=2,
                         max_tip_length_to_length_ratio=0.08)

        self.add(
            always_redraw(x_interval), always_redraw(y_interval), always_redraw(z_interval),
            always_redraw(x_dot), always_redraw(y_dot), always_redraw(z_dot),
            always_redraw(arrow_top_mid), always_redraw(arrow_mid_bot),
        )

        # Live readout with the three stretch factors
        def stretch_text():
            x0 = x_tracker.get_value()
            g0 = g(x0)
            gpx = gp(x0)
            fpy = fp(g0)
            return VGroup(
                MathTex(rf"x = {x0:+.2f}", color=BLUE, font_size=26),
                MathTex(rf"g'(x) = \cos(x) = {gpx:+.2f}", color=GREEN, font_size=26),
                MathTex(rf"f'(y) = 2y = {fpy:+.2f}", color=YELLOW, font_size=26),
                MathTex(rf"f'(g(x))\cdot g'(x) = {fpy * gpx:+.3f}",
                        color=ORANGE, font_size=28),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(DR).shift(UP * 0.2 + LEFT * 0.1)

        self.add(always_redraw(stretch_text))

        self.play(x_tracker.animate.set_value(PI / 2 - 0.3),
                  run_time=6, rate_func=smooth)
        self.wait(0.4)
        self.play(x_tracker.animate.set_value(0.1),
                  run_time=3, rate_func=smooth)
        self.wait(0.4)

        formula = MathTex(
            r"(f \circ g)'(x) = f'(g(x))\cdot g'(x)",
            font_size=36, color=ORANGE,
        ).to_edge(DOWN)
        self.play(Write(formula))
        self.wait(1.0)
