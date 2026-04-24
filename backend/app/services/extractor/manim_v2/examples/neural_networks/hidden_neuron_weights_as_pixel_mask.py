from manim import *
import numpy as np


class HiddenNeuronWeightsAsPixelMask(Scene):
    """A single hidden neuron's 14x14 weights rendered as a 'pixel mask':
    positive weights GREEN, negative weights RED, opacity = |w| / max|w|.
    Visually overlay it on an input digit, element-wise multiply, sum to get
    the pre-activation z, then pass through sigmoid to get activation a."""

    def construct(self):
        title = Tex(
            r"A hidden neuron's weights as a pixel mask",
            font_size=30,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        n = 14
        rng = np.random.default_rng(2)
        cx, cy = 6, 6
        W = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                r = np.sqrt((i - cy) ** 2 + (j - cx) ** 2)
                W[i, j] = np.exp(-(r - 3.0) ** 2 / 2.0) - 0.4
        W += rng.normal(0, 0.05, size=(n, n))
        W_max = np.max(np.abs(W))

        img = np.zeros((n, n))
        for a in range(-3, 4):
            for b in range(-3, 4):
                if 2.5 <= np.sqrt(a * a + b * b) <= 3.5:
                    img[cy + a, cx + b] = 1.0

        cell = 0.22

        def build_grid(arr, fn_color, fn_opacity, center):
            grp = VGroup()
            for i in range(n):
                for j in range(n):
                    c = fn_color(arr[i, j])
                    o = fn_opacity(arr[i, j])
                    sq = Square(
                        side_length=cell, stroke_width=0.3,
                        stroke_color=GREY_D,
                        fill_opacity=o, fill_color=c,
                    )
                    sq.move_to([
                        center[0] + j * cell - n * cell / 2 + cell / 2,
                        center[1] - i * cell + n * cell / 2 - cell / 2,
                        0,
                    ])
                    grp.add(sq)
            return grp

        def wcolor(v):
            return GREEN if v >= 0 else RED

        def wop(v):
            return min(1.0, abs(v) / W_max)

        w_grid = build_grid(W, wcolor, wop, [-3.8, 0, 0])
        w_label = Tex("weights $w$", font_size=24).next_to(
            w_grid, DOWN, buff=0.2
        )

        img_grid = build_grid(
            img,
            lambda v: WHITE,
            lambda v: float(v),
            [0, 0, 0],
        )
        img_label = Tex("input $x$", font_size=24).next_to(
            img_grid, DOWN, buff=0.2
        )

        prod = W * img
        prod_grid = build_grid(
            prod,
            lambda v: GREEN if v >= 0 else RED,
            lambda v: min(1.0, abs(v) / W_max),
            [3.8, 0, 0],
        )
        prod_label = Tex(
            "element-wise $w \\odot x$", font_size=22,
        ).next_to(prod_grid, DOWN, buff=0.2)

        self.play(FadeIn(w_grid), Write(w_label))
        self.play(FadeIn(img_grid), Write(img_label))
        self.play(TransformFromCopy(img_grid, prod_grid),
                  Write(prod_label))

        z_val = float(np.sum(prod))
        bias = -0.3
        sig = 1.0 / (1.0 + np.exp(-(z_val + bias)))

        summary = VGroup(
            MathTex(rf"z = \sum_i w_i x_i + b = {z_val:.2f} + ({bias:.2f})",
                    font_size=28),
            MathTex(rf"a = \sigma(z) \approx {sig:.3f}",
                    font_size=28, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        summary.to_edge(DOWN, buff=0.25)
        self.play(FadeIn(summary[0]))
        self.play(FadeIn(summary[1]))
        self.wait(1.5)
