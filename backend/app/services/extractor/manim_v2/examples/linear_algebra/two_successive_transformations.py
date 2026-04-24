from manim import *
import numpy as np


class TwoSuccessiveTransformationsExample(Scene):
    """
    Apply one linear transformation A, then another B, on a grid.
    The net effect is the composition B∘A, a single linear transform.

    SINGLE_FOCUS: NumberPlane with colored grid that gets deformed by
    A=[[2, 1], [1, 2]] then B=[[-1, 0], [-0.5, -0.5]].
    ValueTracker stage_tr ∈ [0, 2]: 0=original, 1=after A, 2=after B.
    """

    def construct(self):
        title = Tex(r"Two successive linear transformations",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane_center = DOWN * 0.1
        unit_scale = 0.7

        A = np.array([[2.0, 1.0], [1.0, 2.0]])
        B = np.array([[-1.0, 0.0], [-0.5, -0.5]])

        stage_tr = ValueTracker(0.0)

        def M_of():
            s = stage_tr.get_value()
            if s <= 1:
                return (1 - s) * np.eye(2) + s * A
            alpha = s - 1
            return (1 - alpha) * A + alpha * (B @ A)

        # Draw a grid of colored segments (horizontal + vertical lines)
        def transformed_grid():
            M = M_of()
            grp = VGroup()
            # Horizontal lines
            for y0 in range(-3, 4):
                pts = []
                for x in np.linspace(-4, 4, 20):
                    v = M @ np.array([x, y0])
                    pts.append(np.array([v[0] * unit_scale, v[1] * unit_scale, 0]) + plane_center)
                col = interpolate_color(BLUE, GREEN, (y0 + 3) / 6)
                grp.add(VMobject().set_points_as_corners(pts)
                         .set_color(col).set_stroke(width=2, opacity=0.7))
            # Vertical lines
            for x0 in range(-4, 5):
                pts = []
                for y in np.linspace(-3, 3, 15):
                    v = M @ np.array([x0, y])
                    pts.append(np.array([v[0] * unit_scale, v[1] * unit_scale, 0]) + plane_center)
                col = interpolate_color(ORANGE, RED, (x0 + 4) / 8)
                grp.add(VMobject().set_points_as_corners(pts)
                         .set_color(col).set_stroke(width=2, opacity=0.7))
            return grp

        def i_arrow():
            M = M_of()
            i = M @ np.array([1, 0])
            return Arrow(plane_center, np.array([i[0] * unit_scale, i[1] * unit_scale, 0]) + plane_center,
                          color=GREEN, buff=0, stroke_width=5)

        def j_arrow():
            M = M_of()
            j = M @ np.array([0, 1])
            return Arrow(plane_center, np.array([j[0] * unit_scale, j[1] * unit_scale, 0]) + plane_center,
                          color=RED, buff=0, stroke_width=5)

        self.add(always_redraw(transformed_grid),
                 always_redraw(i_arrow), always_redraw(j_arrow))

        # Stage label
        def stage_str():
            s = stage_tr.get_value()
            if s < 0.05: return r"start: identity"
            if s < 0.95: return r"applying $A$"
            if s < 1.05: return r"after $A$"
            if s < 1.95: return r"applying $B$"
            return r"after $B\!\circ\!A$"

        stage_tex = Tex(stage_str(), color=YELLOW, font_size=26).to_edge(DOWN, buff=0.4)
        self.add(stage_tex)
        def update_stage(mob, dt):
            new = Tex(stage_str(), color=YELLOW, font_size=26).move_to(stage_tex)
            stage_tex.become(new)
            return stage_tex
        stage_tex.add_updater(update_stage)

        info = VGroup(
            Tex(r"$A=\begin{pmatrix}2&1\\1&2\end{pmatrix}$",
                font_size=22),
            Tex(r"$B=\begin{pmatrix}-1&0\\-0.5&-0.5\end{pmatrix}$",
                font_size=22),
            VGroup(Tex(r"$t=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22).set_color(YELLOW)
                   ).arrange(RIGHT, buff=0.1),
            Tex(r"net: $B\circ A$",
                color=YELLOW, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.3)
        info[2][1].add_updater(lambda m: m.set_value(stage_tr.get_value()))
        self.add(info)

        self.play(stage_tr.animate.set_value(1.0), run_time=2.5, rate_func=smooth)
        self.wait(0.5)
        self.play(stage_tr.animate.set_value(2.0), run_time=2.5, rate_func=smooth)
        self.wait(0.8)
