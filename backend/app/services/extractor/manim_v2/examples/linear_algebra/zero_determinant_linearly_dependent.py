from manim import *
import numpy as np


class ZeroDeterminantLinearlyDependentExample(Scene):
    """
    det A = 0 iff columns of A are linearly dependent — they span
    less than full dimension, collapsing area/volume to zero.

    SINGLE_FOCUS: 2D NumberPlane. ValueTracker s_tr sweeps a
    parameter that makes columns parallel → det → 0. Show
    parallelogram collapsing to a line.
    """

    def construct(self):
        title = Tex(r"$\det A = 0$ iff columns linearly dependent",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 4, 1], y_range=[-3, 3, 1],
                            x_length=9, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.1)
        self.play(Create(plane))

        s_tr = ValueTracker(0.0)

        # Columns: v1 = (2, 1), v2 = (1, s) where s sweeps 0.5 → 1/2·1 + ... actually
        # let v2 = (1, s); columns linearly dependent when v2 is multiple of v1.
        # v2 parallel to v1 when s/1 = 1/2, i.e. s = 0.5.
        # Start at s = 2 (independent), end at s = 0.5 (parallel).

        def columns():
            s = s_tr.get_value()
            v1 = np.array([2.0, 1.0])
            v2 = np.array([1.0, s])
            return v1, v2

        def parallelogram():
            v1, v2 = columns()
            pts = [plane.c2p(*p) for p in
                    [np.zeros(2), v1, v1 + v2, v2]]
            d = v1[0] * v2[1] - v1[1] * v2[0]
            col = GREEN if d > 0.1 else (RED if d < -0.1 else YELLOW)
            return Polygon(*pts, color=col, stroke_width=3,
                            fill_color=col, fill_opacity=0.4)

        def v1_arrow():
            v1, _ = columns()
            return Arrow(plane.c2p(0, 0), plane.c2p(v1[0], v1[1]),
                          color=BLUE, buff=0, stroke_width=5)

        def v2_arrow():
            _, v2 = columns()
            return Arrow(plane.c2p(0, 0), plane.c2p(v2[0], v2[1]),
                          color=ORANGE, buff=0, stroke_width=5)

        self.add(always_redraw(parallelogram),
                 always_redraw(v1_arrow), always_redraw(v2_arrow))

        info = VGroup(
            Tex(r"$A=\begin{pmatrix}2&1\\1&s\end{pmatrix}$", font_size=24),
            VGroup(Tex(r"$s=$", font_size=22),
                   DecimalNumber(2.0, num_decimal_places=3,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\det A=2s-1=$", font_size=22),
                   DecimalNumber(3.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"cols parallel $\Leftrightarrow s=0.5$",
                color=YELLOW, font_size=22),
            Tex(r"at $s=0.5$: $\det=0$, cols dep.",
                color=YELLOW, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.3)
        info[1][1].add_updater(lambda m: m.set_value(s_tr.get_value() * 1.5 + 0.5 - s_tr.get_value() * 1))  # quick ratio
        # Fix: s_tr range [0, 1] maps to s ∈ [2, 0.5]
        info[1][1].clear_updaters()
        info[1][1].add_updater(lambda m: m.set_value(2 - 1.5 * s_tr.get_value()))
        info[2][1].add_updater(lambda m: m.set_value(2 * (2 - 1.5 * s_tr.get_value()) - 1))
        self.add(info)

        self.play(s_tr.animate.set_value(1.0), run_time=4, rate_func=smooth)
        self.wait(0.8)
