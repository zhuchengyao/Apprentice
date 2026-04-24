from manim import *
import numpy as np


class ResidueTheoremSimplePoleExample(Scene):
    """
    Residue theorem for a simple pole: ∮_γ f(z) dz = 2πi · Res(f, z_0)
    for f = 1/(z - z_0)² + 1/(z - z_0): the first has residue 0,
    the second has residue 1 → integral is 2πi.

    COMPARISON:
      LEFT z-plane with contour + two pole markers; RIGHT running
      integral value for each, converging to 0 and 2πi.
    """

    def construct(self):
        title = Tex(r"Residue theorem: $\oint f\,dz = 2\pi i \cdot \text{Res}(f, z_0)$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = ComplexPlane(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                               x_length=5, y_length=5,
                               background_line_style={"stroke_opacity": 0.25}
                               ).move_to([-3.5, -0.3, 0])
        self.play(Create(plane))

        R = 1.5
        z0 = 0.5 + 0.0j
        gamma_circ = Circle(radius=plane.c2p(R, 0)[0] - plane.c2p(0, 0)[0],
                              color=BLUE, stroke_width=3
                              ).move_to(plane.c2p(0, 0))
        pole_dot = Dot(plane.c2p(z0.real, z0.imag),
                         color=RED, radius=0.12)
        pole_lbl = MathTex(r"z_0", color=RED, font_size=22
                             ).next_to(pole_dot, UR, buff=0.1)
        self.play(Create(gamma_circ), FadeIn(pole_dot), Write(pole_lbl))

        theta_tr = ValueTracker(0.0)

        def arc_trail():
            t = theta_tr.get_value()
            pts = [plane.c2p(R * np.cos(ti), R * np.sin(ti))
                   for ti in np.linspace(0, t, max(10, int(100 * t / (2 * PI))))]
            m = VMobject(color=YELLOW, stroke_width=4)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        def pos_dot():
            t = theta_tr.get_value()
            return Dot(plane.c2p(R * np.cos(t), R * np.sin(t)),
                        color=YELLOW, radius=0.1)

        self.add(always_redraw(arc_trail), always_redraw(pos_dot))

        # RIGHT: integral progression axes
        ax = Axes(x_range=[0, 2 * PI + 0.1, PI / 2],
                   y_range=[-1, 7, 1],
                   x_length=5.5, y_length=4, tips=False,
                   axis_config={"font_size": 14}).move_to([3, -0.3, 0])
        xl = MathTex(r"\theta", font_size=20).next_to(ax, DOWN, buff=0.1)
        yl = MathTex(r"\text{Im}\,I(\theta)", font_size=18).next_to(ax, LEFT, buff=0.1)
        self.play(Create(ax), Write(xl), Write(yl))

        # Reference 2π line
        two_pi_line = DashedLine(ax.c2p(0, 2 * PI), ax.c2p(2 * PI, 2 * PI),
                                   color=GREEN, stroke_width=2)
        two_pi_lbl = MathTex(r"2\pi", color=GREEN,
                               font_size=20).next_to(ax.c2p(0, 2 * PI), LEFT, buff=0.1)
        zero_line = DashedLine(ax.c2p(0, 0), ax.c2p(2 * PI, 0),
                                 color=ORANGE, stroke_width=2)
        zero_lbl = MathTex(r"0", color=ORANGE,
                             font_size=20).next_to(ax.c2p(0, 0), LEFT, buff=0.1)
        self.play(Create(two_pi_line), Create(zero_line),
                   Write(two_pi_lbl), Write(zero_lbl))

        def I1(t):
            """Integral of 1/(z - z0) around partial arc, N trapezoidal."""
            N = max(2, int(200 * t / (2 * PI)))
            taus = np.linspace(0.0001, t, N)
            total = 0 + 0j
            for i in range(N - 1):
                tau = taus[i]
                z = R * np.exp(1j * tau)
                dz = 1j * R * np.exp(1j * tau) * (taus[i + 1] - tau)
                total += dz / (z - z0)
            return total

        def I2(t):
            """Integral of 1/(z - z0)²."""
            N = max(2, int(200 * t / (2 * PI)))
            taus = np.linspace(0.0001, t, N)
            total = 0 + 0j
            for i in range(N - 1):
                tau = taus[i]
                z = R * np.exp(1j * tau)
                dz = 1j * R * np.exp(1j * tau) * (taus[i + 1] - tau)
                total += dz / (z - z0) ** 2
            return total

        def trace_1():
            t_cur = theta_tr.get_value()
            pts = []
            step = 0.05
            t = 0.0
            while t <= t_cur:
                val = I1(t)
                pts.append(ax.c2p(t, val.imag))
                t += step
            pts.append(ax.c2p(t_cur, I1(t_cur).imag))
            m = VMobject(color=GREEN, stroke_width=3)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        def trace_2():
            t_cur = theta_tr.get_value()
            pts = []
            step = 0.05
            t = 0.0
            while t <= t_cur:
                val = I2(t)
                pts.append(ax.c2p(t, val.imag))
                t += step
            pts.append(ax.c2p(t_cur, I2(t_cur).imag))
            m = VMobject(color=ORANGE, stroke_width=3)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        self.add(always_redraw(trace_1), always_redraw(trace_2))

        legend = VGroup(
            Tex(r"GREEN: $f = 1/(z - z_0)$, Res $= 1$",
                 color=GREEN, font_size=18),
            Tex(r"ORANGE: $f = 1/(z - z_0)^2$, Res $= 0$",
                 color=ORANGE, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.3)
        self.play(Write(legend))

        self.play(theta_tr.animate.set_value(2 * PI),
                   run_time=7, rate_func=linear)
        self.wait(0.5)
