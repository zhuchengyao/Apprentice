from manim import *
import numpy as np


class ImplicitDifferentiationTangentExample(Scene):
    """
    Implicit differentiation: for F(x, y) = 0, dy/dx = -F_x/F_y.

    Curve: x³ + y³ = 3xy (folium of Descartes). F(x, y) = x³ + y³ − 3xy.
    F_x = 3x² − 3y, F_y = 3y² − 3x ⇒ dy/dx = (y − x²)/(y² − x).

    SINGLE_FOCUS: plot folium; ValueTracker t_tr walks the point
    around the loop via parametrization x = 3t/(1+t³), y = 3t²/(1+t³).
    always_redraw tangent line + slope readout.
    """

    def construct(self):
        title = Tex(r"Implicit diff: $x^3+y^3=3xy$, $\frac{dy}{dx}=\frac{y-x^2}{y^2-x}$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[-2, 2.5, 1], y_range=[-2, 2.5, 1],
                    x_length=6.5, y_length=6.5,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(LEFT * 1.5 + DOWN * 0.2)
        self.play(Create(axes))

        # Folium loop via parametric form
        def folium(t):
            denom = 1 + t ** 3
            if abs(denom) < 1e-6:
                return np.array([0, 0])
            return np.array([3 * t / denom, 3 * t ** 2 / denom])

        loop_pts = []
        for t in np.linspace(-20, 20, 400):
            p = folium(t)
            if np.linalg.norm(p) < 5:
                loop_pts.append(axes.c2p(p[0], p[1]))
        loop = VMobject().set_points_as_corners(loop_pts)\
            .set_color(BLUE).set_stroke(width=2.5)
        self.play(Create(loop))

        t_tr = ValueTracker(0.3)

        def slope(x, y):
            num = y - x ** 2
            den = y ** 2 - x
            if abs(den) < 1e-6:
                return None
            return num / den

        def P_pt():
            return folium(t_tr.get_value())

        def tangent_line():
            p = P_pt()
            s = slope(*p)
            if s is None:
                # vertical tangent
                return Line(axes.c2p(p[0], p[1] - 1.2),
                             axes.c2p(p[0], p[1] + 1.2),
                             color=RED, stroke_width=4)
            dx = 0.9
            dy = s * dx
            return Line(axes.c2p(p[0] - dx, p[1] - dy),
                         axes.c2p(p[0] + dx, p[1] + dy),
                         color=RED, stroke_width=4)

        def P_dot():
            p = P_pt()
            return Dot(axes.c2p(p[0], p[1]), color=YELLOW, radius=0.12)

        self.add(always_redraw(tangent_line), always_redraw(P_dot))

        # Right panel
        def t_readout():
            return t_tr.get_value()

        info = VGroup(
            VGroup(Tex(r"$t=$", font_size=22),
                   DecimalNumber(0.3, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$x=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$y=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$dy/dx=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
            Tex(r"vertical tangent: $y^2=x$",
                color=GREY_B, font_size=20),
            Tex(r"$=$ at $t=2^{1/3}$",
                color=GREY_B, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.3)

        info[0][1].add_updater(lambda m: m.set_value(t_readout()))
        info[1][1].add_updater(lambda m: m.set_value(P_pt()[0]))
        info[2][1].add_updater(lambda m: m.set_value(P_pt()[1]))
        info[3][1].add_updater(
            lambda m: m.set_value(slope(*P_pt()) if slope(*P_pt()) is not None else 999.0))
        self.add(info)

        for tval in [1.0, 2 ** (1 / 3) - 0.01, 1.5, 0.7, 0.5]:
            self.play(t_tr.animate.set_value(tval),
                      run_time=2.0, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.5)
