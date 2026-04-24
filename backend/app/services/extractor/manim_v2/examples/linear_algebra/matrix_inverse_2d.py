from manim import *
import numpy as np


class MatrixInverse2DExample(Scene):
    """
    2×2 matrix inverse: A^(-1) = (1/det A) · [[d, -b], [-c, a]].
    Visualize with unit square under A then A^(-1), recovering unit.

    SINGLE_FOCUS:
      NumberPlane with unit square outline; ValueTracker s_tr
      advances: s ∈ [0, 1] applies A, s ∈ [1, 2] applies A^(-1),
      landing back at unit square.
    """

    def construct(self):
        title = Tex(r"$A \cdot A^{-1} = I$: apply $A$ then $A^{-1}$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-3, 3, 1], y_range=[-3, 3, 1],
                             x_length=6, y_length=6,
                             background_line_style={"stroke_opacity": 0.25}
                             ).move_to([-2, -0.3, 0])
        self.play(Create(plane))

        A = np.array([[1.5, 0.8], [0.3, 1.2]])
        A_inv = np.linalg.inv(A)

        s_tr = ValueTracker(0.0)

        def square_transform():
            s = s_tr.get_value()
            # s ∈ [0, 1]: apply A via (1-s)·I + s·A
            # s ∈ [1, 2]: apply A^(-1) on top: start from A, go to I
            if s <= 1:
                M = (1 - s) * np.eye(2) + s * A
            else:
                # At s=1, we're at A. Then A_inv * A = I, so
                # interpolate between A and A_inv @ A = I
                t = s - 1
                # Actually we want the composition to end at I:
                # Step 2 is multiplication by A_inv on LEFT, so
                # M(s) = (A_inv @ A when s=2, A when s=1). That's
                # just M = ((1-t) A + t I).
                M = (1 - t) * A + t * np.eye(2)
            unit_corners = [np.array([0, 0]), np.array([1, 0]),
                            np.array([1, 1]), np.array([0, 1])]
            transformed = [M @ c for c in unit_corners]
            scene_pts = [plane.c2p(p[0], p[1]) for p in transformed]
            return Polygon(*scene_pts, color=YELLOW,
                             fill_opacity=0.3, stroke_width=3)

        # Unit square reference
        unit_sq = Polygon(plane.c2p(0, 0), plane.c2p(1, 0),
                            plane.c2p(1, 1), plane.c2p(0, 1),
                            color=GREY_B, stroke_width=1.5,
                            fill_opacity=0, stroke_opacity=0.5)
        self.add(unit_sq)

        self.add(always_redraw(square_transform))

        def info():
            s = s_tr.get_value()
            if s <= 1:
                phase = "applying A"
                col = BLUE
            else:
                phase = "applying A^{-1}"
                col = GREEN
            return VGroup(
                MathTex(rf"s = {s:.2f}", color=YELLOW, font_size=24),
                Tex(phase, color=col, font_size=22),
                MathTex(r"A = \begin{pmatrix} 1.5 & 0.8 \\ 0.3 & 1.2 \end{pmatrix}",
                         color=BLUE, font_size=20),
                MathTex(r"A^{-1} \approx \begin{pmatrix} 0.86 & -0.57 \\ -0.21 & 1.07 \end{pmatrix}",
                         color=GREEN, font_size=18),
                MathTex(rf"\det A = {np.linalg.det(A):.3f}",
                         color=WHITE, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        self.play(s_tr.animate.set_value(1.0),
                   run_time=2.5, rate_func=smooth)
        self.wait(0.5)
        self.play(s_tr.animate.set_value(2.0),
                   run_time=2.5, rate_func=smooth)
        self.wait(0.5)
