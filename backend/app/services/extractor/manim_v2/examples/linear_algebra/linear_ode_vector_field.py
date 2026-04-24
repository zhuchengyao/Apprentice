from manim import *
import numpy as np


class LinearODEVectorFieldExample(Scene):
    """
    Linear ODE system x' = A x visualized as a vector field with
    integral-curve tracers. Eigen structure determines the phase-
    portrait shape (stable spiral for this A).

    SINGLE_FOCUS:
      Plane with vector field arrows for A = [[-0.3, -1.2],
      [1.0, -0.3]] (stable spiral). ValueTracker t_tr drives
      12 always_redraw tracer dots along precomputed trajectories
      from different initial conditions — they spiral inward.
    """

    def construct(self):
        title = Tex(r"Linear ODE: $\dot{\mathbf x} = A\,\mathbf x$ — stable spiral",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 4, 1], y_range=[-3, 3, 1],
                             x_length=7.5, y_length=5.5,
                             background_line_style={"stroke_opacity": 0.25}
                             ).move_to([-2, -0.3, 0])
        self.play(Create(plane))

        A = np.array([[-0.3, -1.2],
                       [1.0, -0.3]])

        # Sparse vector-field arrows
        arrows = VGroup()
        for xv in np.arange(-3, 3.01, 1.0):
            for yv in np.arange(-2.0, 2.01, 0.8):
                v = A @ np.array([xv, yv])
                mag = np.linalg.norm(v)
                if mag < 1e-4:
                    continue
                s = 0.35 / max(mag, 0.35)
                start = plane.c2p(xv, yv)
                end = plane.c2p(xv + s * v[0], yv + s * v[1])
                arrows.add(Arrow(start, end, buff=0, color=BLUE_D,
                                   stroke_width=2,
                                   max_tip_length_to_length_ratio=0.3))
        self.play(FadeIn(arrows))

        # Precompute 12 trajectories via Euler
        dt = 0.05
        n_steps = 400
        seeds = []
        rng = np.random.default_rng(7)
        for _ in range(12):
            seeds.append(rng.uniform(-3, 3, 2))

        trajs = []
        for s0 in seeds:
            path = [s0.copy()]
            x = s0.copy()
            for _ in range(n_steps):
                x = x + dt * A @ x
                path.append(x.copy())
            trajs.append(path)

        t_tr = ValueTracker(0.0)

        tracer_colors = [YELLOW, ORANGE, RED, PURPLE,
                          TEAL, GREEN, PINK, WHITE,
                          BLUE_A, GOLD, MAROON, LIGHT_BROWN]

        def tracers():
            progress = t_tr.get_value()
            idx = int(progress * (n_steps - 1))
            idx = max(0, min(idx, n_steps - 1))
            grp = VGroup()
            for k, path in enumerate(trajs):
                p = path[idx]
                grp.add(Dot(plane.c2p(p[0], p[1]),
                              color=tracer_colors[k % len(tracer_colors)],
                              radius=0.08))
            return grp

        def trails():
            progress = t_tr.get_value()
            idx = int(progress * (n_steps - 1))
            idx = max(0, min(idx, n_steps - 1))
            grp = VGroup()
            for k, path in enumerate(trajs):
                if idx < 2:
                    continue
                pts = [plane.c2p(p[0], p[1]) for p in path[:idx+1]]
                v = VMobject(color=tracer_colors[k % len(tracer_colors)],
                               stroke_width=1.8, stroke_opacity=0.55)
                v.set_points_as_corners(pts)
                grp.add(v)
            return grp

        self.add(always_redraw(trails), always_redraw(tracers))

        info = VGroup(
            MathTex(r"A = \begin{pmatrix} -0.3 & -1.2 \\ 1.0 & -0.3 \end{pmatrix}",
                    color=YELLOW, font_size=22),
            MathTex(r"\lambda = -0.3 \pm i\sqrt{1.2}",
                    color=GREEN, font_size=22),
            Tex(r"stable spiral", color=GREEN, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.35).shift(UP * 0.3)
        self.play(Write(info))

        self.play(t_tr.animate.set_value(1.0),
                   run_time=8, rate_func=linear)
        self.wait(0.4)
