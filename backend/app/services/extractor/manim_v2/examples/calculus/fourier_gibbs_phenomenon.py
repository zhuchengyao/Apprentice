from manim import *
import numpy as np


class FourierGibbsPhenomenonExample(Scene):
    """
    Gibbs phenomenon: Fourier series of a square wave overshoots the
    discontinuity by ≈ 8.95%, independent of N (number of terms).

    Square wave with period 2π: f(x) = 1 if 0 < x < π, else -1.
    Partial sums S_N(x) = (4/π) Σ_{k=1, 3, 5, ...} sin(kx)/k.

    TWO_COLUMN: LEFT axes with f and S_N; ValueTracker N_tr sweeps;
    RIGHT shows the Gibbs overshoot % approaching 8.95%.
    """

    def construct(self):
        title = Tex(r"Gibbs phenomenon: overshoot $\to 8.95\%$ regardless of $N$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[-PI, PI, PI / 2], y_range=[-1.5, 1.5, 0.5],
                    x_length=7.0, y_length=4.0,
                    axis_config={"include_numbers": False}).shift(LEFT * 2.0 + DOWN * 0.2)
        self.play(Create(axes))

        # True square wave
        left_seg = Line(axes.c2p(-PI, -1), axes.c2p(0, -1),
                         color=BLUE, stroke_width=3)
        right_seg = Line(axes.c2p(0, 1), axes.c2p(PI, 1),
                          color=BLUE, stroke_width=3)
        jump_l = DashedLine(axes.c2p(0, -1), axes.c2p(0, 1),
                             color=BLUE, stroke_width=1.5, stroke_opacity=0.6)
        self.add(left_seg, right_seg, jump_l)

        N_tr = ValueTracker(1.0)

        def N_now():
            return max(1, min(60, int(round(N_tr.get_value()))))

        def S_N(x, N):
            s = 0.0
            for k in range(1, 2 * N, 2):
                s += np.sin(k * x) / k
            return 4 / PI * s

        def partial_curve():
            N = N_now()
            return axes.plot(lambda x: float(S_N(x, N)),
                             x_range=[-PI + 0.01, PI - 0.01],
                             color=YELLOW, stroke_width=3)

        self.add(always_redraw(partial_curve))

        # Overshoot calculation
        def overshoot_pct():
            N = N_now()
            # Max of S_N(x) for x > 0 near 0
            xs = np.linspace(0.001, 1.0, 400)
            vals = [S_N(x, N) for x in xs]
            max_val = max(vals)
            return 100 * (max_val - 1)

        # Reference line at 8.95% overshoot (value = 1.08949)
        self.add(DashedLine(axes.c2p(-PI, 1.08949), axes.c2p(PI, 1.08949),
                             color=ORANGE, stroke_width=1.5, stroke_opacity=0.5))
        self.add(Tex(r"$1.08949$ (limit)", color=ORANGE,
                     font_size=18).next_to(axes.c2p(PI, 1.08949), UR, buff=0.1))

        info = VGroup(
            VGroup(Tex(r"$N=$", font_size=22),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"overshoot $=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22).set_color(ORANGE),
                   Tex(r"\%", font_size=22)).arrange(RIGHT, buff=0.05),
            Tex(r"limit: $8.95\%$",
                color=ORANGE, font_size=22),
            Tex(r"overshoot zone narrows with $N$,",
                color=GREY_B, font_size=18),
            Tex(r"but height stays $\approx$ $8.95\%$.",
                color=GREY_B, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.2)
        info[0][1].add_updater(lambda m: m.set_value(N_now()))
        info[1][1].add_updater(lambda m: m.set_value(overshoot_pct()))
        self.add(info)

        for target in [3, 8, 20, 40, 60]:
            self.play(N_tr.animate.set_value(float(target)),
                      run_time=1.4, rate_func=smooth)
            self.wait(0.3)
        self.wait(0.8)
