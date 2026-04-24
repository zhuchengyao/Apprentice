from manim import *
import numpy as np


class GreensTheoremGeometricExample(Scene):
    """
    Green's theorem: ∮_γ (P dx + Q dy) = ∫∫_D (∂Q/∂x - ∂P/∂y) dA.
    Visualize with F = (-y/2, x/2) along a shape γ: ∮ F·dr gives
    the enclosed area.

    SINGLE_FOCUS:
      Closed curve γ parametrized by θ. ValueTracker θ_tr advances;
      always_redraw F-arrows along the traversed portion + running
      ∮ value approaching the enclosed area.
    """

    def construct(self):
        title = Tex(r"Green's theorem: $\oint (-y/2\,dx + x/2\,dy) = $ Area",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-3, 3, 1], y_range=[-2.5, 2.5, 1],
                             x_length=7, y_length=5,
                             background_line_style={"stroke_opacity": 0.25}
                             ).move_to([-2, -0.3, 0])
        self.play(Create(plane))

        # Closed curve: ellipse x = 2 cos θ, y = 1.3 sin θ
        a, b = 2.0, 1.3
        true_area = PI * a * b

        ellipse_pts = [plane.c2p(a * np.cos(t), b * np.sin(t))
                        for t in np.linspace(0, 2 * PI, 200)]
        ellipse = VMobject(color=YELLOW, stroke_width=3)
        ellipse.set_points_as_corners(ellipse_pts + [ellipse_pts[0]])
        self.play(Create(ellipse))

        theta_tr = ValueTracker(0.001)

        def traversed():
            t = theta_tr.get_value()
            pts = [plane.c2p(a * np.cos(ti), b * np.sin(ti))
                   for ti in np.linspace(0, t, max(10, int(120 * t / (2 * PI))))]
            m = VMobject(color=GREEN, stroke_width=5)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        def rider():
            t = theta_tr.get_value()
            return Dot(plane.c2p(a * np.cos(t), b * np.sin(t)),
                        color=RED, radius=0.12)

        def local_F():
            t = theta_tr.get_value()
            x = a * np.cos(t)
            y = b * np.sin(t)
            Fx, Fy = -y / 2, x / 2
            start = plane.c2p(x, y)
            end = plane.c2p(x + Fx, y + Fy)
            return Arrow(start, end, color=BLUE, buff=0,
                          stroke_width=4,
                          max_tip_length_to_length_ratio=0.2)

        def enclosed_shade():
            t = theta_tr.get_value()
            pts = [plane.c2p(0, 0)]
            for ti in np.linspace(0, t, 60):
                pts.append(plane.c2p(a * np.cos(ti), b * np.sin(ti)))
            if len(pts) < 3:
                return VGroup()
            return Polygon(*pts, color=GREEN,
                             fill_opacity=0.25, stroke_width=0)

        self.add(always_redraw(enclosed_shade),
                  always_redraw(traversed),
                  always_redraw(local_F),
                  always_redraw(rider))

        def running_integral(t):
            N = max(2, int(200 * t / (2 * PI)))
            ts = np.linspace(0.0001, t, N)
            total = 0.0
            for i in range(N - 1):
                tau = ts[i]
                x = a * np.cos(tau)
                y = b * np.sin(tau)
                dx = -a * np.sin(tau) * (ts[i + 1] - tau)
                dy = b * np.cos(tau) * (ts[i + 1] - tau)
                total += (-y / 2) * dx + (x / 2) * dy
            return total

        def info():
            t = theta_tr.get_value()
            val = running_integral(t)
            return VGroup(
                MathTex(rf"\theta = {np.degrees(t):.0f}^\circ",
                         color=RED, font_size=22),
                MathTex(rf"\oint_0^\theta (-y/2\,dx + x/2\,dy) = {val:.4f}",
                         color=GREEN, font_size=20),
                MathTex(rf"\text{{true area}} = \pi a b = {true_area:.4f}",
                         color=YELLOW, font_size=22),
                Tex(r"$\partial_x Q - \partial_y P = 1/2 - (-1/2) = 1$",
                     color=WHITE, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.3).shift(UP * 0.5)

        self.add(always_redraw(info))

        self.play(theta_tr.animate.set_value(2 * PI),
                   run_time=7, rate_func=linear)
        self.wait(0.4)
