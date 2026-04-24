from manim import *
import numpy as np


class BrownianBridgeExample(Scene):
    """
    Brownian bridge: Brownian motion B_t conditioned on B_0 = 0
    and B_1 = 0. Variance Var[B_t] = t(1-t), maximum at t=0.5.

    SINGLE_FOCUS:
      Axes with 5 precomputed Brownian bridge paths + GREY variance
      envelope ±√(t(1-t)). ValueTracker t_tr advances time 0→1.
    """

    def construct(self):
        title = Tex(r"Brownian bridge: $B_0 = B_1 = 0$, $\text{Var}(B_t) = t(1-t)$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ax = Axes(x_range=[0, 1, 0.25], y_range=[-1.2, 1.2, 0.5],
                   x_length=9, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-0.5, -0.3, 0])
        self.play(Create(ax))

        # Variance envelope ±√(t(1-t))
        env_up = ax.plot(lambda t: np.sqrt(t * (1 - t)),
                           x_range=[0.001, 0.999, 0.005],
                           color=GREY_B, stroke_width=2)
        env_lo = ax.plot(lambda t: -np.sqrt(t * (1 - t)),
                           x_range=[0.001, 0.999, 0.005],
                           color=GREY_B, stroke_width=2)
        self.play(Create(env_up), Create(env_lo))

        # 5 paths
        rng = np.random.default_rng(11)
        N_paths = 5
        N_steps = 300
        dt = 1 / N_steps
        paths = []
        for _ in range(N_paths):
            inc = rng.normal(scale=np.sqrt(dt), size=N_steps)
            B = np.concatenate([[0], np.cumsum(inc)])
            # Convert to bridge: B_t^{bridge} = B_t - t · B_1
            bridge = B - np.linspace(0, B[-1], N_steps + 1)
            paths.append(bridge)

        colors = [BLUE, GREEN, ORANGE, PURPLE, PINK]

        t_tr = ValueTracker(0.0)

        def path_curves():
            t = t_tr.get_value()
            n = int(t * N_steps)
            n = max(1, min(n, N_steps))
            grp = VGroup()
            for i, path in enumerate(paths):
                pts = [ax.c2p(k * dt, path[k]) for k in range(n + 1)]
                m = VMobject(color=colors[i], stroke_width=2)
                if len(pts) >= 2:
                    m.set_points_as_corners(pts)
                grp.add(m)
            return grp

        self.add(always_redraw(path_curves))

        # Start/end markers
        start_dot = Dot(ax.c2p(0, 0), color=RED, radius=0.12)
        end_dot = Dot(ax.c2p(1, 0), color=RED, radius=0.12)
        self.play(FadeIn(start_dot, end_dot))

        def info():
            t = t_tr.get_value()
            var = t * (1 - t)
            return VGroup(
                MathTex(rf"t = {t:.3f}", color=WHITE, font_size=22),
                MathTex(rf"\text{{Var}}(B_t) = t(1-t) = {var:.3f}",
                         color=GREY_B, font_size=20),
                Tex(r"max var at $t=0.5$",
                     color=GREEN, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        self.play(t_tr.animate.set_value(1.0),
                   run_time=7, rate_func=linear)
        self.wait(0.4)
