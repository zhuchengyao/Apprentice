from manim import *
import numpy as np


class InstantaneousVelocityParadoxExample(Scene):
    """
    Zeno / instantaneous-velocity paradox resolved: as Δt → 0,
    (s(t + Δt) - s(t))/Δt → s'(t). Not an "average over nothing" —
    a limit of non-trivial averages.

    TWO_COLUMN:
      LEFT  — axes y = s(t) = t² − t³/4 (rise then fall); green
              secant between (t₀, s(t₀)) and (t₀ + Δt, s(t₀+Δt))
              rotates into the tangent as ValueTracker dt_tr shrinks.
      RIGHT — live Δt, secant slope, exact derivative s'(t₀), and
              the formal statement.
    """

    def construct(self):
        title = Tex(r"Instantaneous velocity: $v(t_0) = \lim_{\Delta t \to 0} \tfrac{s(t_0+\Delta t) - s(t_0)}{\Delta t}$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ax = Axes(x_range=[0, 3.2, 1], y_range=[0, 2, 0.5],
                   x_length=7, y_length=4.5, tips=False,
                   axis_config={"font_size": 16, "include_numbers": True}
                   ).move_to([-2.6, -0.4, 0])
        self.play(Create(ax))

        def s(t):
            return t ** 2 - t ** 3 / 4

        def dsdt(t):
            return 2 * t - 3 * t ** 2 / 4

        curve = ax.plot(s, x_range=[0, 3.2], color=BLUE, stroke_width=3)
        self.play(Create(curve))

        t0 = 1.5
        dt_tr = ValueTracker(1.2)

        def secant_line():
            dt = dt_tr.get_value()
            y0 = s(t0)
            y1 = s(t0 + dt)
            slope = (y1 - y0) / dt
            # extend line beyond secant endpoints
            x_lo = max(0, t0 - 0.8)
            x_hi = min(3.2, t0 + dt + 0.8)
            return ax.plot(lambda x: y0 + slope * (x - t0),
                            x_range=[x_lo, x_hi], color=GREEN,
                            stroke_width=3)

        def pts():
            dt = dt_tr.get_value()
            d0 = Dot(ax.c2p(t0, s(t0)), color=YELLOW, radius=0.1)
            d1 = Dot(ax.c2p(t0 + dt, s(t0 + dt)), color=ORANGE, radius=0.1)
            return VGroup(d0, d1)

        self.add(always_redraw(secant_line), always_redraw(pts))

        def info():
            dt = dt_tr.get_value()
            slope = (s(t0 + dt) - s(t0)) / dt if abs(dt) > 1e-8 else dsdt(t0)
            exact = dsdt(t0)
            return VGroup(
                MathTex(rf"t_0 = {t0:.2f}", color=YELLOW, font_size=24),
                MathTex(rf"\Delta t = {dt:.4f}", color=ORANGE, font_size=24),
                MathTex(rf"\text{{secant slope}} = {slope:.4f}",
                         color=GREEN, font_size=22),
                MathTex(rf"s'(t_0) = {exact:.4f}",
                         color=RED, font_size=22),
                MathTex(rf"|\text{{error}}| = {abs(slope - exact):.2e}",
                         color=WHITE, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.3, 0.3, 0])

        self.add(always_redraw(info))

        self.play(dt_tr.animate.set_value(0.002),
                   run_time=8, rate_func=linear)
        self.wait(0.5)
