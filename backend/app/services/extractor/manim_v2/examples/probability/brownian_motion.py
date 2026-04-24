from manim import *
import numpy as np


class BrownianMotionExample(Scene):
    """
    Brownian motion (Wiener process): continuous-time random walk
    with independent Gaussian increments. B_t ~ N(0, t). Show 5
    sample paths.

    SINGLE_FOCUS:
      Axes with 5 precomputed paths of B_t for t ∈ [0, 1]; always_redraw
      reveals them as ValueTracker t_tr advances. Confidence band
      ±√t shown in GREY.
    """

    def construct(self):
        title = Tex(r"Brownian motion: $B_t \sim \mathcal N(0, t)$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ax = Axes(x_range=[0, 1, 0.25], y_range=[-2, 2, 0.5],
                   x_length=9, y_length=5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-0.5, -0.3, 0])
        tl = MathTex(r"t", font_size=20).next_to(ax, DOWN, buff=0.1)
        self.play(Create(ax), Write(tl))

        # ±√t confidence band
        band_pts_upper = [ax.c2p(t, np.sqrt(t)) for t in np.linspace(0.001, 1, 50)]
        band_pts_lower = [ax.c2p(t, -np.sqrt(t)) for t in np.linspace(0.001, 1, 50)]
        band_pts = band_pts_upper + band_pts_lower[::-1]
        band = Polygon(*band_pts, color=GREY_B, fill_opacity=0.25,
                         stroke_width=0)
        band_upper = ax.plot(lambda t: np.sqrt(t), x_range=[0.001, 1, 0.005],
                               color=GREY_B, stroke_width=2)
        band_lower = ax.plot(lambda t: -np.sqrt(t), x_range=[0.001, 1, 0.005],
                               color=GREY_B, stroke_width=2)
        self.play(Create(band), Create(band_upper), Create(band_lower))

        # Precompute 5 BM paths
        rng = np.random.default_rng(3)
        N_steps = 500
        dt = 1 / N_steps
        num_paths = 5
        paths = []
        for _ in range(num_paths):
            inc = rng.normal(scale=np.sqrt(dt), size=N_steps)
            path = np.concatenate([[0], np.cumsum(inc)])
            paths.append(path)

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

        def info():
            t = t_tr.get_value()
            return VGroup(
                MathTex(rf"t = {t:.3f}", color=WHITE, font_size=22),
                MathTex(r"E[B_t] = 0", color=GREEN, font_size=22),
                MathTex(rf"\text{{Var}}[B_t] = t = {t:.3f}",
                         color=YELLOW, font_size=22),
                MathTex(rf"\pm\sqrt t = \pm {np.sqrt(max(t, 0)):.3f}",
                         color=GREY_B, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        self.play(t_tr.animate.set_value(1.0),
                   run_time=8, rate_func=linear)
        self.wait(0.5)
