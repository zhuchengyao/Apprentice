from manim import *
import numpy as np


class ChangeBasisVectorsExample(Scene):
    """
    Coordinate change: if basis change P takes standard basis to
    (b_1, b_2), then a vector v with coords [v]_B in basis B satisfies
    v = P [v]_B. To find [v]_B given v in standard coords:
        [v]_B = P^{-1} v.

    SINGLE_FOCUS: fixed vector v = (3, 2) stays at world position.
    ValueTracker s_tr morphs basis from standard ((1, 0), (0, 1)) to
    b_1=(2, 1), b_2=(-1, 1); always_redraw basis arrows + grid lines
    aligned to new basis + v's coordinates in new basis computed live.
    """

    def construct(self):
        title = Tex(r"Change of basis: $[v]_B=P^{-1}v$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 5, 1], y_range=[-2, 4, 1],
                            x_length=9, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(DOWN * 0.1)
        self.play(Create(plane))

        v = np.array([3.0, 2.0])
        v_arrow = Arrow(plane.c2p(0, 0), plane.c2p(v[0], v[1]),
                         color=YELLOW, buff=0, stroke_width=5)
        v_lbl = Tex(r"$v=(3,2)$", color=YELLOW, font_size=22).next_to(
            plane.c2p(v[0], v[1]), UR, buff=0.1)
        self.add(v_arrow, v_lbl)

        s_tr = ValueTracker(0.0)

        b1_target = np.array([2.0, 1.0])
        b2_target = np.array([-1.0, 1.0])

        def basis():
            s = s_tr.get_value()
            b1 = (1 - s) * np.array([1.0, 0.0]) + s * b1_target
            b2 = (1 - s) * np.array([0.0, 1.0]) + s * b2_target
            return b1, b2

        def b1_arrow():
            b1, _ = basis()
            return Arrow(plane.c2p(0, 0), plane.c2p(b1[0], b1[1]),
                          color=GREEN, buff=0, stroke_width=4)

        def b2_arrow():
            _, b2 = basis()
            return Arrow(plane.c2p(0, 0), plane.c2p(b2[0], b2[1]),
                          color=ORANGE, buff=0, stroke_width=4)

        def new_basis_grid():
            b1, b2 = basis()
            grp = VGroup()
            for k in range(-4, 5):
                # b1 direction lines
                p0 = k * b2
                end = p0 + 10 * b1
                start = p0 - 10 * b1
                grp.add(Line(plane.c2p(start[0], start[1]),
                              plane.c2p(end[0], end[1]),
                              color=GREEN, stroke_width=1, stroke_opacity=0.35))
                # b2 direction lines
                p0 = k * b1
                end = p0 + 10 * b2
                start = p0 - 10 * b2
                grp.add(Line(plane.c2p(start[0], start[1]),
                              plane.c2p(end[0], end[1]),
                              color=ORANGE, stroke_width=1, stroke_opacity=0.35))
            return grp

        self.add(always_redraw(new_basis_grid),
                 always_redraw(b1_arrow), always_redraw(b2_arrow))

        def v_coords():
            b1, b2 = basis()
            P = np.column_stack([b1, b2])
            return np.linalg.solve(P, v)

        info = VGroup(
            VGroup(Tex(r"morph $s=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$b_1=$", color=GREEN, font_size=22),
                   DecimalNumber(1.0, num_decimal_places=2,
                                 font_size=22).set_color(GREEN),
                   Tex(",", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22).set_color(GREEN)
                   ).arrange(RIGHT, buff=0.05),
            VGroup(Tex(r"$b_2=$", color=ORANGE, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22).set_color(ORANGE),
                   Tex(",", font_size=22),
                   DecimalNumber(1.0, num_decimal_places=2,
                                 font_size=22).set_color(ORANGE)
                   ).arrange(RIGHT, buff=0.05),
            VGroup(Tex(r"$[v]_B=$", color=YELLOW, font_size=22),
                   DecimalNumber(3.0, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW),
                   Tex(",", font_size=22),
                   DecimalNumber(2.0, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW)
                   ).arrange(RIGHT, buff=0.05),
            Tex(r"$v$ stays at $(3,2)$ world",
                color=YELLOW, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(DL, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(s_tr.get_value()))
        info[1][1].add_updater(lambda m: m.set_value(basis()[0][0]))
        info[1][3].add_updater(lambda m: m.set_value(basis()[0][1]))
        info[2][1].add_updater(lambda m: m.set_value(basis()[1][0]))
        info[2][3].add_updater(lambda m: m.set_value(basis()[1][1]))
        info[3][1].add_updater(lambda m: m.set_value(v_coords()[0]))
        info[3][3].add_updater(lambda m: m.set_value(v_coords()[1]))
        self.add(info)

        self.play(s_tr.animate.set_value(1.0),
                  run_time=5, rate_func=smooth)
        self.wait(0.8)
        self.play(s_tr.animate.set_value(0.0),
                  run_time=3, rate_func=smooth)
        self.wait(0.5)
