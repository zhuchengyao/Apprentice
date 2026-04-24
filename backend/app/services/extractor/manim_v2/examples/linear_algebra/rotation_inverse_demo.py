from manim import *
import numpy as np


class RotationInverseDemoExample(Scene):
    """
    The inverse of a 90° counter-clockwise rotation is a 90° clockwise
    rotation. Apply one, then the other, return to identity.
    """

    def construct(self):
        title = Tex(r"Inverse of $90°$ CCW rotation = $90°$ CW rotation",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 4, 1], y_range=[-3, 3, 1],
                            x_length=9, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.1)
        self.play(Create(plane))

        R_ccw = np.array([[0.0, -1.0], [1.0, 0.0]])
        R_cw = np.array([[0.0, 1.0], [-1.0, 0.0]])  # inverse

        stage_tr = ValueTracker(0.0)

        def M_of():
            s = stage_tr.get_value()
            if s <= 1:
                return (1 - s) * np.eye(2) + s * R_ccw
            alpha = s - 1
            return (1 - alpha) * R_ccw + alpha * (R_cw @ R_ccw)  # = I

        def grid():
            M = M_of()
            grp = VGroup()
            for k in range(-3, 4):
                pts_h = [plane.c2p(*(M @ np.array([x, k]))) for x in np.linspace(-4, 4, 15)]
                pts_v = [plane.c2p(*(M @ np.array([k, y]))) for y in np.linspace(-4, 4, 15)]
                grp.add(VMobject().set_points_as_corners(pts_h).set_color(BLUE)
                         .set_stroke(width=1.2, opacity=0.55))
                grp.add(VMobject().set_points_as_corners(pts_v).set_color(ORANGE)
                         .set_stroke(width=1.2, opacity=0.55))
            return grp

        def i_arrow():
            M = M_of()
            p = M @ np.array([1, 0])
            return Arrow(plane.c2p(0, 0), plane.c2p(p[0], p[1]),
                          color=GREEN, buff=0, stroke_width=5)

        def j_arrow():
            M = M_of()
            p = M @ np.array([0, 1])
            return Arrow(plane.c2p(0, 0), plane.c2p(p[0], p[1]),
                          color=RED, buff=0, stroke_width=5)

        self.add(always_redraw(grid), always_redraw(i_arrow), always_redraw(j_arrow))

        def stage_str():
            s = stage_tr.get_value()
            if s < 0.05: return r"identity"
            if s < 1.05: return r"CCW rotation ($90°$)"
            return r"CW rotation inverse: back to identity"

        stage_tex = Tex(stage_str(), color=YELLOW, font_size=24).to_edge(DOWN, buff=0.3)
        self.add(stage_tex)
        def update_stage(mob, dt):
            new = Tex(stage_str(), color=YELLOW, font_size=24).move_to(stage_tex)
            stage_tex.become(new)
            return stage_tex
        stage_tex.add_updater(update_stage)

        info = VGroup(
            Tex(r"$R=\begin{pmatrix}0&-1\\1&0\end{pmatrix}$",
                color=BLUE, font_size=22),
            Tex(r"$R^{-1}=\begin{pmatrix}0&1\\-1&0\end{pmatrix}$",
                color=GREEN, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.3)
        self.add(info)

        self.play(stage_tr.animate.set_value(1.0), run_time=2.5, rate_func=smooth)
        self.wait(0.5)
        self.play(stage_tr.animate.set_value(2.0), run_time=2.5, rate_func=smooth)
        self.wait(0.8)
