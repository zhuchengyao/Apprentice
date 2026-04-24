from manim import *
import numpy as np


class YoungDiagramsHookExample(Scene):
    """
    Hook length formula: the number of standard Young tableaux of
    shape λ is n! / Π hooks, where hook(i, j) = # cells to the right
    + # cells below + 1.

    SINGLE_FOCUS: Young diagram for λ = (4, 3, 1), n = 8.
    Hooks: (6, 4, 3, 1; 4, 2, 1; 1). Product = 576. 8! / 576 = 70.

    ValueTracker cell_tr walks through cells; always_redraw highlights
    current cell + shows its hook (L-shape of RIGHT + DOWN cells).
    """

    def construct(self):
        title = Tex(r"Hook length formula: $\#\mathrm{SYT}(\lambda)=\dfrac{n!}{\prod h(i,j)}$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        shape = [4, 3, 1]
        n = sum(shape)
        cell_s = 0.9
        origin = np.array([-3.0, 1.3, 0])

        # Build cells
        cells = {}
        for i, row_len in enumerate(shape):
            for j in range(row_len):
                pos = origin + RIGHT * j * cell_s - UP * i * cell_s
                c = Square(side_length=cell_s * 0.94, color=GREY_B,
                           stroke_width=1.2,
                           fill_color=GREY_B, fill_opacity=0.05).move_to(pos)
                cells[(i, j)] = (c, pos)
                self.add(c)

        # Compute hooks
        def hook_len(i, j):
            arm = shape[i] - 1 - j
            leg = sum(1 for k in range(i + 1, len(shape)) if j < shape[k])
            return arm + leg + 1

        hooks = {(i, j): hook_len(i, j) for (i, j) in cells}
        # Display hook number in each cell (static)
        for (i, j), h in hooks.items():
            pos = cells[(i, j)][1]
            self.add(Tex(str(h), font_size=28, color=BLUE).move_to(pos))

        cell_list = list(cells.keys())
        cell_tr = ValueTracker(0.0)

        def idx_now():
            return max(0, min(len(cell_list) - 1, int(round(cell_tr.get_value()))))

        def highlight_current():
            (i, j) = cell_list[idx_now()]
            pos = cells[(i, j)][1]
            return Square(side_length=cell_s * 0.94, color=YELLOW,
                          stroke_width=3.5).move_to(pos)

        def hook_shape():
            (i, j) = cell_list[idx_now()]
            grp = VGroup()
            # right cells
            for k in range(j + 1, shape[i]):
                pos = cells[(i, k)][1]
                grp.add(Square(side_length=cell_s * 0.94, color=GREEN,
                                stroke_width=2, fill_opacity=0.3,
                                fill_color=GREEN).move_to(pos))
            # below cells
            for k in range(i + 1, len(shape)):
                if j < shape[k]:
                    pos = cells[(k, j)][1]
                    grp.add(Square(side_length=cell_s * 0.94, color=ORANGE,
                                    stroke_width=2, fill_opacity=0.3,
                                    fill_color=ORANGE).move_to(pos))
            return grp

        self.add(always_redraw(hook_shape), always_redraw(highlight_current))

        info = VGroup(
            Tex(r"$\lambda=(4,3,1)$, $n=8$", font_size=22),
            VGroup(Tex(r"cell $(i,j)=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0, font_size=22).set_color(YELLOW),
                   Tex(",", font_size=22),
                   DecimalNumber(0, num_decimal_places=0, font_size=22).set_color(YELLOW)
                   ).arrange(RIGHT, buff=0.05),
            VGroup(Tex(r"$h(i,j)=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0, font_size=22).set_color(BLUE)
                   ).arrange(RIGHT, buff=0.1),
            Tex(r"$\prod h = 6\cdot 4\cdot 3\cdot 1\cdot 4\cdot 2\cdot 1\cdot 1 = 576$",
                color=GREEN, font_size=20),
            Tex(r"$n!/576 = 40320/576 = 70$", color=YELLOW, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(DR, buff=0.3)
        info[1][1].add_updater(lambda m: m.set_value(cell_list[idx_now()][0]))
        info[1][3].add_updater(lambda m: m.set_value(cell_list[idx_now()][1]))
        info[2][1].add_updater(lambda m: m.set_value(hooks[cell_list[idx_now()]]))
        self.add(info)

        for k in range(1, len(cell_list)):
            self.play(cell_tr.animate.set_value(float(k)),
                      run_time=0.7, rate_func=smooth)
            self.wait(0.25)
        self.wait(0.8)
