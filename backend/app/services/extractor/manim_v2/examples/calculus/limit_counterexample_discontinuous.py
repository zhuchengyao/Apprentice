from manim import *
import numpy as np


class LimitCounterexampleDiscontinuousExample(Scene):
    """
    A function f(x) that jumps at x=a has no limit at a: left and
    right limits differ. Example: f(x) = 1 for x < 2, f(x) = 3 for x ≥ 2.
    """

    def construct(self):
        title = Tex(r"Limit does not exist: left $\ne$ right",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[0, 4, 1], y_range=[-0.5, 4, 1],
                    x_length=9, y_length=4.5,
                    axis_config={"include_numbers": True, "font_size": 16}
                    ).shift(DOWN * 0.3)
        self.play(Create(axes))

        # Left part
        left_curve = Line(axes.c2p(0, 1), axes.c2p(2, 1),
                           color=BLUE, stroke_width=4)
        right_curve = Line(axes.c2p(2, 3), axes.c2p(4, 3),
                            color=GREEN, stroke_width=4)
        self.add(left_curve, right_curve)

        # Open/closed dots at jump
        self.add(Dot(axes.c2p(2, 1), color=BLUE, radius=0.1,
                      stroke_width=2, fill_opacity=0))
        self.add(Dot(axes.c2p(2, 3), color=GREEN, radius=0.1))

        # Approach dot
        x_tr = ValueTracker(0.3)

        def approach_dot():
            x = x_tr.get_value()
            y = 1 if x < 2 else 3
            col = BLUE if x < 2 else GREEN
            return Dot(axes.c2p(x, y), color=col, radius=0.12)

        self.add(always_redraw(approach_dot))

        info = VGroup(
            VGroup(Tex(r"$x=$", font_size=22),
                   DecimalNumber(0.3, num_decimal_places=3,
                                 font_size=22)).arrange(RIGHT, buff=0.1),
            Tex(r"$\lim_{x\to 2^-} f(x)=1$", color=BLUE, font_size=22),
            Tex(r"$\lim_{x\to 2^+} f(x)=3$", color=GREEN, font_size=22),
            Tex(r"$\lim_{x\to 2} f(x)$ does not exist",
                color=RED, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(x_tr.get_value()))
        self.add(info)

        # Approach 2 from left, then from right
        self.play(x_tr.animate.set_value(1.95), run_time=2.5, rate_func=smooth)
        self.wait(0.4)
        self.play(x_tr.animate.set_value(2.05), run_time=0.6)
        self.wait(0.4)
        self.play(x_tr.animate.set_value(3.7), run_time=2.5, rate_func=smooth)
        self.wait(0.8)
