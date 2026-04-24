from manim import *
import numpy as np


class BolzanoWeierstrassExample(Scene):
    """
    Bolzano-Weierstrass: every bounded sequence in ℝ has a convergent
    subsequence. Illustrate with a sequence oscillating in [-1, 1];
    extract a subsequence converging to a limit.

    SINGLE_FOCUS:
      Number line [-1, 1]. 30 sample points a_n from a bounded
      sequence. ValueTracker step_tr extracts a subsequence
      converging (highlighted) to 0.5.
    """

    def construct(self):
        title = Tex(r"Bolzano-Weierstrass: bounded seq $\Rightarrow$ convergent subseq.",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        N = 30
        rng = np.random.default_rng(31)
        # Bounded sequence in [-1, 1] with cluster at 0.5
        a_n = rng.uniform(-1, 1, size=N)
        # Add cluster near 0.5 (every 3rd term)
        for i in range(0, N, 3):
            a_n[i] = 0.5 + rng.normal(0, 0.05)

        nl = NumberLine(x_range=[-1.2, 1.2, 0.25], length=11,
                         include_numbers=True,
                         decimal_number_config={"num_decimal_places": 2,
                                                 "font_size": 16}
                         ).move_to([0, -0.5, 0])
        self.play(Create(nl))

        # Show all samples as BLUE dots
        sample_group = VGroup()
        for i, a in enumerate(a_n):
            y_off = 0.4 + (i % 4) * 0.35
            d = Dot(nl.n2p(a) + UP * y_off, color=BLUE_D, radius=0.06)
            sample_group.add(d)
            lbl = MathTex(f"{i}", font_size=10, color=GREY_B
                            ).next_to(d, UP, buff=0.05)
            sample_group.add(lbl)
        self.play(FadeIn(sample_group))

        # Limit marker at 0.5
        lim_line = DashedLine(nl.n2p(0.5) + UP * 0.2,
                                nl.n2p(0.5) + UP * 2.0,
                                color=YELLOW, stroke_width=2)
        lim_lbl = MathTex(r"\lim = 0.5", color=YELLOW, font_size=20
                            ).next_to(lim_line.get_top(), UP, buff=0.1)
        self.play(Create(lim_line), Write(lim_lbl))

        step_tr = ValueTracker(0)

        def subseq_highlights():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, 10))
            # Pick indices 0, 3, 6, ... (cluster elements)
            indices = list(range(0, 3 * s, 3))
            grp = VGroup()
            for i in indices[:s]:
                if i >= N:
                    continue
                y_off = 0.4 + (i % 4) * 0.35
                d = Dot(nl.n2p(a_n[i]) + UP * y_off,
                          color=RED, radius=0.12)
                grp.add(d)
            return grp

        self.add(always_redraw(subseq_highlights))

        def info():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, 10))
            indices = list(range(0, 3 * s, 3))
            if not indices:
                dist = 0.0
            else:
                last_i = indices[-1]
                dist = abs(a_n[last_i] - 0.5) if last_i < N else 0
            return VGroup(
                MathTex(rf"\text{{subseq length}} = {s}",
                         color=RED, font_size=22),
                MathTex(rf"\text{{last}}\ |a_{{n_k}} - 0.5| = {dist:.4f}",
                         color=YELLOW, font_size=20),
                Tex(r"convergent subsequence found",
                     color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        for s in range(1, 11):
            self.play(step_tr.animate.set_value(s),
                       run_time=0.6, rate_func=smooth)
            self.wait(0.3)
        self.wait(0.5)
