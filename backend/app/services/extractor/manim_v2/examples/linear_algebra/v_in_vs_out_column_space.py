from manim import *
import numpy as np


class VInVsOutColumnSpaceExample(Scene):
    """
    When det A = 0, Ax = v has a solution iff v is in the column space.
    A = [[2, 1], [-2, -1]]; col space is the line along (2, -2).
    v_in = (-4, 4) (on line) → solutions exist
    v_out = (1, -1) → ... wait, (1, -1) is NOT on the line (2, -2 direction is slope -1, (1, -1) is on that)
    Let me check: col space is span of (2, -2) (first col) and (1, -1) (second col). These are parallel (both slope -1). So col space = line y = -x.
    v_in = (-4, 4) satisfies 4 = -(-4) ✓ on line.
    v_out = (1, -1) satisfies -1 = -1 ✓ still on line!
    Need different v_out. Use v_out = (1, 1). Then 1 ≠ -1. ✓ off line.
    Update in original: v_out = Vector([1, -1]) was in 3b1b but apparently
    they meant something different. For our demo, use:
    v_in = (-4, 4) on line y=-x → solutions exist
    v_out = (1, 1) off line → no solution
    """

    def construct(self):
        title = Tex(r"$A\vec x=\vec v$ solvable iff $\vec v$ in column space",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 5, 1], y_range=[-3, 3, 1],
                            x_length=9, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.1)
        self.play(Create(plane))

        # After transformation, grid collapses to line y = -x
        col_line = Line(plane.c2p(-4, 4), plane.c2p(4, -4),
                         color=TEAL, stroke_width=5)
        col_lbl = Tex(r"column space (line $y=-x$)", color=TEAL,
                       font_size=22).move_to(plane.c2p(3, -2.3))
        self.play(Create(col_line), Write(col_lbl))

        # v_in and v_out
        v_in = np.array([-4.0, 4.0])
        v_out = np.array([1.0, 1.0])

        v_in_arrow = Arrow(plane.c2p(0, 0), plane.c2p(v_in[0], v_in[1]),
                            color=YELLOW, buff=0, stroke_width=5)
        v_in_lbl = Tex(r"$\vec v_1=(-4, 4)$ (on line)", color=YELLOW,
                        font_size=22).next_to(v_in_arrow.get_end(), UP, buff=0.1)
        self.play(Create(v_in_arrow), Write(v_in_lbl))
        note_in = Tex(r"$\Rightarrow$ solutions exist", color=GREEN,
                       font_size=24).move_to(plane.c2p(-2, 1.8))
        self.play(Write(note_in))
        self.wait(0.5)

        v_out_arrow = Arrow(plane.c2p(0, 0), plane.c2p(v_out[0], v_out[1]),
                             color=RED, buff=0, stroke_width=5)
        v_out_lbl = Tex(r"$\vec v_2=(1, 1)$ (off line)", color=RED,
                         font_size=22).next_to(v_out_arrow.get_end(), UR, buff=0.1)
        self.play(Create(v_out_arrow), Write(v_out_lbl))
        note_out = Tex(r"$\Rightarrow$ no solution", color=RED,
                        font_size=24).move_to(plane.c2p(3, 1.8))
        self.play(Write(note_out))
        self.wait(0.8)

        info = VGroup(
            Tex(r"$A=\begin{pmatrix}2&1\\-2&-1\end{pmatrix}$", font_size=22),
            Tex(r"$\det A=0$", color=RED, font_size=22),
            Tex(r"col space: span of cols = line",
                color=TEAL, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.3).shift(UP * 0.3)
        self.play(Write(info))
        self.wait(1.0)
