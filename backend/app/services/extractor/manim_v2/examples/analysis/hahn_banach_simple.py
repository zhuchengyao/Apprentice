from manim import *
import numpy as np


class HahnBanachSimpleExample(Scene):
    """
    Hahn-Banach (geometric form): in ℝ², a closed convex set can be
    separated from an external point by a hyperplane (line).

    SINGLE_FOCUS:
      Convex set (ellipse) + external point; ValueTracker t_tr moves
      the point on a trajectory; always_redraw separating line that
      is perpendicular to (point - closest on set).
    """

    def construct(self):
        title = Tex(r"Hahn-Banach: separate convex set from external point",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-5, 5, 1], y_range=[-3, 3, 1],
                             x_length=9, y_length=5.5,
                             background_line_style={"stroke_opacity": 0.3}
                             ).move_to([0, -0.3, 0])
        self.play(Create(plane))

        # Convex set: ellipse centered at origin, semi-axes (2, 1)
        ellipse_pts = [plane.c2p(2 * np.cos(t), np.sin(t))
                        for t in np.linspace(0, 2 * PI, 80)]
        ellipse_mob = VMobject(color=BLUE, fill_opacity=0.3,
                                 stroke_width=3)
        ellipse_mob.set_points_as_corners(ellipse_pts + [ellipse_pts[0]])
        self.play(Create(ellipse_mob))

        t_tr = ValueTracker(0.0)

        def external_point():
            t = t_tr.get_value()
            # Circular path at radius 3.5
            x = 3.5 * np.cos(t)
            y = 3.5 * np.sin(t)
            return np.array([x, y])

        def closest_on_ellipse(P):
            # Brute force over boundary
            best = None
            best_d = 1e9
            for s in np.linspace(0, 2 * PI, 200):
                q = np.array([2 * np.cos(s), np.sin(s)])
                d = np.linalg.norm(P - q)
                if d < best_d:
                    best_d = d
                    best = q
            return best

        def point_dot():
            P = external_point()
            return Dot(plane.c2p(P[0], P[1]), color=RED, radius=0.12)

        def separating_line():
            P = external_point()
            Q = closest_on_ellipse(P)
            # Separator line: passes through (P + Q)/2, perpendicular to P - Q
            mid = (P + Q) / 2
            diff = P - Q
            perp = np.array([-diff[1], diff[0]])
            perp = perp / (np.linalg.norm(perp) + 1e-8) * 4
            start = plane.c2p(mid[0] - perp[0], mid[1] - perp[1])
            end = plane.c2p(mid[0] + perp[0], mid[1] + perp[1])
            return Line(start, end, color=YELLOW, stroke_width=3)

        def perpendicular_seg():
            P = external_point()
            Q = closest_on_ellipse(P)
            return DashedLine(plane.c2p(Q[0], Q[1]),
                                plane.c2p(P[0], P[1]),
                                color=GREEN, stroke_width=2)

        def closest_pt_dot():
            P = external_point()
            Q = closest_on_ellipse(P)
            return Dot(plane.c2p(Q[0], Q[1]),
                        color=GREEN, radius=0.1)

        self.add(always_redraw(separating_line),
                  always_redraw(perpendicular_seg),
                  always_redraw(closest_pt_dot),
                  always_redraw(point_dot))

        info = VGroup(
            Tex(r"BLUE: convex set", color=BLUE, font_size=20),
            Tex(r"RED: external point", color=RED, font_size=20),
            Tex(r"YELLOW: separating line",
                 color=YELLOW, font_size=20),
            Tex(r"GREEN: closest boundary point",
                 color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.13).to_edge(DOWN, buff=0.25)
        self.play(Write(info))

        self.play(t_tr.animate.set_value(2 * PI),
                   run_time=8, rate_func=linear)
        self.wait(0.4)
