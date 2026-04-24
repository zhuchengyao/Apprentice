from manim import *
import numpy as np


class MomentGeneratingFunctionExample(Scene):
    """
    MGF for X ~ Exponential(λ): M(t) = λ/(λ-t) for t < λ.

    TWO_COLUMN:
      LEFT  — Axes plotting the integrand e^(tx)·λ·e^(-λx) = λ·e^((t-λ)x)
              for the current t. ValueTracker t sweeps from -1 toward
              λ-0.05; when t < 0 the integrand decays fast (small MGF
              value), as t → λ the area blows up.
      RIGHT — live readouts t, M(t) = λ/(λ-t) (or "diverges" when
              t ≥ λ), the moment expansion 1 + tμ₁ + (t²/2!)μ₂ + ...,
              and a mini-axes plot of M(t) vs t with a vertical
              asymptote at t = λ.
    """

    def construct(self):
        title = Tex(r"MGF $M_X(t) = \mathbb{E}[e^{tX}]$ for $X \sim$ Exp$(\lambda)$",
                    font_size=28).to_edge(UP, buff=0.4)
        self.play(Write(title))

        lam = 1.5

        axes = Axes(
            x_range=[0, 6, 1], y_range=[0, 2.5, 0.5],
            x_length=6.4, y_length=4.0,
            axis_config={"include_tip": True, "include_numbers": True, "font_size": 18},
        ).move_to([-2.6, +0.0, 0])
        self.play(Create(axes))

        t_tr = ValueTracker(-1.0)

        def integrand_curve():
            t = t_tr.get_value()
            return axes.plot(lambda x: lam * np.exp((t - lam) * x),
                             x_range=[0, 5.9, 0.05], color=ORANGE)

        def integrand_area():
            t = t_tr.get_value()
            curve = axes.plot(lambda x: lam * np.exp((t - lam) * x),
                              x_range=[0, 5.9, 0.05])
            return axes.get_area(curve, x_range=[0, 5.9],
                                 color=ORANGE, opacity=0.4)

        # Reference: Exp pdf λ·e^(-λx)
        pdf = axes.plot(lambda x: lam * np.exp(-lam * x),
                        x_range=[0, 5.9], color=BLUE,
                        stroke_width=2, stroke_opacity=0.7)
        pdf_lbl = MathTex(r"\lambda e^{-\lambda x}", color=BLUE,
                          font_size=20).next_to(axes.c2p(1.2, lam * np.exp(-lam * 1.2)),
                                                UR, buff=0.05)
        self.play(Create(pdf), Write(pdf_lbl))

        self.add(always_redraw(integrand_area), always_redraw(integrand_curve))

        # RIGHT COLUMN
        rcol_x = +4.0

        def info_panel():
            t = t_tr.get_value()
            valid = t < lam - 1e-3
            if valid:
                M = lam / (lam - t)
                M_str = f"{M:.4f}"
            else:
                M_str = r"\text{diverges}"
            return VGroup(
                MathTex(rf"\lambda = {lam}", color=BLUE, font_size=22),
                MathTex(rf"t = {t:+.2f}", color=ORANGE, font_size=24),
                MathTex(r"M(t) = \int_0^\infty \lambda e^{(t-\lambda)x} dx",
                        color=YELLOW, font_size=20),
                MathTex(rf"= \tfrac{{\lambda}}{{\lambda - t}} = {M_str}",
                        color=YELLOW if valid else RED, font_size=22),
                MathTex(r"= 1 + t\mu_1 + \tfrac{t^2}{2!}\mu_2 + \cdots",
                        color=GREY_B, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([rcol_x, +1.4, 0])

        self.add(always_redraw(info_panel))

        # Mini M(t) vs t plot
        mini_axes = Axes(
            x_range=[-1.5, 1.5, 0.5], y_range=[0, 6, 1],
            x_length=2.6, y_length=1.6,
            axis_config={"include_tip": False, "include_numbers": False, "font_size": 14},
        ).move_to([rcol_x, -1.8, 0])
        M_curve = mini_axes.plot(
            lambda t: lam / (lam - t) if t < lam - 0.1 else 8,
            x_range=[-1.5, lam - 0.1, 0.02],
            color=YELLOW,
        )
        asymptote = DashedLine(mini_axes.c2p(lam, 0), mini_axes.c2p(lam, 6),
                                color=RED, stroke_width=2, stroke_opacity=0.5)
        M_lbl = Tex(r"$M(t)$ vs $t$", color=YELLOW,
                    font_size=18).next_to(mini_axes, UP, buff=0.08)
        self.play(Create(mini_axes), Create(M_curve), Create(asymptote), Write(M_lbl))

        def cursor():
            t = t_tr.get_value()
            if t < lam - 0.05:
                return Dot(mini_axes.c2p(t, lam / (lam - t)),
                           color=YELLOW, radius=0.07)
            return Dot([0, 0, 0], color=BLACK, radius=0.001)

        self.add(always_redraw(cursor))

        for tgt in [0.0, 0.8, 1.3, -0.5, 1.45]:
            self.play(t_tr.animate.set_value(tgt),
                      run_time=2.0, rate_func=smooth)
            self.wait(0.4)

        self.wait(0.5)
