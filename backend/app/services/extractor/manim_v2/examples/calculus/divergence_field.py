from manim import *
import numpy as np


class DivergenceFieldExample(Scene):
    """
    Divergence of a vector field: a small GREEN area element around
    the probe point expands (∇·F > 0), shrinks (< 0), or stays
    constant (= 0) under the flow.

    TWO_COLUMN:
      LEFT  — plane with field arrows; small disk at origin grows
              or shrinks via ValueTracker s_tr driving radius
              e^(div·s). Transform cycles through 3 fields.
      RIGHT — live divergence, field expression, and formula.
    """

    def construct(self):
        title = Tex(r"Divergence $\nabla \cdot \vec F$: area-element growth",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 4, 1], y_range=[-3, 3, 1],
                             x_length=7, y_length=5.2,
                             background_line_style={"stroke_opacity": 0.25}
                             ).move_to([-2.5, -0.3, 0])
        self.play(Create(plane))

        def arrows_for(F, color):
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

        def F_radial(x, y):   # div = 2
            return (x, y)

        def F_sink(x, y):     # div = -2
            return (-x, -y)

        def F_shear(x, y):    # div = 0
            return (y, 0)

        arrows = arrows_for(F_radial, RED)
        self.play(FadeIn(arrows))

        state = {"div": 2.0, "name": r"(x, y)"}

        s_tr = ValueTracker(0.0)

        def disk():
            s = s_tr.get_value()
            r = 0.35 * np.exp(state["div"] * s * 0.5)
            return Circle(radius=r, color=GREEN,
                           fill_opacity=0.4, stroke_width=2
                           ).move_to(plane.c2p(0, 0))

        self.add(always_redraw(disk))

        def info():
            return VGroup(
                Tex(rf"$\vec F = {state['name']}$", color=RED, font_size=24),
                MathTex(rf"\nabla\cdot\vec F = {state['div']:+.2f}",
                         color=YELLOW, font_size=24),
                MathTex(r"A(t) = A_0\, e^{(\nabla\cdot\vec F)\,t}",
                         color=GREEN, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.3, 1.2, 0])

        info_grp = info()
        self.add(info_grp)

        # Phase 1: radial outward (div = +2), disk expands
        self.play(s_tr.animate.set_value(0.8),
                   run_time=2.5, rate_func=linear)

        # Transform to sink
        new_arrows = arrows_for(F_sink, BLUE)
        self.play(Transform(arrows, new_arrows), s_tr.animate.set_value(0))
        state["div"] = -2.0
        state["name"] = r"(-x, -y)"
        new_info = info()
        self.play(Transform(info_grp, new_info))
        self.play(s_tr.animate.set_value(0.8),
                   run_time=2.5, rate_func=linear)

        # Transform to shear
        new_arrows = arrows_for(F_shear, TEAL)
        self.play(Transform(arrows, new_arrows), s_tr.animate.set_value(0))
        state["div"] = 0.0
        state["name"] = r"(y, 0)"
        new_info = info()
        self.play(Transform(info_grp, new_info))
        self.play(s_tr.animate.set_value(0.8),
                   run_time=2, rate_func=linear)
        self.wait(0.4)
