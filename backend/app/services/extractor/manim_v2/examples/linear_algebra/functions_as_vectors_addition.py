from manim import *
import numpy as np


class FunctionsAsVectorsAdditionExample(Scene):
    """
    Functions are vectors: addition is pointwise. (f + g)(x) = f(x) + g(x).
    Shown with f = sin(x) and g = 0.5 * cos(2x).
    """

    def construct(self):
        title = Tex(r"Functions as vectors: $(f+g)(x)=f(x)+g(x)$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[-PI, PI, PI / 2], y_range=[-2, 2, 1],
                    x_length=9, y_length=4.5,
                    axis_config={"include_numbers": False}).shift(DOWN * 0.3)
        self.play(Create(axes))

        f = axes.plot(lambda x: np.sin(x), x_range=[-PI, PI],
                       color=BLUE, stroke_width=3)
        g = axes.plot(lambda x: 0.5 * np.cos(2 * x), x_range=[-PI, PI],
                       color=ORANGE, stroke_width=3)
        f_plus_g = axes.plot(lambda x: np.sin(x) + 0.5 * np.cos(2 * x),
                                x_range=[-PI, PI], color=GREEN, stroke_width=4)

        self.play(Create(f))
        self.add(Tex(r"$f=\sin x$", color=BLUE, font_size=22).next_to(axes, UP, buff=0.1).shift(LEFT * 2.5))
        self.wait(0.3)
        self.play(Create(g))
        self.add(Tex(r"$g=\tfrac12\cos 2x$", color=ORANGE, font_size=22).next_to(axes, UP, buff=0.1))
        self.wait(0.3)
        self.play(Create(f_plus_g))
        self.add(Tex(r"$f+g$", color=GREEN, font_size=22).next_to(axes, UP, buff=0.1).shift(RIGHT * 2.5))
        self.wait(0.4)

        # Pointwise illustration: a probe at a specific x
        x_tr = ValueTracker(-PI + 0.2)

        def probe_group():
            x = x_tr.get_value()
            f_val = float(np.sin(x))
            g_val = float(0.5 * np.cos(2 * x))
            s = f_val + g_val
            grp = VGroup(
                Dot(axes.c2p(x, f_val), color=BLUE, radius=0.1),
                Dot(axes.c2p(x, g_val), color=ORANGE, radius=0.1),
                Dot(axes.c2p(x, s), color=GREEN, radius=0.1),
                DashedLine(axes.c2p(x, -2), axes.c2p(x, 2),
                            color=GREY_B, stroke_width=1),
            )
            return grp

        self.add(always_redraw(probe_group))

        self.play(x_tr.animate.set_value(PI - 0.2), run_time=5, rate_func=linear)
        self.wait(0.5)

        self.play(Write(
            Tex(r"pointwise addition just like coordinate-wise!",
                 color=YELLOW, font_size=24).to_edge(DOWN, buff=0.5)
        ))
        self.wait(1.0)
