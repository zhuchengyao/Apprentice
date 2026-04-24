from manim import *
import numpy as np


class MixtureOfGaussiansEMExample(Scene):
    """
    Gaussian mixture model: fit two Gaussians via Expectation-Maximization.
    Each iteration: E-step computes responsibilities γ_{ik}; M-step
    updates means/weights. Illustrate with 1D mixture.

    SINGLE_FOCUS:
      Axes with 200 samples (bimodal); 2 Gaussian components fit
      over iterations; ValueTracker step_tr advances EM steps.
    """

    def construct(self):
        title = Tex(r"Gaussian mixture EM: fit 2 components",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        rng = np.random.default_rng(42)
        N = 200
        # True params
        mix1 = rng.normal(loc=-1.0, scale=0.5, size=N // 2)
        mix2 = rng.normal(loc=1.5, scale=0.8, size=N // 2)
        data = np.concatenate([mix1, mix2])

        ax = Axes(x_range=[-4, 4, 1], y_range=[0, 0.6, 0.1],
                   x_length=9, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([0, -0.3, 0])
        self.play(Create(ax))

        # Data rug plot
        rug = VGroup()
        for x in data:
            rug.add(Line(ax.c2p(x, 0), ax.c2p(x, 0.02),
                           color=GREY_B, stroke_width=1))
        self.play(FadeIn(rug))

        # EM precomputed iterations
        # Start with mu_1 = -2, mu_2 = 2, both sigma=1, pi=0.5
        em_history = []
        mu1, mu2, sigma1, sigma2, pi1 = -2.0, 2.0, 1.0, 1.0, 0.5
        em_history.append((mu1, mu2, sigma1, sigma2, pi1))
        for _ in range(10):
            # E-step
            p1 = pi1 * np.exp(-(data - mu1) ** 2 / (2 * sigma1 ** 2)) / (sigma1 * np.sqrt(2 * PI))
            p2 = (1 - pi1) * np.exp(-(data - mu2) ** 2 / (2 * sigma2 ** 2)) / (sigma2 * np.sqrt(2 * PI))
            total = p1 + p2 + 1e-10
            gamma1 = p1 / total
            gamma2 = p2 / total
            # M-step
            pi1 = gamma1.sum() / N
            mu1 = (gamma1 * data).sum() / gamma1.sum()
            mu2 = (gamma2 * data).sum() / gamma2.sum()
            sigma1 = np.sqrt((gamma1 * (data - mu1) ** 2).sum() / gamma1.sum())
            sigma2 = np.sqrt((gamma2 * (data - mu2) ** 2).sum() / gamma2.sum())
            em_history.append((mu1, mu2, sigma1, sigma2, pi1))

        step_tr = ValueTracker(0)

        def gauss(x, mu, sigma):
            return np.exp(-(x - mu) ** 2 / (2 * sigma ** 2)) / (sigma * np.sqrt(2 * PI))

        def mix_components():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, len(em_history) - 1))
            mu1, mu2, s1, s2, p1 = em_history[s]
            c1 = ax.plot(lambda x: p1 * gauss(x, mu1, s1),
                           x_range=[-4, 4, 0.02],
                           color=BLUE, stroke_width=3)
            c2 = ax.plot(lambda x: (1 - p1) * gauss(x, mu2, s2),
                           x_range=[-4, 4, 0.02],
                           color=ORANGE, stroke_width=3)
            mix = ax.plot(lambda x: p1 * gauss(x, mu1, s1) + (1 - p1) * gauss(x, mu2, s2),
                            x_range=[-4, 4, 0.02],
                            color=GREEN, stroke_width=3.5)
            return VGroup(c1, c2, mix)

        self.add(always_redraw(mix_components))

        def info():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, len(em_history) - 1))
            mu1, mu2, s1, s2, p1 = em_history[s]
            return VGroup(
                MathTex(rf"\text{{iter}} = {s}/10",
                         color=WHITE, font_size=22),
                MathTex(rf"\mu_1 = {mu1:+.3f}, \sigma_1 = {s1:.3f}",
                         color=BLUE, font_size=18),
                MathTex(rf"\mu_2 = {mu2:+.3f}, \sigma_2 = {s2:.3f}",
                         color=ORANGE, font_size=18),
                MathTex(rf"\pi_1 = {p1:.3f}",
                         color=WHITE, font_size=18),
                Tex(r"GREEN: mixture density",
                     color=GREEN, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        for s in [2, 4, 6, 10]:
            self.play(step_tr.animate.set_value(s),
                       run_time=1.3, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
