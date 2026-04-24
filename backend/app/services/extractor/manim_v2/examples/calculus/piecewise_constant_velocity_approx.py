from manim import *
import numpy as np


class PiecewiseConstantVelocityApproxExample(Scene):
    """
    Approximate a smooth v(t) by N piecewise-constant pieces.
    As N → ∞, rectangle sum → ∫ v dt (exact distance).
    """

    def construct(self):
        title = Tex(r"Smooth $v(t)$ $\approx$ piecewise-constant, $\to$ integral",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[0, 8, 1], y_range=[0, 5, 1],
                    x_length=8.5, y_length=4.2,
                    axis_config={"include_numbers": True, "font_size": 16}
                    ).shift(DOWN * 0.2)
        self.play(Create(axes))

        def v(t):
            return t * (8 - t) / 4

        self.add(axes.plot(v, x_range=[0, 8], color=BLUE, stroke_width=2, stroke_opacity=0.6))

        n_tr = ValueTracker(4.0)

        def n_now():
            return max(2, min(50, int(round(n_tr.get_value()))))

        def rectangles():
            n = n_now()
            grp = VGroup()
            dx = 8 / n
            for i in range(n):
                x_mid = (i + 0.5) * dx
                rect = Rectangle(width=dx * axes.x_length / 8,
                                  height=v(x_mid) * axes.y_length / 5,
                                  color=GREEN, stroke_width=1,
                                  fill_color=GREEN, fill_opacity=0.5)
                rect.move_to(axes.c2p(x_mid, v(x_mid) / 2))
                grp.add(rect)
            return grp

        self.add(always_redraw(rectangles))

        def approx_sum():
            n = n_now()
            dx = 8 / n
            return sum(v((i + 0.5) * dx) * dx for i in range(n))

        # Exact: ∫_0^8 t(8-t)/4 dt = 1/4 · [4t² - t³/3] from 0 to 8 = 1/4 · (256 - 512/3) = 1/4 · 256/3 = 64/3 ≈ 21.33
        exact = 64 / 3

        info = VGroup(
            VGroup(Tex(r"$N=$", font_size=22),
                   DecimalNumber(4, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"sum $=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"exact $=\int_0^8 v\,dt=$", font_size=22),
                   DecimalNumber(exact, num_decimal_places=3,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"error $=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=4,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(n_now()))
        info[1][1].add_updater(lambda m: m.set_value(approx_sum()))
        info[3][1].add_updater(lambda m: m.set_value(abs(approx_sum() - exact)))
        self.add(info)

        for N in [8, 16, 32, 50]:
            self.play(n_tr.animate.set_value(float(N)), run_time=1.5, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.5)
