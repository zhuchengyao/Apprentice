from manim import *
import numpy as np


class ColumnSpaceExample(Scene):
    """
    Column space of A as the set of outputs Ax for all inputs x.

    TWO_COLUMN:
      LEFT  — input plane (x₁, x₂); a moving input dot driven by two
              ValueTrackers x1, x2 sweeps a scan path.
      RIGHT — output plane; image dot lives at A·x = x₁·a₁ + x₂·a₂.
              Persistent yellow trail records every visited image so
              the column-space (= ℝ² when A is full rank) gets covered.

      Below RIGHT — the matrix A and a live equation A·x = (...).
    """

    def construct(self):
        title = Tex(r"Column space: image of $A\,\mathbf{x}$ as $\mathbf{x}$ varies",
                    font_size=30).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # The matrix
        A = np.array([[2.0, -1.0],
                      [1.0,  2.0]])
        a1 = A[:, 0]
        a2 = A[:, 1]

        # LEFT input plane
        plane_in = NumberPlane(
            x_range=[-2.5, 2.5, 1], y_range=[-2.5, 2.5, 1],
            x_length=4.6, y_length=4.6,
            background_line_style={"stroke_opacity": 0.3},
        ).move_to([-3.4, -0.3, 0])
        in_lbl = Tex(r"input $\mathbf{x} \in \mathbb{R}^2$",
                     color=BLUE, font_size=24).next_to(plane_in, UP, buff=0.1)
        self.play(Create(plane_in), Write(in_lbl))

        # RIGHT output plane
        plane_out = NumberPlane(
            x_range=[-5, 5, 1], y_range=[-5, 5, 1],
            x_length=4.6, y_length=4.6,
            background_line_style={"stroke_opacity": 0.3},
        ).move_to([+3.0, -0.3, 0])
        out_lbl = Tex(r"output $A\mathbf{x}$ — col space",
                      color=YELLOW, font_size=24).next_to(plane_out, UP, buff=0.1)
        self.play(Create(plane_out), Write(out_lbl))

        # Persistent column vectors a1, a2 in the output plane
        a1_arrow = Arrow(plane_out.c2p(0, 0), plane_out.c2p(*a1), buff=0,
                         color=GREEN, stroke_width=4,
                         max_tip_length_to_length_ratio=0.15)
        a2_arrow = Arrow(plane_out.c2p(0, 0), plane_out.c2p(*a2), buff=0,
                         color=ORANGE, stroke_width=4,
                         max_tip_length_to_length_ratio=0.15)
        a1_lbl = Tex(r"$\mathbf{a}_1$", color=GREEN, font_size=22).next_to(
            plane_out.c2p(*a1), DR, buff=0.1)
        a2_lbl = Tex(r"$\mathbf{a}_2$", color=ORANGE, font_size=22).next_to(
            plane_out.c2p(*a2), UL, buff=0.1)
        self.play(GrowArrow(a1_arrow), GrowArrow(a2_arrow),
                  Write(a1_lbl), Write(a2_lbl))

        # Trackers for input coords
        x1 = ValueTracker(1.5)
        x2 = ValueTracker(0.7)

        def x_dot():
            return Dot(plane_in.c2p(x1.get_value(), x2.get_value()),
                       color=BLUE, radius=0.10)

        def Ax_dot():
            v = A @ np.array([x1.get_value(), x2.get_value()])
            return Dot(plane_out.c2p(v[0], v[1]),
                       color=YELLOW, radius=0.11)

        def x_arrow():
            return Arrow(plane_in.c2p(0, 0),
                         plane_in.c2p(x1.get_value(), x2.get_value()),
                         buff=0, color=BLUE, stroke_width=4,
                         max_tip_length_to_length_ratio=0.15)

        def Ax_arrow():
            v = A @ np.array([x1.get_value(), x2.get_value()])
            return Arrow(plane_out.c2p(0, 0), plane_out.c2p(v[0], v[1]),
                         buff=0, color=YELLOW, stroke_width=4,
                         max_tip_length_to_length_ratio=0.15)

        self.add(always_redraw(x_arrow), always_redraw(x_dot),
                 always_redraw(Ax_arrow), always_redraw(Ax_dot))

        # Trail of Ax visited
        trail_pts: list[np.ndarray] = []

        def trail():
            path = VMobject(color=YELLOW, stroke_width=2, stroke_opacity=0.5)
            if len(trail_pts) >= 2:
                path.set_points_as_corners(trail_pts.copy())
            else:
                v = A @ np.array([x1.get_value(), x2.get_value()])
                p = plane_out.c2p(v[0], v[1])
                path.set_points_as_corners([p, p])
            return path

        def record_trail(_, dt):
            v = A @ np.array([x1.get_value(), x2.get_value()])
            trail_pts.append(plane_out.c2p(v[0], v[1]))
            if len(trail_pts) > 4000:
                del trail_pts[: len(trail_pts) - 4000]

        recorder = Mobject()
        recorder.add_updater(record_trail)
        self.add(recorder)
        self.add(always_redraw(trail))

        # Bottom: matrix and live A·x equation
        matrix = MathTex(
            r"A = \begin{bmatrix} 2 & -1 \\ 1 & \phantom{-}2 \end{bmatrix}",
            color=WHITE, font_size=28,
        ).move_to([0, -3.2, 0])

        def equation():
            x_v = np.array([x1.get_value(), x2.get_value()])
            v = A @ x_v
            return MathTex(
                rf"A\mathbf{{x}} = ({x_v[0]:+.2f})\mathbf{{a}}_1 + "
                rf"({x_v[1]:+.2f})\mathbf{{a}}_2 = ({v[0]:+.2f}, {v[1]:+.2f})",
                color=YELLOW, font_size=24,
            ).move_to([0, -3.6, 0])

        self.play(Write(matrix))
        self.add(always_redraw(equation))

        # Sweep input through several positions to fan out the column-space cover
        scan = [(2.0, 1.0), (-2.0, 1.0), (-2.0, -1.5), (2.0, -1.5),
                (2.0, 1.5), (1.0, -2.0), (-1.5, 2.0), (0.0, 0.0)]
        for tx, ty in scan:
            self.play(x1.animate.set_value(tx), x2.animate.set_value(ty),
                      run_time=1.4, rate_func=smooth)

        recorder.clear_updaters()

        conclusion = Tex(r"col$(A) = \mathrm{span}(\mathbf{a}_1, \mathbf{a}_2) = \mathbb{R}^2$",
                         color=YELLOW, font_size=28).next_to(matrix, UP, buff=0.15)
        self.play(Write(conclusion))
        self.wait(1.0)
