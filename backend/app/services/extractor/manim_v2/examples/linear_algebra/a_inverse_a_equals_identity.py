from manim import *
import numpy as np


class AInverseAEqualsIdentityExample(Scene):
    """
    A^(-1) A = I: apply A, then apply A^(-1); the plane returns to
    identity. Formula A^(-1) A = I emphasizes 'do-nothing matrix'.
    """

    def construct(self):
        title = Tex(r"$A^{-1}A = I$: the ``do nothing'' matrix",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 4, 1], y_range=[-3, 3, 1],
                            x_length=8, y_length=5,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(LEFT * 2.3 + DOWN * 0.3)
        self.play(Create(plane))

        A = np.array([[1.5, 0.8], [0.5, 1.5]])
        A_inv = np.linalg.inv(A)

        stage_tr = ValueTracker(0.0)

        def M_of():
            s = stage_tr.get_value()
            if s <= 1:
                return (1 - s) * np.eye(2) + s * A
            alpha = s - 1
            return (1 - alpha) * A + alpha * np.eye(2)

        def grid():
            M = M_of()
            grp = VGroup()
            for k in range(-3, 4):
                pts_h = [plane.c2p(*(M @ np.array([x, k]))) for x in np.linspace(-4, 4, 15)]
                pts_v = [plane.c2p(*(M @ np.array([k, y]))) for y in np.linspace(-4, 4, 15)]
                grp.add(VMobject().set_points_as_corners(pts_h).set_color(BLUE)
                         .set_stroke(width=1.3, opacity=0.6))
                grp.add(VMobject().set_points_as_corners(pts_v).set_color(ORANGE)
                         .set_stroke(width=1.3, opacity=0.6))
            return grp

        def i_arrow():
            M = M_of()
            p = M @ np.array([1, 0])
            return Arrow(plane.c2p(0, 0), plane.c2p(p[0], p[1]),
                          color=GREEN, buff=0, stroke_width=4)

        def j_arrow():
            M = M_of()
            p = M @ np.array([0, 1])
            return Arrow(plane.c2p(0, 0), plane.c2p(p[0], p[1]),
                          color=RED, buff=0, stroke_width=4)

        self.add(always_redraw(grid), always_redraw(i_arrow), always_redraw(j_arrow))

        # Right: symbolic equation
        info = VGroup(
            Tex(r"$A$", color=PINK, font_size=36),
            Tex(r"$\cdot A^{-1}$", color=GREEN, font_size=32),
            Tex(r"$= I$", color=YELLOW, font_size=36),
        ).arrange(RIGHT, buff=0.15).shift(RIGHT * 3.0 + UP * 1.0)
        self.add(info)

        def stage_str():
            s = stage_tr.get_value()
            if s < 0.05: return r"identity"
            if s < 1.05: return r"after $A$ (transformed)"
            return r"after $A^{-1} A$: identity restored"

        stage_tex = Tex(stage_str(), color=YELLOW, font_size=22).to_edge(DOWN, buff=0.3)
        self.add(stage_tex)
        def update_stage(mob, dt):
            new = Tex(stage_str(), color=YELLOW, font_size=22).move_to(stage_tex)
            stage_tex.become(new)
            return stage_tex
        stage_tex.add_updater(update_stage)

        identity_matrix = MathTex(r"I = \begin{pmatrix}1&0\\0&1\end{pmatrix}",
                                    color=YELLOW, font_size=28).shift(RIGHT * 3.0 + DOWN * 0.8)
        self.add(identity_matrix)

        self.play(stage_tr.animate.set_value(1.0), run_time=2.5, rate_func=smooth)
        self.wait(0.5)
        self.play(stage_tr.animate.set_value(2.0), run_time=2.5, rate_func=smooth)
        self.wait(0.8)
