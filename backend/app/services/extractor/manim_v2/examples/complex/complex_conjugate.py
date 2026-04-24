from manim import *
import numpy as np


class ComplexConjugateExample(Scene):
    """
    Complex conjugation as reflection across the real axis.

    TWO_COLUMN:
      LEFT  — ComplexPlane with two ValueTrackers a, b driving z = a + bi
              and its conjugate z̄ = a - bi. Always_redraw arrows for
              both, plus a dashed mirror line on the real axis. As b
              sweeps positive→negative, z and z̄ swap roles.
      RIGHT — live readouts of a, b, |z|, |z̄|, z·z̄ = a²+b², plus
              the algebraic identity. Watch z·z̄ stay always real and
              positive; |z| = |z̄| stays equal.
    """

    def construct(self):
        title = Tex(r"Complex conjugation: $\bar z = a - bi$ reflects $z$ across $\mathbb{R}$",
                    font_size=26).to_edge(UP, buff=0.4)
        self.play(Write(title))

        plane = ComplexPlane(
            x_range=[-3.2, 3.2, 1], y_range=[-2.4, 2.4, 1],
            x_length=6.4, y_length=4.8,
            background_line_style={"stroke_opacity": 0.3},
        ).move_to([-2.4, -0.4, 0])
        self.play(Create(plane))

        # Highlight real axis as the mirror line
        real_axis = Line(plane.c2p(-3.2, 0), plane.c2p(3.2, 0),
                         color=GREY_B, stroke_width=3)
        self.play(Create(real_axis))

        a_tr = ValueTracker(2.0)
        b_tr = ValueTracker(1.5)

        def z_arrow():
            a, b = a_tr.get_value(), b_tr.get_value()
            return Arrow(plane.c2p(0, 0), plane.c2p(a, b),
                         buff=0, color=YELLOW, stroke_width=5,
                         max_tip_length_to_length_ratio=0.10)

        def zbar_arrow():
            a, b = a_tr.get_value(), b_tr.get_value()
            return Arrow(plane.c2p(0, 0), plane.c2p(a, -b),
                         buff=0, color=ORANGE, stroke_width=5,
                         max_tip_length_to_length_ratio=0.10)

        def z_dot():
            a, b = a_tr.get_value(), b_tr.get_value()
            return Dot(plane.c2p(a, b), color=YELLOW, radius=0.10)

        def zbar_dot():
            a, b = a_tr.get_value(), b_tr.get_value()
            return Dot(plane.c2p(a, -b), color=ORANGE, radius=0.10)

        def z_lbl():
            a, b = a_tr.get_value(), b_tr.get_value()
            return MathTex(r"z", color=YELLOW, font_size=28).next_to(
                plane.c2p(a, b), UR, buff=0.05)

        def zbar_lbl():
            a, b = a_tr.get_value(), b_tr.get_value()
            return MathTex(r"\bar z", color=ORANGE, font_size=28).next_to(
                plane.c2p(a, -b), DR, buff=0.05)

        def reflection_segment():
            a, b = a_tr.get_value(), b_tr.get_value()
            return DashedLine(plane.c2p(a, b), plane.c2p(a, -b),
                              color=GREY_B, stroke_width=2)

        self.add(always_redraw(z_arrow), always_redraw(zbar_arrow),
                 always_redraw(z_dot), always_redraw(zbar_dot),
                 always_redraw(z_lbl), always_redraw(zbar_lbl),
                 always_redraw(reflection_segment))

        # RIGHT COLUMN
        rcol_x = +4.0

        def info_panel():
            a, b = a_tr.get_value(), b_tr.get_value()
            mod_z = np.sqrt(a ** 2 + b ** 2)
            return VGroup(
                MathTex(rf"a = {a:+.2f},\ b = {b:+.2f}",
                        color=WHITE, font_size=22),
                MathTex(rf"z = {a:+.2f}{b:+.2f}\,i",
                        color=YELLOW, font_size=22),
                MathTex(rf"\bar z = {a:+.2f}{-b:+.2f}\,i",
                        color=ORANGE, font_size=22),
                MathTex(rf"|z| = |\bar z| = {mod_z:.3f}",
                        color=GREEN, font_size=22),
                MathTex(rf"z \cdot \bar z = a^2 + b^2 = {mod_z**2:.3f}",
                        color=YELLOW, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([rcol_x, +1.2, 0])

        self.add(always_redraw(info_panel))

        identities = VGroup(
            MathTex(r"\overline{z + w} = \bar z + \bar w", color=GREY_B, font_size=22),
            MathTex(r"\overline{z \cdot w} = \bar z \cdot \bar w", color=GREY_B, font_size=22),
            MathTex(r"z + \bar z = 2\,\mathrm{Re}(z)", color=GREY_B, font_size=22),
            MathTex(r"z - \bar z = 2i\,\mathrm{Im}(z)", color=GREY_B, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([rcol_x, -2.0, 0])
        self.play(Write(identities))

        # Sweep through several (a, b) pairs
        for tgt in [(2.5, 1.0), (-1.8, 1.5), (-1.0, -2.0),
                    (1.0, -1.5), (0.0, 1.5), (2.0, 1.5)]:
            self.play(a_tr.animate.set_value(tgt[0]),
                      b_tr.animate.set_value(tgt[1]),
                      run_time=1.5, rate_func=smooth)
        self.wait(0.8)
