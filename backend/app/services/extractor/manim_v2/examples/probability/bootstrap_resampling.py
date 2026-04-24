from manim import *
import numpy as np


class BootstrapResamplingExample(Scene):
    """
    Bootstrap: resample WITH replacement from data many times, form a
    sampling distribution of the statistic (e.g., mean). 95% CI
    from the 2.5%/97.5% quantiles.

    TWO_COLUMN:
      LEFT  — 15 data points drawn as stems; ValueTracker b_tr advances
              1 → 500 bootstrap replicates; always_redraw a running
              histogram of bootstrap-mean values.
      RIGHT — live 95% CI + true-population mean.
    """

    def construct(self):
        title = Tex(r"Bootstrap: sampling distribution via resample-with-replacement",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        rng = np.random.default_rng(17)
        n_data = 15
        true_mu = 3.0
        data = rng.normal(loc=true_mu, scale=1.2, size=n_data)
        data_mean = float(np.mean(data))

        # LEFT: data display (stems)
        ax_d = Axes(x_range=[0, 6, 1], y_range=[-0.3, 1.3, 0.5],
                     x_length=5.5, y_length=2, tips=False,
                     axis_config={"font_size": 14, "include_numbers": True}
                     ).move_to([-3.3, 1.6, 0])
        self.play(Create(ax_d))

        stems = VGroup()
        for x in data:
            stems.add(Dot(ax_d.c2p(x, 0.2), color=BLUE, radius=0.07))
        mean_tick = DashedLine(ax_d.c2p(data_mean, 0),
                                 ax_d.c2p(data_mean, 1.1),
                                 color=YELLOW, stroke_width=2)
        mean_lbl = MathTex(rf"\bar x = {data_mean:.2f}",
                             color=YELLOW, font_size=18
                             ).next_to(mean_tick, UP, buff=0.1)
        self.play(FadeIn(stems), Create(mean_tick), Write(mean_lbl))

        # Precompute 500 bootstrap means
        B = 500
        boot_means = []
        for _ in range(B):
            sample = rng.choice(data, size=n_data, replace=True)
            boot_means.append(float(np.mean(sample)))
        boot_means = np.array(boot_means)

        # LEFT bottom: histogram
        ax_h = Axes(x_range=[1, 5, 1], y_range=[0, 80, 20],
                     x_length=5.5, y_length=2.5, tips=False,
                     axis_config={"font_size": 14, "include_numbers": True}
                     ).move_to([-3.3, -1.5, 0])
        xl = Tex(r"bootstrap $\bar x^*$",
                  font_size=18).next_to(ax_h, DOWN, buff=0.1)
        yl = Tex(r"count", font_size=18).next_to(ax_h, LEFT, buff=0.1)
        self.play(Create(ax_h), Write(xl), Write(yl))

        b_tr = ValueTracker(1)

        def hist():
            b = int(round(b_tr.get_value()))
            b = max(1, min(b, B))
            vals = boot_means[:b]
            bins = np.linspace(1, 5, 21)
            counts, _ = np.histogram(vals, bins=bins)
            grp = VGroup()
            bw = bins[1] - bins[0]
            for i, c in enumerate(counts):
                if c == 0:
                    continue
                x_center = (bins[i] + bins[i + 1]) / 2
                h_scene = ax_h.c2p(0, c)[1] - ax_h.c2p(0, 0)[1]
                bar = Rectangle(width=bw * 0.9 * (ax_h.c2p(1, 0)[0] - ax_h.c2p(0, 0)[0]),
                                 height=h_scene,
                                 color=GREEN, fill_opacity=0.6,
                                 stroke_width=0.8)
                bar.move_to([ax_h.c2p(x_center, 0)[0],
                             ax_h.c2p(0, 0)[1] + h_scene / 2, 0])
                grp.add(bar)
            return grp

        self.add(always_redraw(hist))

        def ci_lines():
            b = int(round(b_tr.get_value()))
            b = max(1, min(b, B))
            if b < 10:
                return VGroup()
            vals = np.sort(boot_means[:b])
            lo = vals[max(0, int(0.025 * b))]
            hi = vals[min(b - 1, int(0.975 * b))]
            grp = VGroup()
            grp.add(DashedLine(ax_h.c2p(lo, 0), ax_h.c2p(lo, 80),
                                 color=ORANGE, stroke_width=2))
            grp.add(DashedLine(ax_h.c2p(hi, 0), ax_h.c2p(hi, 80),
                                 color=ORANGE, stroke_width=2))
            return grp

        self.add(always_redraw(ci_lines))

        def info():
            b = int(round(b_tr.get_value()))
            b = max(1, min(b, B))
            vals = np.sort(boot_means[:b])
            lo = vals[max(0, int(0.025 * b))] if b >= 10 else float("nan")
            hi = vals[min(b - 1, int(0.975 * b))] if b >= 10 else float("nan")
            se = float(np.std(vals))
            lo_s = f"{lo:.3f}" if b >= 10 else "-"
            hi_s = f"{hi:.3f}" if b >= 10 else "-"
            return VGroup(
                MathTex(rf"B = {b}", color=WHITE, font_size=22),
                MathTex(rf"SE^* = {se:.3f}",
                         color=GREEN, font_size=22),
                MathTex(rf"95\%\,CI = [{lo_s},\ {hi_s}]",
                         color=ORANGE, font_size=22),
                MathTex(rf"\mu_{{\text{{true}}}} = {true_mu}",
                         color=YELLOW, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        self.play(b_tr.animate.set_value(B),
                   run_time=9, rate_func=linear)
        self.wait(0.4)
