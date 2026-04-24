from manim import *
import numpy as np


class CurlFieldExample(Scene):
    """
    Curl of a vector field: ValueTracker probe position sweeps
    through a rotating vector field F(x, y) = (-y, x)/r + ...
    while a small "paddle wheel" indicator at the probe point
    spins at rate ∝ (∂Q/∂x - ∂P/∂y). Two configurations
    (high-curl vs zero-curl) shown via Transform.

    TWO_COLUMN:
      LEFT  — 2D vector field arrows + probe wheel; ValueTracker
              phi_tr rotates 4-spoke paddle at ω ∝ curl.
      RIGHT — curl formula + live values + phase tour through 3
              test fields.
    """

    def construct(self):
        title = Tex(r"Curl $\nabla \times \vec F$: paddle-wheel spin rate",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 4, 1], y_range=[-3, 3, 1],
                             x_length=7, y_length=5.2,
                             background_line_style={"stroke_opacity": 0.25}
                             ).move_to([-2.5, -0.3, 0])
        self.play(Create(plane))

        # Static sparse vector field arrows for F1 = (-y, x): pure rotation
        def field_arrows(F, color):
            grp = VGroup()
            for xv in np.arange(-3, 3.1, 1.0):
                for yv in np.arange(-2, 2.1, 1.0):
                    vx, vy = F(xv, yv)
                    mag = np.hypot(vx, vy)
                    if mag < 1e-6:
                        continue
                    s = 0.4 / max(mag, 0.4)
                    start = plane.c2p(xv, yv)
                    end = plane.c2p(xv + s * vx, yv + s * vy)
                    grp.add(Arrow(start, end, buff=0, color=color,
                                   stroke_width=2, max_tip_length_to_length_ratio=0.3))
            return grp

        def F_rot(x, y):
            return (-y, x)

        def F_shear(x, y):
            return (y, 0)  # curl = -1

        def F_uniform(x, y):
            return (1, 0.5)  # curl = 0

        arrows = field_arrows(F_rot, BLUE)
        self.play(FadeIn(arrows))

        phi_tr = ValueTracker(0)

        wheel_center = np.array([0, 0, 0])

        def paddle():
            phi = phi_tr.get_value()
            grp = VGroup()
            for i in range(4):
                a = phi + i * PI / 2
                v = 0.7 * np.array([np.cos(a), np.sin(a), 0])
                grp.add(Line(plane.c2p(0, 0) - v,
                               plane.c2p(0, 0) + v,
                               color=YELLOW, stroke_width=4))
            grp.add(Dot(plane.c2p(0, 0), color=RED, radius=0.08))
            return grp

        self.add(always_redraw(paddle))

        # info panel
        state = {"curl": 2.0, "name": r"\vec F = (-y, x)"}

        def info():
            return VGroup(
                Tex(rf"${state['name']}$", color=BLUE, font_size=24),
                MathTex(rf"\text{{curl}} = {state['curl']:+.2f}",
                         color=YELLOW, font_size=24),
                MathTex(r"\omega = \tfrac{1}{2}(\partial_x Q - \partial_y P)",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.3, 1.2, 0])

        info_grp = info()
        self.add(info_grp)

        # Phase 1: F = (-y, x), curl = 2 → paddle spins fast CCW
        self.play(phi_tr.animate.set_value(PI),
                   run_time=2.5, rate_func=linear)

        # Transform to shear field (curl = -1)
        new_arrows = field_arrows(F_shear, TEAL)
        self.play(Transform(arrows, new_arrows))
        state["curl"] = -1.0
        state["name"] = r"\vec F = (y, 0)"
        new_info = info()
        self.play(Transform(info_grp, new_info))

        self.play(phi_tr.animate.set_value(PI / 2),
                   run_time=2.5, rate_func=linear)

        # Transform to uniform field (curl = 0)
        new_arrows = field_arrows(F_uniform, GREEN_B)
        self.play(Transform(arrows, new_arrows))
        state["curl"] = 0.0
        state["name"] = r"\vec F = (1, 1/2)"
        new_info = info()
        self.play(Transform(info_grp, new_info))

        self.wait(1.5)  # paddle freezes
        self.wait(0.4)
