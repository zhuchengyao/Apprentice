from manim import *
import numpy as np


class QRDecompositionExample(Scene):
    """
    QR decomposition: A = QR where Q has orthonormal columns and R
    is upper triangular. Gram-Schmidt on columns of A produces Q;
    R records the projections.

    SINGLE_FOCUS:
      Two column vectors of A in 2D; ValueTracker step_tr reveals
      Gram-Schmidt steps: u_1 = a_1, e_1 = u_1/|u_1|, projection
      of a_2 onto e_1, u_2 = a_2 - proj, e_2 = u_2/|u_2|.
    """

    def construct(self):
        title = Tex(r"QR decomposition: $A = QR$ via Gram-Schmidt",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 4, 1], y_range=[-3, 3, 1],
                             x_length=9, y_length=6,
                             background_line_style={"stroke_opacity": 0.3}
                             ).move_to([-1, -0.3, 0])
        self.play(Create(plane))

        a1 = np.array([3, 1])
        a2 = np.array([1, 2])

        # Compute QR
        e1 = a1 / np.linalg.norm(a1)
        proj = np.dot(a2, e1) * e1
        u2 = a2 - proj
        e2 = u2 / np.linalg.norm(u2)

        step_tr = ValueTracker(0)

        def stage():
            s = int(round(step_tr.get_value()))
            origin_s = plane.c2p(0, 0)
            grp = VGroup()
            # Original columns
            if s >= 0:
                grp.add(Arrow(origin_s, plane.c2p(*a1),
                                color=BLUE, buff=0, stroke_width=5,
                                max_tip_length_to_length_ratio=0.15))
                grp.add(MathTex(r"a_1", color=BLUE, font_size=22
                                  ).next_to(plane.c2p(*a1), UR, buff=0.1))
                grp.add(Arrow(origin_s, plane.c2p(*a2),
                                color=GREEN, buff=0, stroke_width=5,
                                max_tip_length_to_length_ratio=0.15))
                grp.add(MathTex(r"a_2", color=GREEN, font_size=22
                                  ).next_to(plane.c2p(*a2), UR, buff=0.1))
            if s >= 1:
                grp.add(Arrow(origin_s, plane.c2p(*e1),
                                color=YELLOW, buff=0, stroke_width=6,
                                max_tip_length_to_length_ratio=0.2))
                grp.add(MathTex(r"e_1", color=YELLOW, font_size=22
                                  ).next_to(plane.c2p(*e1), DR, buff=0.1))
            if s >= 2:
                # proj of a_2 onto e_1
                grp.add(Arrow(origin_s, plane.c2p(*proj),
                                color=ORANGE, buff=0, stroke_width=4,
                                max_tip_length_to_length_ratio=0.2))
                grp.add(DashedLine(plane.c2p(*a2),
                                     plane.c2p(*proj),
                                     color=GREY_B, stroke_width=2))
            if s >= 3:
                grp.add(Arrow(plane.c2p(*proj),
                                plane.c2p(*(proj + u2)),
                                color=PURPLE, buff=0, stroke_width=4,
                                max_tip_length_to_length_ratio=0.2))
                grp.add(MathTex(r"u_2", color=PURPLE, font_size=20
                                  ).next_to(plane.c2p(*(proj + 0.5 * u2)),
                                              RIGHT, buff=0.1))
            if s >= 4:
                grp.add(Arrow(origin_s, plane.c2p(*e2),
                                color=RED, buff=0, stroke_width=6,
                                max_tip_length_to_length_ratio=0.2))
                grp.add(MathTex(r"e_2", color=RED, font_size=22
                                  ).next_to(plane.c2p(*e2), UL, buff=0.1))
            return grp

        self.add(always_redraw(stage))

        descriptions = [
            r"start: $a_1, a_2$",
            r"$e_1 = a_1 / \|a_1\|$",
            r"proj $a_2$ onto $e_1$",
            r"$u_2 = a_2 - $ proj",
            r"$e_2 = u_2 / \|u_2\|$",
        ]

        def desc_text():
            s = int(round(step_tr.get_value())) % len(descriptions)
            return MathTex(descriptions[s], color=YELLOW, font_size=22
                             ).to_edge(DOWN, buff=0.4)

        self.add(always_redraw(desc_text))

        for s in range(1, 5):
            self.play(step_tr.animate.set_value(s),
                       run_time=1.3, rate_func=smooth)
            self.wait(0.8)
        self.wait(0.5)
