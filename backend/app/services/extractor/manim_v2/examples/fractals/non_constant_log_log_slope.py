from manim import *
import numpy as np


class NonConstantLogLogSlope(Scene):
    """For a non-self-similar object (e.g. a coastline at finite resolution),
    the log-log box-counting plot curves instead of forming a straight line.
    The local slope — the effective fractal dimension — differs across scales.
    Draw tangent lines at three zoom ranges to show the slopes changing."""

    def construct(self):
        title = Tex(
            r"Real-world data: different slopes at different scales",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(
            x_range=[0, 15, 2],
            y_range=[0, 8, 1],
            x_length=9.5,
            y_length=5.2,
            tips=False,
            axis_config={"stroke_width": 2, "include_ticks": True},
        ).shift(DOWN * 0.2)
        x_lab = MathTex(r"\log(1/\varepsilon)", font_size=30).next_to(
            axes.x_axis.get_end(), DOWN, buff=0.15
        )
        y_lab = MathTex(r"\log N(\varepsilon)", font_size=30).next_to(
            axes.y_axis.get_end(), LEFT, buff=0.2
        )
        self.play(Create(axes), FadeIn(x_lab), FadeIn(y_lab))

        def f(x):
            return 0.01 * (x - 5) ** 3 + 0.3 * x + 3

        graph = axes.plot(f, x_range=[0.5, 14.0], color=BLUE, stroke_width=3)

        rng = np.random.default_rng(1)
        xs = np.linspace(0.7, 13.8, 22)
        points = VGroup(*[
            Dot(axes.c2p(x, f(x) + rng.uniform(-0.25, 0.25)),
                radius=0.06, color=YELLOW)
            for x in xs
        ])
        self.play(LaggedStart(*[FadeIn(d) for d in points],
                              lag_ratio=0.06, run_time=2))
        self.play(Create(graph), run_time=1.5)

        def local_slope_line(x0, half_width=1.6, color=GREEN):
            h = 1e-2
            slope = (f(x0 + h) - f(x0 - h)) / (2 * h)
            y0 = f(x0)
            x_left = x0 - half_width
            x_right = x0 + half_width
            return Line(
                axes.c2p(x_left, y0 - slope * half_width),
                axes.c2p(x_right, y0 + slope * half_width),
                color=color, stroke_width=4,
            ), slope

        tangent_spots = [2.0, 7.5, 12.5]
        slope_colors = [GREEN, ORANGE, RED]
        tangent_labels = []
        for x0, color in zip(tangent_spots, slope_colors):
            line, slope = local_slope_line(x0, 1.6, color)
            dot = Dot(axes.c2p(x0, f(x0)), radius=0.08, color=color)
            lab = MathTex(
                rf"d\approx {slope:.2f}", font_size=26, color=color,
            )
            lab.move_to(
                axes.c2p(x0, f(x0) - 1.0) if x0 < 10 else
                axes.c2p(x0 - 1.6, f(x0) - 1.2)
            )
            self.play(FadeIn(dot), Create(line), FadeIn(lab), run_time=1.0)
            tangent_labels.append(lab)

        note = Tex(
            r"A single ``fractal dimension'' only exists\\ when the log-log slope is constant.",
            font_size=26, color=YELLOW,
        )
        note.to_corner(DR, buff=0.4)
        self.play(FadeIn(note))
        self.wait(1.5)
