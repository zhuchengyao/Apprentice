from manim import *
import numpy as np


class SigmoidNeuronExample(Scene):
    """
    Single-neuron sigmoid: y = σ(w x + b), σ(z) = 1/(1 + e^{-z}).

    TWO_COLUMN:
      LEFT  — axes; always_redraw sigmoid curve σ(wx+b) for
              ValueTracker weight w_tr and bias b_tr. Horizontal
              dashed line at 0.5; VERTICAL dashed line at the
              decision boundary x = -b/w; a BLUE cursor x_tr
              sweeps and a YELLOW rider dot tracks the curve.
      RIGHT — live w, b, x, z = wx+b, σ(z); tour: w phase,
              b phase, x phase.
    """

    def construct(self):
        title = Tex(r"Sigmoid neuron: $y = \sigma(wx + b)$, $\sigma(z) = \tfrac{1}{1+e^{-z}}$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ax = Axes(x_range=[-6, 6, 1], y_range=[-0.15, 1.15, 0.25],
                   x_length=7, y_length=4.2, tips=False,
                   axis_config={"font_size": 16, "include_numbers": True}
                   ).move_to([-2.5, -0.3, 0])
        self.play(Create(ax))

        w_tr = ValueTracker(1.0)
        b_tr = ValueTracker(0.0)
        x_tr = ValueTracker(0.0)

        def sigma(z):
            return 1 / (1 + np.exp(-z))

        def curve():
            w = w_tr.get_value()
            b = b_tr.get_value()
            return ax.plot(lambda x: sigma(w * x + b),
                            x_range=[-6, 6, 0.05],
                            color=BLUE, stroke_width=4)

        def boundary():
            w = w_tr.get_value()
            b = b_tr.get_value()
            if abs(w) < 1e-4:
                x0 = 0
            else:
                x0 = -b / w
            x0 = max(-6, min(6, x0))
            return DashedLine(ax.c2p(x0, -0.1), ax.c2p(x0, 1.1),
                               color=RED, stroke_width=2)

        half_line = DashedLine(ax.c2p(-6, 0.5), ax.c2p(6, 0.5),
                                color=GREY_B, stroke_width=1.5)

        def rider():
            x = x_tr.get_value()
            w = w_tr.get_value()
            b = b_tr.get_value()
            return Dot(ax.c2p(x, sigma(w * x + b)),
                        color=YELLOW, radius=0.11)

        def x_drop():
            x = x_tr.get_value()
            return DashedLine(ax.c2p(x, 0), ax.c2p(x, 1.05),
                               color=YELLOW_E, stroke_width=1.2)

        self.add(half_line,
                  always_redraw(curve),
                  always_redraw(boundary),
                  always_redraw(x_drop),
                  always_redraw(rider))

        def info():
            w = w_tr.get_value()
            b = b_tr.get_value()
            x = x_tr.get_value()
            z = w * x + b
            y = sigma(z)
            return VGroup(
                MathTex(rf"w = {w:+.2f}", color=WHITE, font_size=24),
                MathTex(rf"b = {b:+.2f}", color=WHITE, font_size=24),
                MathTex(rf"x = {x:+.2f}", color=YELLOW, font_size=24),
                MathTex(rf"z = wx + b = {z:+.2f}",
                         color=BLUE, font_size=22),
                MathTex(rf"y = \sigma(z) = {y:.3f}",
                         color=GREEN, font_size=24),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.3, 0.0, 0])

        self.add(always_redraw(info))

        # Phase 1: sweep w (w determines steepness)
        for wv in [0.5, 2.5, -2.0, 1.0]:
            self.play(w_tr.animate.set_value(wv),
                       run_time=1.2, rate_func=smooth)
            self.wait(0.2)
        # Phase 2: sweep b (b shifts the curve left/right)
        for bv in [2.0, -3.0, 0.0]:
            self.play(b_tr.animate.set_value(bv),
                       run_time=1.2, rate_func=smooth)
            self.wait(0.2)
        # Phase 3: sweep input x
        self.play(x_tr.animate.set_value(5.0),
                   run_time=2.5, rate_func=smooth)
        self.play(x_tr.animate.set_value(-5.0),
                   run_time=2.5, rate_func=smooth)
        self.play(x_tr.animate.set_value(0.0),
                   run_time=1.5, rate_func=smooth)
        self.wait(0.4)
