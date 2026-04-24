from manim import *
import numpy as np


class HigherOrderDerivativesExample(Scene):
    """
    f, f', f'', f''' for f(x) = sin(x), each on its own stacked axes.

    THREE_ROW (extended to 4 rows): one shared x-axis vertically aligned.
    A ValueTracker x sweeps from -2π to 2π; four always_redraw dots
    track f(x), f'(x), f''(x), f'''(x). A vertical dashed cursor
    descends through all four panels at the current x.
    """

    def construct(self):
        title = Tex(r"Derivatives cycle: $\sin \to \cos \to -\sin \to -\cos$",
                    font_size=28).to_edge(UP, buff=0.4)
        self.play(Write(title))

        f0 = lambda x: np.sin(x)
        f1 = lambda x: np.cos(x)
        f2 = lambda x: -np.sin(x)
        f3 = lambda x: -np.cos(x)
        funcs = [(f0, BLUE, "f"),
                 (f1, GREEN, "f'"),
                 (f2, ORANGE, "f''"),
                 (f3, RED, "f'''")]

        ys = [+2.4, +0.8, -0.8, -2.4]
        ax_height = 1.2
        all_axes = []
        all_curves = []
        for (fn, col, lbl), y in zip(funcs, ys):
            ax = Axes(
                x_range=[-2 * PI, 2 * PI, PI], y_range=[-1.4, 1.4, 1],
                x_length=10, y_length=ax_height,
                axis_config={"include_tip": False, "include_numbers": False, "font_size": 14},
            ).move_to([-0.4, y, 0])
            curve = ax.plot(fn, x_range=[-2 * PI, 2 * PI, 0.05], color=col)
            tag = Tex(rf"${lbl}$", color=col, font_size=24).next_to(ax, LEFT, buff=0.1)
            self.play(Create(ax), Create(curve), Write(tag), run_time=0.4)
            all_axes.append(ax)
            all_curves.append((ax, fn, col))

        x_tr = ValueTracker(-2 * PI + 0.1)

        def cursor():
            x = x_tr.get_value()
            top_y = ys[0] + ax_height / 2 + 0.1
            bot_y = ys[-1] - ax_height / 2 - 0.1
            screen_x = all_axes[0].c2p(x, 0)[0]
            return DashedLine([screen_x, top_y, 0],
                              [screen_x, bot_y, 0],
                              color=YELLOW, stroke_width=2)

        def dot_for(ax, fn, col):
            def make():
                x = x_tr.get_value()
                return Dot(ax.c2p(x, fn(x)), color=col, radius=0.08)
            return make

        self.add(always_redraw(cursor))
        for ax, fn, col in all_curves:
            self.add(always_redraw(dot_for(ax, fn, col)))

        rcol_x = +5.2

        def info_panel():
            x = x_tr.get_value()
            return VGroup(
                MathTex(rf"x = {x:+.2f}", color=WHITE, font_size=24),
                MathTex(rf"f = {f0(x):+.3f}", color=BLUE, font_size=22),
                MathTex(rf"f' = {f1(x):+.3f}", color=GREEN, font_size=22),
                MathTex(rf"f'' = {f2(x):+.3f}", color=ORANGE, font_size=22),
                MathTex(rf"f''' = {f3(x):+.3f}", color=RED, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([rcol_x, +0.6, 0])

        self.add(always_redraw(info_panel))

        self.play(x_tr.animate.set_value(2 * PI - 0.1),
                  run_time=8, rate_func=linear)
        self.wait(0.5)

        cycle = MathTex(r"f^{(n+4)} = f^{(n)}",
                        color=YELLOW, font_size=28).move_to([rcol_x, -2.5, 0])
        self.play(Write(cycle))
        self.wait(1.0)
