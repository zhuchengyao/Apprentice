from manim import *
import numpy as np


class MnistPixelGridToInputLayer(Scene):
    """A simplified 14x14 MNIST-style digit-3 silhouette.  Each pixel value in
    [0, 1] becomes an activation in a column of 196 input-layer circles.
    Visualize the pixel->neuron correspondence by flashing TransformFromCopy
    arrows sending 9 representative pixels to their neurons."""

    def construct(self):
        title = Tex(
            r"Pixel grid $\to$ input layer activations",
            font_size=30,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        n = 14
        img = np.zeros((n, n))
        for j in range(3, 11):
            img[3, j] = 1.0
            img[6, j] = 1.0
            img[9, j] = 1.0
        for i in range(3, 7):
            img[i, 10] = 1.0
        for i in range(6, 10):
            img[i, 10] = 1.0

        cell = 0.25
        grid = VGroup()
        for i in range(n):
            for j in range(n):
                sq = Square(
                    side_length=cell,
                    stroke_width=0.5,
                    stroke_color=GREY,
                    fill_opacity=float(img[i, j]),
                    fill_color=WHITE,
                )
                sq.move_to([j * cell - n * cell / 2 + cell / 2,
                            -i * cell + n * cell / 2 - cell / 2, 0])
                grid.add(sq)
        grid.shift(LEFT * 3.3 + DOWN * 0.2)
        self.play(Create(grid, run_time=1.2))

        input_col = VGroup()
        for k in range(14):
            c = Circle(radius=0.12, color=BLUE,
                       stroke_width=2, fill_opacity=0.0)
            c.move_to([3.2, 3 - k * 0.45, 0])
            input_col.add(c)

        dots_above = MathTex(r"\vdots", font_size=28).next_to(
            input_col, UP, buff=0.1
        )
        dots_below = MathTex(r"\vdots", font_size=28).next_to(
            input_col, DOWN, buff=0.1
        )
        col_caption = Tex(
            r"$\mathbf{a}^{(0)} \in \mathbb{R}^{196}$",
            font_size=26, color=YELLOW,
        ).next_to(input_col, DOWN, buff=0.7)
        self.play(
            LaggedStart(*[FadeIn(c) for c in input_col],
                        lag_ratio=0.04, run_time=1.2),
            FadeIn(dots_above), FadeIn(dots_below),
            Write(col_caption),
        )

        sample_coords = [
            (3, 5), (3, 9), (6, 6), (6, 10),
            (9, 4), (9, 8), (5, 10), (7, 10), (8, 10),
        ]
        flashes = []
        for idx, (i, j) in enumerate(sample_coords):
            k = idx + 2
            src = grid[i * n + j].get_center()
            dst = input_col[k].get_center()
            arrow = Arrow(src, dst, buff=0.05,
                          color=YELLOW, stroke_width=2,
                          max_tip_length_to_length_ratio=0.08)
            val = float(img[i, j])
            flashes.append((arrow, k, val))

        for arrow, k, val in flashes:
            self.play(
                GrowArrow(arrow),
                input_col[k].animate.set_fill(WHITE, opacity=val),
                run_time=0.3,
            )

        note = Tex(
            r"each pixel intensity in $[0,1]$ becomes one activation",
            font_size=24, color=YELLOW,
        ).to_edge(DOWN, buff=0.25)
        self.play(FadeIn(note))
        self.wait(1.5)
