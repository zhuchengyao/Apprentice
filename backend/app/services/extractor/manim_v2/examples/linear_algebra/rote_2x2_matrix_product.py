from manim import *
import numpy as np


class Rote2x2MatrixProductExample(Scene):
    """
    Rote 2×2 matrix multiplication:
    [[-3, 1], [2, 5]] · [[5, 3], [7, -3]] = ?

    SINGLE_FOCUS: draw both matrices side-by-side; ValueTracker step_tr
    reveals each of 4 output entries by showing the row·col computation:
    e.g. (-3)·5 + 1·7 = -8 for entry (1, 1).
    """

    def construct(self):
        title = Tex(r"Rote $2\!\times\!2$ product: $A\cdot B$",
                    font_size=30).to_edge(UP, buff=0.3)
        self.play(Write(title))

        A = np.array([[-3, 1], [2, 5]])
        B = np.array([[5, 3], [7, -3]])
        AB = A @ B

        A_tex = Matrix([[-3, 1], [2, 5]]).set_color(BLUE).scale(0.95)
        B_tex = Matrix([[5, 3], [7, -3]]).set_color(ORANGE).scale(0.95)
        eq = MathTex(r"=", font_size=48)
        result_strs = [[r"?", r"?"], [r"?", r"?"]]
        result_tex = Matrix(result_strs).scale(0.95)

        row = VGroup(A_tex, B_tex, eq, result_tex).arrange(RIGHT, buff=0.3)
        row.shift(UP * 0.5)
        self.add(row)

        # Step tracker
        step_tr = ValueTracker(-1.0)

        entries_order = [(0, 0), (0, 1), (1, 0), (1, 1)]

        def k_now():
            return int(round(step_tr.get_value()))

        # Build revealed output
        def revealed():
            k = k_now()
            grp = VGroup()
            # position cells from result_tex
            for idx, (r, c) in enumerate(entries_order):
                if idx <= k:
                    val = AB[r, c]
                    cell = result_tex.get_rows()[r].submobjects[c]
                    grp.add(Tex(str(val), font_size=36, color=GREEN).move_to(cell))
            return grp

        self.add(always_redraw(revealed))

        # Highlights
        def A_row_hi():
            k = k_now()
            if k < 0 or k >= 4: return VMobject()
            r = entries_order[k][0]
            target_row = A_tex.get_rows()[r]
            return SurroundingRectangle(target_row, color=BLUE, stroke_width=3, buff=0.08)

        def B_col_hi():
            k = k_now()
            if k < 0 or k >= 4: return VMobject()
            c = entries_order[k][1]
            col_elements = VGroup(*[B_tex.get_rows()[i].submobjects[c] for i in range(2)])
            return SurroundingRectangle(col_elements, color=ORANGE,
                                           stroke_width=3, buff=0.08)

        self.add(always_redraw(A_row_hi), always_redraw(B_col_hi))

        # Computation string below
        def compute_str():
            k = k_now()
            if k < 0: return ""
            r, c = entries_order[k]
            a1, a2 = A[r, 0], A[r, 1]
            b1, b2 = B[0, c], B[1, c]
            val = AB[r, c]
            return rf"$({a1})\cdot{b1}+({a2})\cdot{b2}={val}$"

        comp_tex = Tex(compute_str(), color=GREEN, font_size=32).to_edge(DOWN, buff=0.8)
        self.add(comp_tex)
        def update_comp(mob, dt):
            new = Tex(compute_str(), color=GREEN, font_size=32).move_to(comp_tex)
            comp_tex.become(new)
            return comp_tex
        comp_tex.add_updater(update_comp)

        # Current entry indicator
        indicator = Tex(r"entry $(r, c)$", color=YELLOW, font_size=24)
        indicator.next_to(comp_tex, DOWN, buff=0.3)
        self.add(indicator)

        def update_indicator(mob, dt):
            k = k_now()
            if k < 0: txt = r"ready..."
            else:
                r, c = entries_order[k]
                txt = rf"entry ({r+1}, {c+1}): row {r+1} of $A$ $\cdot$ col {c+1} of $B$"
            new = Tex(txt, color=YELLOW, font_size=24).move_to(indicator)
            indicator.become(new)
            return indicator
        indicator.add_updater(update_indicator)

        for k in range(4):
            self.play(step_tr.animate.set_value(float(k)),
                      run_time=1.8, rate_func=smooth)
            self.wait(0.6)
        self.wait(0.8)
