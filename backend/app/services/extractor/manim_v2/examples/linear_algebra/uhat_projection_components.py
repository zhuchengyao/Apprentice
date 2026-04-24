from manim import *
import numpy as np


class UhatProjectionComponentsExample(Scene):
    """
    Projecting î and ĵ onto unit vector û gives û's components
    (û_x, û_y) directly. This is why the projection-onto-û map has
    matrix [û_x û_y] — the "columns" of the 2→1 map are where the
    basis vectors land, and those are û's components.
    """

    def construct(self):
        title = Tex(r"Projecting $\hat\imath,\hat\jmath$ onto $\hat u$ gives $\hat u$'s components",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-2, 2, 1], y_range=[-1, 2, 1],
                            x_length=6, y_length=5,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(LEFT * 2.0 + DOWN * 0.3)
        self.play(Create(plane))

        u_angle = 35 * DEGREES
        u_hat = np.array([np.cos(u_angle), np.sin(u_angle)])
        u_x, u_y = u_hat[0], u_hat[1]

        # û
        u_arrow = Arrow(plane.c2p(0, 0), plane.c2p(u_hat[0] * 1.6, u_hat[1] * 1.6),
                         color=YELLOW, buff=0, stroke_width=5)
        u_lbl = Tex(rf"$\hat u$", color=YELLOW, font_size=24).next_to(u_arrow.get_end(), UP, buff=0.05)
        self.add(u_arrow, u_lbl)

        # û-line
        u_line = Line(plane.c2p(-2 * u_hat[0], -2 * u_hat[1]),
                       plane.c2p(2 * u_hat[0], 2 * u_hat[1]),
                       color=YELLOW, stroke_width=2, stroke_opacity=0.6)
        self.add(u_line)

        # î and ĵ
        i_arrow = Arrow(plane.c2p(0, 0), plane.c2p(1, 0),
                         color=GREEN, buff=0, stroke_width=5)
        j_arrow = Arrow(plane.c2p(0, 0), plane.c2p(0, 1),
                         color=RED, buff=0, stroke_width=5)
        self.add(i_arrow, j_arrow)
        self.add(Tex(r"$\hat\imath$", color=GREEN, font_size=22).next_to(i_arrow.get_end(), DR, buff=0.05))
        self.add(Tex(r"$\hat\jmath$", color=RED, font_size=22).next_to(j_arrow.get_end(), UL, buff=0.05))

        self.wait(0.4)

        # Project î onto û
        i_proj = u_x * u_hat  # = (u_x², u_x u_y)
        j_proj = u_y * u_hat  # = (u_x u_y, u_y²)

        i_drop = DashedLine(plane.c2p(1, 0), plane.c2p(i_proj[0], i_proj[1]),
                             color=GREEN, stroke_width=1.5)
        j_drop = DashedLine(plane.c2p(0, 1), plane.c2p(j_proj[0], j_proj[1]),
                             color=RED, stroke_width=1.5)
        i_proj_arrow = Arrow(plane.c2p(0, 0), plane.c2p(i_proj[0], i_proj[1]),
                              color=GREEN, buff=0, stroke_width=3)
        j_proj_arrow = Arrow(plane.c2p(0, 0), plane.c2p(j_proj[0], j_proj[1]),
                              color=RED, buff=0, stroke_width=3)

        self.play(Create(i_drop), Create(i_proj_arrow))
        self.wait(0.3)
        self.play(Create(j_drop), Create(j_proj_arrow))
        self.wait(0.4)

        # Right column: labels
        right_info = VGroup(
            Tex(r"projection of $\hat\imath$ onto $\hat u$ has length",
                font_size=22),
            MathTex(r"\hat\imath\cdot\hat u = u_x", color=GREEN, font_size=30),
            Tex(r"projection of $\hat\jmath$ onto $\hat u$ has length",
                font_size=22),
            MathTex(r"\hat\jmath\cdot\hat u = u_y", color=RED, font_size=30),
            Tex(r"so projection matrix $=$", font_size=22),
            Matrix([[r"u_x", r"u_y"]]).scale(0.9).set_color(YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.3).shift(UP * 0.2)
        self.play(Write(right_info))
        self.wait(1.0)
