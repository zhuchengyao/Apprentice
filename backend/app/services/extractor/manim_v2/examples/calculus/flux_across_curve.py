from manim import *
import numpy as np


class FluxAcrossCurveExample(Scene):
    """
    Flux of F across a closed curve γ: ∮ F · n̂ ds. For F = (x, y)
    (div = 2) and γ = unit circle: flux = ∫∫ ∇·F dA = 2 · π = 2π.

    SINGLE_FOCUS:
      NumberPlane with unit circle + vector field F = (x, y); ValueTracker
      t_tr moves rider along γ; always_redraw running flux sum + local
      outward normal + F components.
    """

    def construct(self):
        title = Tex(r"Flux: $\oint \vec F \cdot \hat n\,ds = \iint \nabla\cdot\vec F\,dA$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-2.5, 2.5, 1], y_range=[-2, 2, 1],
                             x_length=8, y_length=6,
                             background_line_style={"stroke_opacity": 0.25}
                             ).move_to([-1, -0.3, 0])
        self.play(Create(plane))

        # Unit circle
        circle = Circle(radius=plane.c2p(1, 0)[0] - plane.c2p(0, 0)[0],
                          color=YELLOW, stroke_width=3
                          ).move_to(plane.c2p(0, 0))
        self.play(Create(circle))

        # Sparse field F = (x, y) arrows
        field = VGroup()
        for xv in np.arange(-2, 2.1, 0.8):
            for yv in np.arange(-1.8, 1.9, 0.7):
                Fx = xv
                Fy = yv
                mag = np.hypot(Fx, Fy)
                if mag < 0.1:
                    continue
                s = 0.25 / max(mag, 0.25)
                start = plane.c2p(xv, yv)
                end = plane.c2p(xv + s * Fx, yv + s * Fy)
                field.add(Arrow(start, end, color=BLUE_D,
                                  buff=0, stroke_width=1.5,
                                  max_tip_length_to_length_ratio=0.3))
        self.play(FadeIn(field))

        t_tr = ValueTracker(0.0)

        def rider():
            t = t_tr.get_value()
            return Dot(plane.c2p(np.cos(t), np.sin(t)),
                        color=RED, radius=0.11)

        def normal_arrow():
            t = t_tr.get_value()
            x, y = np.cos(t), np.sin(t)
            # Outward normal = (x, y) on unit circle
            start = plane.c2p(x, y)
            end = plane.c2p(x + 0.4 * x, y + 0.4 * y)
            return Arrow(start, end, color=GREEN, buff=0,
                          stroke_width=4,
                          max_tip_length_to_length_ratio=0.25)

        def F_local():
            t = t_tr.get_value()
            x, y = np.cos(t), np.sin(t)
            Fx, Fy = x, y  # F at point
            start = plane.c2p(x, y)
            end = plane.c2p(x + 0.3 * Fx, y + 0.3 * Fy)
            return Arrow(start, end, color=ORANGE, buff=0,
                          stroke_width=4,
                          max_tip_length_to_length_ratio=0.25)

        self.add(always_redraw(rider),
                  always_redraw(normal_arrow),
                  always_redraw(F_local))

        def running_flux(t_cur):
            # ∮ F · n ds for F = (x, y) on unit circle:
            # F · n = x·x + y·y = 1 → flux(θ) = θ (arc length)
            return t_cur

        def info():
            t = t_tr.get_value()
            flux = running_flux(t)
            return VGroup(
                MathTex(rf"\theta = {np.degrees(t):.0f}^\circ",
                         color=RED, font_size=22),
                MathTex(rf"\vec F \cdot \hat n = 1 \text{{ at every point}}",
                         color=ORANGE, font_size=20),
                MathTex(rf"\text{{running flux}} = \theta = {flux:.3f}",
                         color=GREEN, font_size=20),
                MathTex(rf"\text{{total}} = 2\pi \approx 6.283",
                         color=YELLOW, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.3).shift(UP * 0.5)

        self.add(always_redraw(info))

        self.play(t_tr.animate.set_value(2 * PI),
                   run_time=7, rate_func=linear)
        self.wait(0.4)
