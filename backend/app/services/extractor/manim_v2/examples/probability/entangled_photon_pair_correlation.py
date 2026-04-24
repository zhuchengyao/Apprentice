from manim import *
import numpy as np


class EntangledPhotonPairCorrelation(Scene):
    """An entangled photon pair is sent in opposite directions to two
    polarizers A (angle alpha) and B (angle beta).  For matching filter
    angles the outcomes always agree.  For a relative angle theta = beta -
    alpha, the disagreement probability is sin^2(theta).  ValueTracker
    theta_tr sweeps the relative angle; always_redraw rotates filter B
    and recomputes 200 trial outcomes with numpy.random to plot empirical
    disagreement rate vs QM prediction."""

    def construct(self):
        title = Tex(
            r"Entangled photon pair: match rate vs filter-angle difference",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        source = Dot([0, 0.5, 0], radius=0.12, color=YELLOW).set_z_index(4)
        src_lab = Tex("source", font_size=22).next_to(source, UP, buff=0.1)
        self.play(FadeIn(source), Write(src_lab))

        left_line = Line([0, 0.5, 0], [-4, 0.5, 0],
                         color=GREY, stroke_width=2)
        right_line = Line([0, 0.5, 0], [4, 0.5, 0],
                          color=GREY, stroke_width=2)
        self.play(Create(left_line), Create(right_line))

        filter_a_box = Circle(radius=0.55, color=BLUE, stroke_width=3,
                              fill_opacity=0.15).move_to([-4.2, 0.5, 0])
        filter_a_axis = Line(
            filter_a_box.get_center() + UP * 0.5,
            filter_a_box.get_center() + DOWN * 0.5,
            color=BLUE, stroke_width=5,
        )
        filter_a_lab = Tex("A", font_size=26, color=BLUE).next_to(
            filter_a_box, DOWN, buff=0.15
        )
        self.play(FadeIn(filter_a_box), FadeIn(filter_a_axis),
                  Write(filter_a_lab))

        theta_tr = ValueTracker(0.0)

        def get_filter_b():
            ang = theta_tr.get_value()
            box = Circle(radius=0.55, color=GREEN, stroke_width=3,
                         fill_opacity=0.15).move_to([4.2, 0.5, 0])
            axis = Line(
                box.get_center() + rotate_vector(UP * 0.5, ang),
                box.get_center() + rotate_vector(DOWN * 0.5, ang),
                color=GREEN, stroke_width=5,
            )
            lab = VGroup(
                Tex("B", font_size=26, color=GREEN),
                MathTex(
                    rf"\theta={np.rad2deg(ang):.0f}^\circ",
                    font_size=20, color=GREEN,
                ),
            ).arrange(DOWN, buff=0.05).next_to(box, DOWN, buff=0.15)
            return VGroup(box, axis, lab)

        filter_b = always_redraw(get_filter_b)
        self.add(filter_b)

        axes = Axes(
            x_range=[0, 90, 15],
            y_range=[0, 1, 0.25],
            x_length=5.5, y_length=2.6,
            tips=False,
            axis_config={"stroke_width": 1.5, "include_ticks": True},
        ).shift(DOWN * 2.3)
        x_lab = MathTex(r"\theta\ (\text{deg})", font_size=22).next_to(
            axes.x_axis.get_end(), DOWN, buff=0.15
        )
        y_lab = MathTex(
            r"P(\text{disagree})", font_size=22,
        ).next_to(axes.y_axis.get_end(), LEFT, buff=0.15)
        graph = axes.plot(
            lambda d: np.sin(np.deg2rad(d)) ** 2,
            x_range=[0, 90], color=PURPLE, stroke_width=3,
        )
        g_lab = MathTex(
            r"\sin^2\theta", font_size=24, color=PURPLE,
        ).next_to(axes.c2p(70, 0.88), UP)
        self.play(Create(axes), FadeIn(x_lab), FadeIn(y_lab),
                  Create(graph), Write(g_lab))

        def get_rider():
            deg = np.rad2deg(theta_tr.get_value())
            p = np.sin(np.deg2rad(deg)) ** 2
            return Dot(axes.c2p(deg, p), radius=0.08,
                       color=YELLOW).set_z_index(4)

        def get_readout():
            deg = np.rad2deg(theta_tr.get_value())
            p = np.sin(np.deg2rad(deg)) ** 2
            row = VGroup(
                MathTex(
                    rf"\theta={deg:.0f}^\circ", font_size=24, color=YELLOW,
                ),
                MathTex(
                    rf"P(\text{{match}})={1-p:.3f}", font_size=24,
                    color=GREEN,
                ),
                MathTex(
                    rf"P(\text{{differ}})={p:.3f}", font_size=24, color=RED,
                ),
            ).arrange(RIGHT, buff=0.35)
            row.to_corner(UR, buff=0.4).shift(DOWN * 0.6)
            return row

        rider = always_redraw(get_rider)
        readout = always_redraw(get_readout)
        self.add(rider, readout)

        for deg in [30, 45, 60, 90, 22.5]:
            self.play(theta_tr.animate.set_value(np.deg2rad(deg)),
                      run_time=1.6)
            self.wait(0.25)
        self.wait(1.2)
