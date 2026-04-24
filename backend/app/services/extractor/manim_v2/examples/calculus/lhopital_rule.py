from manim import *
import numpy as np


class LHopitalRuleExample(Scene):
    """
    L'Hôpital's rule resolves 0/0 by switching to derivative ratio.

    Example: lim_{x→0} sin(x)/x = 1, also lim of cos(x)/1 = 1.

    TWO_COLUMN:
      LEFT  — graphs of f(x) = sin(x) and g(x) = x with always_redraw
              dots tracking position at the current x; below them their
              ratio f(x)/g(x) drawn as a separate curve with an always_
              redraw dot moving along it. ValueTracker x sweeps from
              1.5 toward 0.001.
      RIGHT — live readouts of f(x), g(x), f(x)/g(x), f'(x), g'(x),
              and the (constant in the limit) derivative ratio.
    """

    def construct(self):
        title = Tex(r"L'H\^opital's rule: $\lim \tfrac{f}{g} = \lim \tfrac{f'}{g'}$ for $0/0$ forms",
                    font_size=30).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # LEFT: graphs of sin(x), x, and sin(x)/x near 0
        axes_top = Axes(
            x_range=[-1.6, 1.6, 0.5], y_range=[-1.2, 1.6, 0.5],
            x_length=6.4, y_length=2.6,
            axis_config={"include_tip": False, "include_numbers": True, "font_size": 18},
        ).move_to([-2.4, +1.4, 0])
        sin_curve = axes_top.plot(np.sin, x_range=[-1.55, 1.55], color=BLUE)
        line_curve = axes_top.plot(lambda x: x, x_range=[-1.55, 1.55], color=GREEN)
        sin_lbl = MathTex(r"f(x)=\sin x", color=BLUE, font_size=22).next_to(
            axes_top.c2p(1.5, np.sin(1.5)), RIGHT, buff=0.1)
        g_lbl = MathTex(r"g(x)=x", color=GREEN, font_size=22).next_to(
            axes_top.c2p(1.5, 1.5), RIGHT, buff=0.1)
        self.play(Create(axes_top), Create(sin_curve), Create(line_curve),
                  Write(sin_lbl), Write(g_lbl))

        axes_bot = Axes(
            x_range=[-1.6, 1.6, 0.5], y_range=[0.5, 1.1, 0.1],
            x_length=6.4, y_length=2.4,
            axis_config={"include_tip": False, "include_numbers": True, "font_size": 18},
        ).move_to([-2.4, -1.6, 0])

        def safe_ratio(x: float) -> float:
            if abs(x) < 1e-6:
                return 1.0
            return np.sin(x) / x

        ratio_curve = axes_bot.plot(safe_ratio, x_range=[-1.55, 1.55, 0.01],
                                    color=YELLOW)
        ratio_lbl = MathTex(r"\frac{\sin x}{x}", color=YELLOW, font_size=22).next_to(
            axes_bot.c2p(1.5, safe_ratio(1.5)), UR, buff=0.1)
        self.play(Create(axes_bot), Create(ratio_curve), Write(ratio_lbl))

        x_tracker = ValueTracker(1.5)

        def top_dot_f():
            x = x_tracker.get_value()
            return Dot(axes_top.c2p(x, np.sin(x)), color=BLUE, radius=0.09)

        def top_dot_g():
            x = x_tracker.get_value()
            return Dot(axes_top.c2p(x, x), color=GREEN, radius=0.09)

        def bot_dot():
            x = x_tracker.get_value()
            return Dot(axes_bot.c2p(x, safe_ratio(x)), color=YELLOW, radius=0.09)

        self.add(always_redraw(top_dot_f), always_redraw(top_dot_g),
                 always_redraw(bot_dot))

        # RIGHT COLUMN
        rcol_x = +4.4

        def info_panel():
            x = x_tracker.get_value()
            f, g = np.sin(x), x
            ratio = safe_ratio(x)
            fp, gp = np.cos(x), 1.0
            return VGroup(
                MathTex(rf"x = {x:+.4f}", color=WHITE, font_size=24),
                MathTex(rf"f(x) = {f:+.4f}", color=BLUE, font_size=22),
                MathTex(rf"g(x) = {g:+.4f}", color=GREEN, font_size=22),
                MathTex(rf"\tfrac{{f}}{{g}} = {ratio:.4f}", color=YELLOW, font_size=24),
                MathTex(rf"f'(x) = {fp:.4f}", color=BLUE, font_size=22),
                MathTex(rf"g'(x) = {gp:.4f}", color=GREEN, font_size=22),
                MathTex(rf"\tfrac{{f'}}{{g'}} = {fp / gp:.4f}",
                        color=ORANGE, font_size=24),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([rcol_x, +0.4, 0])

        self.add(always_redraw(info_panel))

        # Sweep x toward 0
        self.play(x_tracker.animate.set_value(0.001),
                  run_time=6, rate_func=smooth)
        self.wait(0.5)

        conclusion = MathTex(
            r"\lim_{x\to 0}\frac{\sin x}{x} = \lim_{x\to 0}\frac{\cos x}{1} = 1",
            font_size=28, color=YELLOW,
        ).move_to([rcol_x, -3.0, 0])
        self.play(Write(conclusion))
        self.wait(1.0)
