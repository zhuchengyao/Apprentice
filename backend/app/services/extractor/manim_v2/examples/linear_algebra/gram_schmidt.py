from manim import *
import numpy as np


class GramSchmidtExample(Scene):
    """
    Gram-Schmidt orthogonalization in ℝ²: given linearly independent
    v_1, v_2, produce orthonormal u_1, u_2.
      u_1 = v_1 / |v_1|
      u_2 = (v_2 - (v_2·u_1) u_1) / |v_2 - (v_2·u_1) u_1|

    SINGLE_FOCUS:
      2D plane with v_1 (BLUE), v_2 (GREEN), then fade to
      u_1, u_2 (YELLOW, RED). ValueTracker step_tr cycles through
      4 stages: input → u_1 → projection → u_2.
    """

    def construct(self):
        title = Tex(r"Gram-Schmidt: $\{v_1, v_2\} \to \{u_1, u_2\}$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 4, 1], y_range=[-3, 3, 1],
                             x_length=9, y_length=6,
                             background_line_style={"stroke_opacity": 0.3}
                             ).move_to([0, -0.3, 0])
        self.play(Create(plane))

        v1 = np.array([3, 1])
        v2 = np.array([1, 2])

        u1 = v1 / np.linalg.norm(v1)
        proj = np.dot(v2, u1) * u1
        v2_perp = v2 - proj
        u2 = v2_perp / np.linalg.norm(v2_perp)

        step_tr = ValueTracker(0)

        def stage_group():
            s = int(round(step_tr.get_value()))
            grp = VGroup()
            origin_s = plane.c2p(0, 0)
            if s >= 0:
                grp.add(Arrow(origin_s,
                                plane.c2p(v1[0], v1[1]),
                                color=BLUE, buff=0, stroke_width=5,
                                max_tip_length_to_length_ratio=0.15))
                grp.add(MathTex(r"v_1", color=BLUE, font_size=22
                                  ).next_to(plane.c2p(v1[0], v1[1]),
                                              UR, buff=0.1))
                grp.add(Arrow(origin_s,
                                plane.c2p(v2[0], v2[1]),
                                color=GREEN, buff=0, stroke_width=5,
                                max_tip_length_to_length_ratio=0.15))
                grp.add(MathTex(r"v_2", color=GREEN, font_size=22
                                  ).next_to(plane.c2p(v2[0], v2[1]),
                                              UR, buff=0.1))
            if s >= 1:
                grp.add(Arrow(origin_s,
                                plane.c2p(u1[0], u1[1]),
                                color=YELLOW, buff=0, stroke_width=6,
                                max_tip_length_to_length_ratio=0.2))
                grp.add(MathTex(r"u_1", color=YELLOW, font_size=22
                                  ).next_to(plane.c2p(u1[0], u1[1]),
                                              DR, buff=0.1))
            if s >= 2:
                # proj v2 onto u1
                grp.add(Arrow(origin_s,
                                plane.c2p(proj[0], proj[1]),
                                color=ORANGE, buff=0, stroke_width=4,
                                max_tip_length_to_length_ratio=0.2))
                # dashed perpendicular from v2 tip to proj tip
                grp.add(DashedLine(plane.c2p(v2[0], v2[1]),
                                     plane.c2p(proj[0], proj[1]),
                                     color=GREY_B, stroke_width=2))
            if s >= 3:
                # v2_perp vector from proj tip
                grp.add(Arrow(plane.c2p(proj[0], proj[1]),
                                plane.c2p(proj[0] + v2_perp[0],
                                             proj[1] + v2_perp[1]),
                                color=PURPLE, buff=0, stroke_width=4,
                                max_tip_length_to_length_ratio=0.2))
                # u2 from origin
                grp.add(Arrow(origin_s,
                                plane.c2p(u2[0], u2[1]),
                                color=RED, buff=0, stroke_width=6,
                                max_tip_length_to_length_ratio=0.2))
                grp.add(MathTex(r"u_2", color=RED, font_size=22
                                  ).next_to(plane.c2p(u2[0], u2[1]),
                                              UL, buff=0.1))
            return grp

        self.add(always_redraw(stage_group))

        explanations = [
            r"\text{start: } v_1, v_2",
            r"u_1 = v_1 / \|v_1\|",
            r"\text{proj: } (v_2 \cdot u_1) u_1",
            r"u_2 = (v_2 - \text{proj}) / \|\cdot\|",
        ]

        def step_label():
            s = int(round(step_tr.get_value())) % len(explanations)
            return MathTex(explanations[s],
                             color=YELLOW, font_size=24
                             ).to_edge(DOWN, buff=0.4)

        self.add(always_redraw(step_label))

        for s in [1, 2, 3]:
            self.play(step_tr.animate.set_value(s),
                       run_time=1.2, rate_func=smooth)
            self.wait(1.2)
        self.wait(0.5)
