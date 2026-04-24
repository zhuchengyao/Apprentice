from manim import *
import numpy as np


class SIREpidemicExample(Scene):
    """
    SIR model played out in time with a sweep of β (infectiousness).

    TWO_COLUMN:
      LEFT  — Axes plotting the S, I, R curves over t. ValueTracker
              t_now sweeps; three always_redraw moving dots track the
              current S(t), I(t), R(t) on their curves; vertical
              dashed cursor marks t_now.
      RIGHT — live readouts for current S, I, R, R₀ = β/γ, plus the
              ODE system. After the first run completes, β is bumped
              up via Transform on the curves to show how the peak
              shifts and grows.
    """

    def construct(self):
        title = Tex(r"SIR model: $\dot S = -\beta S I,\ \dot I = \beta S I - \gamma I,\ \dot R = \gamma I$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        gamma = 0.12

        def simulate(beta_val: float, T=30.0, dt=0.05):
            ts, ss, iis, rs = [], [], [], []
            s, i, r = 0.99, 0.01, 0.0
            t = 0.0
            while t <= T:
                ts.append(t); ss.append(s); iis.append(i); rs.append(r)
                ds = -beta_val * s * i
                di = beta_val * s * i - gamma * i
                dr = gamma * i
                s += ds * dt; i += di * dt; r += dr * dt
                t += dt
            return ts, ss, iis, rs

        beta_initial = 0.5
        ts, ss, iis, rs = simulate(beta_initial)

        axes = Axes(
            x_range=[0, 30, 5], y_range=[0, 1, 0.2],
            x_length=7.0, y_length=4.4,
            axis_config={"include_tip": True, "include_numbers": True, "font_size": 18},
        ).move_to([-2.6, -0.4, 0])
        x_lbl = Tex(r"time $t$", font_size=20).next_to(axes, DOWN, buff=0.1)
        y_lbl = Tex(r"fraction", font_size=20).next_to(axes, LEFT, buff=0.1).rotate(PI / 2)
        self.play(Create(axes), Write(x_lbl), Write(y_lbl))

        def to_curve(ys, color):
            pts = [axes.c2p(t, y) for t, y in zip(ts, ys)]
            c = VMobject(stroke_color=color, stroke_width=3)
            c.set_points_as_corners(pts)
            return c

        s_curve = to_curve(ss, BLUE)
        i_curve = to_curve(iis, RED)
        r_curve = to_curve(rs, GREEN)
        self.play(Create(s_curve), Create(i_curve), Create(r_curve), run_time=2.5)

        # ValueTracker for "current time" cursor
        t_now = ValueTracker(0.001)

        def lookup(arr, t):
            idx = min(int(t / 0.05), len(arr) - 1)
            return arr[idx]

        def cursor():
            t = t_now.get_value()
            top_y = axes.c2p(t, 1.0)[1]
            bot_y = axes.c2p(t, 0)[1]
            screen_x = axes.c2p(t, 0)[0]
            return DashedLine([screen_x, bot_y, 0], [screen_x, top_y, 0],
                              color=YELLOW, stroke_width=2)

        def s_dot():
            t = t_now.get_value()
            return Dot(axes.c2p(t, lookup(ss, t)), color=BLUE, radius=0.10)

        def i_dot():
            t = t_now.get_value()
            return Dot(axes.c2p(t, lookup(iis, t)), color=RED, radius=0.10)

        def r_dot():
            t = t_now.get_value()
            return Dot(axes.c2p(t, lookup(rs, t)), color=GREEN, radius=0.10)

        self.add(always_redraw(cursor), always_redraw(s_dot),
                 always_redraw(i_dot), always_redraw(r_dot))

        # RIGHT COLUMN
        rcol_x = +4.0

        def stats_panel():
            t = t_now.get_value()
            S = lookup(ss, t)
            I = lookup(iis, t)
            R = lookup(rs, t)
            return VGroup(
                MathTex(rf"t = {t:.1f}", color=WHITE, font_size=24),
                MathTex(rf"S = {S:.3f}", color=BLUE, font_size=24),
                MathTex(rf"I = {I:.3f}", color=RED, font_size=24),
                MathTex(rf"R = {R:.3f}", color=GREEN, font_size=24),
                MathTex(rf"\beta = {beta_initial:.2f},\ \gamma = {gamma:.2f}",
                        color=GREY_B, font_size=22),
                MathTex(rf"R_0 = \beta/\gamma = {beta_initial / gamma:.2f}",
                        color=YELLOW, font_size=24),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([rcol_x, +0.4, 0])

        self.add(always_redraw(stats_panel))

        # First sweep: time advances showing the epidemic play out
        self.play(t_now.animate.set_value(30.0),
                  run_time=6, rate_func=linear)
        self.wait(0.5)

        # Second pass: bump β to 0.9, watch the peak shift up and earlier
        beta2 = 0.9
        ts2, ss2, iis2, rs2 = simulate(beta2)
        s_curve2 = to_curve(ss2, BLUE)
        i_curve2 = to_curve(iis2, RED)
        r_curve2 = to_curve(rs2, GREEN)

        new_R0 = MathTex(rf"R_0 = {beta2/gamma:.2f}\ \text{{(higher)}}",
                         color=YELLOW, font_size=24).move_to([rcol_x, -2.2, 0])
        self.play(
            Transform(s_curve, s_curve2),
            Transform(i_curve, i_curve2),
            Transform(r_curve, r_curve2),
            Write(new_R0),
            run_time=3,
        )
        self.wait(1.0)
