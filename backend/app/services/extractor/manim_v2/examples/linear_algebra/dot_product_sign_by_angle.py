from manim import *
import numpy as np


class DotProductSignByAngleExample(Scene):
    """
    Sign of v·w tells the angle kind:
      v·w > 0  ⇔  θ < 90° (acute)
      v·w = 0  ⇔  θ = 90° (perpendicular)
      v·w < 0  ⇔  θ > 90° (obtuse)
    """

    def construct(self):
        title = Tex(r"Sign of $\vec v\cdot\vec w$ reveals angle kind",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-3, 3, 1], y_range=[-2.5, 2.5, 1],
                            x_length=7, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(LEFT * 2.5 + DOWN * 0.2)
        self.play(Create(plane))

        v = np.array([2.0, 0.0])
        v_arrow = Arrow(plane.c2p(0, 0), plane.c2p(v[0], v[1]),
                         color=BLUE, buff=0, stroke_width=5)
        v_lbl = Tex(r"$\vec v$", color=BLUE, font_size=24).next_to(v_arrow.get_end(), UP, buff=0.1)
        self.add(v_arrow, v_lbl)

        theta_tr = ValueTracker(0.3)

        def w_vec():
            t = theta_tr.get_value()
            return 2.2 * np.array([np.cos(t), np.sin(t)])

        def w_arrow():
            w = w_vec()
            return Arrow(plane.c2p(0, 0), plane.c2p(w[0], w[1]),
                          color=ORANGE, buff=0, stroke_width=5)

        def angle_arc():
            t = theta_tr.get_value()
            scale = plane.x_length / (plane.x_range[1] - plane.x_range[0])
            return Arc(radius=0.6 * scale, start_angle=0, angle=t,
                        color=YELLOW, stroke_width=3).move_arc_center_to(plane.c2p(0, 0))

        self.add(always_redraw(w_arrow), always_redraw(angle_arc))

        # Right: readouts
        def dot_val():
            w = w_vec()
            return float(np.dot(v, w))

        def theta_val():
            return float(np.degrees(theta_tr.get_value()))

        def sign_color():
            d = dot_val()
            if d > 0.05: return GREEN
            if d < -0.05: return RED
            return YELLOW

        def sign_label():
            d = dot_val()
            if d > 0.05: return r"$\vec v\cdot\vec w>0$: acute"
            if d < -0.05: return r"$\vec v\cdot\vec w<0$: obtuse"
            return r"$\vec v\cdot\vec w=0$: perpendicular"

        info = VGroup(
            VGroup(Tex(r"$\theta=$", font_size=24),
                   DecimalNumber(17.0, num_decimal_places=1,
                                 font_size=24).set_color(YELLOW),
                   Tex(r"$^\circ$", font_size=24)).arrange(RIGHT, buff=0.05),
            VGroup(Tex(r"$\vec v\cdot\vec w=$", font_size=24),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=24).set_color(GREEN)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(theta_val()))
        info[1][1].add_updater(lambda m: m.set_value(dot_val()).set_color(sign_color()))
        self.add(info)

        # Sign label
        label_tex = Tex(sign_label(), color=sign_color(),
                         font_size=26).to_edge(DOWN, buff=0.4)
        self.add(label_tex)
        def update_label(mob, dt):
            new = Tex(sign_label(), color=sign_color(),
                       font_size=26).move_to(label_tex)
            label_tex.become(new)
            return label_tex
        label_tex.add_updater(update_label)

        # Sweep
        self.play(theta_tr.animate.set_value(PI - 0.2),
                  run_time=6, rate_func=linear)
        self.wait(0.8)
