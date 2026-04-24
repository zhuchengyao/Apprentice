from manim import *
import numpy as np


class ToeplitzCirculantExample(Scene):
    """
    Toeplitz matrix: constant along each diagonal, T[i, j] = c_{i-j}.
    Circulant matrix: each row is a cyclic shift of the previous,
    T[i, j] = c_{(j-i) mod n}. Every circulant is diagonalized by
    the DFT matrix F: C = F* diag(DFT(c)) F.

    SINGLE_FOCUS: 7×7 matrix display. ValueTracker k_tr cyclically
    shifts the top row (c = [3, 1, 0, 0, 0, 1, 2]) to show the
    circulant structure emerging. Each cell shows its value; diagonals
    color-coded.
    """

    def construct(self):
        title = Tex(r"Circulant = every row is a cyclic shift;" +
                    r"\ $C=F^*\mathrm{diag}(\hat c)F$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        n = 7
        c = np.array([3, 1, 0, 0, 0, 1, 2])
        shift_tr = ValueTracker(0.0)

        cell_s = 0.65
        origin = np.array([-2.6, 1.2, 0])

        def matrix_cells():
            s = int(round(shift_tr.get_value())) % n
            grp = VGroup()
            c_shift = np.roll(c, s)  # sliding the "row 0" definition
            # Build circulant: row i = np.roll(c_shift, i)
            for i in range(n):
                row = np.roll(c_shift, i)
                for j in range(n):
                    val = int(row[j])
                    x = origin[0] + j * cell_s
                    y = origin[1] - i * cell_s
                    # color by diagonal = (j - i) mod n
                    d = (j - i) % n
                    # map d → color cycle
                    base_col = [BLUE, GREEN, YELLOW, ORANGE, RED, PURPLE, TEAL][d]
                    rect = Square(side_length=cell_s * 0.9,
                                  color=base_col, stroke_width=1.2,
                                  fill_color=base_col,
                                  fill_opacity=0.15 + 0.12 * val).move_to([x, y, 0])
                    grp.add(rect)
                    grp.add(Tex(str(val), font_size=22).move_to([x, y, 0]))
            return grp

        self.add(always_redraw(matrix_cells))

        # Top row banner outside
        banner_lbl = Tex(r"top row $c=$", font_size=22).move_to(
            [origin[0] - 1.6, origin[1] - 2.0 + cell_s, 0])
        self.add(banner_lbl)

        def banner():
            s = int(round(shift_tr.get_value())) % n
            c_shift = np.roll(c, s)
            grp = VGroup()
            for j in range(n):
                x = origin[0] + j * cell_s
                val = int(c_shift[j])
                d = j % n
                base_col = [BLUE, GREEN, YELLOW, ORANGE, RED, PURPLE, TEAL][d]
                rect = Square(side_length=cell_s * 0.9,
                              color=base_col, stroke_width=2,
                              fill_color=base_col,
                              fill_opacity=0.15 + 0.12 * val).move_to([x, origin[1] - 2.0 + cell_s, 0])
                grp.add(rect)
                grp.add(Tex(str(val), font_size=22).move_to([x, origin[1] - 2.0 + cell_s, 0]))
            return grp
        self.add(always_redraw(banner))

        # DFT eigenvalues panel
        def eigen_panel():
            s = int(round(shift_tr.get_value())) % n
            c_shift = np.roll(c, s)
            evals = np.fft.fft(c_shift)
            lines = [r"$\hat c =$"]
            for k, ev in enumerate(evals):
                lines.append(f"$\\lambda_{{{k}}}={ev.real:+.2f}" +
                             (f"{ev.imag:+.2f}i" if abs(ev.imag) > 0.01 else "") + "$")
            return VGroup(*[Tex(l, font_size=20) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(RIGHT, buff=0.3)

        eig_grp = eigen_panel()
        eig_grp.add_updater(lambda m, dt: m.become(eigen_panel()))
        self.add(eig_grp)

        # Shift animation
        for target in [1, 3, 5, 7, 0]:
            self.play(shift_tr.animate.set_value(float(target)),
                      run_time=1.8, rate_func=smooth)
            self.wait(0.3)
        self.wait(0.5)
