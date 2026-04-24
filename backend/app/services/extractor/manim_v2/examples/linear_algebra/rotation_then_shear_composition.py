from manim import *
import numpy as np


class RotationThenShearCompositionExample(Scene):
    """
    Concrete composition: 90° counterclockwise rotation then horizontal
    shear. R = [[0, -1], [1, 0]], S = [[1, 1], [0, 1]]. Composite
    C = S·R = [[1, -1], [1, 0]].

    SINGLE_FOCUS: grid + labeled î, ĵ. Phase 1 applies R (90° rotation).
    Phase 2 applies S (shear). Final position of î, ĵ forms columns of C.
    """

    def construct(self):
        title = Tex(r"Rotation $\to$ shear: $S\circ R$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane_center = DOWN * 0.3
        scale = 0.8

        R = np.array([[0.0, -1.0], [1.0, 0.0]])
        S = np.array([[1.0, 1.0], [0.0, 1.0]])
        C = S @ R  # [[1, -1], [1, 0]]

        stage_tr = ValueTracker(0.0)

        def M_of():
            s = stage_tr.get_value()
            if s <= 1:
                return (1 - s) * np.eye(2) + s * R
            alpha = s - 1
            return (1 - alpha) * R + alpha * C

        def to_screen(v):
            return np.array([v[0] * scale, v[1] * scale, 0]) + plane_center

        def grid_lines():
            M = M_of()
            grp = VGroup()
            for k in range(-3, 4):
                pts_h = [to_screen(M @ np.array([x, k])) for x in np.linspace(-4, 4, 20)]
                pts_v = [to_screen(M @ np.array([k, y])) for y in np.linspace(-4, 4, 20)]
                col_h = interpolate_color(BLUE, TEAL, (k + 3) / 6)
                col_v = interpolate_color(ORANGE, YELLOW, (k + 3) / 6)
                grp.add(VMobject().set_points_as_corners(pts_h)
                         .set_color(col_h).set_stroke(width=1.5, opacity=0.7))
                grp.add(VMobject().set_points_as_corners(pts_v)
                         .set_color(col_v).set_stroke(width=1.5, opacity=0.7))
            return grp

        def i_arrow():
            M = M_of()
            p = M @ np.array([1, 0])
            return Arrow(plane_center, to_screen(p),
                          color=GREEN, buff=0, stroke_width=5)

        def j_arrow():
            M = M_of()
            p = M @ np.array([0, 1])
            return Arrow(plane_center, to_screen(p),
                          color=RED, buff=0, stroke_width=5)

        self.add(always_redraw(grid_lines),
                 always_redraw(i_arrow), always_redraw(j_arrow))

        # Dynamic matrix display
        def M_str():
            M = M_of()
            return rf"$M=\begin{{pmatrix}}{M[0, 0]:+.2f}&{M[0, 1]:+.2f}\\{M[1, 0]:+.2f}&{M[1, 1]:+.2f}\end{{pmatrix}}$"

        mat_tex = Tex(M_str(), font_size=24)
        mat_tex.to_corner(UR, buff=0.3).shift(UP * 0.2)
        self.add(mat_tex)
        def update_mat(mob, dt):
            new = Tex(M_str(), font_size=24).move_to(mat_tex)
            mat_tex.become(new)
            return mat_tex
        mat_tex.add_updater(update_mat)

        info = VGroup(
            Tex(r"$R=\begin{pmatrix}0&-1\\1&0\end{pmatrix}$ (90° rot)",
                color=BLUE, font_size=20),
            Tex(r"$S=\begin{pmatrix}1&1\\0&1\end{pmatrix}$ (shear)",
                color=ORANGE, font_size=20),
            Tex(r"$C=S R=\begin{pmatrix}1&-1\\1&0\end{pmatrix}$",
                color=YELLOW, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(DR, buff=0.3)
        self.add(info)

        self.play(stage_tr.animate.set_value(1.0), run_time=2.5, rate_func=smooth)
        self.wait(0.5)
        self.play(stage_tr.animate.set_value(2.0), run_time=2.5, rate_func=smooth)
        self.wait(1.0)
