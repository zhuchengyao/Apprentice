from manim import *
import numpy as np


class ExponentialMemorylessExample(Scene):
    """
    Exponential distribution is memoryless: P(X > s + t | X > s) =
    P(X > t). Condition on survival past s; the remaining lifetime
    still has rate λ.

    TWO_COLUMN:
      LEFT  — axes with λe^(-λt) pdf; ValueTracker s_tr shifts
              conditional-origin; always_redraw rescaled density
              conditional on X > s overlaid on original.
      RIGHT — live P(X > s+t | X > s) = e^(-λt) computation.
    """

    def construct(self):
        title = Tex(r"Exponential memoryless: $P(X>s+t \mid X>s) = P(X>t)$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        lam = 0.8

        ax = Axes(x_range=[0, 6, 1], y_range=[0, 1, 0.25],
                   x_length=8, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-0.5, -0.3, 0])
        self.play(Create(ax))

        # Original pdf
        pdf_curve = ax.plot(lambda t: lam * np.exp(-lam * t),
                              x_range=[0, 6, 0.02],
                              color=BLUE, stroke_width=3)
        self.play(Create(pdf_curve))

        s_tr = ValueTracker(0.0)

        def survived_shade():
            s = s_tr.get_value()
            # Shade {t > s} in the original pdf
            pts = [ax.c2p(s, 0)]
            for t in np.linspace(s, 6, 60):
                pts.append(ax.c2p(t, lam * np.exp(-lam * t)))
            pts.append(ax.c2p(6, 0))
            return Polygon(*pts, color=GREY_B, fill_opacity=0.3,
                             stroke_width=0)

        def s_line():
            s = s_tr.get_value()
            return DashedLine(ax.c2p(s, 0), ax.c2p(s, 1.0),
                               color=GREEN, stroke_width=2)

        def conditional_curve():
            """Conditional density f_{X-s|X>s}(t) = λe^(-λt) (same as
            original, plotted shifted by s for visual."""
            s = s_tr.get_value()
            return ax.plot(
                lambda t: lam * np.exp(-lam * (t - s)) if t >= s else 0,
                x_range=[s, 6, 0.02],
                color=ORANGE, stroke_width=3)

        self.add(always_redraw(survived_shade),
                  always_redraw(s_line),
                  always_redraw(conditional_curve))

        def info():
            s = s_tr.get_value()
            return VGroup(
                MathTex(rf"\lambda = {lam}", color=WHITE, font_size=22),
                MathTex(rf"s = {s:.2f}", color=GREEN, font_size=22),
                MathTex(rf"P(X > s) = e^{{-\lambda s}} = {np.exp(-lam * s):.4f}",
                         color=GREY_B, font_size=20),
                MathTex(r"P(X > s+t \mid X > s)",
                         color=ORANGE, font_size=20),
                MathTex(r"= e^{-\lambda t}\ \text{same shape as original}",
                         color=ORANGE, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        self.play(s_tr.animate.set_value(3.0),
                   run_time=6, rate_func=smooth)
        self.wait(0.4)
