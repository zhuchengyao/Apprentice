from manim import *
import numpy as np


class BlaschkeProductsExample(Scene):
    """
    Blaschke product: B(z) = ∏ (z - a_i)/(1 - \overline{a_i} z) maps
    the unit disk to itself and has zeros at a_i. Illustrate a
    single Blaschke factor (a = 0.5).

    SINGLE_FOCUS:
      Unit disk; ValueTracker θ_tr walks z around |z|=1; always_redraw
      B(z) in the same disk showing it still lands on the boundary.
    """

    def construct(self):
        title = Tex(r"Blaschke factor: $B(z) = \tfrac{z - a}{1 - \bar a z}$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = ComplexPlane(x_range=[-1.3, 1.3, 0.5],
                               y_range=[-1.3, 1.3, 0.5],
                               x_length=6, y_length=6,
                               background_line_style={"stroke_opacity": 0.3}
                               ).move_to([-2, -0.3, 0])
        self.play(Create(plane))

        # Unit circle
        unit_c = Circle(radius=plane.c2p(1, 0)[0] - plane.c2p(0, 0)[0],
                          color=YELLOW, stroke_width=2.5
                          ).move_to(plane.c2p(0, 0))
        self.play(Create(unit_c))

        a = 0.5 + 0.0j
        a_dot = Dot(plane.c2p(a.real, a.imag), color=RED, radius=0.12)
        a_lbl = MathTex(r"a = 0.5", color=RED, font_size=20
                          ).next_to(a_dot, UR, buff=0.1)
        self.play(FadeIn(a_dot), Write(a_lbl))

        theta_tr = ValueTracker(0.0)

        def z_dot():
            t = theta_tr.get_value()
            return Dot(plane.c2p(np.cos(t), np.sin(t)),
                        color=BLUE, radius=0.12)

        def Bz_dot():
            t = theta_tr.get_value()
            z = np.exp(1j * t)
            Bz = (z - a) / (1 - np.conj(a) * z)
            return Dot(plane.c2p(Bz.real, Bz.imag),
                        color=GREEN, radius=0.12)

        def z_trail():
            t_cur = theta_tr.get_value()
            pts = []
            for t in np.linspace(0, t_cur, max(20, int(100 * t_cur / (2 * PI)))):
                pts.append(plane.c2p(np.cos(t), np.sin(t)))
            m = VMobject(color=BLUE, stroke_width=2, stroke_opacity=0.5)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        def Bz_trail():
            t_cur = theta_tr.get_value()
            pts = []
            for t in np.linspace(0, t_cur, max(20, int(100 * t_cur / (2 * PI)))):
                z = np.exp(1j * t)
                Bz = (z - a) / (1 - np.conj(a) * z)
                pts.append(plane.c2p(Bz.real, Bz.imag))
            m = VMobject(color=GREEN, stroke_width=3)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        self.add(always_redraw(z_trail), always_redraw(Bz_trail),
                  always_redraw(z_dot), always_redraw(Bz_dot))

        def info():
            t = theta_tr.get_value()
            z = np.exp(1j * t)
            Bz = (z - a) / (1 - np.conj(a) * z)
            return VGroup(
                MathTex(rf"\theta = {np.degrees(t):.0f}^\circ",
                         color=BLUE, font_size=22),
                MathTex(rf"|B(z)| = {abs(Bz):.4f}",
                         color=GREEN, font_size=22),
                Tex(r"$|B(z)| = 1$ on unit circle",
                     color=YELLOW, font_size=20),
                MathTex(r"B(a) = 0", color=RED, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        self.play(theta_tr.animate.set_value(2 * PI),
                   run_time=6, rate_func=linear)
        self.wait(0.4)
