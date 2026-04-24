from manim import *
import numpy as np


class NonsquareProjectionExample(Scene):
    """
    A 2×3 matrix maps ℝ³ → ℝ²: visualize the kernel as a line in ℝ³
    that the matrix collapses to the origin.

    THREE_ROW + TWO_COLUMN-style:
      LEFT (3D box) — A 3×3 grid of input dots in ℝ³ shown via a
                      ThreeDScene-substitute layout (use 2D plane with
                      stacked rows representing z-slices).
      MIDDLE — the matrix A and the (live) Ax for a moving x.
      RIGHT (2D plane) — output dots in ℝ². ValueTrackers x_a, x_b, x_c
                          drive a single input vector x = (a, b, c)
                          and the always_redraw output dot Ax.

    For A = [[1, 0, -1], [0, 1, 1]], the kernel is span((1, -1, 1)).
    Sweep input along the kernel direction to confirm output stays at 0.
    """

    def construct(self):
        title = Tex(r"$2\times 3$ matrix $A: \mathbb{R}^3 \to \mathbb{R}^2$ has a 1D kernel",
                    font_size=24).to_edge(UP, buff=0.4)
        self.play(Write(title))

        A = np.array([[1.0, 0.0, -1.0],
                      [0.0, 1.0, 1.0]])

        # LEFT: input space ℝ³ rendered as 3 stacked rows of dots representing z=-1,0,+1
        in_anchor = np.array([-4.0, 0.0, 0])
        z_levels = [-1, 0, 1]
        z_colors = {-1: BLUE_E, 0: GREEN, 1: ORANGE}
        in_dots = VGroup()
        for z in z_levels:
            row = VGroup()
            for x in [-1.5, -0.5, 0.5, 1.5]:
                for y in [-1.0, -0.3, 0.4, 1.1]:
                    pos = in_anchor + np.array([x * 0.4, y * 0.4 + z * 1.1, 0])
                    row.add(Dot(pos, color=z_colors[z], radius=0.04))
            in_dots.add(row)
        self.play(FadeIn(in_dots))

        in_lbl = Tex(r"$\mathbb{R}^3$ input", color=WHITE,
                     font_size=22).next_to(in_anchor + UP * 1.8, UP, buff=0.05)
        # Z-level legend
        z_legend = VGroup(
            Tex(r"$z=+1$", color=ORANGE, font_size=18),
            Tex(r"$z=\phantom{+}0$", color=GREEN, font_size=18),
            Tex(r"$z=-1$", color=BLUE_E, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(in_dots, LEFT, buff=0.1)
        self.play(Write(in_lbl), Write(z_legend))

        # RIGHT: output ℝ² as a NumberPlane
        plane = NumberPlane(
            x_range=[-4, 4, 1], y_range=[-3, 3, 1],
            x_length=4.4, y_length=4.0,
            background_line_style={"stroke_opacity": 0.3},
        ).move_to([+3.0, -0.4, 0])
        self.play(Create(plane))
        out_lbl = Tex(r"$\mathbb{R}^2$ output ($Ax$)", color=YELLOW,
                      font_size=22).next_to(plane, UP, buff=0.05)
        self.play(Write(out_lbl))

        # Image of all input dots
        out_dots = VGroup()
        for z in z_levels:
            for x in [-1.5, -0.5, 0.5, 1.5]:
                for y in [-1.0, -0.3, 0.4, 1.1]:
                    v = A @ np.array([x, y, z])
                    out_dots.add(Dot(plane.c2p(v[0], v[1]),
                                     color=z_colors[z], radius=0.04))
        self.play(FadeIn(out_dots))

        # Now sweep along the KERNEL direction (1, -1, 1)
        # x(t) = (1, -1, 1) * t
        kernel_dir = np.array([1, -1, 1])

        t_tr = ValueTracker(0)

        def kernel_pt_in():
            t = t_tr.get_value()
            x_v = kernel_dir * t * 0.4
            # Position in the input rendering: (x, y) component, z determines row
            # x_v = (x, y, z). We use x for horizontal, y for vertical within row.
            # For visualization, render as a YELLOW dot in the corresponding z-slice.
            x, y, z = x_v
            # Map to z-slice (continuous, but discretize for now)
            z_pos = z * 1.1  # use z for vertical offset within in_anchor
            return in_anchor + np.array([x * 0.4, y * 0.4 + z_pos, 0])

        def kernel_pt_out():
            t = t_tr.get_value()
            x_v = kernel_dir * t * 0.4
            v = A @ x_v
            return plane.c2p(v[0], v[1])

        in_marker = always_redraw(lambda: Dot(kernel_pt_in(), color=YELLOW,
                                              radius=0.10))
        out_marker = always_redraw(lambda: Dot(kernel_pt_out(), color=YELLOW,
                                               radius=0.12))
        self.add(in_marker, out_marker)

        # Middle column with the matrix and equations
        mat_lbl = MathTex(
            r"A = \begin{bmatrix} 1 & 0 & -1 \\ 0 & 1 & \phantom{-}1 \end{bmatrix}",
            color=WHITE, font_size=26,
        ).move_to([0, +2.8, 0])
        kernel_lbl = MathTex(
            r"\ker A = \mathrm{span}\!\left(\begin{bmatrix}1 \\ -1 \\ 1\end{bmatrix}\right)",
            color=YELLOW, font_size=24,
        ).move_to([0, -2.8, 0])
        self.play(Write(mat_lbl), Write(kernel_lbl))

        # Sweep t through kernel direction — output stays at origin
        self.play(t_tr.animate.set_value(2.0), run_time=2.5, rate_func=smooth)
        self.wait(0.4)
        self.play(t_tr.animate.set_value(-2.0), run_time=3.0, rate_func=smooth)
        self.wait(0.4)
        self.play(t_tr.animate.set_value(0), run_time=1.5, rate_func=smooth)

        principle = Tex(r"Yellow input slides along $\ker A$; output stays at origin",
                        color=YELLOW, font_size=22).to_edge(DOWN, buff=0.4)
        self.play(Write(principle))
        self.wait(1.0)
