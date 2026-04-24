from manim import *
import numpy as np


class AxEqualsVFindXExample(Scene):
    """
    Given A and target v, find x such that Ax = v. Visualized:
    start with v YELLOW, apply inverse of A (i.e. play transformation
    in reverse), and the image is x.
    """

    def construct(self):
        title = Tex(r"Find $\vec x$ so that $A\vec x=\vec v$ (play in reverse)",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 4, 1], y_range=[-3, 3, 1],
                            x_length=9, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.1)
        self.play(Create(plane))

        A = np.array([[2.0, 1.0], [2.0, 3.0]])
        v = np.array([-4.0, -1.0])
        x_sol = np.linalg.solve(A, v)  # x such that Ax = v

        # Show A applied first (forward)
        stage_tr = ValueTracker(0.0)

        def M_of():
            s = stage_tr.get_value()
            if s <= 1:
                return (1 - s) * np.eye(2) + s * A
            alpha = s - 1
            return (1 - alpha) * A + alpha * np.eye(2)

        def grid_lines():
            M = M_of()
            grp = VGroup()
            for k in range(-3, 4):
                pts_h = [plane.c2p(*(M @ np.array([x, k]))) for x in np.linspace(-4, 4, 20)]
                pts_v = [plane.c2p(*(M @ np.array([k, y]))) for y in np.linspace(-4, 4, 20)]
                grp.add(VMobject().set_points_as_corners(pts_h).set_color(BLUE)
                         .set_stroke(width=1.2, opacity=0.55))
                grp.add(VMobject().set_points_as_corners(pts_v).set_color(ORANGE)
                         .set_stroke(width=1.2, opacity=0.55))
            return grp

        self.add(always_redraw(grid_lines))

        # YELLOW v arrow stays fixed in world
        v_arrow = Arrow(plane.c2p(0, 0), plane.c2p(v[0], v[1]),
                         color=YELLOW, buff=0, stroke_width=6)
        v_lbl = Tex(r"$\vec v=(-4,-1)$", color=YELLOW,
                     font_size=22).next_to(v_arrow.get_end(), DR, buff=0.1)
        self.add(v_arrow, v_lbl)

        # During reverse (stage 1→2), v's "pre-image" approaches x.
        # In world coordinates: if apply inverse, v is at v fixed; but the "source x"
        # in the original grid is at x_sol after reverse-mapping.

        # Mark x_sol as PINK dot when reached
        x_dot = Dot(plane.c2p(x_sol[0], x_sol[1]), color=PINK, radius=0.13)
        x_lbl = Tex(rf"$\vec x=({x_sol[0]:+.2f}, {x_sol[1]:+.2f})$", color=PINK,
                     font_size=22).next_to(x_dot, UL, buff=0.1)

        self.play(stage_tr.animate.set_value(1.0), run_time=2.5, rate_func=smooth)
        self.wait(0.4)
        self.play(Write(Tex(r"now play in reverse...", color=GREEN,
                             font_size=22).to_edge(DOWN, buff=0.4)))
        self.play(stage_tr.animate.set_value(2.0), run_time=2.5, rate_func=smooth)
        self.wait(0.3)
        self.play(FadeIn(x_dot), Write(x_lbl))
        self.wait(1.0)
