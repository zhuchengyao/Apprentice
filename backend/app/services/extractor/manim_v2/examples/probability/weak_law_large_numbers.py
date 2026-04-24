from manim import *
import numpy as np


class WeakLawLargeNumbersExample(Scene):
    """
    Weak law of large numbers: for iid X_i with mean μ, the sample
    mean X̄_n converges to μ in probability: for any ε > 0,
    P(|X̄_n - μ| > ε) → 0.

    TWO_COLUMN:
      LEFT  — 30 sample paths (n up to N) of the running mean from
              iid Uniform(0, 1); each path in a faint color; the
              ε-band around μ=0.5 shaded.
      RIGHT — live fraction of paths inside ε-band vs n.
    """

    def construct(self):
        title = Tex(r"Weak LLN: $P(|\bar X_n - \mu| > \varepsilon) \to 0$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        N = 300
        num_paths = 30
        mu = 0.5
        eps = 0.1

        rng = np.random.default_rng(44)
        samples = rng.random((num_paths, N))
        running_means = np.cumsum(samples, axis=1) / np.arange(1, N + 1)

        ax_L = Axes(x_range=[0, N, N // 4], y_range=[0, 1, 0.25],
                     x_length=7, y_length=4, tips=False,
                     axis_config={"font_size": 14, "include_numbers": True}
                     ).move_to([-2.8, -0.3, 0])
        self.play(Create(ax_L))

        # ε-band around μ
        band = Rectangle(
            width=ax_L.c2p(N, 0)[0] - ax_L.c2p(0, 0)[0],
            height=ax_L.c2p(0, mu + eps)[1] - ax_L.c2p(0, mu - eps)[1],
            color=YELLOW, fill_opacity=0.2, stroke_width=1
        ).move_to([(ax_L.c2p(0, 0)[0] + ax_L.c2p(N, 0)[0]) / 2,
                     ax_L.c2p(0, mu)[1], 0])
        mu_line = DashedLine(ax_L.c2p(0, mu), ax_L.c2p(N, mu),
                               color=YELLOW, stroke_width=2)
        self.play(Create(band), Create(mu_line))

        n_tr = ValueTracker(1)

        def sample_paths():
            n = int(round(n_tr.get_value()))
            n = max(1, min(n, N))
            grp = VGroup()
            for i in range(num_paths):
                pts = [ax_L.c2p(j + 1, running_means[i, j]) for j in range(n)]
                m = VMobject(color=BLUE_D, stroke_width=1.5,
                               stroke_opacity=0.5)
                if len(pts) >= 2:
                    m.set_points_as_corners(pts)
                grp.add(m)
            return grp

        self.add(always_redraw(sample_paths))

        # RIGHT: fraction inside band
        ax_R = Axes(x_range=[0, N, N // 4], y_range=[0, 1, 0.25],
                     x_length=4, y_length=3, tips=False,
                     axis_config={"font_size": 12, "include_numbers": True}
                     ).move_to([4.0, 0.5, 0])
        xl_R = Tex("n", font_size=16).next_to(ax_R, DOWN, buff=0.08)
        yl_R = Tex(r"$P(|\bar X_n - \mu| \le \varepsilon)$",
                    font_size=14).next_to(ax_R, LEFT, buff=0.08)
        self.play(Create(ax_R), Write(xl_R), Write(yl_R))

        def fraction_curve():
            n_cur = int(round(n_tr.get_value()))
            n_cur = max(1, min(n_cur, N))
            pts = []
            for j in range(n_cur):
                in_band = np.abs(running_means[:, j] - mu) <= eps
                frac = in_band.sum() / num_paths
                pts.append(ax_R.c2p(j + 1, frac))
            m = VMobject(color=GREEN, stroke_width=3)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        self.add(always_redraw(fraction_curve))

        def info():
            n = int(round(n_tr.get_value()))
            n = max(1, min(n, N))
            in_band = np.abs(running_means[:, n - 1] - mu) <= eps
            frac = in_band.sum() / num_paths
            return VGroup(
                MathTex(rf"n = {n}", color=WHITE, font_size=22),
                MathTex(rf"\mu = {mu},\ \varepsilon = {eps}",
                         color=YELLOW, font_size=20),
                MathTex(rf"\hat P(|\bar X_n - \mu| \le \varepsilon) = {frac:.3f}",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        self.play(n_tr.animate.set_value(N),
                   run_time=8, rate_func=linear)
        self.wait(0.4)
