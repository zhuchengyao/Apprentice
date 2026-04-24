from manim import *
import numpy as np


class SimpsonAdaptiveQuadratureExample(Scene):
    """
    Adaptive Simpson: recursively subdivide intervals where the
    rule's error estimate exceeds tolerance. Concentrates nodes
    where f changes rapidly.

    Example: f(x) = 1/(1 + 25 x²) on [-1, 1] (Runge function).

    SINGLE_FOCUS: ValueTracker tol_tr → refinement depth.
    always_redraw node placement.
    """

    def construct(self):
        title = Tex(r"Adaptive Simpson: nodes cluster at high curvature",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[-1, 1, 0.5], y_range=[0, 1.1, 0.3],
                    x_length=9, y_length=4,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(DOWN * 0.5)
        self.play(Create(axes))

        def f(x): return 1 / (1 + 25 * x * x)
        f_curve = axes.plot(f, x_range=[-1, 1], color=BLUE, stroke_width=3)
        self.add(f_curve)

        def simpson(a, b, fa, fm, fb):
            return (b - a) / 6 * (fa + 4 * fm + fb)

        def adaptive_nodes(a, b, tol, depth=0, max_depth=9):
            fa, fb = f(a), f(b)
            m = (a + b) / 2
            fm = f(m)
            whole = simpson(a, b, fa, fm, fb)
            lm = (a + m) / 2
            rm = (m + b) / 2
            flm, frm = f(lm), f(rm)
            left = simpson(a, m, fa, flm, fm)
            right = simpson(m, b, fm, frm, fb)
            err = abs(left + right - whole) / 15
            nodes = [a, m, b]
            if depth >= max_depth or err < tol:
                return nodes
            nodes = (adaptive_nodes(a, m, tol / 2, depth + 1, max_depth)
                     + adaptive_nodes(m, b, tol / 2, depth + 1, max_depth))
            return sorted(set(nodes))

        tol_tr = ValueTracker(0.1)

        def tol_now():
            return max(0.0005, min(0.5, tol_tr.get_value()))

        def node_dots():
            nodes = adaptive_nodes(-1, 1, tol_now())
            grp = VGroup()
            for x in nodes:
                grp.add(Dot(axes.c2p(x, f(x)), color=RED, radius=0.08))
                grp.add(DashedLine(axes.c2p(x, 0), axes.c2p(x, f(x)),
                                    color=RED, stroke_width=1, stroke_opacity=0.45))
            return grp

        self.add(always_redraw(node_dots))

        info = VGroup(
            VGroup(Tex(r"tolerance $=$", font_size=22),
                   DecimalNumber(0.1, num_decimal_places=5,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"nodes $=$", font_size=22),
                   DecimalNumber(3, num_decimal_places=0,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
            Tex(r"$f(x)=1/(1+25x^2)$ (Runge)",
                color=BLUE, font_size=22),
            Tex(r"density $\uparrow$ at sharp peak",
                color=RED, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(tol_now()))
        info[1][1].add_updater(lambda m: m.set_value(len(adaptive_nodes(-1, 1, tol_now()))))
        self.add(info)

        for t_val in [0.03, 0.005, 0.001, 0.0005, 0.1]:
            self.play(tol_tr.animate.set_value(t_val),
                      run_time=1.8, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.5)
