from manim import *
import numpy as np


class CosSquaredHalfAngleExample(Scene):
    """
    Half-angle identity cos²x = (1 + cos 2x)/2 — pointwise check.

    SINGLE_FOCUS:
      One axes shows BOTH curves: cos²x (BLUE, thin) and
      (1 + cos 2x)/2 (YELLOW, thick semi-transparent) — they trace
      identical shapes. ValueTracker x_tr sweeps x through 0..2π;
      a BLUE dot on cos²x and a YELLOW dot on the half-angle form
      stay visually coincident every frame, connected by a thin
      dashed vertical drop. A live panel shows x, the two values,
      and |difference| staying at machine epsilon.
    """

    def construct(self):
        title = Tex(r"Half-angle identity: $\cos^2 x = \tfrac{1}{2} + \tfrac{1}{2}\cos(2x)$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(
            x_range=[0, 2 * PI + 0.1, PI / 2],
            y_range=[-0.15, 1.15, 0.25],
            x_length=9, y_length=3.2,
            tips=False,
            axis_config={"font_size": 16},
        ).move_to([-0.5, -0.1, 0])

        # Replace numeric x-axis ticks with π-labels
        x_lbls = VGroup()
        for k, lbl in [(0, r"0"), (1, r"\tfrac{\pi}{2}"),
                        (2, r"\pi"), (3, r"\tfrac{3\pi}{2}"),
                        (4, r"2\pi")]:
            x_lbls.add(MathTex(lbl, font_size=20).next_to(
                axes.c2p(k * PI / 2, 0), DOWN, buff=0.12))
        self.play(Create(axes), FadeIn(x_lbls))

        cos_sq = axes.plot(lambda x: np.cos(x) ** 2,
                           x_range=[0, 2 * PI], color=BLUE, stroke_width=4)
        half_angle = axes.plot(lambda x: 0.5 + np.cos(2 * x) / 2,
                               x_range=[0, 2 * PI], color=YELLOW,
                               stroke_width=8, stroke_opacity=0.45)
        self.play(Create(cos_sq), Create(half_angle))

        legend = VGroup(
            MathTex(r"\cos^2 x", color=BLUE, font_size=26),
            MathTex(r"\tfrac{1}{2}+\tfrac{1}{2}\cos(2x)",
                    color=YELLOW, font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([-5.3, 2.3, 0])
        self.play(Write(legend))

        # Sweeping cursor
        x_tr = ValueTracker(0.001)

        def cos_dot():
            x = x_tr.get_value()
            return Dot(axes.c2p(x, np.cos(x) ** 2),
                       color=BLUE, radius=0.09)

        def half_dot():
            x = x_tr.get_value()
            return Dot(axes.c2p(x, 0.5 + np.cos(2 * x) / 2),
                       color=YELLOW, radius=0.09)

        def drop():
            x = x_tr.get_value()
            return DashedLine(axes.c2p(x, 0),
                              axes.c2p(x, 1.08),
                              color=GREY_B, stroke_width=1.5)

        self.add(always_redraw(drop),
                 always_redraw(cos_dot),
                 always_redraw(half_dot))

        def info_panel():
            x = x_tr.get_value()
            a = np.cos(x) ** 2
            b = 0.5 + np.cos(2 * x) / 2
            return VGroup(
                MathTex(rf"x = {x:.3f}", color=WHITE, font_size=22),
                MathTex(rf"\cos^2 x = {a:.4f}",
                        color=BLUE, font_size=22),
                MathTex(rf"\tfrac{{1+\cos 2x}}{{2}} = {b:.4f}",
                        color=YELLOW, font_size=22),
                MathTex(rf"|\text{{diff}}| = {abs(a - b):.1e}",
                        color=GREEN, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.2, -2.6, 0])

        self.add(always_redraw(info_panel))

        self.play(x_tr.animate.set_value(2 * PI),
                  run_time=8, rate_func=linear)
        self.wait(0.6)
