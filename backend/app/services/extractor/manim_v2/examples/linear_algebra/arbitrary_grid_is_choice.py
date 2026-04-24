from manim import *
import numpy as np


class ArbitraryGridIsChoiceExample(Scene):
    """Space has no built-in grid."""

    def construct(self):
        title = Tex(r"Space has no built-in grid; basis is a choice",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 4, 1], y_range=[-3, 3, 1],
                            x_length=9, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.1)
        self.play(Create(plane))

        i_std = Arrow(plane.c2p(0, 0), plane.c2p(1, 0), color=GREEN, buff=0, stroke_width=5)
        j_std = Arrow(plane.c2p(0, 0), plane.c2p(0, 1), color=RED, buff=0, stroke_width=5)
        self.add(i_std, j_std)
        self.wait(0.4)

        b1 = np.array([2.0, 1.0])
        b2 = np.array([-1.0, 1.0])
        s_tr = ValueTracker(0.0)

        def jenny_grid():
            alpha = s_tr.get_value()
            if alpha < 0.05: return VGroup()
            grp = VGroup()
            for k in range(-4, 5):
                p0 = k * b2
                grp.add(Line(plane.c2p(*(p0 - 10 * b1)), plane.c2p(*(p0 + 10 * b1)),
                              color=BLUE, stroke_width=1, stroke_opacity=0.4 * alpha))
                p0 = k * b1
                grp.add(Line(plane.c2p(*(p0 - 10 * b2)), plane.c2p(*(p0 + 10 * b2)),
                              color=PURPLE, stroke_width=1, stroke_opacity=0.4 * alpha))
            return grp

        def jenny_arrows():
            alpha = s_tr.get_value()
            if alpha < 0.05: return VGroup()
            return VGroup(
                Arrow(plane.c2p(0, 0), plane.c2p(b1[0], b1[1]),
                       color=BLUE, buff=0, stroke_width=5, stroke_opacity=alpha),
                Arrow(plane.c2p(0, 0), plane.c2p(b2[0], b2[1]),
                       color=PURPLE, buff=0, stroke_width=5, stroke_opacity=alpha),
            )

        self.add(always_redraw(jenny_grid), always_redraw(jenny_arrows))
        self.play(s_tr.animate.set_value(1.0), run_time=2.5, rate_func=smooth)
        self.add(Tex(r"$\vec b_1=(2, 1)$", color=BLUE, font_size=20).to_corner(UR, buff=0.3))
        self.add(Tex(r"$\vec b_2=(-1, 1)$", color=PURPLE, font_size=20).to_corner(UR, buff=0.3).shift(DOWN * 0.5))
        self.play(Write(
            Tex(r"same space, different coordinate systems",
                 color=YELLOW, font_size=26).to_edge(DOWN, buff=0.4)
        ))
        self.wait(1.0)
