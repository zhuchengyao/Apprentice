from manim import *
import numpy as np


class LagrangeMultipliersExample(Scene):
    """
    Lagrange multipliers: to extremize f(x, y) subject to g(x, y)=c,
    at optimum ∇f = λ ∇g. Example: maximize f = xy subject to
    x² + y² = 1 (unit circle). Max at (±1/√2, ±1/√2), value 0.5.

    SINGLE_FOCUS NumberPlane. ValueTracker theta_tr moves a YELLOW
    point around constraint circle. always_redraw builds level curves
    of f near current value + ∇f and ∇g arrows at the point. When
    the point hits the optimum, gradients become parallel (and RED).
    Live (x, y, f, ∇f·tangent).
    """

    def construct(self):
        title = Tex(r"Lagrange: $\nabla f=\lambda\nabla g$ at constrained optimum",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-2, 2, 0.5], y_range=[-2, 2, 0.5],
                            x_length=6.5, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(LEFT * 1.8 + DOWN * 0.2)
        self.play(Create(plane))

        # Constraint circle g(x, y) = x² + y² = 1
        circ = Circle(radius=plane.x_length / (plane.x_range[1] - plane.x_range[0]),
                      color=BLUE, stroke_width=3).move_to(plane.c2p(0, 0))
        circ_lbl = Tex(r"$g=x^2+y^2=1$", color=BLUE, font_size=22).to_corner(UR, buff=0.3).shift(UP * 0.5)
        self.play(Create(circ), Write(circ_lbl))

        theta_tr = ValueTracker(0.3)

        def P_pt():
            t = theta_tr.get_value()
            return np.array([np.cos(t), np.sin(t)])

        def point_dot():
            P = P_pt()
            return Dot(plane.c2p(P[0], P[1]), color=YELLOW, radius=0.11)

        def grad_f_arrow():
            P = P_pt()
            # ∇f = (y, x)
            gf = np.array([P[1], P[0]])
            gf = gf * 0.6
            return Arrow(plane.c2p(P[0], P[1]),
                          plane.c2p(P[0] + gf[0], P[1] + gf[1]),
                          color=GREEN, buff=0, stroke_width=3,
                          max_tip_length_to_length_ratio=0.2)

        def grad_g_arrow():
            P = P_pt()
            # ∇g = (2x, 2y)
            gg = 2 * P
            gg = gg * 0.3
            return Arrow(plane.c2p(P[0], P[1]),
                          plane.c2p(P[0] + gg[0], P[1] + gg[1]),
                          color=ORANGE, buff=0, stroke_width=3,
                          max_tip_length_to_length_ratio=0.2)

        def parallel_marker():
            P = P_pt()
            gf = np.array([P[1], P[0]])
            gg = 2 * P
            # angle between
            cross = gf[0] * gg[1] - gf[1] * gg[0]
            if abs(cross) < 0.01:
                return Dot(plane.c2p(P[0], P[1]), color=RED, radius=0.18,
                            stroke_width=2, fill_opacity=0)
            return VMobject()

        self.add(always_redraw(point_dot),
                 always_redraw(grad_f_arrow),
                 always_redraw(grad_g_arrow),
                 always_redraw(parallel_marker))

        # Level curves of f=xy
        def level_curves():
            grp = VGroup()
            for L in [-0.5, -0.25, 0, 0.25, 0.5]:
                # f(x, y)=L ⇒ y=L/x (2 branches)
                for sign in [+1]:
                    try:
                        if abs(L) < 0.01:
                            # x=0 and y=0 axes
                            grp.add(Line(plane.c2p(-2, 0), plane.c2p(2, 0),
                                          color=GREY_B, stroke_width=1,
                                          stroke_opacity=0.5))
                            grp.add(Line(plane.c2p(0, -2), plane.c2p(0, 2),
                                          color=GREY_B, stroke_width=1,
                                          stroke_opacity=0.5))
                        else:
                            hyp = ParametricFunction(
                                lambda t, L=L: plane.c2p(t, L / t),
                                t_range=[max(0.1, abs(L) / 1.9), 1.95]
                                if L > 0 else [max(0.1, abs(L) / 1.9), 1.95],
                                color=TEAL, stroke_width=1.5,
                                stroke_opacity=0.45)
                            grp.add(hyp)
                            hyp2 = ParametricFunction(
                                lambda t, L=L: plane.c2p(-t, -L / t),
                                t_range=[max(0.1, abs(L) / 1.9), 1.95],
                                color=TEAL, stroke_width=1.5,
                                stroke_opacity=0.45)
                            grp.add(hyp2)
                    except Exception:
                        pass
            return grp
        self.add(level_curves())

        # Info
        def f_val():
            P = P_pt()
            return float(P[0] * P[1])

        def tangent_component():
            # d(f)/dθ along constraint = cos(2θ)
            return float(np.cos(2 * theta_tr.get_value()))

        info = VGroup(
            Tex(r"$f(x,y)=xy$", color=GREEN, font_size=22),
            VGroup(Tex(r"$(x,y)=$", font_size=22),
                   DecimalNumber(1.0, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW),
                   Tex(r", ", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW)
                   ).arrange(RIGHT, buff=0.05),
            VGroup(Tex(r"$f=xy=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$df/d\theta=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
            Tex(r"zero at $\theta=\pi/4, 3\pi/4, ...$",
                color=RED, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.2)
        info[1][1].add_updater(lambda m: m.set_value(P_pt()[0]))
        info[1][3].add_updater(lambda m: m.set_value(P_pt()[1]))
        info[2][1].add_updater(lambda m: m.set_value(f_val()))
        info[3][1].add_updater(lambda m: m.set_value(tangent_component()))
        self.add(info)

        for target in [PI / 4, PI / 2, 3 * PI / 4, PI, 5 * PI / 4, 3 * PI / 2, TAU - 0.01]:
            self.play(theta_tr.animate.set_value(target),
                      run_time=1.4, rate_func=smooth)
            self.wait(0.25)
        self.wait(0.5)
