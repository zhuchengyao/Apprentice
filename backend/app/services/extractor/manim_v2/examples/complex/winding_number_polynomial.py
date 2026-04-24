from manim import *
import numpy as np


class WindingNumberPolynomialExample(Scene):
    """
    Winding number of p(z) = z^n - 1 around a large circle (from
    _2018/WindingNumber_G). For a polynomial of degree n on a large
    enough circle the image winds n times around 0 — proving the
    Fundamental Theorem of Algebra.

    TWO_COLUMN:
      LEFT  — z-plane with a circle |z| = R traced by ValueTracker
              t_tr (full revolution).
      RIGHT — w-plane image with always_redraw trail for
              w = z^n - 1; winds n times around 0.
    """

    def construct(self):
        title = Tex(r"FTA via winding: $z^n - 1$ winds $n$ times",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        left = ComplexPlane(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                              x_length=5, y_length=5,
                              background_line_style={"stroke_opacity": 0.25}
                              ).move_to([-3.5, -0.3, 0])
        right = ComplexPlane(x_range=[-4, 4, 1], y_range=[-4, 4, 1],
                               x_length=5, y_length=5,
                               background_line_style={"stroke_opacity": 0.25}
                               ).move_to([3.5, -0.3, 0])
        self.play(Create(left), Create(right))

        z_lbl = MathTex(r"z\text{-plane}", color=WHITE, font_size=20
                         ).next_to(left, UP, buff=0.1)
        w_lbl = MathTex(r"w = z^n - 1", color=YELLOW, font_size=20
                         ).next_to(right, UP, buff=0.1)
        self.play(Write(z_lbl), Write(w_lbl))

        R = 1.5
        n = 3  # degree

        # Source circle
        source_circle = Circle(radius=left.c2p(R, 0)[0] - left.c2p(0, 0)[0],
                                 color=BLUE, stroke_width=2
                                 ).move_to(left.c2p(0, 0))
        self.play(Create(source_circle))

        t_tr = ValueTracker(0.0)

        def z_dot():
            t = t_tr.get_value()
            return Dot(left.c2p(R * np.cos(t), R * np.sin(t)),
                        color=BLUE, radius=0.12)

        def w_trail():
            t_cur = t_tr.get_value()
            pts = []
            ts = np.linspace(0, t_cur, max(10, int(200 * t_cur / (2 * PI))))
            for ti in ts:
                z = R * np.exp(1j * ti)
                w = z ** n - 1
                pts.append(right.c2p(w.real, w.imag))
            m = VMobject(color=YELLOW, stroke_width=3)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        def w_dot():
            t = t_tr.get_value()
            z = R * np.exp(1j * t)
            w = z ** n - 1
            return Dot(right.c2p(w.real, w.imag),
                        color=RED, radius=0.12)

        # Origin marker on w-plane
        origin_dot = Dot(right.c2p(0, 0), color=YELLOW_E, radius=0.1)
        origin_lbl = MathTex(r"0", color=YELLOW_E,
                               font_size=18).next_to(origin_dot, DR, buff=0.1)
        self.play(FadeIn(origin_dot), Write(origin_lbl))

        self.add(always_redraw(z_dot),
                  always_redraw(w_trail),
                  always_redraw(w_dot))

        def info():
            t = t_tr.get_value()
            winding = int(t / (2 * PI) * n)
            return VGroup(
                MathTex(rf"n = {n}", color=YELLOW, font_size=22),
                MathTex(rf"R = {R}", color=BLUE, font_size=22),
                MathTex(rf"\theta = {np.degrees(t):.0f}^\circ",
                         color=WHITE, font_size=22),
                MathTex(rf"\text{{winding so far}} = {t*n/(2*PI):.2f}",
                         color=RED, font_size=22),
                MathTex(r"\text{full: } n \text{ winds} = 3",
                         color=GREEN, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        self.play(t_tr.animate.set_value(2 * PI),
                   run_time=8, rate_func=linear)
        self.wait(0.5)
