from manim import *
import numpy as np


class Convolution2DKernelExample(Scene):
    """
    2D convolution: input I (10×10) convolved with a 3×3 kernel K
    produces output O (8×8). Visualize the sliding window.

    SINGLE_FOCUS:
      LEFT input grid with YELLOW highlighted 3×3 patch; RIGHT output
      grid with colored result cell. ValueTracker slide_tr advances
      the patch across all 64 positions; always_redraw highlight +
      output cell.
    """

    def construct(self):
        title = Tex(r"2D convolution: sliding $3\times 3$ kernel over input",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        rng = np.random.default_rng(4)
        I = rng.integers(0, 10, (10, 10)).astype(float) / 10.0
        # Edge-detection kernel (Sobel-like)
        K = np.array([[-1, -1, -1],
                        [-1, 8, -1],
                        [-1, -1, -1]]).astype(float)

        cell = 0.35
        in_origin = np.array([-4.5, 1.8, 0])
        out_origin = np.array([2, 1.8, 0])

        # Draw input grid
        input_cells = VGroup()
        for i in range(10):
            for j in range(10):
                sq = Square(side_length=cell * 0.95,
                              color=WHITE, stroke_width=0.6,
                              fill_opacity=0.1 + I[i, j] * 0.55,
                              fill_color=BLUE_E)
                sq.move_to(in_origin + np.array([j * cell, -i * cell, 0]))
                input_cells.add(sq)
        in_lbl = Tex(r"input $I$ (10$\times$10)",
                      color=WHITE, font_size=20
                      ).next_to(input_cells, UP, buff=0.2)
        self.play(FadeIn(input_cells), Write(in_lbl))

        # Draw output grid (empty initially)
        output_cells_grid = VGroup()
        for i in range(8):
            for j in range(8):
                sq = Square(side_length=cell * 0.95,
                              color=WHITE, stroke_width=0.6,
                              fill_opacity=0.0)
                sq.move_to(out_origin + np.array([j * cell, -i * cell, 0]))
                output_cells_grid.add(sq)
        out_lbl = Tex(r"output $O = I * K$ (8$\times$8)",
                       color=WHITE, font_size=20
                       ).next_to(output_cells_grid, UP, buff=0.2)
        self.play(FadeIn(output_cells_grid), Write(out_lbl))

        # Precompute convolution output
        O = np.zeros((8, 8))
        for i in range(8):
            for j in range(8):
                patch = I[i:i+3, j:j+3]
                O[i, j] = np.sum(patch * K)

        slide_tr = ValueTracker(0)

        def kernel_patch():
            s = int(round(slide_tr.get_value()))
            s = max(0, min(s, 63))
            i, j = s // 8, s % 8
            # Box around input patch (i, j) to (i+2, j+2)
            top_left = in_origin + np.array([j * cell - cell * 0.45,
                                                 -i * cell + cell * 0.45, 0])
            box = Rectangle(width=cell * 3, height=cell * 3,
                              color=YELLOW, stroke_width=3,
                              fill_opacity=0.2).move_to(
                top_left + np.array([cell * 1.5 - cell * 0.5,
                                        -cell * 1.5 + cell * 0.5, 0]))
            return box

        def output_filled():
            s = int(round(slide_tr.get_value()))
            s = max(-1, min(s, 63))
            grp = VGroup()
            for k in range(s + 1):
                i, j = k // 8, k % 8
                val = O[i, j]
                # Normalize to [-1, 1] range for color
                norm = max(-1.0, min(1.0, val / 4))
                if norm > 0:
                    col = interpolate_color(GREY_B, RED, norm)
                else:
                    col = interpolate_color(GREY_B, BLUE, -norm)
                sq = Square(side_length=cell * 0.95,
                              color=col, fill_opacity=0.85,
                              stroke_width=0.8)
                sq.move_to(out_origin + np.array([j * cell, -i * cell, 0]))
                grp.add(sq)
            return grp

        def current_output_highlight():
            s = int(round(slide_tr.get_value()))
            s = max(0, min(s, 63))
            i, j = s // 8, s % 8
            box = Square(side_length=cell * 0.95,
                           color=YELLOW, stroke_width=3,
                           fill_opacity=0.0)
            box.move_to(out_origin + np.array([j * cell, -i * cell, 0]))
            return box

        self.add(always_redraw(kernel_patch),
                  always_redraw(output_filled),
                  always_redraw(current_output_highlight))

        def info():
            s = int(round(slide_tr.get_value()))
            s = max(0, min(s, 63))
            i, j = s // 8, s % 8
            val = O[i, j]
            return VGroup(
                MathTex(rf"\text{{position}} = ({i}, {j})",
                         color=YELLOW, font_size=20),
                MathTex(rf"O[{i},{j}] = {val:.3f}",
                         color=WHITE, font_size=20),
                Tex(r"kernel: Sobel-edge",
                     color=GREEN, font_size=18),
                MathTex(r"K = [-1,-1,-1;\,-1,8,-1;\,-1,-1,-1]",
                         color=WHITE, font_size=14),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        self.play(slide_tr.animate.set_value(63),
                   run_time=10, rate_func=linear)
        self.wait(0.4)
