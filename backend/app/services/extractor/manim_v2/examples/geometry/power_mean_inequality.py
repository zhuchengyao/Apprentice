from manim import *
import numpy as np


class PowerMeanInequalityExample(Scene):
    """
    Power-mean inequality: for positive a, b: HM ≤ GM ≤ AM ≤ QM
    (RMS). Visualize with specific a = 1, b = 4 and a semicircle
    construction.

    SINGLE_FOCUS:
      Semicircle on a segment of length a + b; vertical from the
      meeting point gives GM; radius gives AM; specific lines give
      HM, QM. All four values marked on vertical scale.
    """

    def construct(self):
        title = Tex(r"Power means: $HM \le GM \le AM \le QM$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        a_tr = ValueTracker(1.0)
        b_tr = ValueTracker(4.0)

        # Reference ground line
        base_y = -2.0
        base_start_x = -5.0

        def geom():
            a = a_tr.get_value()
            b = b_tr.get_value()
            AM = (a + b) / 2
            GM = np.sqrt(a * b)
            HM = 2 * a * b / (a + b)
            QM = np.sqrt((a * a + b * b) / 2)

            # Base segment [0, a] and [a, a+b] at base_y
            L = a + b
            scale = 8.0 / L  # fit in 8 units
            p_start = np.array([base_start_x, base_y, 0])
            p_mid = p_start + np.array([a * scale, 0, 0])
            p_end = p_start + np.array([(a + b) * scale, 0, 0])

            grp = VGroup()
            grp.add(Line(p_start, p_end, color=WHITE, stroke_width=3))
            grp.add(Dot(p_start, color=WHITE, radius=0.08))
            grp.add(Dot(p_mid, color=RED, radius=0.1))
            grp.add(Dot(p_end, color=WHITE, radius=0.08))

            # Labels for a, b
            grp.add(MathTex(rf"a = {a:.2f}", font_size=18, color=BLUE
                              ).move_to((p_start + p_mid) / 2 + DOWN * 0.35))
            grp.add(MathTex(rf"b = {b:.2f}", font_size=18, color=ORANGE
                              ).move_to((p_mid + p_end) / 2 + DOWN * 0.35))

            # Semicircle of diameter a+b
            center = (p_start + p_end) / 2
            radius = L * scale / 2
            semi = Arc(radius=radius, start_angle=0, angle=PI,
                        color=BLUE_D, stroke_width=2
                        ).move_arc_center_to(center)
            grp.add(semi)

            # GM: perpendicular from p_mid up to circle
            # GM length in scaled units = √(a*b) * scale
            GM_top = p_mid + np.array([0, GM * scale, 0])
            grp.add(Line(p_mid, GM_top, color=GREEN, stroke_width=3))
            grp.add(Dot(GM_top, color=GREEN, radius=0.08))
            grp.add(MathTex(rf"GM", color=GREEN, font_size=18
                              ).next_to(GM_top, UP, buff=0.1))

            # AM: radius to center of circle up
            AM_top = center + np.array([0, radius, 0])
            grp.add(Line(center, AM_top, color=YELLOW,
                           stroke_width=3))
            grp.add(MathTex(rf"AM", color=YELLOW, font_size=18
                              ).next_to(AM_top, UP, buff=0.1))

            # HM: drop from GM_top perpendicular to radius from center
            # HM = GM² / AM = 2ab/(a+b)
            # Visualize HM as horizontal from GM_top to AM-line
            GM_on_AM = np.array([center[0], GM_top[1], 0])
            grp.add(Line(GM_top, GM_on_AM, color=PINK,
                           stroke_width=2, stroke_opacity=0.7))
            # Actually HM is the portion of this line from GM_top
            # down to the center vertical... Simplify with labels
            HM_marker_y = base_y + HM * scale
            HM_marker = np.array([base_start_x - 0.3, HM_marker_y, 0])
            grp.add(Dot(HM_marker, color=PINK, radius=0.07))
            grp.add(MathTex(r"HM", color=PINK, font_size=16
                              ).next_to(HM_marker, LEFT, buff=0.1))

            # QM marker
            QM_marker_y = base_y + QM * scale
            QM_marker = np.array([base_start_x - 0.8, QM_marker_y, 0])
            grp.add(Dot(QM_marker, color=PURPLE, radius=0.07))
            grp.add(MathTex(r"QM", color=PURPLE, font_size=16
                              ).next_to(QM_marker, LEFT, buff=0.1))

            return grp

        self.add(always_redraw(geom))

        def info():
            a = a_tr.get_value()
            b = b_tr.get_value()
            AM = (a + b) / 2
            GM = np.sqrt(a * b)
            HM = 2 * a * b / (a + b)
            QM = np.sqrt((a * a + b * b) / 2)
            return VGroup(
                MathTex(rf"a = {a:.2f},\ b = {b:.2f}",
                         color=WHITE, font_size=22),
                MathTex(rf"HM = \tfrac{{2ab}}{{a+b}} = {HM:.3f}",
                         color=PINK, font_size=20),
                MathTex(rf"GM = \sqrt{{ab}} = {GM:.3f}",
                         color=GREEN, font_size=20),
                MathTex(rf"AM = \tfrac{{a+b}}{{2}} = {AM:.3f}",
                         color=YELLOW, font_size=20),
                MathTex(rf"QM = \sqrt{{\tfrac{{a^2+b^2}}{{2}}}} = {QM:.3f}",
                         color=PURPLE, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for av, bv in [(1, 4), (2, 3), (1, 7), (2, 2), (1, 4)]:
            self.play(a_tr.animate.set_value(av),
                       b_tr.animate.set_value(bv),
                       run_time=1.6, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
