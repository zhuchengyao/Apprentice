from manim import *
import numpy as np


class AdMinusBcGeometricIntuitionExample(Scene):
    """
    Geometric intuition for ad-bc: build the transformation as a
    sequence — first stretch î by a, then stretch ĵ by d, then shear
    by b/d, then adjust by -c. Each stage's effect on unit square's
    area adds up to ad-bc.

    4-phase demo with ValueTracker stage_tr ∈ [0, 4].
    """

    def construct(self):
        title = Tex(r"Build $ad-bc$ as sequence of transformations",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-2, 5, 1], y_range=[-2, 4, 1],
                            x_length=9, y_length=5.0,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.3)
        self.play(Create(plane))

        a_v, d_v, b_v, c_v = 3.0, 2.0, 1.5, 0.5

        stage_tr = ValueTracker(0.0)

        def M_of():
            s = stage_tr.get_value()
            if s <= 1:
                return np.array([[1 + s * (a_v - 1), 0], [0, 1]])
            if s <= 2:
                alpha = s - 1
                return np.array([[a_v, 0], [0, 1 + alpha * (d_v - 1)]])
            if s <= 3:
                alpha = s - 2
                return np.array([[a_v, alpha * b_v], [0, d_v]])
            alpha = s - 3
            return np.array([[a_v, b_v], [alpha * c_v, d_v]])

        def square():
            M = M_of()
            pts = [plane.c2p(*(M @ p)) for p in
                    [np.zeros(2), np.array([1, 0]), np.array([1, 1]), np.array([0, 1])]]
            d = M[0, 0] * M[1, 1] - M[0, 1] * M[1, 0]
            col = GREEN if d > 0.1 else (RED if d < -0.1 else YELLOW)
            return Polygon(*pts, color=col, stroke_width=3,
                            fill_color=col, fill_opacity=0.4)

        def i_arrow():
            M = M_of()
            p = M @ np.array([1, 0])
            return Arrow(plane.c2p(0, 0), plane.c2p(p[0], p[1]),
                          color=GREEN, buff=0, stroke_width=4)

        def j_arrow():
            M = M_of()
            p = M @ np.array([0, 1])
            return Arrow(plane.c2p(0, 0), plane.c2p(p[0], p[1]),
                          color=RED, buff=0, stroke_width=4)

        self.add(always_redraw(square), always_redraw(i_arrow), always_redraw(j_arrow))

        def stage_str():
            s = stage_tr.get_value()
            if s < 1: return rf"1: $\hat\imath\to a\hat\imath$ (area $\to a={a_v:.0f}$)"
            if s < 2: return rf"2: $\hat\jmath\to d\hat\jmath$ (area $\to ad={a_v * d_v:.0f}$)"
            if s < 3: return rf"3: shear $\hat\jmath$ right by $b$ (area unchanged)"
            return rf"4: shear $\hat\imath$ up by $c$ (area $-bc$: det$=ad-bc={a_v * d_v - b_v * c_v:.2f}$)"

        stage_tex = Tex(stage_str(), color=YELLOW, font_size=22).to_edge(DOWN, buff=0.3)
        self.add(stage_tex)
        def update_stage(mob, dt):
            new = Tex(stage_str(), color=YELLOW, font_size=22).move_to(stage_tex)
            stage_tex.become(new)
            return stage_tex
        stage_tex.add_updater(update_stage)

        info = VGroup(
            Tex(rf"$a={a_v:.0f}, b={b_v:.1f}$", font_size=22),
            Tex(rf"$c={c_v:.1f}, d={d_v:.0f}$", font_size=22),
            VGroup(Tex(r"$\det=$", font_size=22),
                   DecimalNumber(1.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.3)
        info[2][1].add_updater(lambda m: m.set_value(float(np.linalg.det(M_of()))))
        self.add(info)

        for target in [1, 2, 3, 4]:
            self.play(stage_tr.animate.set_value(float(target)),
                      run_time=1.8, rate_func=smooth)
            self.wait(0.6)
        self.wait(0.8)
