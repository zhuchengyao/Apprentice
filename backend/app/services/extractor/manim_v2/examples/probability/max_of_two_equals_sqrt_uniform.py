from manim import *
import numpy as np


class MaxOfTwoEqualsSqrtUniform(Scene):
    """Surprising identity: if U, V are i.i.d. Uniform(0, 1), then
    max(U, V) has the same distribution as sqrt(W) where W ~ Uniform(0, 1).
    Both have CDF F(x) = x^2 and density f(x) = 2x on [0, 1].  Visualize
    by sampling 500 pairs, taking max, and separately sampling 500 W and
    plotting sqrt(W) — the histograms match."""

    def construct(self):
        title = Tex(
            r"$\max(U, V)$ has the same law as $\sqrt{W}$",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ax_l = Axes(
            x_range=[0, 1, 0.2], y_range=[0, 2.4, 0.5],
            x_length=5.5, y_length=4.0,
            tips=False,
            axis_config={"stroke_width": 1.5, "include_ticks": True},
        ).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax_r = Axes(
            x_range=[0, 1, 0.2], y_range=[0, 2.4, 0.5],
            x_length=5.5, y_length=4.0,
            tips=False,
            axis_config={"stroke_width": 1.5, "include_ticks": True},
        ).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.3)
        cap_l = Tex(r"Distribution of $\max(U, V)$", font_size=22,
                    color=BLUE).next_to(ax_l, UP, buff=0.1)
        cap_r = Tex(r"Distribution of $\sqrt{W}$", font_size=22,
                    color=GREEN).next_to(ax_r, UP, buff=0.1)
        self.play(Create(ax_l), Create(ax_r),
                  Write(cap_l), Write(cap_r))

        target_pdf_l = ax_l.plot(
            lambda x: 2 * x, x_range=[0, 1, 0.01],
            color=BLUE, stroke_width=3,
        )
        target_pdf_r = ax_r.plot(
            lambda x: 2 * x, x_range=[0, 1, 0.01],
            color=GREEN, stroke_width=3,
        )
        self.play(Create(target_pdf_l), Create(target_pdf_r))

        rng = np.random.default_rng(17)
        u = rng.uniform(0, 1, 1500)
        v = rng.uniform(0, 1, 1500)
        maxes = np.maximum(u, v)
        w = rng.uniform(0, 1, 1500)
        sqrts = np.sqrt(w)

        bins = np.linspace(0, 1, 21)
        def histogram(data, ax, color):
            hist, edges = np.histogram(data, bins=bins, density=True)
            bars = VGroup()
            for i in range(len(hist)):
                x0 = edges[i]
                x1 = edges[i + 1]
                h = hist[i]
                rect = Rectangle(
                    width=(ax.c2p(x1, 0)[0] - ax.c2p(x0, 0)[0]),
                    height=(ax.c2p(0, h)[1] - ax.c2p(0, 0)[1]),
                    stroke_width=0.6, stroke_color=WHITE,
                    fill_color=color, fill_opacity=0.5,
                )
                rect.move_to(ax.c2p((x0 + x1) / 2, h / 2))
                bars.add(rect)
            return bars

        hist_l = histogram(maxes, ax_l, BLUE)
        hist_r = histogram(sqrts, ax_r, GREEN)
        self.play(LaggedStart(*[FadeIn(b) for b in hist_l],
                              lag_ratio=0.03, run_time=1.2))
        self.play(LaggedStart(*[FadeIn(b) for b in hist_r],
                              lag_ratio=0.03, run_time=1.2))

        derivation = VGroup(
            MathTex(r"P(\max(U, V) \le x) = P(U\le x)\,P(V\le x) = x^2",
                    font_size=24),
            MathTex(r"P(\sqrt{W} \le x) = P(W \le x^2) = x^2",
                    font_size=24),
            MathTex(r"\Rightarrow\ \text{same CDF} = x^2,"
                    r"\ \text{same density}\ 2x", font_size=24,
                    color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        derivation.to_edge(DOWN, buff=0.25)
        self.play(FadeIn(derivation[0]))
        self.play(FadeIn(derivation[1]))
        self.play(FadeIn(derivation[2]))
        self.wait(1.5)
