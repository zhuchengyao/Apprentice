from manim import *
import numpy as np


class MetropolisHastingsExample(Scene):
    """
    Metropolis-Hastings MCMC: sample from p(x) ∝ exp(−U(x)) using
    proposal q(x'|x). Here p is a mixture of two Gaussians on ℝ.
    Proposal: normal random walk with σ=0.5. 2000 steps.

    TWO_COLUMN: LEFT axes show target density (BLUE) + trace of chain
    (YELLOW line connecting samples) + current point (ORANGE dot);
    ValueTracker step_tr reveals steps. RIGHT histogram of accepted
    samples converging to target.
    """

    def construct(self):
        title = Tex(r"Metropolis-Hastings: chain converges to $p(x)\propto e^{-U(x)}$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        def target(x):
            return 0.5 * np.exp(-0.5 * (x - 1.5) ** 2 / 0.3) / np.sqrt(TAU * 0.3) \
                 + 0.5 * np.exp(-0.5 * (x + 1.5) ** 2 / 0.5) / np.sqrt(TAU * 0.5)

        np.random.seed(4)
        N = 2000
        sigma = 0.5
        x = 0.0
        samples = np.zeros(N)
        for i in range(N):
            x_prop = x + np.random.randn() * sigma
            alpha = min(1.0, target(x_prop) / target(x))
            if np.random.random() < alpha:
                x = x_prop
            samples[i] = x

        axes = Axes(x_range=[-4, 4, 1], y_range=[0, 0.7, 0.2],
                    x_length=5.8, y_length=3.8,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(LEFT * 2.5 + DOWN * 0.2)
        self.play(Create(axes))

        target_curve = axes.plot(lambda xx: float(target(xx)),
                                  x_range=[-4, 4], color=BLUE, stroke_width=3)
        self.play(Create(target_curve))

        step_tr = ValueTracker(1.0)

        def chain_trace():
            k = int(round(step_tr.get_value()))
            k = max(1, min(N, k))
            pts = [axes.c2p(samples[i], 0.05 + 0.002 * i) for i in range(k)]
            return VMobject().set_points_as_corners(pts).set_color(YELLOW).set_stroke(width=1.5, opacity=0.6)

        def current_dot():
            k = int(round(step_tr.get_value()))
            k = max(0, min(N - 1, k))
            return Dot(axes.c2p(samples[k], target(samples[k])),
                        color=ORANGE, radius=0.1)

        self.add(always_redraw(chain_trace), always_redraw(current_dot))

        # Right histogram
        h_axes = Axes(x_range=[-4, 4, 1], y_range=[0, 0.7, 0.2],
                      x_length=4.8, y_length=3.4,
                      axis_config={"include_numbers": True,
                                   "font_size": 14}).shift(RIGHT * 2.5 + DOWN * 0.6)
        self.add(h_axes)
        self.add(h_axes.plot(lambda xx: float(target(xx)),
                              x_range=[-4, 4], color=BLUE, stroke_width=2))

        def hist_bars():
            k = max(1, min(N, int(round(step_tr.get_value()))))
            xs = samples[:k]
            edges = np.linspace(-4, 4, 25)
            counts, _ = np.histogram(xs, bins=edges)
            counts = counts / (k * (edges[1] - edges[0]))
            grp = VGroup()
            for i in range(len(counts)):
                x_c = (edges[i] + edges[i + 1]) / 2
                rect = Rectangle(width=0.28,
                                 height=counts[i] * h_axes.y_length / 0.7,
                                 color=YELLOW, stroke_width=0,
                                 fill_color=YELLOW, fill_opacity=0.5)
                rect.move_to(h_axes.c2p(x_c, counts[i] / 2))
                grp.add(rect)
            return grp

        self.add(always_redraw(hist_bars))

        info = VGroup(
            VGroup(Tex(r"steps $N=$", font_size=22),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=22)).arrange(RIGHT, buff=0.1),
            Tex(r"proposal $\mathcal{N}(x,\sigma^2)$, $\sigma=0.5$",
                font_size=20),
            Tex(r"$\alpha=\min(1,p(x')/p(x))$",
                font_size=20, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3).shift(RIGHT * 2.5)
        info[0][1].add_updater(lambda m: m.set_value(
            max(1, min(N, int(round(step_tr.get_value()))))))
        self.add(info)

        self.play(step_tr.animate.set_value(float(N)),
                  run_time=8, rate_func=linear)
        self.wait(0.8)
