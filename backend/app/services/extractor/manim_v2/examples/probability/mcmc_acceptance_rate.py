from manim import *
import numpy as np


class MCMCAcceptanceRateExample(Scene):
    """
    MCMC sampler acceptance vs proposal step size σ: for target
    N(0, 1) with Gaussian random-walk proposal, too-small σ ⇒
    high acceptance but slow mixing; too-large σ ⇒ low acceptance.
    Optimal around 0.234 for high-dim (Roberts-Gelman-Gilks).

    SINGLE_FOCUS: run 2000 steps with σ ∈ {0.1, 0.5, 1.5, 3.0}
    (ValueTracker sigma_idx_tr). always_redraw trace + histogram.
    """

    def construct(self):
        title = Tex(r"MCMC acceptance vs proposal size $\sigma$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        np.random.seed(5)
        sigmas = [0.1, 0.5, 1.5, 3.0]
        N = 2000

        def target(x):
            return np.exp(-x * x / 2) / np.sqrt(TAU)

        runs = {}
        for sigma in sigmas:
            x = 0.0
            samples = np.zeros(N)
            accepted = 0
            for i in range(N):
                x_prop = x + np.random.randn() * sigma
                alpha = min(1.0, target(x_prop) / target(x))
                if np.random.random() < alpha:
                    x = x_prop
                    accepted += 1
                samples[i] = x
            runs[sigma] = (samples, accepted / N)

        # LEFT: trace
        axes = Axes(x_range=[0, N, 500], y_range=[-4, 4, 2],
                    x_length=5.5, y_length=3.5,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(LEFT * 2.5 + DOWN * 1.2)
        self.add(axes)
        trace_lbl = Tex(r"MCMC trace", font_size=22).next_to(axes, UP, buff=0.1)
        self.add(trace_lbl)

        sigma_idx_tr = ValueTracker(0.0)

        def s_now():
            return sigmas[max(0, min(len(sigmas) - 1, int(round(sigma_idx_tr.get_value()))))]

        def trace_curve():
            s = s_now()
            samples, _ = runs[s]
            pts = [axes.c2p(i, samples[i]) for i in range(0, N, 5)]
            return VMobject().set_points_as_corners(pts).set_color(YELLOW).set_stroke(width=1.2)

        self.add(always_redraw(trace_curve))

        # RIGHT: histogram
        h_axes = Axes(x_range=[-4, 4, 1], y_range=[0, 0.45, 0.1],
                      x_length=4.5, y_length=3.5,
                      axis_config={"include_numbers": True,
                                   "font_size": 14}).shift(RIGHT * 3.0 + DOWN * 1.2)
        self.add(h_axes)
        h_axes_lbl = Tex(r"histogram vs $\mathcal{N}(0, 1)$", font_size=20).next_to(h_axes, UP, buff=0.1)
        self.add(h_axes_lbl)
        target_curve = h_axes.plot(lambda xx: float(target(xx)),
                                    x_range=[-4, 4], color=BLUE, stroke_width=2)
        self.add(target_curve)

        def hist_bars():
            s = s_now()
            samples, _ = runs[s]
            edges = np.linspace(-4, 4, 25)
            counts, _ = np.histogram(samples, bins=edges)
            counts = counts / (N * (edges[1] - edges[0]))
            grp = VGroup()
            for i in range(len(counts)):
                x_c = (edges[i] + edges[i + 1]) / 2
                rect = Rectangle(width=0.31,
                                 height=counts[i] * h_axes.y_length / 0.45,
                                 color=YELLOW, stroke_width=0,
                                 fill_color=YELLOW, fill_opacity=0.5)
                rect.move_to(h_axes.c2p(x_c, counts[i] / 2))
                grp.add(rect)
            return grp

        self.add(always_redraw(hist_bars))

        info = VGroup(
            VGroup(Tex(r"$\sigma=$", font_size=24),
                   DecimalNumber(0.1, num_decimal_places=2,
                                 font_size=24).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"acceptance $=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"small $\sigma$: high acceptance, slow mixing",
                color=GREY_B, font_size=18),
            Tex(r"large $\sigma$: low acceptance, wasted steps",
                color=GREY_B, font_size=18),
            Tex(r"optimal $\approx 0.234$ acceptance (RGG)",
                color=YELLOW, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(UP, buff=1.1).shift(LEFT * 2.5)
        info[0][1].add_updater(lambda m: m.set_value(s_now()))
        info[1][1].add_updater(lambda m: m.set_value(runs[s_now()][1]))
        self.add(info)

        for k in range(1, len(sigmas)):
            self.play(sigma_idx_tr.animate.set_value(float(k)),
                      run_time=2.0, rate_func=smooth)
            self.wait(0.6)
        self.wait(0.5)
