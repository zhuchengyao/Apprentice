from manim import *
import numpy as np


class CentralLimitTheoremExample(Scene):
    """
    CLT: a sum of n iid uniforms (suitably scaled) becomes Gaussian.

    Single-focus layout with a TWO_COLUMN-style overlay panel.
    A precomputed table of histograms for n = 1, 2, 3, 5, 8, 12, 20, 30
    is held in memory; an integer ValueTracker n_idx steps through the
    table via Transform on the histogram VGroup. The reference standard
    normal stays drawn the whole time; the histogram morphs toward it.
    """

    def construct(self):
        title = Tex(r"CLT: scaled sum of $n$ iid uniforms $\to \mathcal{N}(0, 1)$",
                    font_size=32).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # Single LEFT-leaning panel for the histogram, RIGHT panel for the n-readout.
        axes = Axes(
            x_range=[-4, 4, 1], y_range=[0, 0.55, 0.1],
            x_length=8.4, y_length=4.8,
            axis_config={"include_tip": True, "include_numbers": True, "font_size": 20},
        ).move_to([-1.6, -0.2, 0])
        self.play(Create(axes))

        # Reference 𝒩(0, 1) stays put
        gauss = axes.plot(lambda x: np.exp(-x ** 2 / 2) / np.sqrt(2 * PI),
                          x_range=[-3.9, 3.9], color=RED, stroke_width=3)
        gauss_lbl = MathTex(r"\mathcal{N}(0, 1)", color=RED,
                            font_size=24).next_to(axes.c2p(2.5, 0.45), RIGHT, buff=0.1)
        self.play(Create(gauss), Write(gauss_lbl))

        # Precompute scaled-sum histograms for several n
        rng = np.random.default_rng(seed=42)
        n_values = [1, 2, 3, 5, 8, 12, 20, 30]
        n_samples = 8000

        bins = 41
        edges = np.linspace(-4, 4, bins + 1)

        def make_histogram_for(n: int) -> VGroup:
            # Sum of n Uniform(-0.5, 0.5) has variance n/12, scale by sqrt(12/n) for unit variance
            samples = rng.uniform(-0.5, 0.5, size=(n_samples, n)).sum(axis=1)
            samples = samples * np.sqrt(12 / n)
            counts, _ = np.histogram(samples, bins=edges, density=True)
            xs = (edges[:-1] + edges[1:]) / 2
            bar_w = (edges[1] - edges[0]) * 0.92
            bars = VGroup()
            for x, c in zip(xs, counts):
                if c <= 0:
                    continue
                base = axes.c2p(x, 0)
                top = axes.c2p(x, c)
                h = abs(top[1] - base[1])
                # Bar width measured in screen coords
                pix_w = abs(axes.c2p(x + bar_w / 2, 0)[0] - axes.c2p(x - bar_w / 2, 0)[0])
                rect = Rectangle(width=pix_w, height=h,
                                 color=BLUE, fill_opacity=0.55, stroke_width=0.4)
                rect.move_to((np.array(base) + np.array(top)) / 2)
                bars.add(rect)
            return bars

        histograms = [make_histogram_for(n) for n in n_values]

        # Right side: live n indicator
        rcol_x = +5.2

        n_idx = ValueTracker(0.0)
        current_hist = histograms[0].copy()
        self.add(current_hist)

        def n_panel():
            i = int(round(n_idx.get_value()))
            i = max(0, min(i, len(n_values) - 1))
            return VGroup(
                MathTex(rf"n = {n_values[i]}",
                        color=BLUE, font_size=42),
                MathTex(r"\frac{1}{\sqrt{n/12}}\sum_{i=1}^n U_i",
                        color=BLUE, font_size=22),
                MathTex(r"U_i \sim \text{Uniform}(-\tfrac{1}{2}, \tfrac{1}{2})",
                        color=GREY_B, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([rcol_x, +1.0, 0])

        self.add(always_redraw(n_panel))

        # Step through n_values, morphing the histogram to the next via Transform
        for i in range(1, len(n_values)):
            self.play(
                Transform(current_hist, histograms[i]),
                n_idx.animate.set_value(i),
                run_time=1.4, rate_func=smooth,
            )
            self.wait(0.3)

        formula = MathTex(
            r"\frac{S_n - n\mu}{\sigma\sqrt{n}} \xrightarrow{d} \mathcal{N}(0, 1)",
            font_size=28, color=YELLOW,
        ).move_to([rcol_x, -2.4, 0])
        self.play(Write(formula))
        self.wait(1.2)
