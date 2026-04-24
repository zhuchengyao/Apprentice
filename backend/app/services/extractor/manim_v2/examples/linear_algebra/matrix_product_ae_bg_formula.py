from manim import *
import numpy as np


class MatrixProductAeBgFormulaExample(Scene):
    """
    Derive the general 2×2 matrix product formula from composition.
    M_1 = [[e, f], [g, h]], M_2 = [[a, b], [c, d]]. Composite
    M_2·M_1 has columns = M_2 applied to columns of M_1.

    Column 1: M_2·(e, g) = (ae+bg, ce+dg).
    Column 2: M_2·(f, h) = (af+bh, cf+dh).

    So M_2 M_1 = [[ae+bg, af+bh], [ce+dg, cf+dh]].

    SINGLE_FOCUS: reveal each entry sequentially by highlighting
    the corresponding row·column operation.
    """

    def construct(self):
        title = Tex(r"General 2$\times$2 product via basis columns",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # M_2 on left, M_1 on right (applied after)
        M2_tex = MathTex(r"\begin{pmatrix}a&b\\c&d\end{pmatrix}",
                          font_size=48).set_color(PINK)
        M1_tex = MathTex(r"\begin{pmatrix}e&f\\g&h\end{pmatrix}",
                          font_size=48).set_color(YELLOW)
        eq = MathTex(r"=", font_size=48)
        result = MathTex(r"\begin{pmatrix}\square&\square\\\square&\square\end{pmatrix}",
                          font_size=48)

        row = VGroup(M2_tex, M1_tex, eq, result).arrange(RIGHT, buff=0.3)
        row.shift(UP * 0.5)
        self.add(row)

        # Label M_1, M_2
        M2_lbl = Tex(r"$M_2$", color=PINK, font_size=22).next_to(M2_tex, DOWN, buff=0.2)
        M1_lbl = Tex(r"$M_1$", color=YELLOW, font_size=22).next_to(M1_tex, DOWN, buff=0.2)
        self.add(M2_lbl, M1_lbl)

        # Entries to reveal
        entries = [
            (0, 0, r"ae+bg"),
            (0, 1, r"af+bh"),
            (1, 0, r"ce+dg"),
            (1, 1, r"cf+dh"),
        ]

        # Placement constants: the bounding box of the result matrix
        result_bbox = result.get_bounding_box()
        cell_positions = [
            result.get_center() + LEFT * 0.55 + UP * 0.4,   # (0, 0)
            result.get_center() + RIGHT * 0.55 + UP * 0.4,  # (0, 1)
            result.get_center() + LEFT * 0.55 + DOWN * 0.4, # (1, 0)
            result.get_center() + RIGHT * 0.55 + DOWN * 0.4, # (1, 1)
        ]

        idx_tr = ValueTracker(-1.0)

        def k_now():
            return int(round(idx_tr.get_value()))

        # Revealed-entry labels
        revealed = VGroup()
        def revealed_text():
            k = k_now()
            grp = VGroup()
            for i, (r, c, expr) in enumerate(entries):
                if i <= k:
                    grp.add(MathTex(expr, font_size=30).move_to(cell_positions[i]))
            return grp

        self.add(always_redraw(revealed_text))

        # Highlighting for current step
        def highlight_M2_row():
            k = k_now()
            if k < 0 or k >= 4:
                return VMobject()
            row = entries[k][0]
            # Row in M_2
            row_y = M2_tex.get_y() + (0.38 if row == 0 else -0.38)
            return Rectangle(width=M2_tex.width * 0.9, height=0.5,
                              color=PINK, stroke_width=3,
                              fill_opacity=0).move_to(
                np.array([M2_tex.get_x(), row_y, 0]))

        def highlight_M1_col():
            k = k_now()
            if k < 0 or k >= 4:
                return VMobject()
            col = entries[k][1]
            col_x = M1_tex.get_x() + (-0.25 if col == 0 else 0.25)
            return Rectangle(width=0.5, height=M1_tex.height * 0.9,
                              color=YELLOW, stroke_width=3,
                              fill_opacity=0).move_to(
                np.array([col_x, M1_tex.get_y(), 0]))

        self.add(always_redraw(highlight_M2_row), always_redraw(highlight_M1_col))

        # Explanation text bottom
        def expl_str():
            k = k_now()
            if k < 0: return r"composite: $M_2(M_1\hat\imath), M_2(M_1\hat\jmath)$"
            r, c, _ = entries[k]
            col_name = r"$\hat\imath$" if c == 0 else r"$\hat\jmath$"
            return rf"entry ({r+1}, {c+1}): row {r+1} of $M_2$ $\cdot$ col {c+1} of $M_1$ (= where {col_name} lands)"

        expl = Tex(expl_str(), color=GREEN, font_size=22).to_edge(DOWN, buff=0.5)
        self.add(expl)
        def update_expl(mob, dt):
            new = Tex(expl_str(), color=GREEN, font_size=22).move_to(expl)
            expl.become(new)
            return expl
        expl.add_updater(update_expl)

        for k in range(4):
            self.play(idx_tr.animate.set_value(float(k)),
                      run_time=1.4, rate_func=smooth)
            self.wait(0.6)
        self.wait(0.8)
