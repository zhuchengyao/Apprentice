from manim import *
import numpy as np


class HomotopyEquivalenceExample(Scene):
    """
    Two spaces are homotopy-equivalent if one can be continuously
    deformed to the other. Example: annulus ≃ circle (radial
    projection onto inner circle is a homotopy equivalence).

    SINGLE_FOCUS: annulus morphs to circle via radial deformation.
    ValueTracker s_tr drives the homotopy.
    """

    def construct(self):
        title = Tex(r"Homotopy equivalence: annulus $\simeq S^1$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-3, 3, 1], y_range=[-2.5, 2.5, 1],
                            x_length=7, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.1)
        self.play(Create(plane))

        R_in = 1.0
        R_out = 2.5

        s_tr = ValueTracker(0.0)

        def annulus():
            s = s_tr.get_value()
            # At s=0: full annulus. At s=1: just the inner circle.
            grp = VGroup()
            # Outer boundary shrinks from R_out to R_in
            R_outer_now = (1 - s) * R_out + s * R_in
            outer = Circle(radius=R_outer_now, color=BLUE,
                            stroke_width=3).move_to(plane.c2p(0, 0))
            inner = Circle(radius=R_in, color=GREEN,
                            stroke_width=3).move_to(plane.c2p(0, 0))
            # Filled annulus
            filled = AnnularSector(inner_radius=R_in, outer_radius=R_outer_now,
                                     angle=TAU, color=BLUE,
                                     fill_color=BLUE, fill_opacity=0.25)\
                .move_to(plane.c2p(0, 0))
            grp.add(filled, outer, inner)
            # A point on a given ray at angle θ
            return grp

        self.add(always_redraw(annulus))

        # Sample points showing homotopy
        angles = np.linspace(0, TAU, 12, endpoint=False)

        def sample_dots():
            s = s_tr.get_value()
            grp = VGroup()
            for theta in angles:
                # start at (R_out cos θ, R_out sin θ), end at (R_in cos θ, R_in sin θ)
                r = (1 - s) * R_out + s * R_in
                p = plane.c2p(r * np.cos(theta), r * np.sin(theta))
                grp.add(Dot(p, color=YELLOW, radius=0.07))
                # Faint radial line
                start = plane.c2p(R_out * np.cos(theta), R_out * np.sin(theta))
                end = plane.c2p(R_in * np.cos(theta), R_in * np.sin(theta))
                grp.add(DashedLine(start, end, color=GREY_B,
                                    stroke_width=1, stroke_opacity=0.4))
            return grp

        self.add(always_redraw(sample_dots))

        info = VGroup(
            VGroup(Tex(r"homotopy $s=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"radial deformation retract",
                color=YELLOW, font_size=22),
            Tex(r"$\pi_1(\text{annulus})=\pi_1(S^1)=\mathbb{Z}$",
                color=GREEN, font_size=22),
            Tex(r"both have one $H_1$-generator",
                color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(DR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(s_tr.get_value()))
        self.add(info)

        self.play(s_tr.animate.set_value(1.0),
                  run_time=4, rate_func=smooth)
        self.wait(0.8)
        self.play(s_tr.animate.set_value(0.0),
                  run_time=3, rate_func=smooth)
        self.wait(0.5)
