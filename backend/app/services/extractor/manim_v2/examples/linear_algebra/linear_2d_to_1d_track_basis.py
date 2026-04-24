from manim import *
import numpy as np


class Linear2Dto1DTrackBasisExample(Scene):
    """
    A 2D→1D linear map is fully determined by L(î) and L(ĵ). Its
    matrix is the 1×2 row [L(î), L(ĵ)]. Then L(x, y) = L(î)·x + L(ĵ)·y.
    """

    def construct(self):
        title = Tex(r"Track $\hat\imath, \hat\jmath\to$ build 1$\times$2 matrix",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-3, 3, 1], y_range=[-2, 2, 1],
                            x_length=5.5, y_length=4.5,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(LEFT * 3.0 + DOWN * 0.2)
        num_line = NumberLine(x_range=[-4, 4, 1], length=6,
                              include_numbers=True,
                              font_size=18).shift(RIGHT * 2.5 + DOWN * 0.3)
        self.play(Create(plane), Create(num_line))

        # L(x, y) = 2x - y.
        # L(î) = 2, L(ĵ) = -1.
        L_i = 2.0
        L_j = -1.0

        i_arrow = Arrow(plane.c2p(0, 0), plane.c2p(1, 0),
                         color=GREEN, buff=0, stroke_width=5)
        j_arrow = Arrow(plane.c2p(0, 0), plane.c2p(0, 1),
                         color=RED, buff=0, stroke_width=5)
        self.add(i_arrow, j_arrow)
        self.add(Tex(r"$\hat\imath$", color=GREEN, font_size=22).next_to(i_arrow.get_end(), UR, buff=0.05))
        self.add(Tex(r"$\hat\jmath$", color=RED, font_size=22).next_to(j_arrow.get_end(), UL, buff=0.05))

        # Animate î → L(î)=2 on number line
        stage_tr = ValueTracker(0.0)

        def i_mapped():
            t = stage_tr.get_value()
            t = min(1.0, t)
            start = plane.c2p(1, 0)
            end = num_line.n2p(L_i)
            pos = (1 - t) * start + t * end
            return Dot(pos, color=GREEN, radius=0.13)

        def j_mapped():
            t = stage_tr.get_value()
            t = max(0, t - 1)
            start = plane.c2p(0, 1)
            end = num_line.n2p(L_j)
            pos = (1 - t) * start + t * end
            return Dot(pos, color=RED, radius=0.13)

        self.add(always_redraw(i_mapped), always_redraw(j_mapped))

        # Matrix construction
        matrix_stage_tr = ValueTracker(0.0)

        def matrix_tex():
            s = matrix_stage_tr.get_value()
            if s < 0.05:
                return MathTex(r"L=\begin{pmatrix}?&?\end{pmatrix}",
                                font_size=40, color=WHITE)
            if s < 0.95:
                return MathTex(r"L=\begin{pmatrix}2&?\end{pmatrix}",
                                font_size=40).set_color_by_tex("2", GREEN)
            return MathTex(r"L=\begin{pmatrix}2&-1\end{pmatrix}",
                            font_size=40).set_color_by_tex("2", GREEN)

        m = matrix_tex().to_edge(DOWN, buff=1.0)
        self.add(m)
        def update_m(mob, dt):
            new = matrix_tex().move_to(m)
            m.become(new)
            return m
        m.add_updater(update_m)

        self.play(stage_tr.animate.set_value(1.0), run_time=2.0, rate_func=smooth)
        self.play(matrix_stage_tr.animate.set_value(0.5), run_time=0.8)
        self.wait(0.3)
        self.play(stage_tr.animate.set_value(2.0), run_time=2.0, rate_func=smooth)
        self.play(matrix_stage_tr.animate.set_value(1.0), run_time=0.8)
        self.wait(0.5)

        formula = Tex(r"$L(x, y) = 2x - y$", color=YELLOW, font_size=26).to_edge(DOWN, buff=0.4)
        self.play(Write(formula))
        self.wait(0.8)
