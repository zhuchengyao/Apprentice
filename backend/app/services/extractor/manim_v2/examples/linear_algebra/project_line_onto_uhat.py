from manim import *
import numpy as np


class ProjectLineOntoUhatExample(Scene):
    """
    Project a line of evenly-spaced dots onto a unit vector û. The
    dots land on a 1D number line aligned with û, evenly spaced
    (linear projection).
    """

    def construct(self):
        title = Tex(r"Project line of dots onto unit vector $\hat u$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 4, 1], y_range=[-2.5, 2.5, 1],
                            x_length=9, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.1)
        self.play(Create(plane))

        # Unit vector û
        u_angle = 25 * DEGREES
        u_hat = np.array([np.cos(u_angle), np.sin(u_angle)])
        u_arrow = Arrow(plane.c2p(0, 0), plane.c2p(u_hat[0], u_hat[1]),
                         color=YELLOW, buff=0, stroke_width=5)
        u_lbl = Tex(r"$\hat u$", color=YELLOW, font_size=24).next_to(u_arrow.get_end(), UP, buff=0.05)
        self.add(u_arrow, u_lbl)

        # û-line extending through origin
        u_line_ext = Line(plane.c2p(-4 * u_hat[0], -4 * u_hat[1]),
                           plane.c2p(4 * u_hat[0], 4 * u_hat[1]),
                           color=YELLOW, stroke_width=2, stroke_opacity=0.6)
        self.add(u_line_ext)

        # Input dots on vertical line x=1
        input_dots = []
        colors = []
        for y, col in [(-1.5, BLUE), (-0.75, GREEN), (0, ORANGE),
                       (0.75, RED), (1.5, PURPLE)]:
            p = np.array([1.0, y])
            input_dots.append(p)
            colors.append(col)
            self.add(Dot(plane.c2p(p[0], p[1]), color=col, radius=0.12))

        # Connect them with a line
        line_in = Line(plane.c2p(1, -1.5), plane.c2p(1, 1.5),
                        color=GREY_B, stroke_width=2, stroke_opacity=0.5)
        self.add(line_in)

        self.wait(0.5)

        # Animate projection
        t_tr = ValueTracker(0.0)

        def projected_dots():
            t = t_tr.get_value()
            grp = VGroup()
            for p, col in zip(input_dots, colors):
                proj = np.dot(p, u_hat) * u_hat
                pos = (1 - t) * plane.c2p(p[0], p[1]) + t * plane.c2p(proj[0], proj[1])
                grp.add(Dot(pos, color=col, radius=0.12))
            return grp

        def drop_lines():
            t = t_tr.get_value()
            grp = VGroup()
            for p, col in zip(input_dots, colors):
                proj = np.dot(p, u_hat) * u_hat
                start = plane.c2p(p[0], p[1])
                pos_now = (1 - t) * start + t * plane.c2p(proj[0], proj[1])
                grp.add(DashedLine(start, pos_now, color=col,
                                    stroke_width=1.5, stroke_opacity=0.6))
            return grp

        self.add(always_redraw(drop_lines), always_redraw(projected_dots))

        self.play(t_tr.animate.set_value(1.0), run_time=3, rate_func=smooth)
        self.wait(0.5)

        note = Tex(r"evenly-spaced dots $\to$ evenly-spaced projections",
                    color=GREEN, font_size=24).to_edge(DOWN, buff=0.3)
        self.play(Write(note))
        self.wait(1.0)
