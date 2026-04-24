from manim import *
import numpy as np


class PythagorasRightTriangleExample(Scene):
    """
    Pythagorean theorem for a right triangle: a² + b² = c².

    SINGLE_FOCUS:
      Right triangle with variable leg lengths (a, b) driven by
      ValueTrackers a_tr and b_tr; always_redraw rebuilds the
      triangle + three squares on the sides. Live a², b², a²+b², c²
      values stay equal each frame; tour through 4 (a, b) configs.
    """

    def construct(self):
        title = Tex(r"Right triangle: $a^2 + b^2 = c^2$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        a_tr = ValueTracker(3.0)
        b_tr = ValueTracker(2.0)

        # Origin for geometry (keep in left half)
        O = np.array([-5.0, -2.6, 0])

        def geom():
            a = a_tr.get_value()
            b = b_tr.get_value()
            c = np.hypot(a, b)
            # Scale to fit in [0, 3.6] on both axes
            S = 1.1
            A = O
            B = O + S * np.array([a, 0, 0])
            C = O + S * np.array([0, b, 0])

            grp = VGroup()
            tri = Polygon(A, B, C, color=YELLOW,
                           fill_opacity=0.35, stroke_width=3)
            grp.add(tri)

            # Square on side a (bottom), below A-B
            sq_a = Polygon(
                A, B, B + S * a * DOWN, A + S * a * DOWN,
                color=RED, fill_opacity=0.4, stroke_width=2)
            grp.add(sq_a)
            a_lbl = MathTex(rf"a^2 = {a**2:.2f}", font_size=20,
                             color=RED).move_to(
                (A + B) / 2 + np.array([0, -S * a / 2, 0]))
            grp.add(a_lbl)

            # Square on side b (left of A-C)
            sq_b = Polygon(
                A, C, C + S * b * LEFT, A + S * b * LEFT,
                color=BLUE, fill_opacity=0.4, stroke_width=2)
            grp.add(sq_b)
            b_lbl = MathTex(rf"b^2 = {b**2:.2f}", font_size=20,
                             color=BLUE).move_to(
                (A + C) / 2 + np.array([-S * b / 2, 0, 0]))
            grp.add(b_lbl)

            # Square on hypotenuse (outward)
            hyp_dir = (C - B) / np.linalg.norm(C - B)
            perp = np.array([-hyp_dir[1], hyp_dir[0], 0]) * S * c
            sq_c = Polygon(
                B, C, C + perp, B + perp,
                color=GREEN, fill_opacity=0.4, stroke_width=2)
            grp.add(sq_c)
            c_lbl = MathTex(rf"c^2 = {c**2:.2f}", font_size=20,
                             color=GREEN).move_to(
                (B + C) / 2 + perp / 2)
            grp.add(c_lbl)

            # triangle side labels
            ta = MathTex(rf"a = {a:.2f}", font_size=18,
                           color=RED).next_to((A + B) / 2, UP, buff=0.1)
            tb = MathTex(rf"b = {b:.2f}", font_size=18,
                           color=BLUE).next_to((A + C) / 2, RIGHT, buff=0.1)
            tc = MathTex(rf"c = {c:.2f}", font_size=18,
                           color=GREEN).next_to((B + C) / 2, hyp_dir, buff=0.1)
            grp.add(ta, tb, tc)
            return grp

        self.add(always_redraw(geom))

        def info():
            a = a_tr.get_value()
            b = b_tr.get_value()
            c = np.hypot(a, b)
            return VGroup(
                MathTex(rf"a = {a:.2f}", color=RED, font_size=24),
                MathTex(rf"b = {b:.2f}", color=BLUE, font_size=24),
                MathTex(rf"c = {c:.3f}", color=GREEN, font_size=24),
                MathTex(rf"a^2 + b^2 = {a**2 + b**2:.3f}",
                         color=YELLOW, font_size=22),
                MathTex(rf"c^2 = {c**2:.3f}", color=YELLOW, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.3, 1.5, 0])

        self.add(always_redraw(info))

        tour = [(3, 4), (1.5, 3.5), (2.5, 2.5), (4, 1), (3, 2)]
        for (a, b) in tour:
            self.play(a_tr.animate.set_value(a),
                       b_tr.animate.set_value(b),
                       run_time=1.8, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.4)
