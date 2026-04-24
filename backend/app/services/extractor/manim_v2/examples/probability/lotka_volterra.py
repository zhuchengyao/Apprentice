from manim import *
import numpy as np


class LotkaVolterraExample(Scene):
    """
    Lotka-Volterra predator-prey: dx/dt = αx - βxy, dy/dt = δxy - γy.
    Solutions are closed orbits in phase space (ecological cycles).

    TWO_COLUMN:
      LEFT  — phase plane (x, y) with trajectory; ValueTracker t_tr
              advances precomputed trajectory.
      RIGHT — time series x(t), y(t) showing oscillations.
    """

    def construct(self):
        title = Tex(r"Lotka-Volterra: predator-prey cycles",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Integrate LV
        alpha, beta, delta, gamma = 0.8, 0.5, 0.4, 0.6
        x, y = 2.0, 1.0
        dt = 0.02
        N = 1500
        traj = [(x, y)]
        for _ in range(N):
            dx = alpha * x - beta * x * y
            dy = delta * x * y - gamma * y
            x += dt * dx
            y += dt * dy
            traj.append((x, y))

        # Phase plane
        plane = NumberPlane(x_range=[0, 4, 1], y_range=[0, 3.5, 1],
                             x_length=5.5, y_length=4,
                             background_line_style={"stroke_opacity": 0.25}
                             ).move_to([-3, -0.3, 0])
        x_lbl = MathTex(r"x \text{ (prey)}", font_size=16).next_to(plane, DOWN, buff=0.1)
        y_lbl = MathTex(r"y \text{ (pred.)}", font_size=16).next_to(plane, LEFT, buff=0.1)
        self.play(Create(plane), Write(x_lbl), Write(y_lbl))

        # Time-series axes
        ax_t = Axes(x_range=[0, N * dt, N * dt / 4], y_range=[0, 4, 1],
                     x_length=5.5, y_length=3.5, tips=False,
                     axis_config={"font_size": 12, "include_numbers": True}
                     ).move_to([3, -0.3, 0])
        t_xl = MathTex(r"t", font_size=16).next_to(ax_t, DOWN, buff=0.1)
        self.play(Create(ax_t), Write(t_xl))

        t_tr = ValueTracker(0.0)

        def phase_trail():
            t_cur = t_tr.get_value()
            n = int(t_cur * N / (N * dt))
            n = max(1, min(n, N))
            pts = [plane.c2p(traj[k][0], traj[k][1]) for k in range(n + 1)]
            m = VMobject(color=YELLOW, stroke_width=3)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        def phase_rider():
            t_cur = t_tr.get_value()
            n = int(t_cur * N / (N * dt))
            n = max(0, min(n, N))
            x, y = traj[n]
            return Dot(plane.c2p(x, y), color=RED, radius=0.11)

        def x_curve():
            t_cur = t_tr.get_value()
            n = int(t_cur * N / (N * dt))
            n = max(1, min(n, N))
            pts = [ax_t.c2p(k * dt, traj[k][0]) for k in range(n + 1)]
            m = VMobject(color=BLUE, stroke_width=2.5)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        def y_curve():
            t_cur = t_tr.get_value()
            n = int(t_cur * N / (N * dt))
            n = max(1, min(n, N))
            pts = [ax_t.c2p(k * dt, traj[k][1]) for k in range(n + 1)]
            m = VMobject(color=RED, stroke_width=2.5)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        self.add(always_redraw(phase_trail), always_redraw(phase_rider),
                  always_redraw(x_curve), always_redraw(y_curve))

        legend_t = VGroup(
            Tex(r"BLUE: x (prey)", color=BLUE, font_size=16),
            Tex(r"RED: y (predator)", color=RED, font_size=16),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12
                    ).move_to([3, 2.2, 0])
        self.play(Write(legend_t))

        def info():
            return VGroup(
                MathTex(rf"\alpha={alpha},\,\beta={beta}",
                         color=WHITE, font_size=16),
                MathTex(rf"\delta={delta},\,\gamma={gamma}",
                         color=WHITE, font_size=16),
                Tex(r"closed cycles in phase space",
                     color=YELLOW, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        self.play(t_tr.animate.set_value(N * dt),
                   run_time=9, rate_func=linear)
        self.wait(0.4)
