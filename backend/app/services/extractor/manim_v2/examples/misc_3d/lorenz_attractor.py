from manim import *
import numpy as np


class LorenzAttractorExample(ThreeDScene):
    """
    Lorenz attractor (from _2024/manim_demo/lorenz):
      ẋ = σ(y − x),  ẏ = x(ρ − z) − y,  ż = xy − βz
    σ = 10, ρ = 28, β = 8/3 — the classic chaotic butterfly.

    3D scene:
      Precomputed 6000-step trajectory; ValueTracker t_tr reveals it
      progressively via always_redraw; rider dot marks current
      position. Ambient camera rotation shows the 3D structure.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-40 * DEGREES)
        axes = ThreeDAxes(x_range=[-25, 25, 10], y_range=[-25, 25, 10],
                           z_range=[0, 50, 10],
                           x_length=5, y_length=5, z_length=4)
        self.add(axes)

        sigma, rho, beta = 10.0, 28.0, 8 / 3

        def step(x, y, z, dt=0.01):
            dx = sigma * (y - x)
            dy = x * (rho - z) - y
            dz = x * y - beta * z
            return x + dx * dt, y + dy * dt, z + dz * dt

        N = 6000
        traj = [(0.1, 0.0, 0.0)]
        x, y, z = traj[0]
        for _ in range(N - 1):
            x, y, z = step(x, y, z, dt=0.01)
            traj.append((x, y, z))

        t_tr = ValueTracker(0.0)

        def trail():
            t = t_tr.get_value()
            idx = int(t * (len(traj) - 1))
            idx = max(1, min(idx, len(traj) - 1))
            # Downsample for performance
            step_size = max(1, idx // 400)
            pts = [axes.c2p(*traj[k]) for k in range(0, idx + 1, step_size)]
            pts.append(axes.c2p(*traj[idx]))
            m = VMobject(color=BLUE, stroke_width=1.8)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        def rider():
            t = t_tr.get_value()
            idx = int(t * (len(traj) - 1))
            idx = max(0, min(idx, len(traj) - 1))
            return Dot3D(axes.c2p(*traj[idx]), color=YELLOW, radius=0.12)

        self.add(always_redraw(trail), always_redraw(rider))

        title = Tex(r"Lorenz attractor: $\dot x, \dot y, \dot z = \sigma(y-x),\ x(\rho-z)-y,\ xy - \beta z$",
                    font_size=22).to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        def panel():
            t = t_tr.get_value()
            idx = int(t * (len(traj) - 1))
            idx = max(0, min(idx, len(traj) - 1))
            x, y, z = traj[idx]
            return VGroup(
                MathTex(rf"t = {idx * 0.01:.2f}", color=WHITE, font_size=22),
                MathTex(rf"(x,y,z) = ({x:+.2f}, {y:+.2f}, {z:+.2f})",
                         color=YELLOW, font_size=20),
                MathTex(rf"\sigma={sigma},\ \rho={rho},\ \beta=8/3",
                         color=BLUE, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DR, buff=0.4)

        p = panel()
        self.add_fixed_in_frame_mobjects(p)

        self.begin_ambient_camera_rotation(rate=0.15)
        self.play(t_tr.animate.set_value(1.0),
                   run_time=12, rate_func=linear)
        new_p = panel()
        self.add_fixed_in_frame_mobjects(new_p)
        self.play(Transform(p, new_p), run_time=0.2)
        self.stop_ambient_camera_rotation()
        self.wait(0.5)
