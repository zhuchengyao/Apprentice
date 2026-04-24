from manim import *
import numpy as np


class EpsilonDeltaLimitExample(Scene):
    """
    ε–δ definition of a limit, animated by a shrinking ε.

    Function: f(x) = x², point a = 2, limit L = 4.

    TWO_COLUMN layout:
      LEFT  — graph of f with a horizontal yellow band of half-height ε
              around y=L and a vertical green band of half-width δ
              around x=a. ValueTracker eps sweeps from 1.2 → 0.05; on
              each frame δ is recomputed so that the entire green band
              maps inside the yellow band (δ = √(L+ε) − a, the largest
              valid δ on the right side).
      RIGHT — live readouts of ε and δ, plus the formal statement.
    """

    def construct(self):
        title = Tex(r"$\varepsilon$–$\delta$ limit: any window around $L$ has a matching $\delta$",
                    font_size=32).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # LEFT COLUMN: graph
        a, L = 2.0, 4.0
        f = lambda x: x * x

        axes = Axes(
            x_range=[0, 4, 1], y_range=[0, 9, 2],
            x_length=6.4, y_length=5.2,
            axis_config={"include_tip": True, "include_numbers": True, "font_size": 20},
        ).move_to([-2.6, -0.2, 0])
        graph = axes.plot(f, x_range=[0, 3.0], color=BLUE)
        self.play(Create(axes), Create(graph))

        anchor = Dot(axes.c2p(a, L), color=YELLOW, radius=0.1)
        anchor_lbl = MathTex(rf"(a, L) = ({a:.0f}, {L:.0f})",
                             color=YELLOW, font_size=22).next_to(anchor, UR, buff=0.1)
        self.play(FadeIn(anchor), Write(anchor_lbl))

        eps_tracker = ValueTracker(1.2)

        def delta_for(eps_val: float) -> float:
            # Largest δ so that f((a-δ, a+δ)) ⊂ (L-ε, L+ε). For f(x)=x² near a=2,
            # the binding constraint is the right side: (a+δ)² = L+ε ⇒ δ = √(L+ε) - a.
            return np.sqrt(L + eps_val) - a

        def y_band():
            eps = eps_tracker.get_value()
            top = axes.c2p(0, L + eps)
            bot = axes.c2p(0, L - eps)
            height = abs(top[1] - bot[1])
            band = Rectangle(width=axes.x_length, height=height,
                             color=YELLOW, fill_opacity=0.25, stroke_width=0)
            band.move_to([axes.get_center()[0], (top[1] + bot[1]) / 2, 0])
            return band

        def x_band():
            eps = eps_tracker.get_value()
            d = delta_for(eps)
            left = axes.c2p(a - d, 0)
            right = axes.c2p(a + d, 0)
            width = abs(right[0] - left[0])
            band = Rectangle(width=width, height=axes.y_length,
                             color=GREEN, fill_opacity=0.25, stroke_width=0)
            band.move_to([(left[0] + right[0]) / 2, axes.get_center()[1], 0])
            return band

        def eps_arrows():
            eps = eps_tracker.get_value()
            tip_top = axes.c2p(0.15, L + eps)
            tip_bot = axes.c2p(0.15, L - eps)
            return DoubleArrow(tip_bot, tip_top, color=YELLOW,
                               buff=0, stroke_width=3,
                               max_tip_length_to_length_ratio=0.08)

        def delta_arrows():
            eps = eps_tracker.get_value()
            d = delta_for(eps)
            tip_l = axes.c2p(a - d, 0.2)
            tip_r = axes.c2p(a + d, 0.2)
            return DoubleArrow(tip_l, tip_r, color=GREEN,
                               buff=0, stroke_width=3,
                               max_tip_length_to_length_ratio=0.08)

        self.add(always_redraw(y_band), always_redraw(x_band),
                 always_redraw(eps_arrows), always_redraw(delta_arrows))
        # Re-add anchor + graph on top of bands
        self.add(graph, anchor, anchor_lbl)

        # RIGHT COLUMN: readouts
        rcol_x = +4.5

        def info_panel():
            eps = eps_tracker.get_value()
            d = delta_for(eps)
            return VGroup(
                MathTex(rf"\varepsilon = {eps:.2f}", color=YELLOW, font_size=30),
                MathTex(rf"\delta = {d:.3f}", color=GREEN, font_size=30),
                MathTex(rf"\delta \approx \frac{{\varepsilon}}{{2a}} = {eps/(2*a):.3f}",
                        color=GREEN, font_size=24),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([rcol_x, 1.6, 0])

        self.add(always_redraw(info_panel))

        rule = MathTex(
            r"\forall \varepsilon > 0\;",
            r"\exists \delta > 0:",
            r"|x - a| < \delta",
            r"\Rightarrow |f(x) - L| < \varepsilon",
            font_size=22,
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([rcol_x, -1.1, 0])
        self.play(Write(rule))

        # Sweep ε down — the green δ-band shrinks in lockstep
        self.play(eps_tracker.animate.set_value(0.05), run_time=6, rate_func=smooth)
        self.wait(0.5)

        conclusion = MathTex(r"\lim_{x \to a} f(x) = L",
                             font_size=30, color=YELLOW).move_to([rcol_x, -3.0, 0])
        self.play(Write(conclusion))
        self.wait(1.0)
