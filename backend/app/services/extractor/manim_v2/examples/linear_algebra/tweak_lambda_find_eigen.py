from manim import *
import numpy as np


class TweakLambdaFindEigenExample(Scene):
    """
    Sweep λ and watch det(A - λI) as a function. Zeros of this function
    are eigenvalues. For A = [[3, 1], [0, 2]], det = (3-λ)(2-λ) has
    zeros at λ=3 and λ=2.
    """

    def construct(self):
        title = Tex(r"Tweak $\lambda$: $\det(A-\lambda I)=0$ at eigenvalues",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[0, 5, 1], y_range=[-2, 8, 2],
                    x_length=8, y_length=4.5,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(DOWN * 0.3)
        self.play(Create(axes))

        # det(A - λI) = (3-λ)(2-λ) = λ² - 5λ + 6
        det_curve = axes.plot(lambda l: (3 - l) * (2 - l),
                                x_range=[0, 5], color=BLUE, stroke_width=3)
        self.add(det_curve)
        self.add(Tex(r"$\det(A-\lambda I)=(3-\lambda)(2-\lambda)$",
                     color=BLUE, font_size=22).next_to(axes, UP, buff=0.1))

        # Zero line
        self.add(DashedLine(axes.c2p(0, 0), axes.c2p(5, 0),
                             color=GREY_B, stroke_width=1.5, stroke_opacity=0.5))

        # Mark zeros
        self.add(Dot(axes.c2p(2, 0), color=GREEN, radius=0.12))
        self.add(Dot(axes.c2p(3, 0), color=ORANGE, radius=0.12))
        self.add(Tex(r"$\lambda=2$", color=GREEN, font_size=20).next_to(axes.c2p(2, 0), DOWN, buff=0.2))
        self.add(Tex(r"$\lambda=3$", color=ORANGE, font_size=20).next_to(axes.c2p(3, 0), DOWN, buff=0.2))

        # Probe dot via ValueTracker
        lam_tr = ValueTracker(0.3)

        def probe_dot():
            l = lam_tr.get_value()
            return Dot(axes.c2p(l, (3 - l) * (2 - l)), color=YELLOW, radius=0.11)

        self.add(always_redraw(probe_dot))

        info = VGroup(
            VGroup(Tex(r"$\lambda=$", font_size=22),
                   DecimalNumber(0.3, num_decimal_places=2,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\det(A-\lambda I)=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.5)
        info[0][1].add_updater(lambda m: m.set_value(lam_tr.get_value()))
        info[1][1].add_updater(lambda m: m.set_value(
            (3 - lam_tr.get_value()) * (2 - lam_tr.get_value())))
        self.add(info)

        self.play(lam_tr.animate.set_value(4.5), run_time=5, rate_func=linear)
        self.wait(0.8)
