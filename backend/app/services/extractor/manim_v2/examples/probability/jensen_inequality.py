from manim import *
import numpy as np


class JensenInequalityExample(Scene):
    """
    Jensen's inequality: for convex φ and random variable X,
       φ(E[X]) ≤ E[φ(X)].
    For concave, reverse. Show φ(x) = x² (convex) with 5-point
    discrete distribution.

    TWO_COLUMN: LEFT axes with convex φ(x)=x² + 5 sample points
    (BLUE) + their mean E[X] (GREEN) + chord between φ samples
    (ORANGE) — E[φ(X)] is above φ(E[X]).
    """

    def construct(self):
        title = Tex(r"Jensen: $\varphi$ convex $\Rightarrow \varphi(E[X])\le E[\varphi(X)]$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[-3, 3, 1], y_range=[-0.5, 9, 2],
                    x_length=7, y_length=4.5,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(DOWN * 0.3)
        self.play(Create(axes))

        phi_curve = axes.plot(lambda x: x * x, x_range=[-3, 3],
                               color=BLUE, stroke_width=3)
        phi_lbl = Tex(r"$\varphi(x)=x^2$", color=BLUE, font_size=22).next_to(
            axes.c2p(2.3, 5.3), UR, buff=0.1)
        self.play(Create(phi_curve), Write(phi_lbl))

        # 5-point discrete distribution
        probs_tr = [ValueTracker(0.2) for _ in range(5)]  # each prob
        # Fix probs here (uniform), but points x_i driven by tracker shape
        xs_tr = ValueTracker(0.0)  # controls spread

        def samples():
            # X points: centered around 0.5, spread determined by xs_tr
            spread = xs_tr.get_value()
            return np.array([-1.8, -0.8, 0.2, 1.2, 2.0]) * (1 + 0.5 * np.sin(spread))

        def sample_dots():
            xs = samples()
            grp = VGroup()
            for x in xs:
                grp.add(Dot(axes.c2p(x, 0), color=BLUE, radius=0.1))
                grp.add(Dot(axes.c2p(x, x * x), color=RED, radius=0.08))
            return grp

        def mean_X():
            xs = samples()
            return float(np.mean(xs))

        def mean_phi():
            xs = samples()
            return float(np.mean(xs ** 2))

        def mean_markers():
            mx = mean_X()
            mp = mean_phi()
            grp = VGroup(
                DashedLine(axes.c2p(mx, -0.5), axes.c2p(mx, 9),
                            color=GREEN, stroke_width=2),
                Dot(axes.c2p(mx, 0), color=GREEN, radius=0.13),
                Dot(axes.c2p(mx, mx * mx), color=GREEN, radius=0.13),
                Dot(axes.c2p(mx, mp), color=ORANGE, radius=0.13),
                DashedLine(axes.c2p(-3, mp), axes.c2p(mx, mp),
                            color=ORANGE, stroke_width=1.5),
                DashedLine(axes.c2p(-3, mx * mx), axes.c2p(mx, mx * mx),
                            color=GREEN, stroke_width=1.5),
            )
            return grp

        self.add(always_redraw(sample_dots), always_redraw(mean_markers))

        info = VGroup(
            VGroup(Tex(r"$E[X]=$", color=GREEN, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\varphi(E[X])=(E[X])^2=$", color=GREEN, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$E[\varphi(X)]=E[X^2]=$", color=ORANGE, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"gap $=\mathrm{Var}(X)=$", color=YELLOW, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"gap $\ge 0$ always (Jensen)",
                color=YELLOW, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(mean_X()))
        info[1][1].add_updater(lambda m: m.set_value(mean_X() ** 2))
        info[2][1].add_updater(lambda m: m.set_value(mean_phi()))
        info[3][1].add_updater(lambda m: m.set_value(mean_phi() - mean_X() ** 2))
        self.add(info)

        self.play(xs_tr.animate.set_value(TAU),
                  run_time=8, rate_func=linear)
        self.wait(0.5)
