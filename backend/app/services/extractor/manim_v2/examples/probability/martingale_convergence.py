from manim import *
import numpy as np


class MartingaleConvergenceExample(Scene):
    """
    Martingale: E[X_{n+1} | X_0, ..., X_n] = X_n. Bounded L¹ martingales
    converge almost surely. Illustrate with a bounded random walk
    stopped at ±1 boundaries (Polya's urn-like process).

    SINGLE_FOCUS:
      Axes for 10 sample martingale paths that are bounded in [-1, 1];
      ValueTracker t_tr advances all paths; all converge to some
      limit (often 0 or ±1).
    """

    def construct(self):
        title = Tex(r"Martingale convergence: bounded $L^1$ martingale $\to$ a.s. limit",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        N_STEPS = 200
        N_PATHS = 10

        rng = np.random.default_rng(11)
        # Polya's urn-like bounded martingale: X_n = ratio of urn fractions
        # Simulate: start with (1 red, 1 blue); each step draw and replace with 2 of drawn color
        # X_n = red/(red + blue) is a bounded martingale on [0, 1]
        paths = np.zeros((N_PATHS, N_STEPS + 1))
        for p in range(N_PATHS):
            red, blue = 1, 1
            paths[p, 0] = red / (red + blue)
            for t in range(N_STEPS):
                frac = red / (red + blue)
                if rng.random() < frac:
                    red += 1
                else:
                    blue += 1
                paths[p, t + 1] = red / (red + blue)

        ax = Axes(x_range=[0, N_STEPS, N_STEPS // 4],
                   y_range=[0, 1, 0.25],
                   x_length=9, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-0.5, -0.3, 0])
        xl = MathTex(r"n", font_size=18).next_to(ax, DOWN, buff=0.1)
        yl = MathTex(r"X_n", font_size=18).next_to(ax, LEFT, buff=0.1)
        self.play(Create(ax), Write(xl), Write(yl))

        # E[X_n] = 1/2 reference
        mean_line = DashedLine(ax.c2p(0, 0.5), ax.c2p(N_STEPS, 0.5),
                                 color=YELLOW, stroke_width=2)
        mean_lbl = MathTex(r"E[X_n] = 0.5", color=YELLOW, font_size=18
                             ).next_to(mean_line.get_end(), RIGHT, buff=0.1)
        self.play(Create(mean_line), Write(mean_lbl))

        t_tr = ValueTracker(0)

        colors = [BLUE, GREEN, ORANGE, PURPLE, PINK, TEAL, RED, GOLD, MAROON, LIGHT_BROWN]

        def path_curves():
            t = int(round(t_tr.get_value()))
            t = max(1, min(t, N_STEPS))
            grp = VGroup()
            for p in range(N_PATHS):
                pts = [ax.c2p(k, paths[p, k]) for k in range(t + 1)]
                m = VMobject(color=colors[p % len(colors)],
                               stroke_width=1.5, stroke_opacity=0.8)
                if len(pts) >= 2:
                    m.set_points_as_corners(pts)
                grp.add(m)
            return grp

        self.add(always_redraw(path_curves))

        def info():
            t = int(round(t_tr.get_value()))
            t = max(1, min(t, N_STEPS))
            current_means = paths[:, t]
            spread = current_means.max() - current_means.min()
            return VGroup(
                MathTex(rf"n = {t}", color=WHITE, font_size=22),
                MathTex(rf"\text{{range of }} X_n = {spread:.3f}",
                         color=YELLOW, font_size=20),
                Tex(r"bounded $\Rightarrow$ converges a.s.",
                     color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        self.play(t_tr.animate.set_value(N_STEPS),
                   run_time=9, rate_func=linear)
        self.wait(0.4)
