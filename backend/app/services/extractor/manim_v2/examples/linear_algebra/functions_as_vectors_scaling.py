from manim import *
import numpy as np


class FunctionsAsVectorsScalingExample(Scene):
    """
    Scalar multiplication of a function: (c·f)(x) = c · f(x).
    ValueTracker c_tr sweeps c across -1, 0, 2, 1 with always_redraw.
    """

    def construct(self):
        title = Tex(r"Scalar times function: $(c\cdot f)(x)=c\cdot f(x)$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[-PI, PI, PI / 2], y_range=[-3, 3, 1],
                    x_length=9, y_length=4.5,
                    axis_config={"include_numbers": False}).shift(DOWN * 0.3)
        self.play(Create(axes))

        # f = sin x fixed as dashed reference
        f_ref = axes.plot(lambda x: np.sin(x), x_range=[-PI, PI],
                           color=BLUE, stroke_width=2, stroke_opacity=0.5)
        self.add(f_ref)
        self.add(Tex(r"$f=\sin x$", color=BLUE, font_size=22).next_to(axes, UP, buff=0.1).shift(LEFT * 3))

        c_tr = ValueTracker(1.0)

        def cf_curve():
            c = c_tr.get_value()
            return axes.plot(lambda x: c * np.sin(x), x_range=[-PI, PI],
                             color=YELLOW, stroke_width=4)

        self.add(always_redraw(cf_curve))

        info = VGroup(
            VGroup(Tex(r"$c=$", font_size=28),
                   DecimalNumber(1.0, num_decimal_places=2,
                                 font_size=28).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"$c\cdot f$ curve (YELLOW)",
                color=YELLOW, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(c_tr.get_value()))
        self.add(info)

        for cval in [2.0, -1.0, 0.0, 1.5]:
            self.play(c_tr.animate.set_value(cval), run_time=1.8, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.5)
