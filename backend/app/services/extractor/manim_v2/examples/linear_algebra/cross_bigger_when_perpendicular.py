from manim import *
import numpy as np


class CrossBiggerWhenPerpendicularExample(Scene):
    """
    |v × w| = |v||w|sin θ is maximized when θ = 90°.
    """

    def construct(self):
        title = Tex(r"$|\vec v\times\vec w|=|\vec v||\vec w|\sin\theta$ peaks at $\theta=90°$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-3, 3, 1], y_range=[-1.5, 2.5, 1],
                            x_length=6, y_length=4.5,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(LEFT * 2.5 + DOWN * 0.3)
        self.play(Create(plane))

        v = np.array([2.0, 0.0])
        theta_tr = ValueTracker(0.1)

        def w_vec():
            t = theta_tr.get_value()
            return 2.0 * np.array([np.cos(t), np.sin(t)])

        def v_arrow():
            return Arrow(plane.c2p(0, 0), plane.c2p(v[0], v[1]),
                          color=BLUE, buff=0, stroke_width=5)

        def w_arrow():
            w = w_vec()
            return Arrow(plane.c2p(0, 0), plane.c2p(w[0], w[1]),
                          color=ORANGE, buff=0, stroke_width=5)

        def parallelogram():
            w = w_vec()
            area = v[0] * w[1] - v[1] * w[0]
            return Polygon(plane.c2p(0, 0),
                            plane.c2p(v[0], v[1]),
                            plane.c2p(v[0] + w[0], v[1] + w[1]),
                            plane.c2p(w[0], w[1]),
                            color=GREEN if area > 0 else RED,
                            stroke_width=3,
                            fill_color=GREEN if area > 0 else RED,
                            fill_opacity=0.3)

        self.add(always_redraw(parallelogram),
                 always_redraw(v_arrow), always_redraw(w_arrow))

        # Right: |v×w| curve
        right_axes = Axes(x_range=[0, PI, PI / 4], y_range=[0, 5, 1],
                          x_length=5, y_length=4,
                          axis_config={"include_numbers": True,
                                       "font_size": 16}
                          ).shift(RIGHT * 2.5 + DOWN * 0.3)
        self.play(Create(right_axes))
        self.add(Tex(r"$|\vec v\times\vec w|=4\sin\theta$",
                     font_size=22).next_to(right_axes, UP, buff=0.15))

        cross_curve = right_axes.plot(lambda t: 4 * np.sin(t), x_range=[0, PI],
                                        color=BLUE, stroke_width=3)
        self.add(cross_curve)

        def cross_dot():
            t = theta_tr.get_value()
            return Dot(right_axes.c2p(t, 4 * np.sin(t)),
                        color=YELLOW, radius=0.1)

        self.add(always_redraw(cross_dot))

        info = VGroup(
            VGroup(Tex(r"$\theta=$", font_size=22),
                   DecimalNumber(6.0, num_decimal_places=1,
                                 font_size=22),
                   Tex(r"$^\circ$", font_size=22)).arrange(RIGHT, buff=0.05),
            VGroup(Tex(r"area $=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(np.degrees(theta_tr.get_value())))
        info[1][1].add_updater(lambda m: m.set_value(4 * np.sin(theta_tr.get_value())))
        self.add(info)

        self.play(theta_tr.animate.set_value(PI - 0.05),
                  run_time=6, rate_func=linear)
        self.wait(0.8)
