from manim import *
import numpy as np


class PendulumTimeSeriesExample(Scene):
    """
    Pendulum θ(t) with small damping (from _2019/diffyq/part1/pendulum):
    θ'' + 2γθ' + sin θ = 0. Compare large vs small initial amplitude
    to show that the linearized small-amplitude solution agrees with
    the nonlinear one only near equilibrium.

    TWO_COLUMN:
      LEFT  — pendulum bob swinging, driven by ValueTracker t_tr
              advancing the precomputed nonlinear trajectory.
      RIGHT — θ(t) time series for both nonlinear (RED) and
              linearized (BLUE dashed); gap grows with amplitude.
    """

    def construct(self):
        title = Tex(r"Pendulum: nonlinear vs linearized $\ddot\theta + \sin\theta = 0$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        gamma = 0.08
        L = 1.5

        # Integrate nonlinear system via RK2
        def integrate(theta0, T=12.0, dt=0.02):
            theta = theta0
            thetad = 0.0
            pts = [(0.0, theta)]
            t = 0.0
            while t < T:
                k1_th = thetad
                k1_thd = -2 * gamma * thetad - np.sin(theta)
                theta += dt * k1_th
                thetad += dt * k1_thd
                t += dt
                pts.append((t, theta))
            return pts

        theta0 = 1.3  # large amplitude
        traj_nonlin = integrate(theta0)

        def linearized(t):
            # θ'' + 2γ θ' + θ = 0 (replacing sin θ with θ)
            # For small γ: θ(t) = θ0 · e^{-γt} · cos(√(1-γ²)t)
            omega = np.sqrt(max(1 - gamma ** 2, 1e-4))
            return theta0 * np.exp(-gamma * t) * np.cos(omega * t)

        # LEFT: pendulum visualization
        pivot = np.array([-4.0, 1.8, 0])
        t_tr = ValueTracker(0.0)

        def bob_and_arm():
            t = t_tr.get_value()
            idx = int(t / 0.02)
            idx = max(0, min(idx, len(traj_nonlin) - 1))
            _, theta = traj_nonlin[idx]
            end = pivot + L * np.array([np.sin(theta), -np.cos(theta), 0])
            grp = VGroup()
            grp.add(Line(pivot, end, color=GREY_B, stroke_width=3))
            grp.add(Dot(pivot, color=WHITE, radius=0.06))
            grp.add(Dot(end, color=RED, radius=0.2))
            return grp

        self.add(always_redraw(bob_and_arm))

        # RIGHT: time series
        ax = Axes(x_range=[0, 12, 2], y_range=[-1.8, 1.8, 0.5],
                   x_length=7, y_length=4, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([2, -0.5, 0])
        self.play(Create(ax))

        # Static nonlinear + linearized curves
        lin_curve = ax.plot(linearized, x_range=[0, 12, 0.02],
                              color=BLUE, stroke_width=2.5)
        lin_curve.set_stroke(dash_array=[0.1, 0.1])

        nonlin_pts = [ax.c2p(t_val, theta_val)
                      for (t_val, theta_val) in traj_nonlin]
        nonlin_curve = VMobject(color=RED, stroke_width=3)
        nonlin_curve.set_points_as_corners(nonlin_pts)

        self.play(Create(nonlin_curve), Create(lin_curve))

        nl_lbl = Tex(r"nonlinear", color=RED, font_size=18
                      ).next_to(ax.c2p(10, 0.8), UP, buff=0.1)
        lin_lbl = Tex(r"linearized", color=BLUE, font_size=18
                       ).next_to(ax.c2p(10, -0.3), DOWN, buff=0.1)
        self.play(Write(nl_lbl), Write(lin_lbl))

        def rider():
            t = t_tr.get_value()
            idx = int(t / 0.02)
            idx = max(0, min(idx, len(traj_nonlin) - 1))
            _, theta = traj_nonlin[idx]
            return Dot(ax.c2p(t, theta), color=YELLOW, radius=0.1)

        self.add(always_redraw(rider))

        def info():
            t = t_tr.get_value()
            idx = int(t / 0.02)
            idx = max(0, min(idx, len(traj_nonlin) - 1))
            _, theta = traj_nonlin[idx]
            lin = linearized(t)
            return VGroup(
                MathTex(rf"t = {t:.2f}", color=WHITE, font_size=22),
                MathTex(rf"\theta_{{\text{{nl}}}} = {theta:+.3f}",
                         color=RED, font_size=20),
                MathTex(rf"\theta_{{\text{{lin}}}} = {lin:+.3f}",
                         color=BLUE, font_size=20),
                MathTex(rf"\text{{gap}} = {abs(theta-lin):.3f}",
                         color=YELLOW, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.3).shift(UP * 2.0)

        self.add(always_redraw(info))

        self.play(t_tr.animate.set_value(12),
                   run_time=10, rate_func=linear)
        self.wait(0.4)
