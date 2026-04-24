from manim import *
import numpy as np


class GramSchmidtProcessExample(Scene):
    """
    Gram-Schmidt orthogonalization in ℝ². Given v_1, v_2 linearly
    independent, produce orthonormal u_1, u_2:
      u_1 = v_1 / ‖v_1‖
      w_2 = v_2 − (v_2·u_1) u_1
      u_2 = w_2 / ‖w_2‖

    SINGLE_FOCUS: v_1 = (3, 1), v_2 = (1, 2). 4-stage animation:
      stage 0: show v_1, v_2 (BLUE, GREEN)
      stage 1: normalize v_1 → u_1 (YELLOW)
      stage 2: project v_2 onto u_1 → projection arrow (ORANGE) + drop
      stage 3: subtract → w_2, normalize → u_2
    """

    def construct(self):
        title = Tex(r"Gram-Schmidt: $u_1=v_1/\|v_1\|$, $u_2=(v_2-(v_2\cdot u_1)u_1)/\|\cdot\|$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-1, 4, 1], y_range=[-1, 3, 1],
                            x_length=7, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.2)
        self.play(Create(plane))

        v1 = np.array([3.0, 1.0])
        v2 = np.array([1.0, 2.0])
        u1 = v1 / np.linalg.norm(v1)
        proj = np.dot(v2, u1) * u1
        w2 = v2 - proj
        u2 = w2 / np.linalg.norm(w2)

        stage_tr = ValueTracker(0.0)  # 0..3

        def v1_arrow():
            return Arrow(plane.c2p(0, 0), plane.c2p(v1[0], v1[1]),
                          color=BLUE, buff=0, stroke_width=4)

        def v2_arrow():
            return Arrow(plane.c2p(0, 0), plane.c2p(v2[0], v2[1]),
                          color=GREEN, buff=0, stroke_width=4)

        def u1_arrow():
            s = stage_tr.get_value()
            if s < 0.9:
                return VMobject()
            return Arrow(plane.c2p(0, 0), plane.c2p(u1[0], u1[1]),
                          color=YELLOW, buff=0, stroke_width=5)

        def proj_arrow():
            s = stage_tr.get_value()
            if s < 1.9:
                return VMobject()
            alpha = min(1.0, (s - 1.9) * 2)
            endpoint = alpha * proj
            return Arrow(plane.c2p(0, 0), plane.c2p(endpoint[0], endpoint[1]),
                          color=ORANGE, buff=0, stroke_width=4)

        def proj_drop():
            s = stage_tr.get_value()
            if s < 1.9:
                return VMobject()
            return DashedLine(plane.c2p(v2[0], v2[1]),
                              plane.c2p(proj[0], proj[1]),
                              color=ORANGE, stroke_width=2)

        def w2_arrow():
            s = stage_tr.get_value()
            if s < 2.9:
                return VMobject()
            return Arrow(plane.c2p(proj[0], proj[1]),
                          plane.c2p(proj[0] + w2[0], proj[1] + w2[1]),
                          color=PURPLE, buff=0, stroke_width=4)

        def u2_arrow():
            s = stage_tr.get_value()
            if s < 3.4:
                return VMobject()
            return Arrow(plane.c2p(0, 0), plane.c2p(u2[0], u2[1]),
                          color=RED, buff=0, stroke_width=5)

        self.add(always_redraw(v1_arrow),
                 always_redraw(v2_arrow),
                 always_redraw(u1_arrow),
                 always_redraw(proj_arrow),
                 always_redraw(proj_drop),
                 always_redraw(w2_arrow),
                 always_redraw(u2_arrow))

        # Static labels
        self.add(always_redraw(lambda: Tex(r"$v_1$", color=BLUE, font_size=24).move_to(
            plane.c2p(v1[0] + 0.2, v1[1] + 0.2))))
        self.add(always_redraw(lambda: Tex(r"$v_2$", color=GREEN, font_size=24).move_to(
            plane.c2p(v2[0] - 0.2, v2[1] + 0.3))))
        def u1_lbl():
            s = stage_tr.get_value()
            if s < 0.9:
                return VMobject()
            return Tex(r"$u_1$", color=YELLOW, font_size=24).move_to(
                plane.c2p(u1[0] + 0.2, u1[1] - 0.15))
        def u2_lbl():
            s = stage_tr.get_value()
            if s < 3.4:
                return VMobject()
            return Tex(r"$u_2$", color=RED, font_size=24).move_to(
                plane.c2p(u2[0] - 0.25, u2[1] + 0.25))
        self.add(always_redraw(u1_lbl), always_redraw(u2_lbl))

        # Info
        info = VGroup(
            VGroup(Tex(r"stage $=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(rf"$v_2\cdot u_1={np.dot(v2, u1):.3f}$",
                color=ORANGE, font_size=20),
            VGroup(Tex(r"$u_1\cdot u_2=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=6,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(DL, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(int(stage_tr.get_value())))
        # u1 · u2 = 0 once both defined
        info[2][1].add_updater(lambda m: m.set_value(
            float(np.dot(u1, u2)) if stage_tr.get_value() >= 3.4 else 0.0))
        self.add(info)

        for target in [1.0, 2.0, 3.0, 3.5]:
            self.play(stage_tr.animate.set_value(target),
                      run_time=1.8, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.5)
