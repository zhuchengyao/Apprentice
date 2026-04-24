from manim import *
import numpy as np


class GreensTheoremExample(Scene):
    """
    Green's theorem: ∮_∂D (P dx + Q dy) = ∬_D (∂Q/∂x − ∂P/∂y) dA.

    F = (P, Q) = (-y/2, x/2) so ∂Q/∂x − ∂P/∂y = 1; line integral
    equals area of D. D is a unit-radius lemniscate-like curve; live
    ValueTracker t_tr sweeps boundary param; always_redraw partial
    traced arc + live signed-area readout via shoelace on traced arc.
    """

    def construct(self):
        title = Tex(r"Green: $\oint_{\partial D}(P\,dx + Q\,dy) = \iint_D (Q_x - P_y)\,dA$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-2.5, 2.5], y_range=[-1.5, 1.5],
                            x_length=6, y_length=3.6,
                            background_line_style={"stroke_opacity": 0.3}).shift(LEFT * 2)
        self.play(Create(plane))

        def curve(t):
            r = np.sqrt(max(0, np.cos(2 * t)))
            x = 1.4 * r * np.cos(t)
            y = 1.4 * r * np.sin(t)
            return plane.c2p(x, y)

        # Lemniscate parametrized piecewise
        full = VMobject().set_points_smoothly(
            [curve(t) for t in np.linspace(-PI / 4, PI / 4, 60)]
        ).set_color(BLUE)
        full2 = VMobject().set_points_smoothly(
            [curve(t) for t in np.linspace(3 * PI / 4, 5 * PI / 4, 60)]
        ).set_color(BLUE)

        # Simpler: use a smooth oval so curl-1 computation is clean.
        oval = ParametricFunction(
            lambda t: plane.c2p(1.6 * np.cos(t), 0.9 * np.sin(t) + 0.25 * np.sin(3 * t)),
            t_range=[0, TAU], color=BLUE, stroke_width=3,
        )
        self.play(Create(oval))

        t_tr = ValueTracker(0.0)

        def traced():
            t = t_tr.get_value()
            return ParametricFunction(
                lambda s: plane.c2p(1.6 * np.cos(s), 0.9 * np.sin(s) + 0.25 * np.sin(3 * s)),
                t_range=[0, max(t, 1e-3)], color=ORANGE, stroke_width=6,
            )

        def probe_dot():
            t = t_tr.get_value()
            return Dot(plane.c2p(1.6 * np.cos(t), 0.9 * np.sin(t) + 0.25 * np.sin(3 * t)),
                       color=YELLOW, radius=0.1)

        self.add(always_redraw(traced), always_redraw(probe_dot))

        def partial_area():
            # shoelace area of traced arc + closing chord to start
            t = t_tr.get_value()
            if t < 1e-3:
                return 0.0
            ss = np.linspace(0, t, 80)
            xs = 1.6 * np.cos(ss)
            ys = 0.9 * np.sin(ss) + 0.25 * np.sin(3 * ss)
            A = 0.5 * abs(np.sum(xs[:-1] * ys[1:] - xs[1:] * ys[:-1])
                          + xs[-1] * ys[0] - xs[0] * ys[-1])
            return A

        info = VGroup(
            Tex(r"$P=-y/2$", font_size=22),
            Tex(r"$Q=x/2$", font_size=22),
            Tex(r"$Q_x - P_y = 1$", color=GREEN, font_size=22),
            DecimalNumber(0.0, num_decimal_places=3,
                          font_size=22).set_color(ORANGE),
            Tex(r"(shoelace of traced arc)", font_size=18, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4).shift(UP * 0.3)
        info[3].add_updater(lambda m: m.set_value(partial_area()))
        self.add(info)

        self.play(t_tr.animate.set_value(TAU), run_time=6, rate_func=linear)
        self.wait(0.8)

        # Final stamp
        final_area = 0.5 * abs(np.trapezoid(
            1.6 * np.cos(np.linspace(0, TAU, 400)) * np.gradient(
                0.9 * np.sin(np.linspace(0, TAU, 400)) + 0.25 * np.sin(3 * np.linspace(0, TAU, 400))
            )
            - (0.9 * np.sin(np.linspace(0, TAU, 400)) + 0.25 * np.sin(3 * np.linspace(0, TAU, 400)))
            * np.gradient(1.6 * np.cos(np.linspace(0, TAU, 400)))
        ))
        final_line = Tex(rf"$\oint = \iint 1\,dA \approx {final_area:.3f}$",
                         color=YELLOW, font_size=26).next_to(info, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(Write(final_line))
        self.wait(1.0)
