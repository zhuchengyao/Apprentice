from manim import *
import numpy as np


class SlowingWavesExample(Scene):
    """
    Wave slowing at a medium interface (from _2023/optics_puzzles/
    slowing_waves): a sinusoidal wave crosses from fast medium
    (v_1 = 1) to slow medium (v_2 = 0.5); wavelength compresses by
    a factor of v_2/v_1, frequency is preserved.

    SINGLE_FOCUS:
      Axes with a traveling wave y(x, t) whose wavenumber changes
      abruptly at x = 0; ValueTracker t_tr advances time; always_redraw
      wave + medium shading + frequency vs wavelength panel.
    """

    def construct(self):
        title = Tex(r"Slowing waves: $v = f\lambda$, $f$ preserved, $\lambda$ shrinks",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ax = Axes(x_range=[-5, 5, 1], y_range=[-1.5, 1.5, 0.5],
                   x_length=11, y_length=4, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([0, -0.3, 0])
        self.play(Create(ax))

        # Shade two media
        left_shade = Rectangle(width=5.5 * 2, height=4.2,
                                  color=BLUE, fill_opacity=0.08,
                                  stroke_width=0)
        left_shade.move_to(ax.c2p(-2.5, 0))
        right_shade = Rectangle(width=5.5 * 2, height=4.2,
                                  color=BLUE_D, fill_opacity=0.2,
                                  stroke_width=0)
        right_shade.move_to(ax.c2p(2.5, 0))
        # Actually we want shade widths to match: the plane is 10 wide over 11 scene units
        # Simpler: fill by two rectangles of x-range [-5, 0] and [0, 5]
        left_rect = Rectangle(width=(ax.c2p(0, 0)[0] - ax.c2p(-5, 0)[0]),
                                height=4.2, color=BLUE,
                                fill_opacity=0.08, stroke_width=0
                                ).move_to([(ax.c2p(-5, 0)[0] + ax.c2p(0, 0)[0]) / 2,
                                             ax.c2p(0, 0)[1], 0])
        right_rect = Rectangle(width=(ax.c2p(5, 0)[0] - ax.c2p(0, 0)[0]),
                                 height=4.2, color=BLUE_D,
                                 fill_opacity=0.22, stroke_width=0
                                 ).move_to([(ax.c2p(0, 0)[0] + ax.c2p(5, 0)[0]) / 2,
                                              ax.c2p(0, 0)[1], 0])
        self.add(left_rect, right_rect)
        self.play(FadeIn(left_rect), FadeIn(right_rect))

        # Labels
        n1_lbl = Tex(r"$n_1 = 1$, $\lambda_1 = 2$",
                      color=BLUE, font_size=22).move_to([-3.0, 2.5, 0])
        n2_lbl = Tex(r"$n_2 = 2$, $\lambda_2 = 1$",
                      color=BLUE_D, font_size=22).move_to([3.0, 2.5, 0])
        self.play(Write(n1_lbl), Write(n2_lbl))

        # Traveling wave: y(x, t) = cos(k(x) x - ω t)
        # In left medium: k1 = 2π/2 = π, ω = π. So phase = k1 x - ω t
        # In right medium: k2 = 2π/1 = 2π, but to keep phase continuous
        #   at x=0: phase = -ω t on the left; on the right, phase = k2·x - ω t
        # So for right side: y = cos(k2 x - ω t).
        omega = PI

        t_tr = ValueTracker(0.0)

        def wave():
            t = t_tr.get_value()

            def y(x):
                if x < 0:
                    return np.cos(PI * x - omega * t)
                else:
                    return np.cos(2 * PI * x - omega * t)

            return ax.plot(y, x_range=[-5, 5, 0.02],
                            color=YELLOW, stroke_width=3)

        self.add(always_redraw(wave))

        # Interface indicator
        inter = DashedLine(ax.c2p(0, -1.5), ax.c2p(0, 1.5),
                             color=RED, stroke_width=2)
        self.play(Create(inter))

        def info():
            t = t_tr.get_value()
            return VGroup(
                MathTex(rf"t = {t:.2f}", color=WHITE, font_size=22),
                MathTex(rf"f = \omega/(2\pi) = 0.5",
                         color=GREEN, font_size=20),
                MathTex(rf"v_1 = 1, v_2 = 0.5",
                         color=YELLOW, font_size=20),
                MathTex(r"\lambda_2 / \lambda_1 = v_2 / v_1 = 1/2",
                         color=RED, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        self.play(t_tr.animate.set_value(8),
                   run_time=8, rate_func=linear)
        self.wait(0.4)
