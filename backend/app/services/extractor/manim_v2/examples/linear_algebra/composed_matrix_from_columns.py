from manim import *
import numpy as np


class ComposedMatrixFromColumnsExample(Scene):
    """
    More complicated example: M_1 = [[1, -2], [1, 0]], M_2 = [[0, 2], [1, 0]].
    Apply M_1 then M_2 to the plane. Read off the composite M_2·M_1's
    columns from where î, ĵ land.

    M_1 î = (1, 1), M_2(M_1 î) = M_2·(1, 1) = (2, 1)
    M_1 ĵ = (-2, 0), M_2·(-2, 0) = (0, -2)
    So M_2·M_1 = [[2, 0], [1, -2]].

    TWO_COLUMN: LEFT plane with composite + basis arrows.
    RIGHT shows M_1, M_2, composite (= M_2·M_1) matrices with ? entries
    filled as transformation progresses.
    """

    def construct(self):
        title = Tex(r"More complex composition: read composite columns from $\hat\imath, \hat\jmath$ landing",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        M1 = np.array([[1.0, -2.0], [1.0, 0.0]])
        M2 = np.array([[0.0, 2.0], [1.0, 0.0]])
        C = M2 @ M1

        plane_center = LEFT * 2.3 + DOWN * 0.3
        scale = 0.48

        stage_tr = ValueTracker(0.0)

        def M_of():
            s = stage_tr.get_value()
            if s <= 1:
                return (1 - s) * np.eye(2) + s * M1
            alpha = s - 1
            return (1 - alpha) * M1 + alpha * C

        def to_screen(v):
            return np.array([v[0] * scale, v[1] * scale, 0]) + plane_center

        def grid():
            M = M_of()
            grp = VGroup()
            for k in range(-3, 4):
                pts_h = [to_screen(M @ np.array([x, k])) for x in np.linspace(-4, 4, 20)]
                pts_v = [to_screen(M @ np.array([k, y])) for y in np.linspace(-4, 4, 20)]
                col_h = interpolate_color(BLUE, TEAL, (k + 3) / 6)
                col_v = interpolate_color(ORANGE, YELLOW, (k + 3) / 6)
                grp.add(VMobject().set_points_as_corners(pts_h)
                         .set_color(col_h).set_stroke(width=1.2, opacity=0.65))
                grp.add(VMobject().set_points_as_corners(pts_v)
                         .set_color(col_v).set_stroke(width=1.2, opacity=0.65))
            return grp

        def i_arrow():
            M = M_of()
            p = M @ np.array([1, 0])
            return Arrow(plane_center, to_screen(p),
                          color=GREEN, buff=0, stroke_width=4)

        def j_arrow():
            M = M_of()
            p = M @ np.array([0, 1])
            return Arrow(plane_center, to_screen(p),
                          color=RED, buff=0, stroke_width=4)

        self.add(always_redraw(grid), always_redraw(i_arrow), always_redraw(j_arrow))

        # Right column: matrices
        def M1_str():
            return r"$M_1=\begin{pmatrix}1&-2\\1&0\end{pmatrix}$"
        def M2_str():
            return r"$M_2=\begin{pmatrix}0&2\\1&0\end{pmatrix}$"

        def C_str():
            M = M_of()
            s = stage_tr.get_value()
            if s < 0.5:
                return r"$M_2 M_1=\begin{pmatrix}?&?\\?&?\end{pmatrix}$"
            return rf"$M_2 M_1=\begin{{pmatrix}}{M[0, 0]:+.1f}&{M[0, 1]:+.1f}\\{M[1, 0]:+.1f}&{M[1, 1]:+.1f}\end{{pmatrix}}$"

        m1_tex = Tex(M1_str(), font_size=28)
        m2_tex = Tex(M2_str(), font_size=28)
        c_tex = Tex(C_str(), font_size=28)
        m1_tex.to_edge(RIGHT, buff=0.3).shift(UP * 1.8)
        m2_tex.next_to(m1_tex, DOWN, buff=0.4, aligned_edge=LEFT)
        c_tex.next_to(m2_tex, DOWN, buff=0.4, aligned_edge=LEFT)
        self.add(m1_tex, m2_tex, c_tex)

        def update_c(mob, dt):
            new = Tex(C_str(), font_size=28).move_to(c_tex, aligned_edge=LEFT)
            c_tex.become(new)
            return c_tex
        c_tex.add_updater(update_c)

        # Col-reading note
        col_note = Tex(r"cols = $C(\hat\imath), C(\hat\jmath)$",
                        color=YELLOW, font_size=22).next_to(c_tex, DOWN, buff=0.3, aligned_edge=LEFT)
        self.add(col_note)

        self.play(stage_tr.animate.set_value(1.0), run_time=2.5, rate_func=smooth)
        self.wait(0.5)
        self.play(stage_tr.animate.set_value(2.0), run_time=2.5, rate_func=smooth)
        self.wait(1.0)
