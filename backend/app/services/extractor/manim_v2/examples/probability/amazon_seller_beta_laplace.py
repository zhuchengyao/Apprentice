from manim import *
import numpy as np
from scipy.special import gammaln


class AmazonSellerBetaLaplace(Scene):
    """The Amazon seller rating problem from 3Blue1Brown's beta-series.
    Three sellers with very different sample sizes all show 100% ratings,
    but which is best?  Bayesian reasoning with a Uniform=Beta(1,1) prior
    (Laplace's rule of succession) gives expected success rates that
    account for sample size.  Compare three scenarios."""

    def construct(self):
        title = Tex(
            r"Amazon seller problem: which 100\%-rated seller is best?",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        sellers = [
            ("A", 10, 0),
            ("B", 48, 2),
            ("C", 186, 14),
        ]

        labels = VGroup()
        for i, (name, s, f) in enumerate(sellers):
            row = VGroup(
                Tex(rf"Seller {name}: {s} positive, {f} negative",
                    font_size=22),
            )
            row.move_to([-5.2, 2.3 - i * 0.5, 0])
            labels.add(row)
        self.play(LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.2))

        ax = Axes(
            x_range=[0, 1, 0.25],
            y_range=[0, 45, 10],
            x_length=8.5, y_length=4.5,
            tips=False,
            axis_config={"stroke_width": 1.5, "include_ticks": True},
        ).move_to([1.2, -0.5, 0])
        x_lab = MathTex(r"p\ \text{(true success rate)}",
                        font_size=22).next_to(ax.x_axis.get_end(),
                                              DOWN, buff=0.15)
        y_lab = MathTex(r"\text{posterior density}",
                        font_size=22).next_to(ax.y_axis.get_end(),
                                              LEFT, buff=0.15)
        self.play(Create(ax), FadeIn(x_lab), FadeIn(y_lab))

        colors = [BLUE, GREEN, ORANGE]
        mean_labs = []
        for (name, s, f), color in zip(sellers, colors):
            alpha = s + 1
            beta = f + 1
            ln_B = gammaln(alpha) + gammaln(beta) - gammaln(alpha + beta)

            def pdf(p, a=alpha, b=beta, lnB=ln_B):
                if p <= 0 or p >= 1:
                    return 0.0
                return np.exp(
                    (a - 1) * np.log(p) + (b - 1) * np.log(1 - p) - lnB
                )

            curve = ax.plot(pdf, x_range=[0.001, 0.999, 0.001],
                            color=color, stroke_width=3)
            curve_lab = MathTex(
                rf"\text{{Beta}}({alpha}, {beta})",
                font_size=22, color=color,
            ).next_to(curve.get_end(), UR, buff=0.1)
            mean = alpha / (alpha + beta)
            line = DashedLine(
                ax.c2p(mean, 0), ax.c2p(mean, 40),
                color=color, stroke_width=2, stroke_opacity=0.8,
            )
            m_lab = MathTex(
                rf"\text{{E}}[p]={mean:.3f}",
                font_size=22, color=color,
            ).move_to(ax.c2p(mean, 37 - 0.03 * mean))
            self.play(Create(curve), Write(curve_lab), Create(line),
                      Write(m_lab), run_time=1.2)
            mean_labs.append((name, mean, color))

        ranking = VGroup(
            *[
                Tex(
                    rf"Seller {name}: $\mathbb{{E}}[p]={m:.3f}$",
                    font_size=24, color=c,
                )
                for name, m, c in sorted(
                    mean_labs, key=lambda t: -t[1],
                )
            ]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        ranking.to_edge(LEFT, buff=0.4).shift(DOWN * 1.2)
        self.play(FadeIn(ranking))

        principle = Tex(
            r"Laplace's rule: $\hat p = (s+1)/(s+f+2)$\\"
            r"— sample size matters!",
            font_size=22, color=YELLOW,
        ).to_edge(DOWN, buff=0.25)
        self.play(FadeIn(principle))
        self.wait(1.5)
