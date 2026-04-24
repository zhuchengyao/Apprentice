from manim import *
import numpy as np


class BarnsleyFernExample(Scene):
    """
    Barnsley fern: iterated function system (IFS) with 4 affine maps
    chosen with probabilities p = (0.01, 0.85, 0.07, 0.07).

    Deterministic chaos-game via ValueTracker n_tr: reveal 10000 pre-
    computed points in batches as n_tr increases; always_redraw shows
    the fern-shape emerging from random-but-fixed seed trajectory.
    Live iteration count + visual sub-stem populations.
    """

    def construct(self):
        title = Tex(r"Barnsley fern: chaos-game with 4 affine maps",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        np.random.seed(42)
        N = 10000
        pts = np.zeros((N, 2))
        p = np.array([0.01, 0.85, 0.07, 0.07])
        cum = np.cumsum(p)
        x, y = 0.0, 0.0
        # Affine maps
        W = [
            (np.array([[0.0, 0.0], [0.0, 0.16]]), np.array([0.0, 0.0])),
            (np.array([[0.85, 0.04], [-0.04, 0.85]]), np.array([0.0, 1.6])),
            (np.array([[0.2, -0.26], [0.23, 0.22]]), np.array([0.0, 1.6])),
            (np.array([[-0.15, 0.28], [0.26, 0.24]]), np.array([0.0, 0.44])),
        ]
        # Also assign which map was used for color
        which = np.zeros(N, dtype=int)
        rs = np.random.random(N)
        for i in range(N):
            r = rs[i]
            k = int(np.searchsorted(cum, r))
            A, b = W[k]
            x, y = A @ np.array([x, y]) + b
            pts[i] = (x, y)
            which[i] = k

        # Normalize pts for display
        pts_scaled = pts.copy()
        pts_scaled[:, 0] *= 0.7
        pts_scaled[:, 0] += 0.0  # centered
        pts_scaled[:, 1] *= 0.55
        pts_scaled[:, 1] -= 2.5  # shift down

        # Dots mobject — create once, partially show via opacity
        dots = VGroup(*[
            Dot(np.array([pts_scaled[i, 0], pts_scaled[i, 1], 0.0]),
                color=[RED, GREEN, BLUE, YELLOW][which[i]],
                radius=0.012,
                fill_opacity=0.0)
            for i in range(N)
        ])
        self.add(dots)

        n_tr = ValueTracker(0.0)

        def update_opacities(mob):
            n = int(round(n_tr.get_value()))
            for i, d in enumerate(mob):
                d.set_fill(opacity=0.85 if i < n else 0.0)
            return mob

        dots.add_updater(update_opacities)

        counter = VGroup(
            VGroup(Tex(r"iterations $=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)
                   ).arrange(RIGHT, buff=0.1),
            Tex(r"$p=(0.01, 0.85, 0.07, 0.07)$", font_size=20),
            Tex(r"stem (R) $\cdot$ frond (G)", color=GREEN, font_size=20),
            Tex(r"L-leaf (B) $\cdot$ R-leaf (Y)", color=YELLOW, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_corner(DL, buff=0.3)
        counter[0][1].add_updater(lambda m: m.set_value(int(round(n_tr.get_value()))))
        self.add(counter)

        self.play(n_tr.animate.set_value(float(N)),
                  run_time=10, rate_func=linear)
        dots.clear_updaters()
        self.wait(1.0)
