from manim import *
import numpy as np


class ActivationFunctionsExample(Scene):
    """
    Three common activations on shared axes, with synchronized cursors
    showing the value AND the derivative at the current input x.

    THREE_ROW (sort of):
      TOP    — sigmoid σ(x), ReLU max(0,x), tanh(x) plotted on shared axes.
      BOTTOM — corresponding derivatives σ'(x), step(x), 1-tanh²(x).

    Single ValueTracker x sweeps -4 → +4. Vertical dashed cursor crosses
    both panels; always_redraw dots track each curve.
    """

    def construct(self):
        title = Tex(r"Activation functions and their derivatives",
                    font_size=28).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # Top axes: f(x)
        ax_top = Axes(
            x_range=[-4, 4, 1], y_range=[-1.2, 1.2, 0.5],
            x_length=10, y_length=2.6,
            axis_config={"include_tip": True, "include_numbers": True, "font_size": 16},
        ).shift(UP * 1.4)
        # Bottom axes: f'(x)
        ax_bot = Axes(
            x_range=[-4, 4, 1], y_range=[-0.05, 1.2, 0.5],
            x_length=10, y_length=2.0,
            axis_config={"include_tip": True, "include_numbers": True, "font_size": 16},
        ).shift(DOWN * 1.6)
        self.play(Create(ax_top), Create(ax_bot))

        # Functions and their derivatives
        sigmoid = lambda x: 1 / (1 + np.exp(-x))
        sigmoid_d = lambda x: sigmoid(x) * (1 - sigmoid(x))
        relu = lambda x: max(0, x)
        relu_d = lambda x: 1.0 if x > 0 else 0.0
        tanh = lambda x: np.tanh(x)
        tanh_d = lambda x: 1 - np.tanh(x) ** 2

        # Top curves
        sig_curve = ax_top.plot(sigmoid, x_range=[-4, 4, 0.05], color=BLUE)
        relu_curve = ax_top.plot(relu, x_range=[-4, 4, 0.05], color=GREEN)
        tanh_curve = ax_top.plot(tanh, x_range=[-4, 4, 0.05], color=ORANGE)
        # Top labels
        sig_lbl = MathTex(r"\sigma", color=BLUE, font_size=22).next_to(
            ax_top.c2p(3.7, sigmoid(3.7)), RIGHT, buff=0.1)
        relu_lbl = MathTex(r"\mathrm{ReLU}", color=GREEN, font_size=22).next_to(
            ax_top.c2p(2.5, relu(2.5)), UR, buff=0.1)
        tanh_lbl = MathTex(r"\tanh", color=ORANGE, font_size=22).next_to(
            ax_top.c2p(3.7, tanh(3.7)), RIGHT, buff=0.1)
        self.play(Create(sig_curve), Create(relu_curve), Create(tanh_curve),
                  Write(sig_lbl), Write(relu_lbl), Write(tanh_lbl))

        # Bottom curves
        sig_d_curve = ax_bot.plot(sigmoid_d, x_range=[-4, 4, 0.05], color=BLUE)
        relu_d_curve = ax_bot.plot(relu_d, x_range=[-4, 4, 0.05], color=GREEN)
        tanh_d_curve = ax_bot.plot(tanh_d, x_range=[-4, 4, 0.05], color=ORANGE)
        sig_d_lbl = MathTex(r"\sigma'", color=BLUE, font_size=22).move_to(
            ax_bot.c2p(2.5, 0.4))
        relu_d_lbl = MathTex(r"\text{step}", color=GREEN, font_size=20).move_to(
            ax_bot.c2p(-2.5, 0.4))
        tanh_d_lbl = MathTex(r"1 - \tanh^2", color=ORANGE, font_size=20).move_to(
            ax_bot.c2p(0, 1.05))
        self.play(Create(sig_d_curve), Create(relu_d_curve), Create(tanh_d_curve),
                  Write(sig_d_lbl), Write(relu_d_lbl), Write(tanh_d_lbl))

        # Cursor + dots driven by x-tracker
        x_tr = ValueTracker(-4 + 0.1)

        def cursor():
            x = x_tr.get_value()
            top_y = ax_top.c2p(x, 1.2)[1]
            bot_y = ax_bot.c2p(x, -0.05)[1]
            screen_x = ax_top.c2p(x, 0)[0]
            return DashedLine([screen_x, top_y, 0], [screen_x, bot_y, 0],
                              color=YELLOW, stroke_width=2)

        def dot_for(ax, fn, col):
            def make():
                x = x_tr.get_value()
                return Dot(ax.c2p(x, fn(x)), color=col, radius=0.07)
            return make

        self.add(always_redraw(cursor),
                 always_redraw(dot_for(ax_top, sigmoid, BLUE)),
                 always_redraw(dot_for(ax_top, relu, GREEN)),
                 always_redraw(dot_for(ax_top, tanh, ORANGE)),
                 always_redraw(dot_for(ax_bot, sigmoid_d, BLUE)),
                 always_redraw(dot_for(ax_bot, relu_d, GREEN)),
                 always_redraw(dot_for(ax_bot, tanh_d, ORANGE)))

        self.play(x_tr.animate.set_value(4 - 0.1),
                  run_time=8, rate_func=linear)
        self.wait(0.6)
