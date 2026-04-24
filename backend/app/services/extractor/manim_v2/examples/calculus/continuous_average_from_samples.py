from manim import *
import numpy as np


class ContinuousAverageFromSamplesExample(Scene):
    """
    The continuous average of f on [a, b] is the limit of finite
    samples' averages: (1/N) Σ f(x_i) → (1/(b-a)) ∫ f dx.
    Example: sin(x) on [0, π]; exact avg = 2/π ≈ 0.6366.
    """

    def construct(self):
        title = Tex(r"Continuous average: $\frac{1}{b-a}\int_a^b f$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[0, PI, PI / 4], y_range=[0, 1.1, 0.5],
                    x_length=9, y_length=4.5,
                    axis_config={"include_numbers": True, "font_size": 14}
                    ).shift(DOWN * 0.3)
        self.play(Create(axes))

        sin_curve = axes.plot(np.sin, x_range=[0, PI], color=BLUE, stroke_width=3)
        self.add(sin_curve)

        n_tr = ValueTracker(5.0)

        def n_now():
            return max(3, min(50, int(round(n_tr.get_value()))))

        def sample_dots():
            n = n_now()
            grp = VGroup()
            for i in range(n):
                x = PI * (i + 0.5) / n
                grp.add(Dot(axes.c2p(x, np.sin(x)), color=YELLOW, radius=0.07))
            return grp

        def avg_line():
            n = n_now()
            xs = [PI * (i + 0.5) / n for i in range(n)]
            avg = np.mean([np.sin(x) for x in xs])
            return DashedLine(axes.c2p(0, avg), axes.c2p(PI, avg),
                               color=GREEN, stroke_width=3)

        self.add(always_redraw(sample_dots), always_redraw(avg_line))

        # Exact avg = 2/π
        exact = 2 / PI
        ref_line = DashedLine(axes.c2p(0, exact), axes.c2p(PI, exact),
                               color=RED, stroke_width=2, stroke_opacity=0.5)
        self.add(ref_line)
        self.add(Tex(rf"$2/\pi\approx {exact:.4f}$", color=RED,
                     font_size=20).next_to(axes.c2p(PI, exact), RIGHT, buff=0.1))

        def avg_val():
            n = n_now()
            xs = [PI * (i + 0.5) / n for i in range(n)]
            return float(np.mean([np.sin(x) for x in xs]))

        info = VGroup(
            VGroup(Tex(r"$N=$", font_size=22),
                   DecimalNumber(5, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"avg $=\frac{1}{N}\sum f(x_i)=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=4,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"$\to \frac{1}{\pi}\int_0^\pi\sin x\,dx=\frac{2}{\pi}$",
                color=RED, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(n_now()))
        info[1][1].add_updater(lambda m: m.set_value(avg_val()))
        self.add(info)

        for N in [10, 20, 40, 50]:
            self.play(n_tr.animate.set_value(float(N)), run_time=1.5, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.5)
