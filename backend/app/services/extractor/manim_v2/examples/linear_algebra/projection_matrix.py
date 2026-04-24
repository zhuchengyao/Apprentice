from manim import *
import numpy as np


class ProjectionMatrixExample(Scene):
    """
    Projection onto a line: for unit vector u, P = u u^T projects
    any v onto span(u). P² = P (idempotent), P has eigenvalues 0 and 1.

    SINGLE_FOCUS:
      2D plane with line span(u) as AXIS; ValueTracker theta_tr
      rotates u; for a test vector v, always_redraw projection
      Pv = (v·u) u.
    """

    def construct(self):
        title = Tex(r"Projection onto line: $P = uu^\top$, $Pv = (v\cdot u)\,u$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-3, 3, 1], y_range=[-2.5, 2.5, 1],
                             x_length=8, y_length=6,
                             background_line_style={"stroke_opacity": 0.3}
                             ).move_to([-1, -0.3, 0])
        self.play(Create(plane))

        theta_tr = ValueTracker(PI / 6)
        v = np.array([2.0, 1.3])

        def u_axis():
            t = theta_tr.get_value()
            u = np.array([np.cos(t), np.sin(t)])
            lim = 3
            return Line(plane.c2p(-lim * u[0], -lim * u[1]),
                          plane.c2p(lim * u[0], lim * u[1]),
                          color=BLUE, stroke_width=2.5)

        def v_arrow():
            return Arrow(plane.c2p(0, 0), plane.c2p(v[0], v[1]),
                          color=YELLOW, buff=0, stroke_width=5,
                          max_tip_length_to_length_ratio=0.15)

        def projection():
            t = theta_tr.get_value()
            u = np.array([np.cos(t), np.sin(t)])
            proj = np.dot(v, u) * u
            return Arrow(plane.c2p(0, 0), plane.c2p(proj[0], proj[1]),
                          color=ORANGE, buff=0, stroke_width=5,
                          max_tip_length_to_length_ratio=0.18)

        def drop_segment():
            t = theta_tr.get_value()
            u = np.array([np.cos(t), np.sin(t)])
            proj = np.dot(v, u) * u
            return DashedLine(plane.c2p(v[0], v[1]),
                                plane.c2p(proj[0], proj[1]),
                                color=GREY_B, stroke_width=2)

        self.add(always_redraw(u_axis),
                  always_redraw(drop_segment),
                  always_redraw(v_arrow),
                  always_redraw(projection))

        v_lbl = MathTex(r"v", color=YELLOW, font_size=22
                          ).next_to(plane.c2p(v[0], v[1]), UR, buff=0.05)
        self.play(Write(v_lbl))

        def info():
            t = theta_tr.get_value()
            u = np.array([np.cos(t), np.sin(t)])
            proj = np.dot(v, u) * u
            # P = u u^T as matrix
            P = np.outer(u, u)
            P_sq = P @ P
            err = np.linalg.norm(P - P_sq)
            return VGroup(
                MathTex(rf"u = ({u[0]:+.2f}, {u[1]:+.2f})",
                         color=BLUE, font_size=22),
                MathTex(rf"Pv = ({proj[0]:+.2f}, {proj[1]:+.2f})",
                         color=ORANGE, font_size=22),
                MathTex(r"P = uu^\top", color=BLUE, font_size=20),
                MathTex(rf"\|P^2 - P\| = {err:.2e}",
                         color=GREEN, font_size=20),
                MathTex(r"\text{idempotent: } P^2 = P",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for deg in [60, 130, 10, 90]:
            self.play(theta_tr.animate.set_value(deg * DEGREES),
                       run_time=1.5, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
