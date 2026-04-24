from manim import *
import numpy as np


class FollowLinearCombinationExample(Scene):
    """
    If v = x·î + y·ĵ, then T(v) = x·T(î) + y·T(ĵ). Trace this
    by scaling T(î) by x and T(ĵ) by y, laying them tip-to-tail,
    recovering T(v).

    SINGLE_FOCUS: transformation T has T(î)=(2, 2), T(ĵ)=(-2, 1).
    ValueTracker stage_tr phases: 0=standard, 1=transformed,
    2=show x·T(î), 3=add y·T(ĵ) tip-to-tail revealing T(v).
    """

    def construct(self):
        title = Tex(r"Follow $v=x\hat\imath+y\hat\jmath$ through transformation",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 4, 1], y_range=[-3, 3, 1],
                            x_length=9, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(DOWN * 0.1)
        self.play(Create(plane))

        i_std = np.array([1.0, 0.0])
        j_std = np.array([0.0, 1.0])
        i_new = np.array([2.0, 2.0])
        j_new = np.array([-2.0, 1.0])
        x_coef, y_coef = -1.0, 2.0  # v = -1·î + 2·ĵ

        stage_tr = ValueTracker(0.0)

        def i_now():
            s = min(1.0, stage_tr.get_value())
            return (1 - s) * i_std + s * i_new

        def j_now():
            s = min(1.0, stage_tr.get_value())
            return (1 - s) * j_std + s * j_new

        def v_now():
            return x_coef * i_now() + y_coef * j_now()

        def i_arrow():
            i = i_now()
            return Arrow(plane.c2p(0, 0), plane.c2p(i[0], i[1]),
                          color=GREEN, buff=0, stroke_width=4)

        def j_arrow():
            j = j_now()
            return Arrow(plane.c2p(0, 0), plane.c2p(j[0], j[1]),
                          color=RED, buff=0, stroke_width=4)

        def v_arrow():
            v = v_now()
            return Arrow(plane.c2p(0, 0), plane.c2p(v[0], v[1]),
                          color=YELLOW, buff=0, stroke_width=5)

        # Scaled arrows (appear in stage 2+)
        def xi_arrow():
            s = stage_tr.get_value()
            if s < 1.5:
                return VMobject()
            alpha = min(1.0, (s - 1.5) * 2)
            xi = alpha * x_coef * i_now()
            return Arrow(plane.c2p(0, 0), plane.c2p(xi[0], xi[1]),
                          color=GREEN, buff=0, stroke_width=3)

        def yj_arrow():
            s = stage_tr.get_value()
            if s < 2.5:
                return VMobject()
            alpha = min(1.0, (s - 2.5) * 2)
            xi = x_coef * i_now()
            yj_vec = alpha * y_coef * j_now()
            return Arrow(plane.c2p(xi[0], xi[1]),
                          plane.c2p(xi[0] + yj_vec[0], xi[1] + yj_vec[1]),
                          color=RED, buff=0, stroke_width=3)

        self.add(always_redraw(i_arrow), always_redraw(j_arrow),
                 always_redraw(v_arrow),
                 always_redraw(xi_arrow), always_redraw(yj_arrow))

        info = VGroup(
            Tex(r"$v=-1\cdot \hat\imath+2\cdot\hat\jmath$",
                color=YELLOW, font_size=22),
            VGroup(Tex(r"stage $=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            Tex(r"0-1: apply transform",
                color=GREY_B, font_size=18),
            Tex(r"1.5-2.5: draw $xT(\hat\imath)$",
                color=GREEN, font_size=18),
            Tex(r"2.5-3: add $yT(\hat\jmath)$ tip-to-tail",
                color=RED, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DR, buff=0.3)
        info[1][1].add_updater(lambda m: m.set_value(stage_tr.get_value()))
        self.add(info)

        self.play(stage_tr.animate.set_value(1.0), run_time=2.5, rate_func=smooth)
        self.wait(0.5)
        self.play(stage_tr.animate.set_value(2.0), run_time=1.5, rate_func=smooth)
        self.wait(0.3)
        self.play(stage_tr.animate.set_value(3.0), run_time=1.5, rate_func=smooth)
        self.wait(0.8)
