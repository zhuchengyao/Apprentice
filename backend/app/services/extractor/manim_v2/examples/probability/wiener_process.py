from manim import *
import numpy as np


class WienerProcessExample(Scene):
    """
    Wiener process (standard Brownian motion) W_t has independent
    Gaussian increments with W_t − W_s ~ N(0, t−s).

    Draw 8 sample paths simultaneously on [0, T=2]. ValueTracker t_tr
    sweeps current time; always_redraw partial-path polylines grow +
    vertical probe line with 8 dots + histogram of W_t values across
    paths (bars) with overlaid Normal(0, t) density reference.
    """

    def construct(self):
        title = Tex(r"Wiener process: $W_t - W_s \sim \mathcal{N}(0,t-s)$, independent increments",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        np.random.seed(1)
        n_paths = 8
        T = 2.0
        N_step = 200
        dt = T / N_step
        # Precompute all paths
        increments = np.random.randn(n_paths, N_step) * np.sqrt(dt)
        paths = np.concatenate([np.zeros((n_paths, 1)),
                                 np.cumsum(increments, axis=1)], axis=1)
        ts_grid = np.linspace(0, T, N_step + 1)

        axes = Axes(x_range=[0, T, 0.5], y_range=[-2.5, 2.5, 1],
                    x_length=6.5, y_length=4.0,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(LEFT * 2.0 + DOWN * 0.2)
        self.play(Create(axes))

        t_tr = ValueTracker(0.01)

        colors = [BLUE, GREEN, ORANGE, RED, YELLOW, PURPLE, TEAL, PINK]

        def path_line(i):
            def f():
                t = t_tr.get_value()
                k = max(1, int(round(t / dt)))
                k = min(N_step, k)
                pts = [axes.c2p(ts_grid[j], paths[i, j]) for j in range(k + 1)]
                return VMobject().set_points_as_corners(pts)\
                    .set_color(colors[i]).set_stroke(width=2)
            return f

        def probe_line():
            t = t_tr.get_value()
            return DashedLine(axes.c2p(t, -2.5), axes.c2p(t, 2.5),
                              color=GREY_B, stroke_width=1.5)

        def probe_dots():
            t = t_tr.get_value()
            k = max(0, min(N_step, int(round(t / dt))))
            grp = VGroup()
            for i in range(n_paths):
                grp.add(Dot(axes.c2p(ts_grid[k], paths[i, k]),
                             color=colors[i], radius=0.08))
            return grp

        for i in range(n_paths):
            self.add(always_redraw(path_line(i)))
        self.add(always_redraw(probe_line),
                 always_redraw(probe_dots))

        # Right: live mean, var
        def stats():
            t = t_tr.get_value()
            k = max(0, min(N_step, int(round(t / dt))))
            vals = paths[:, k]
            return float(np.mean(vals)), float(np.var(vals)), t

        info = VGroup(
            VGroup(Tex(r"$t=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"empirical mean $=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"empirical var $=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"true var $= t=$", color=GREEN, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"$E[W_t]=0,\ \mathrm{Var}(W_t)=t$",
                color=YELLOW, font_size=22),
            Tex(r"a.s. continuous, nowhere diff.",
                color=GREY_B, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.2)

        info[0][1].add_updater(lambda m: m.set_value(stats()[2]))
        info[1][1].add_updater(lambda m: m.set_value(stats()[0]))
        info[2][1].add_updater(lambda m: m.set_value(stats()[1]))
        info[3][1].add_updater(lambda m: m.set_value(stats()[2]))
        self.add(info)

        self.play(t_tr.animate.set_value(T),
                  run_time=8, rate_func=linear)
        self.wait(0.5)
