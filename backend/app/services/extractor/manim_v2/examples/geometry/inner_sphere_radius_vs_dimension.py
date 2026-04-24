from manim import *
import numpy as np


class InnerSphereRadiusVsDimension(Scene):
    """In d dimensions, place unit spheres at each of the 2^d corners
    (±1, ±1, ..., ±1) inside a box [-2, 2]^d.  The sphere tangent to all of
    them, centered at the origin, has radius r_d = sqrt(d) - 1.  This is
    counterintuitive: r_2 ≈ 0.414, r_3 ≈ 0.732, r_4 = 1 (reaches the box
    face), r_9 = 2 (escapes the outer box!), and r_d → ∞."""

    def construct(self):
        title = Tex(
            r"Inner-sphere radius $r_d = \sqrt{d}-1$ vs dimension",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(
            x_range=[0, 20, 2],
            y_range=[0, 4, 1],
            x_length=9.5,
            y_length=5.0,
            tips=False,
            axis_config={"stroke_width": 2, "include_ticks": True},
        ).shift(DOWN * 0.3)
        x_lab = MathTex("d", font_size=28).next_to(
            axes.x_axis.get_end(), DOWN, buff=0.2
        )
        y_lab = MathTex("r_d", font_size=28).next_to(
            axes.y_axis.get_end(), LEFT, buff=0.2
        )
        self.play(Create(axes), FadeIn(x_lab), FadeIn(y_lab))

        graph = axes.plot(
            lambda d: np.sqrt(d) - 1,
            x_range=[1.0, 20.0],
            color=BLUE,
            stroke_width=3,
        )
        self.play(Create(graph), run_time=2)

        one_line = DashedLine(
            axes.c2p(0, 1), axes.c2p(20, 1),
            color=YELLOW, stroke_width=2,
        )
        two_line = DashedLine(
            axes.c2p(0, 2), axes.c2p(20, 2),
            color=ORANGE, stroke_width=2,
        )
        one_lab = MathTex(r"r=1\ \text{(touches box face)}",
                          font_size=24, color=YELLOW).next_to(
            one_line, RIGHT, buff=0.15
        )
        two_lab = MathTex(r"r=2\ \text{(reaches outer box)}",
                          font_size=24, color=ORANGE).next_to(
            two_line, RIGHT, buff=0.15
        )
        self.play(Create(one_line), FadeIn(one_lab))
        self.play(Create(two_line), FadeIn(two_lab))

        d_tr = ValueTracker(2.0)

        def get_rider():
            d = d_tr.get_value()
            return Dot(axes.c2p(d, np.sqrt(d) - 1),
                       radius=0.09, color=RED).set_z_index(4)

        def get_readout():
            d = d_tr.get_value()
            row = VGroup(
                MathTex("d=", font_size=26),
                Integer(int(round(d)), font_size=26),
                MathTex(r"\quad r_d=", font_size=26),
                DecimalNumber(np.sqrt(d) - 1, num_decimal_places=3,
                              font_size=26, color=RED),
            ).arrange(RIGHT, buff=0.1)
            row.to_corner(UL, buff=0.4).shift(DOWN * 0.7)
            return row

        rider = always_redraw(get_rider)
        readout = always_redraw(get_readout)
        self.add(rider, readout)

        for d_val in [3, 4, 6, 9, 12, 16, 20]:
            self.play(d_tr.animate.set_value(d_val), run_time=1.2)
            self.wait(0.25)

        milestone = VGroup(
            Tex(r"$d=4$: inner sphere touches the box face",
                font_size=24, color=YELLOW),
            Tex(r"$d=9$: inner sphere reaches the outer box $[-2,2]^d$",
                font_size=24, color=ORANGE),
            Tex(r"$d\to\infty$: $r_d\to\infty$", font_size=24, color=RED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        milestone.to_corner(DR, buff=0.4).shift(UP * 0.2)
        self.play(FadeIn(milestone))
        self.wait(1.5)
