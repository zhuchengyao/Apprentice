from manim import *
import numpy as np


class ImageConvolutionKernelSweep(Scene):
    """2D image convolution.  A 3x3 kernel slides over a 10x10 grayscale
    image; at each position, the kernel's 9 pixels are multiplied by the
    underlying image pixels and summed.  Animate the sweep with the
    kernel highlight and the output pixel being filled in — using a
    Sobel-x edge detector to highlight vertical edges."""

    def construct(self):
        title = Tex(
            r"2D convolution: Sobel-$x$ kernel applied to an image",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        H, W = 10, 10
        img = np.zeros((H, W))
        img[:, 3:6] = 1.0
        img[1, 5] = 0.8
        img[5, 4] = 0.4

        kernel = np.array([
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1],
        ], dtype=float)

        cell = 0.45

        def draw_grid(arr, origin, color_of):
            grp = VGroup()
            h, w = arr.shape
            for i in range(h):
                for j in range(w):
                    color = color_of(arr[i, j])
                    sq = Square(
                        side_length=cell, stroke_width=0.6,
                        stroke_color=GREY_B,
                        fill_opacity=0.9, fill_color=color,
                    )
                    sq.move_to([
                        origin[0] + j * cell - w * cell / 2 + cell / 2,
                        origin[1] - i * cell + h * cell / 2 - cell / 2,
                        0,
                    ])
                    grp.add(sq)
            return grp

        def img_color(v):
            v = min(1, max(0, v))
            return interpolate_color(BLACK, WHITE, v)

        img_grid = draw_grid(img, [-3.2, 0.2], img_color)
        img_lab = Tex("input image", font_size=22).move_to([-3.2, 2.7, 0])
        self.play(FadeIn(img_grid), Write(img_lab))

        kernel_grid = VGroup()
        for i in range(3):
            for j in range(3):
                v = kernel[i][j]
                if v > 0:
                    color = GREEN
                elif v < 0:
                    color = RED
                else:
                    color = GREY_D
                sq = Square(
                    side_length=0.55, stroke_width=1.5,
                    stroke_color=color,
                    fill_opacity=0.35, fill_color=color,
                )
                t = Tex(rf"{v:+.0f}", font_size=20,
                        color=WHITE).move_to(sq)
                cell_group = VGroup(sq, t)
                cell_group.move_to([
                    2.0 + j * 0.58 - 0.58,
                    2.0 - i * 0.58 + 0.58,
                    0,
                ])
                kernel_grid.add(cell_group)
        kernel_lab = Tex("Sobel-$x$ kernel", font_size=22).move_to(
            [2.0, 2.95, 0]
        )
        self.play(FadeIn(kernel_grid), Write(kernel_lab))

        out_h, out_w = H - 2, W - 2
        output = np.zeros((out_h, out_w))
        for i in range(out_h):
            for j in range(out_w):
                output[i, j] = np.sum(img[i:i + 3, j:j + 3] * kernel)

        def out_color(v):
            v_max = 2.0
            norm = max(-1, min(1, v / v_max))
            if norm >= 0:
                return interpolate_color(BLACK, BLUE, norm)
            return interpolate_color(BLACK, RED, -norm)

        out_origin = [2.5, -0.9]
        out_grid = VGroup()
        out_cells = {}
        for i in range(out_h):
            for j in range(out_w):
                sq = Square(
                    side_length=cell * 0.9, stroke_width=0.6,
                    stroke_color=GREY_B,
                    fill_opacity=0.2, fill_color=GREY_D,
                )
                sq.move_to([
                    out_origin[0] + j * cell * 0.9 - out_w * cell * 0.9 / 2
                    + cell * 0.9 / 2,
                    out_origin[1] - i * cell * 0.9
                    + out_h * cell * 0.9 / 2 - cell * 0.9 / 2,
                    0,
                ])
                out_cells[(i, j)] = sq
                out_grid.add(sq)
        out_lab = Tex("convolution output", font_size=20).next_to(
            out_grid, UP, buff=0.1
        )
        self.play(FadeIn(out_grid), Write(out_lab))

        sweep_positions = [(0, 2), (2, 2), (4, 2), (6, 2), (4, 5),
                           (4, 7), (0, 0), (7, 7)]
        highlight = Rectangle(
            width=cell * 3, height=cell * 3,
            color=YELLOW, stroke_width=3,
        )

        for si, sj in sweep_positions:
            center_x = -3.2 + sj * cell + cell - W * cell / 2 + cell / 2
            center_y = 0.2 - si * cell - cell + H * cell / 2 - cell / 2
            target_pos = np.array([center_x, center_y, 0])
            if highlight not in self.mobjects:
                highlight.move_to(target_pos)
                self.play(Create(highlight), run_time=0.4)
            else:
                self.play(highlight.animate.move_to(target_pos),
                          run_time=0.5)
            out_sq = out_cells[(si, sj)]
            new_color = out_color(output[si, sj])
            self.play(
                out_sq.animate.set_fill(new_color, opacity=0.9),
                run_time=0.3,
            )

        note = Tex(
            r"Sobel-$x$ highlights vertical edges "
            r"(RED $\to$ negative, BLUE $\to$ positive gradient)",
            font_size=22, color=YELLOW,
        ).to_edge(DOWN, buff=0.2)
        self.play(FadeIn(note))
        self.wait(1.3)
