from manim import *
import numpy as np


class TCubedDerivativeExample(Scene):
    """
    Derivative of t³ via the secant-to-tangent limit.

    TWO_COLUMN layout:
      LEFT  — graph of y = t³ with a fixed point at t₀ and a moving
              second point at t₀ + dt; the secant line through them
              redraws as dt shrinks. A ValueTracker dt animates from
              1.5 down to 0.05.
      RIGHT — algebraic expansion shown one row at a time, ending in
              the live numeric secant slope vs the exact limit 3t₀².
    """

    def construct(self):
        title = Tex(r"Derivative of $t^3$ as the secant slope's limit",
                    font_size=34).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # LEFT COLUMN: graph of y = t^3
        axes = Axes(
            x_range=[0, 2.6, 0.5], y_range=[0, 18, 4],
            x_length=5.5, y_length=5.0,
            axis_config={"include_tip": True, "include_numbers": True, "font_size": 20},
        ).move_to([-3.4, -0.2, 0])
        graph = axes.plot(lambda t: t ** 3, x_range=[0, 2.55], color=BLUE)
        self.play(Create(axes), Create(graph))

        t0 = 1.5
        f = lambda t: t ** 3

        p_anchor = Dot(axes.c2p(t0, f(t0)), color=YELLOW, radius=0.1)
        anchor_lbl = MathTex(rf"t_0 = {t0}", color=YELLOW, font_size=24).next_to(
            p_anchor, DL, buff=0.1
        )
        self.play(FadeIn(p_anchor), Write(anchor_lbl))

        dt_tracker = ValueTracker(1.5)

        def moving_dot():
            dt = dt_tracker.get_value()
            return Dot(axes.c2p(t0 + dt, f(t0 + dt)), color=RED, radius=0.1)

        def secant_line():
            dt = dt_tracker.get_value()
            p1 = np.array(axes.c2p(t0, f(t0)))
            p2 = np.array(axes.c2p(t0 + dt, f(t0 + dt)))
            direction = p2 - p1
            unit = direction / np.linalg.norm(direction)
            return Line(p1 - 0.6 * unit, p2 + 0.5 * unit, color=ORANGE, stroke_width=3)

        self.add(always_redraw(moving_dot), always_redraw(secant_line))

        # RIGHT COLUMN: algebraic story stacked top-down at x = +3.4
        rcol_x = +3.4
        steps = [
            MathTex(r"\Delta y = (t_0 + dt)^3 - t_0^3", font_size=26),
            MathTex(r"= 3t_0^2\,dt + 3t_0\,(dt)^2 + (dt)^3", font_size=24),
            MathTex(r"\frac{\Delta y}{dt} = 3t_0^2 + 3t_0\,dt + (dt)^2", font_size=26),
        ]
        ys = [+2.4, +1.6, +0.6]
        for s, y in zip(steps, ys):
            s.move_to([rcol_x, y, 0])
        for s in steps:
            self.play(Write(s), run_time=0.9)

        # Live numeric readouts (slope of secant, exact limit)
        def slope_readout():
            dt = dt_tracker.get_value()
            slope = ((t0 + dt) ** 3 - t0 ** 3) / dt
            return MathTex(rf"\frac{{\Delta y}}{{dt}} = {slope:.3f}",
                           color=ORANGE, font_size=28).move_to([rcol_x, -0.6, 0])

        def dt_readout():
            return MathTex(rf"dt = {dt_tracker.get_value():.3f}",
                           color=RED, font_size=24).move_to([rcol_x, -1.4, 0])

        exact = MathTex(rf"\to 3t_0^2 = {3 * t0 ** 2:.3f}",
                        color=YELLOW, font_size=28).move_to([rcol_x, -2.2, 0])

        self.add(always_redraw(slope_readout), always_redraw(dt_readout))
        self.play(Write(exact))

        # Sweep dt down — the secant rotates onto the tangent
        self.play(dt_tracker.animate.set_value(0.05), run_time=5, rate_func=smooth)
        self.wait(0.5)

        conclusion = MathTex(r"\frac{d}{dt} t^3 = 3t^2",
                             font_size=32, color=YELLOW).move_to([rcol_x, -3.0, 0])
        self.play(Write(conclusion))
        self.wait(1.0)
