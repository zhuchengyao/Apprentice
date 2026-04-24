from manim import *
import numpy as np


class PseudoinverseExample(Scene):
    """
    Moore-Penrose pseudoinverse solves least-squares and minimum-norm
    systems. For A ∈ ℝ^{2×3}, Ax = b underdetermined. A^+ = V Σ^+ U^T
    gives the minimum-norm solution x_LS = A^+ b.

    TWO_COLUMN: LEFT shows the 3D input space (orthographic); ValueTracker t_tr sweeps a ray of general solutions
    x(t) = x_LS + t · n where n spans ker A. Live |x(t)| is minimized at t=0. RIGHT shows the equations,
    A^+ b formula, and live t, |x(t)|.
    """

    def construct(self):
        title = Tex(r"Pseudoinverse: $x_{\mathrm{LS}}=A^+ b$ minimizes $\|x\|$ among $Ax=b$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        A = np.array([[1.0, 2.0, -1.0],
                      [2.0, 1.0,  1.0]])
        b = np.array([3.0, 3.0])
        x_ls, *_ = np.linalg.lstsq(A, b, rcond=None)
        # kernel basis
        _, _, Vt = np.linalg.svd(A)
        n_vec = Vt[-1]  # ker A (1-dimensional)
        # sanity: A @ n_vec ≈ 0
        # sanity: A @ x_ls ≈ b

        # 3D orthographic display
        axes = ThreeDAxes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[-3, 3, 1],
                          x_length=5, y_length=5, z_length=5)
        # Project 3D points to 2D with orthographic axonometric
        def proj(v):
            # simple axonometric projection
            x, y, z = v
            P = np.array([x - 0.4 * y, z - 0.4 * y, 0.0])
            return P * 0.6 + LEFT * 2.8 + DOWN * 0.2

        # Draw axis arrows
        axis_arrows = VGroup(
            Arrow(proj(np.zeros(3)), proj([3, 0, 0]), color=BLUE, buff=0, stroke_width=3),
            Arrow(proj(np.zeros(3)), proj([0, 3, 0]), color=GREEN, buff=0, stroke_width=3),
            Arrow(proj(np.zeros(3)), proj([0, 0, 3]), color=ORANGE, buff=0, stroke_width=3),
            Tex(r"$x_1$", font_size=22, color=BLUE).move_to(proj([3.3, 0, 0])),
            Tex(r"$x_2$", font_size=22, color=GREEN).move_to(proj([0, 3.3, 0])),
            Tex(r"$x_3$", font_size=22, color=ORANGE).move_to(proj([0, 0, 3.3])),
        )
        self.play(FadeIn(axis_arrows))

        # LS solution as RED dot
        ls_dot = Dot(proj(x_ls), color=RED, radius=0.13)
        ls_lbl = Tex(r"$x_{\mathrm{LS}}=A^+b$", color=RED, font_size=22).next_to(
            ls_dot, UL, buff=0.1)
        self.play(FadeIn(ls_dot), Write(ls_lbl))

        # Solution line x_ls + t * n_vec
        line_pts = [proj(x_ls + t * n_vec) for t in np.linspace(-2, 2, 40)]
        sol_line = VMobject().set_points_as_corners(line_pts)\
            .set_color(YELLOW).set_stroke(width=2.5)
        self.play(Create(sol_line))

        t_tr = ValueTracker(0.0)

        def x_of():
            return x_ls + t_tr.get_value() * n_vec

        def xdot():
            return Dot(proj(x_of()), color=YELLOW, radius=0.11)

        self.add(always_redraw(xdot))

        # Right column
        right = VGroup(
            Tex(r"$A=\begin{pmatrix}1&2&-1\\2&1&1\end{pmatrix},\ b=\begin{pmatrix}3\\3\end{pmatrix}$",
                font_size=20),
            Tex(r"$\mathrm{ker}\,A=\mathrm{span}(n)$, $n\approx(0.58, -0.58, 0.58)$",
                font_size=20),
            Tex(r"all solutions: $x(t)=x_{\mathrm{LS}}+tn$", font_size=20),
            VGroup(Tex(r"$t=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\|x(t)\|=$", font_size=22),
                   DecimalNumber(float(np.linalg.norm(x_ls)), num_decimal_places=4,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\|Ax(t)-b\|=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=6,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"$\|x(t)\|$ minimized at $t=0$", color=RED, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.2)

        right[3][1].add_updater(lambda m: m.set_value(t_tr.get_value()))
        right[4][1].add_updater(lambda m: m.set_value(float(np.linalg.norm(x_of()))))
        right[5][1].add_updater(lambda m: m.set_value(float(np.linalg.norm(A @ x_of() - b))))
        self.add(right)

        for tval in [1.5, -1.5, 0.8, -0.8, 0.0]:
            self.play(t_tr.animate.set_value(tval),
                      run_time=1.8, rate_func=smooth)
            self.wait(0.3)
        self.wait(0.5)
