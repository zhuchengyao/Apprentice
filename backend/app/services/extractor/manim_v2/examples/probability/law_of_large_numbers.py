from manim import *
import numpy as np


class LawOfLargeNumbersExample(Scene):
    def construct(self):
        title = Text("Running mean of coin flips converges to 0.5", font_size=26).to_edge(UP)
        self.play(Write(title))

        axes = Axes(
            x_range=[0, 2000, 500], y_range=[0, 1, 0.25],
            x_length=9, y_length=3.8,
            axis_config={"include_tip": True, "include_numbers": True,
                         "decimal_number_config": {"num_decimal_places": 0}},
        ).shift(0.3 * DOWN)
        xlbl = Text("number of flips n", font_size=20).next_to(axes, DOWN, buff=0.1)
        ylbl = Text("running mean", font_size=20).next_to(axes, LEFT, buff=0.1).rotate(PI / 2)
        self.play(Create(axes), Write(xlbl), Write(ylbl))

        # Target line at 0.5
        target = DashedLine(axes.c2p(0, 0.5), axes.c2p(2000, 0.5),
                            color=YELLOW, stroke_width=2)
        target_lbl = MathTex("0.5", color=YELLOW, font_size=22).next_to(axes.c2p(2000, 0.5), RIGHT, buff=0.1)
        self.play(Create(target), Write(target_lbl))

        np.random.seed(42)
        flips = np.random.randint(0, 2, size=2000)
        running = np.cumsum(flips) / (np.arange(2000) + 1)

        # Plot a sparse subset for performance
        sampled_n = list(range(1, 2000, 10))
        points = [axes.c2p(n, running[n - 1]) for n in sampled_n]

        path = VMobject(color=BLUE, stroke_width=2)
        path.set_points_smoothly(points)

        readout = always_redraw(lambda: MathTex(
            rf"n = 2000,\; \bar{{X}}_n \approx {running[-1]:.3f}",
            font_size=26, color=BLUE,
        ).to_corner(UR).shift(LEFT * 0.4 + DOWN * 0.4))

        self.play(Create(path), run_time=3)
        self.play(FadeIn(readout))

        llnformula = MathTex(
            r"\bar{X}_n = \tfrac{1}{n}\sum_{i=1}^n X_i \xrightarrow{n\to\infty} \mathbb{E}[X]",
            font_size=28, color=YELLOW,
        ).to_edge(DOWN)
        self.play(Write(llnformula))
        self.wait(0.6)
