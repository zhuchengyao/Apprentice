from manim import *
import numpy as np


class VectorThroughCompositionExample(Scene):
    """
    Apply two transformations sequentially to a single vector v = (2, 3).
    First R (90° rotation), then S (shear). v → R·v → S·R·v.

    SINGLE_FOCUS: YELLOW vector v tracks through both stages via
    ValueTracker stage_tr. Trail shows intermediate state.
    """

    def construct(self):
        title = Tex(r"Single vector through composition $S\circ R$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 4, 1], y_range=[-3, 3, 1],
                            x_length=9, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(DOWN * 0.1)
        self.play(Create(plane))

        R = np.array([[0.0, -1.0], [1.0, 0.0]])
        S = np.array([[1.0, 1.0], [0.0, 1.0]])

        v0 = np.array([2.0, 3.0])
        v_after_R = R @ v0
        v_after_SR = S @ R @ v0

        stage_tr = ValueTracker(0.0)

        def v_now():
            s = stage_tr.get_value()
            if s <= 1:
                return (1 - s) * v0 + s * v_after_R
            alpha = s - 1
            return (1 - alpha) * v_after_R + alpha * v_after_SR

        def v_arrow():
            v = v_now()
            return Arrow(plane.c2p(0, 0), plane.c2p(v[0], v[1]),
                          color=YELLOW, buff=0, stroke_width=6)

        def v_dot():
            v = v_now()
            return Dot(plane.c2p(v[0], v[1]), color=YELLOW, radius=0.12)

        # Trail positions
        trail_positions = [v0, v_after_R, v_after_SR]
        trail_colors = [BLUE, GREEN, RED]
        trail_labels = [r"$v$", r"$Rv$", r"$SRv$"]

        for pos, col, lbl in zip(trail_positions, trail_colors, trail_labels):
            self.add(Dot(plane.c2p(pos[0], pos[1]),
                         color=col, radius=0.08,
                         fill_opacity=0.5))
            self.add(Tex(lbl, color=col, font_size=22).move_to(
                plane.c2p(pos[0], pos[1]) + UP * 0.3))

        # Basis vectors (also transformed)
        def i_arrow():
            s = stage_tr.get_value()
            if s <= 1:
                M = (1 - s) * np.eye(2) + s * R
            else:
                alpha = s - 1
                M = (1 - alpha) * R + alpha * (S @ R)
            p = M @ np.array([1, 0])
            return Arrow(plane.c2p(0, 0), plane.c2p(p[0], p[1]),
                          color=GREEN, buff=0, stroke_width=3,
                          stroke_opacity=0.6)

        def j_arrow():
            s = stage_tr.get_value()
            if s <= 1:
                M = (1 - s) * np.eye(2) + s * R
            else:
                alpha = s - 1
                M = (1 - alpha) * R + alpha * (S @ R)
            p = M @ np.array([0, 1])
            return Arrow(plane.c2p(0, 0), plane.c2p(p[0], p[1]),
                          color=RED, buff=0, stroke_width=3,
                          stroke_opacity=0.6)

        self.add(always_redraw(i_arrow), always_redraw(j_arrow),
                 always_redraw(v_arrow), always_redraw(v_dot))

        info = VGroup(
            Tex(r"$v=(2, 3)$", color=YELLOW, font_size=22),
            Tex(r"$Rv=(-3, 2)$", color=GREEN, font_size=20),
            Tex(r"$SRv=(-1, 2)$", color=RED, font_size=20),
            VGroup(Tex(r"stage $=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UR, buff=0.3)
        info[3][1].add_updater(lambda m: m.set_value(stage_tr.get_value()))
        self.add(info)

        self.play(stage_tr.animate.set_value(1.0), run_time=2.5, rate_func=smooth)
        self.wait(0.5)
        self.play(stage_tr.animate.set_value(2.0), run_time=2.5, rate_func=smooth)
        self.wait(0.8)
