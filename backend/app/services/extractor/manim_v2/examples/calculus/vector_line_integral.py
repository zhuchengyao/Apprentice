from manim import *
import numpy as np


class VectorLineIntegralExample(Scene):
    """
    Vector line integral ∫_γ F · dr along a curve γ. For F(x, y) =
    (x² y, x) and γ = unit circle CCW, compute ∮ F · dr.

    SINGLE_FOCUS:
      Vector field sketch + closed curve γ; ValueTracker t_tr
      advances along γ; always_redraw running ∫ F · dr. Final value
      equals ∫∫_D (∂Q/∂x - ∂P/∂y) dA = ∫∫ (1 - x²) dA (Green's thm).
    """

    def construct(self):
        title = Tex(r"$\oint_\gamma \vec F \cdot d\vec r$ via Green's theorem",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                             x_length=6, y_length=6,
                             background_line_style={"stroke_opacity": 0.25}
                             ).move_to([-3, -0.3, 0])
        self.play(Create(plane))

        # Sparse field arrows for F = (x²·y, x)
        field = VGroup()
        for xv in np.arange(-1.5, 1.6, 0.5):
            for yv in np.arange(-1.5, 1.6, 0.5):
                Fx = xv ** 2 * yv
                Fy = xv
                mag = np.hypot(Fx, Fy)
                s = 0.3 / max(mag, 0.3)
                start = plane.c2p(xv, yv)
                end = plane.c2p(xv + s * Fx, yv + s * Fy)
                field.add(Arrow(start, end, color=BLUE_D,
                                  buff=0, stroke_width=1.5,
                                  max_tip_length_to_length_ratio=0.3))
        self.play(FadeIn(field))

        # Unit circle γ
        circ = Circle(radius=plane.c2p(1, 0)[0] - plane.c2p(0, 0)[0],
                        color=YELLOW, stroke_width=3
                        ).move_to(plane.c2p(0, 0))
        self.play(Create(circ))

        t_tr = ValueTracker(0.0)

        def rider():
            t = t_tr.get_value()
            return Dot(plane.c2p(np.cos(t), np.sin(t)),
                        color=RED, radius=0.11)

        def arc_trail():
            t_cur = t_tr.get_value()
            pts = [plane.c2p(np.cos(ti), np.sin(ti))
                   for ti in np.linspace(0, t_cur, max(10, int(60 * t_cur / (2 * PI))))]
            m = VMobject(color=YELLOW, stroke_width=5)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        self.add(always_redraw(arc_trail), always_redraw(rider))

        def running_integral(t_cur):
            N = max(2, int(200 * t_cur / (2 * PI)))
            ts = np.linspace(0, t_cur, N)
            total = 0.0
            for i in range(N - 1):
                t = ts[i]
                x = np.cos(t)
                y = np.sin(t)
                # dr = (-sin t, cos t) dt
                F = np.array([x ** 2 * y, x])
                dr = np.array([-np.sin(t), np.cos(t)]) * (ts[i + 1] - t)
                total += np.dot(F, dr)
            return total

        def info():
            t = t_tr.get_value()
            val = running_integral(t)
            # Green's: ∫∫_D (∂Q/∂x - ∂P/∂y) dA = ∫∫ (1 - x²) dA
            # over unit disk: A = π, ∫∫ x² dA = π/4
            # So ∫∫ (1-x²) dA = π - π/4 = 3π/4 ≈ 2.356
            return VGroup(
                MathTex(rf"\theta = {np.degrees(t):.0f}^\circ",
                         color=WHITE, font_size=22),
                MathTex(rf"\int_0^\theta \vec F\cdot d\vec r = {val:.4f}",
                         color=YELLOW, font_size=22),
                MathTex(r"\vec F = (x^2 y,\ x)", color=BLUE, font_size=20),
                MathTex(r"\text{Green: } \oint = \iint_D (1 - x^2)\,dA",
                         color=GREEN, font_size=20),
                MathTex(r"= \pi - \pi/4 = 3\pi/4 \approx 2.356",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        self.play(t_tr.animate.set_value(2 * PI),
                   run_time=6, rate_func=linear)
        self.wait(0.4)
