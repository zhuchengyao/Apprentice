from manim import *
import numpy as np


class ProjectionEqualsDotProductExample(Scene):
    """
    For unit vector û, projecting v onto û has length equal to v·û.
    More generally: projection onto any vector w has length v·w/|w|.

    This is the duality: geometric projection ≡ dot product with
    a 1×2 matrix derived from û (or w).
    """

    def construct(self):
        title = Tex(r"Projection length onto $\hat u$ $=$ $\vec v\cdot\hat u$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-3, 3, 1], y_range=[-2, 2, 1],
                            x_length=7, y_length=5.0,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(LEFT * 2.3 + DOWN * 0.2)
        self.play(Create(plane))

        u_angle_tr = ValueTracker(30 * DEGREES)
        v = np.array([2.5, 1.2])

        def u_hat():
            return np.array([np.cos(u_angle_tr.get_value()),
                              np.sin(u_angle_tr.get_value())])

        v_arrow = Arrow(plane.c2p(0, 0), plane.c2p(v[0], v[1]),
                         color=BLUE, buff=0, stroke_width=5)
        v_lbl = Tex(r"$\vec v$", color=BLUE, font_size=24).next_to(v_arrow.get_end(), UR, buff=0.05)
        self.add(v_arrow, v_lbl)

        def u_arrow():
            u = u_hat()
            return Arrow(plane.c2p(0, 0), plane.c2p(u[0] * 1.5, u[1] * 1.5),
                          color=YELLOW, buff=0, stroke_width=5)

        def u_line():
            u = u_hat()
            return Line(plane.c2p(-3 * u[0], -3 * u[1]),
                         plane.c2p(3 * u[0], 3 * u[1]),
                         color=YELLOW, stroke_width=2, stroke_opacity=0.6)

        def proj_arrow():
            u = u_hat()
            proj = np.dot(v, u) * u
            return Arrow(plane.c2p(0, 0), plane.c2p(proj[0], proj[1]),
                          color=PINK, buff=0, stroke_width=4)

        def drop_line():
            u = u_hat()
            proj = np.dot(v, u) * u
            return DashedLine(plane.c2p(v[0], v[1]),
                               plane.c2p(proj[0], proj[1]),
                               color=GREY_B, stroke_width=2)

        self.add(always_redraw(u_arrow), always_redraw(u_line),
                 always_redraw(proj_arrow), always_redraw(drop_line))

        # Right: symbolic equality
        info = VGroup(
            Tex(r"projection length:", font_size=22),
            VGroup(MathTex(r"|\text{proj}_{\hat u}\vec v| = ", font_size=28, color=PINK),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=28).set_color(PINK)).arrange(RIGHT, buff=0.1),
            Tex(r"dot product:", font_size=22),
            VGroup(MathTex(r"\vec v\cdot\hat u = ", font_size=28, color=GREEN),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=28).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"\textbf{equal}",
                color=YELLOW, font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.3)

        def proj_len():
            return float(np.dot(v, u_hat()))

        info[1][1].add_updater(lambda m: m.set_value(proj_len()))
        info[3][1].add_updater(lambda m: m.set_value(proj_len()))
        self.add(info)

        for target in [PI / 4, PI / 3, 5 * PI / 12, PI / 6, PI / 5]:
            self.play(u_angle_tr.animate.set_value(target),
                      run_time=1.5, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.5)
