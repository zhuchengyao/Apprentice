from manim import *
import numpy as np


class TrackBasisToBuildCompositeExample(Scene):
    """
    After composite transformation C, track where î and ĵ land.
    Those two columns ARE the matrix of C. No multiplication needed
    — just read off coordinates.

    SINGLE_FOCUS: composite R then S (rotation then shear).
    ValueTracker t_tr applies transformation; final positions of
    î = (0, 1) and ĵ = (-1, 0) are highlighted and written as matrix columns.
    Wait, let me re-check: R=[[0, -1], [1, 0]] sends (1, 0)→(0, 1), (0, 1)→(-1, 0).
    Then S=[[1, 1], [0, 1]] sends (0, 1)→(1, 1), (-1, 0)→(-1, 0).
    So C(î)=(1, 1), C(ĵ)=(-1, 0).
    """

    def construct(self):
        title = Tex(r"Track $\hat\imath, \hat\jmath$ to read off composite matrix",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane_center = LEFT * 2.5 + DOWN * 0.3
        scale = 0.6

        R = np.array([[0.0, -1.0], [1.0, 0.0]])
        S = np.array([[1.0, 1.0], [0.0, 1.0]])
        C = S @ R

        t_tr = ValueTracker(0.0)

        def M_of():
            s = t_tr.get_value()
            if s <= 1:
                return (1 - s) * np.eye(2) + s * R
            alpha = s - 1
            return (1 - alpha) * R + alpha * C

        def to_screen(v):
            return np.array([v[0] * scale, v[1] * scale, 0]) + plane_center

        def i_arrow():
            M = M_of()
            p = M @ np.array([1, 0])
            return Arrow(plane_center, to_screen(p), color=GREEN,
                          buff=0, stroke_width=5)

        def j_arrow():
            M = M_of()
            p = M @ np.array([0, 1])
            return Arrow(plane_center, to_screen(p), color=RED,
                          buff=0, stroke_width=5)

        def i_label():
            M = M_of()
            p = M @ np.array([1, 0])
            return Tex(rf"$({M[0, 0]:+.1f}, {M[1, 0]:+.1f})$",
                        color=GREEN, font_size=22).move_to(to_screen(p) + UP * 0.3 + RIGHT * 0.3)

        def j_label():
            M = M_of()
            p = M @ np.array([0, 1])
            return Tex(rf"$({M[0, 1]:+.1f}, {M[1, 1]:+.1f})$",
                        color=RED, font_size=22).move_to(to_screen(p) + UP * 0.3 + LEFT * 0.4)

        # Background plane
        bg_plane = NumberPlane(x_range=[-3, 3, 1], y_range=[-3, 3, 1],
                                x_length=4.5, y_length=4.5,
                                background_line_style={"stroke_opacity": 0.3}
                                ).move_to(plane_center)
        self.add(bg_plane)

        self.add(always_redraw(i_arrow), always_redraw(j_arrow),
                 always_redraw(i_label), always_redraw(j_label))

        # Right: matrix built from columns
        def matrix_str():
            M = M_of()
            return rf"$C=\begin{{pmatrix}}{M[0, 0]:+.1f}&{M[0, 1]:+.1f}\\{M[1, 0]:+.1f}&{M[1, 1]:+.1f}\end{{pmatrix}}$"

        mat_tex = Tex(matrix_str(), font_size=36)
        mat_tex.shift(RIGHT * 2.8)
        self.add(mat_tex)
        def update_mat(mob, dt):
            new = Tex(matrix_str(), font_size=36).move_to(mat_tex)
            mat_tex.become(new)
            return mat_tex
        mat_tex.add_updater(update_mat)

        # Col labels
        self.add(Tex(r"col 1 $= C(\hat\imath)$", color=GREEN, font_size=20).move_to(
            RIGHT * 2.8 + DOWN * 1.1))
        self.add(Tex(r"col 2 $= C(\hat\jmath)$", color=RED, font_size=20).move_to(
            RIGHT * 2.8 + DOWN * 1.6))
        self.add(Tex(r"no multiplication needed",
                     color=YELLOW, font_size=20).move_to(
            RIGHT * 2.8 + DOWN * 2.3))

        self.play(t_tr.animate.set_value(1.0), run_time=2.5, rate_func=smooth)
        self.wait(0.5)
        self.play(t_tr.animate.set_value(2.0), run_time=2.5, rate_func=smooth)
        self.wait(1.0)
