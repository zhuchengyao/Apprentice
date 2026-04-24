from manim import *
import numpy as np


class Cross2dSignedAreaExample(Scene):
    """
    2D cross product v × w = signed area of parallelogram from v, w.
    Sign: positive if ĵ-component of w is ahead of v (CCW orientation).
    v × w = v₁ w₂ - v₂ w₁ (same as 2×2 det).
    """

    def construct(self):
        title = Tex(r"2D cross: $\vec v\times\vec w=v_1w_2-v_2w_1$ = signed area",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-3, 4, 1], y_range=[-2, 3, 1],
                            x_length=9, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.1)
        self.play(Create(plane))

        v = np.array([2.5, 0.5])
        w_theta_tr = ValueTracker(PI / 3)

        def w_vec():
            t = w_theta_tr.get_value()
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
            cross = v[0] * w[1] - v[1] * w[0]
            col = GREEN if cross > 0.05 else (RED if cross < -0.05 else GREY_D)
            pts = [plane.c2p(0, 0),
                    plane.c2p(v[0], v[1]),
                    plane.c2p(v[0] + w[0], v[1] + w[1]),
                    plane.c2p(w[0], w[1])]
            return Polygon(*pts, color=col, stroke_width=3,
                            fill_color=col, fill_opacity=0.35)

        self.add(always_redraw(parallelogram),
                 always_redraw(v_arrow), always_redraw(w_arrow))

        info = VGroup(
            Tex(r"$\vec v=(2.5, 0.5)$", color=BLUE, font_size=22),
            VGroup(Tex(r"$\theta=$", font_size=22),
                   DecimalNumber(60.0, num_decimal_places=1,
                                 font_size=22),
                   Tex(r"$^\circ$", font_size=22)).arrange(RIGHT, buff=0.05),
            VGroup(Tex(r"$\vec v\times\vec w=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"GREEN = CCW (+), RED = CW (-)",
                color=GREY_B, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.3)

        def cross_val():
            w = w_vec()
            return float(v[0] * w[1] - v[1] * w[0])

        info[1][1].add_updater(lambda m: m.set_value(np.degrees(w_theta_tr.get_value())))
        info[2][1].add_updater(lambda m: m.set_value(cross_val())
                                .set_color(GREEN if cross_val() > 0 else RED))
        self.add(info)

        for target in [PI / 2, 2 * PI / 3, PI + 0.3, 3 * PI / 2, PI / 4]:
            self.play(w_theta_tr.animate.set_value(target),
                      run_time=1.6, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.5)
