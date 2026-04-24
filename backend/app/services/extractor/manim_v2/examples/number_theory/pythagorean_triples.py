from manim import *
import numpy as np


class PythagoreanTriplesExample(Scene):
    """
    Generate primitive Pythagorean triples from (m, n) pairs via
    Euclid's formula a = m² - n², b = 2mn, c = m² + n².

    TWO_COLUMN:
      LEFT  — NumberPlane showing the right triangle with sides
              (a, b, c). ValueTrackers m and n drive the triangle's
              side lengths via always_redraw; vertices update live
              and a²+b² = c² verification panel sits below.
      RIGHT — list of recently visited (m, n, a, b, c) tuples plus
              Euclid's parametric formula.
    """

    def construct(self):
        title = Tex(r"Euclid: $(m^2 - n^2,\ 2mn,\ m^2 + n^2)$ generates Pythagorean triples",
                    font_size=24).to_edge(UP, buff=0.4)
        self.play(Write(title))

        m_tr = ValueTracker(2)
        n_tr = ValueTracker(1)

        # Triangle anchor
        anchor = np.array([-3.5, -1.6, 0])

        def triangle_pts():
            m, n = m_tr.get_value(), n_tr.get_value()
            a = m * m - n * n
            b = 2 * m * n
            scale = 0.25  # scale so that c=29 (largest example) fits
            return (anchor,
                    anchor + np.array([a * scale, 0, 0]),
                    anchor + np.array([a * scale, b * scale, 0]))

        def triangle():
            v1, v2, v3 = triangle_pts()
            return Polygon(v1, v2, v3,
                           color=BLUE, fill_opacity=0.45, stroke_width=2)

        def side_labels():
            v1, v2, v3 = triangle_pts()
            m, n = m_tr.get_value(), n_tr.get_value()
            a = m * m - n * n
            b = 2 * m * n
            c = m * m + n * n
            grp = VGroup(
                MathTex(rf"a={int(a)}", color=GREEN, font_size=20).move_to(
                    (v1 + v2) / 2 + DOWN * 0.3),
                MathTex(rf"b={int(b)}", color=GREEN, font_size=20).move_to(
                    (v2 + v3) / 2 + RIGHT * 0.4),
                MathTex(rf"c={int(c)}", color=YELLOW, font_size=20).move_to(
                    (v1 + v3) / 2 + UP * 0.2 + LEFT * 0.3),
            )
            return grp

        self.add(always_redraw(triangle), always_redraw(side_labels))

        # RIGHT COLUMN
        rcol_x = +3.6

        def info_panel():
            m, n = m_tr.get_value(), n_tr.get_value()
            a = m * m - n * n
            b = 2 * m * n
            c = m * m + n * n
            return VGroup(
                MathTex(rf"m = {m:.0f},\ n = {n:.0f}",
                        color=WHITE, font_size=24),
                MathTex(rf"a = m^2 - n^2 = {int(a)}",
                        color=GREEN, font_size=22),
                MathTex(rf"b = 2mn = {int(b)}",
                        color=GREEN, font_size=22),
                MathTex(rf"c = m^2 + n^2 = {int(c)}",
                        color=YELLOW, font_size=22),
                MathTex(rf"a^2 + b^2 = {int(a*a + b*b)} = c^2",
                        color=ORANGE, font_size=24),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([rcol_x, +0.4, 0])

        self.add(always_redraw(info_panel))

        # Sweep through several (m, n) pairs
        for m_v, n_v in [(2, 1), (3, 2), (4, 1), (5, 2), (6, 1), (5, 4)]:
            self.play(m_tr.animate.set_value(m_v),
                      n_tr.animate.set_value(n_v),
                      run_time=1.6, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.5)
