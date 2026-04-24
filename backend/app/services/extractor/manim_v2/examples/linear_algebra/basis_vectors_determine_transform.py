from manim import *
import numpy as np


class BasisVectorsDetermineTransformExample(Scene):
    """
    A 2D linear transformation is fully determined by where it sends
    î and ĵ. Once we know T(î) and T(ĵ), we know T on every vector
    v = xî + yĵ by linearity: T(v) = x·T(î) + y·T(ĵ).

    SINGLE_FOCUS: NumberPlane. Fixed v = (-1, 2). Apply a transformation
    in two stages via ValueTracker s_tr: first only î moves (j held
    fixed), then ĵ moves. v's image is recomputed live as x·î + y·ĵ.
    """

    def construct(self):
        title = Tex(r"Linear transform determined by $T(\hat\imath), T(\hat\jmath)$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 4, 1], y_range=[-3, 3, 1],
                            x_length=9, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(DOWN * 0.1)
        self.play(Create(plane))

        # Target transformation: T(î) = (2, 2), T(ĵ) = (-2, 1)
        ti_end = np.array([2.0, 2.0])
        tj_end = np.array([-2.0, 1.0])
        v_coords = np.array([-1.0, 2.0])

        s_tr = ValueTracker(0.0)  # 0 → standard basis; 1 → î moved; 2 → ĵ also moved

        def i_now():
            s = s_tr.get_value()
            alpha_i = min(1.0, s)
            return (1 - alpha_i) * np.array([1.0, 0.0]) + alpha_i * ti_end

        def j_now():
            s = s_tr.get_value()
            if s < 1: return np.array([0.0, 1.0])
            alpha_j = min(1.0, s - 1)
            return (1 - alpha_j) * np.array([0.0, 1.0]) + alpha_j * tj_end

        def i_arrow():
            i = i_now()
            return Arrow(plane.c2p(0, 0), plane.c2p(i[0], i[1]),
                          color=GREEN, buff=0, stroke_width=4)

        def j_arrow():
            j = j_now()
            return Arrow(plane.c2p(0, 0), plane.c2p(j[0], j[1]),
                          color=RED, buff=0, stroke_width=4)

        def v_arrow():
            v = v_coords[0] * i_now() + v_coords[1] * j_now()
            return Arrow(plane.c2p(0, 0), plane.c2p(v[0], v[1]),
                          color=YELLOW, buff=0, stroke_width=5)

        self.add(always_redraw(i_arrow), always_redraw(j_arrow),
                 always_redraw(v_arrow))

        # Labels
        self.add(always_redraw(lambda: Tex(r"$T(\hat\imath)$", color=GREEN, font_size=22).move_to(
            plane.c2p(*i_now()) + UP * 0.25 + RIGHT * 0.2)))
        self.add(always_redraw(lambda: Tex(r"$T(\hat\jmath)$", color=RED, font_size=22).move_to(
            plane.c2p(*j_now()) + UP * 0.25 + LEFT * 0.3)))
        self.add(always_redraw(lambda: Tex(r"$T(v)=xT(\hat\imath)+yT(\hat\jmath)$",
                                             color=YELLOW, font_size=22).move_to(
            plane.c2p(*(v_coords[0] * i_now() + v_coords[1] * j_now())) + UP * 0.3)))

        # Right info
        info = VGroup(
            Tex(r"$v=-1\cdot\hat\imath+2\cdot\hat\jmath$",
                color=YELLOW, font_size=22),
            VGroup(Tex(r"stage $=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            Tex(r"stage 0-1: $\hat\imath$ moves",
                color=GREEN, font_size=20),
            Tex(r"stage 1-2: $\hat\jmath$ moves",
                color=RED, font_size=20),
            Tex(r"$v$'s image follows linearity",
                color=YELLOW, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(DR, buff=0.3)
        info[1][1].add_updater(lambda m: m.set_value(s_tr.get_value()))
        self.add(info)

        self.play(s_tr.animate.set_value(1.0), run_time=3, rate_func=smooth)
        self.wait(0.5)
        self.play(s_tr.animate.set_value(2.0), run_time=3, rate_func=smooth)
        self.wait(0.8)
