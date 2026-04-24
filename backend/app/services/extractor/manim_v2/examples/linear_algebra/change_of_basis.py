from manim import *
import numpy as np


class ChangeOfBasisExample(Scene):
    """
    Change of basis: same point, different coordinates.

    The screen has two synchronized representations of the same vector v:
      LEFT  — standard basis grid; v = 3·e1 + 2·e2 drawn as parallelogram rule.
      RIGHT — new basis grid (b1=(2,1), b2=(-1,1)); v = (5/3)·b1 + (1/3)·b2.

    A ValueTracker s slides 0→1 to morph the SHARED grid from standard to
    new basis (always_redraw NumberPlane). The yellow point v stays
    pinned in absolute screen position the whole time — it's the same
    physical point in space; only the coordinate ruler underneath
    changes. Live coordinate readouts on the right update accordingly.
    """

    def construct(self):
        title = Text("Change of basis: same vector, different coordinates",
                     font_size=24).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # The two basis-vector pairs, in absolute world coords.
        std_b1 = np.array([1.0, 0.0])
        std_b2 = np.array([0.0, 1.0])
        new_b1 = np.array([2.0, 1.0])
        new_b2 = np.array([-1.0, 1.0])

        # The fixed point v in absolute world coords.
        v_world = np.array([3.0, 2.0])

        s = ValueTracker(0.0)

        # Build a NumberPlane that always_redraws to show the morphing basis.
        # We approximate this by drawing the basis-vector arrows + a sparse
        # colored grid that interpolates between standard and new.
        plane_anchor = np.array([-1.0, -0.4, 0])
        unit = 1.0  # 1 abstract basis-unit = 1 manim screen unit (so v sits at (3, 2) on screen)

        def basis_pair(s_val: float) -> tuple[np.ndarray, np.ndarray]:
            b1 = (1 - s_val) * std_b1 + s_val * new_b1
            b2 = (1 - s_val) * std_b2 + s_val * new_b2
            return b1, b2

        # The interpolated coordinate grid: for each (i, j) in [-3..3]², draw a dot at i·b1 + j·b2
        def grid_dots():
            b1, b2 = basis_pair(s.get_value())
            dots = VGroup()
            for i in range(-2, 5):
                for j in range(-2, 5):
                    p = i * b1 + j * b2
                    if abs(p[0]) > 6.5 or abs(p[1]) > 3.0:
                        continue
                    dots.add(Dot([p[0] + plane_anchor[0], p[1] + plane_anchor[1], 0],
                                 color=GREY_B, radius=0.04))
            return dots

        def grid_lines():
            b1, b2 = basis_pair(s.get_value())
            lines = VGroup()
            for j in range(-2, 5):
                # Lines along b1 direction at integer multiples of b2
                pts = []
                for i in range(-3, 6):
                    p = i * b1 + j * b2
                    pts.append([p[0] + plane_anchor[0], p[1] + plane_anchor[1], 0])
                line = VMobject(stroke_color=GREEN_E, stroke_width=1, stroke_opacity=0.4)
                line.set_points_as_corners(pts)
                lines.add(line)
            for i in range(-2, 5):
                pts = []
                for j in range(-3, 6):
                    p = i * b1 + j * b2
                    pts.append([p[0] + plane_anchor[0], p[1] + plane_anchor[1], 0])
                line = VMobject(stroke_color=RED_E, stroke_width=1, stroke_opacity=0.4)
                line.set_points_as_corners(pts)
                lines.add(line)
            return lines

        def b1_arrow():
            b1, _ = basis_pair(s.get_value())
            return Arrow([plane_anchor[0], plane_anchor[1], 0],
                         [b1[0] + plane_anchor[0], b1[1] + plane_anchor[1], 0],
                         buff=0, color=GREEN, stroke_width=5,
                         max_tip_length_to_length_ratio=0.18)

        def b2_arrow():
            _, b2 = basis_pair(s.get_value())
            return Arrow([plane_anchor[0], plane_anchor[1], 0],
                         [b2[0] + plane_anchor[0], b2[1] + plane_anchor[1], 0],
                         buff=0, color=RED, stroke_width=5,
                         max_tip_length_to_length_ratio=0.18)

        def b1_lbl():
            b1, _ = basis_pair(s.get_value())
            return MathTex(r"\vec b_1", color=GREEN, font_size=24).next_to(
                [b1[0] + plane_anchor[0], b1[1] + plane_anchor[1], 0], DR, buff=0.1)

        def b2_lbl():
            _, b2 = basis_pair(s.get_value())
            return MathTex(r"\vec b_2", color=RED, font_size=24).next_to(
                [b2[0] + plane_anchor[0], b2[1] + plane_anchor[1], 0], UL, buff=0.1)

        # The fixed point v stays at v_world (in screen coords offset by anchor)
        v_screen = [v_world[0] + plane_anchor[0], v_world[1] + plane_anchor[1], 0]
        v_dot = Dot(v_screen, color=YELLOW, radius=0.13)
        v_dot_lbl = MathTex(r"\vec v", color=YELLOW, font_size=28).next_to(v_dot, UR, buff=0.1)

        self.add(always_redraw(grid_lines), always_redraw(grid_dots))
        self.play(GrowArrow(b1_arrow()), GrowArrow(b2_arrow()))
        self.add(always_redraw(b1_arrow), always_redraw(b2_arrow),
                 always_redraw(b1_lbl), always_redraw(b2_lbl))
        self.play(FadeIn(v_dot), Write(v_dot_lbl))

        # RIGHT COLUMN: coordinate readouts that recompute from the current basis
        rcol_x = +5.2

        def coord_panel():
            s_val = s.get_value()
            b1, b2 = basis_pair(s_val)
            # Solve [b1 b2] [c1; c2] = v_world
            M = np.column_stack([b1, b2])
            try:
                coords = np.linalg.solve(M, v_world)
            except np.linalg.LinAlgError:
                coords = np.array([np.nan, np.nan])
            return VGroup(
                MathTex(rf"\vec b_1 = ({b1[0]:+.2f}, {b1[1]:+.2f})",
                        color=GREEN, font_size=22),
                MathTex(rf"\vec b_2 = ({b2[0]:+.2f}, {b2[1]:+.2f})",
                        color=RED, font_size=22),
                MathTex(rf"\vec v = {coords[0]:+.2f}\,\vec b_1 + {coords[1]:+.2f}\,\vec b_2",
                        color=YELLOW, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([rcol_x, +1.0, 0])

        self.add(always_redraw(coord_panel))

        # First settle on standard basis, then morph to new basis, then back
        self.wait(0.4)
        self.play(s.animate.set_value(1.0), run_time=4, rate_func=smooth)
        self.wait(0.6)
        self.play(s.animate.set_value(0.0), run_time=2.5, rate_func=smooth)
        self.wait(0.5)

        conclusion = MathTex(
            r"v = \begin{bmatrix}3\\2\end{bmatrix}_{e}"
            r" = \tfrac{5}{3}\,\vec b_1 + \tfrac{1}{3}\,\vec b_2",
            font_size=26, color=YELLOW,
        ).move_to([rcol_x, -2.6, 0])
        self.play(Write(conclusion))
        self.wait(1.0)
