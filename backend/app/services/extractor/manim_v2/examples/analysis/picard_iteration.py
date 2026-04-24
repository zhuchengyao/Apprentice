from manim import *
import numpy as np


class PicardIterationExample(Scene):
    """
    Picard iteration proves ODE existence/uniqueness via contraction
    T(φ)(t) = y_0 + ∫_0^t f(s, φ(s)) ds.

    Example: y' = y, y(0) = 1. True solution e^t. Successive
    iterates φ_k approximate e^t by truncated Taylor polynomials:
      φ_0 = 1
      φ_1 = 1 + t
      φ_2 = 1 + t + t²/2
      φ_k = Σ_{j=0}^{k} t^j / j!

    TWO_COLUMN: LEFT axes with GREY e^t reference; ValueTracker
    k_tr steps through k=0..8, always_redraw YELLOW φ_k curve + dots
    showing iteration. RIGHT shows current polynomial formula and
    live sup-norm error on [0, 1.5].
    """

    def construct(self):
        title = Tex(r"Picard: $y'=y,\ y(0)=1 \Rightarrow \varphi_{k+1}(t)=1+\int_0^t \varphi_k(s)\,ds$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[0, 1.6, 0.5], y_range=[0, 5.5, 1],
                    x_length=5.6, y_length=4.0,
                    axis_config={"include_numbers": True,
                                 "font_size": 18}).shift(LEFT * 2.5 + DOWN * 0.2)
        self.play(Create(axes))

        true = axes.plot(lambda t: np.exp(t), x_range=[0, 1.5],
                         color=GREY_B, stroke_width=4)
        true_lbl = Tex(r"$e^t$", color=GREY_B, font_size=22).next_to(axes, UP, buff=0.2).shift(RIGHT)
        self.play(Create(true), Write(true_lbl))

        k_tr = ValueTracker(0.0)

        def phi_k(k, t):
            s = 0.0
            term = 1.0
            for j in range(k + 1):
                if j == 0:
                    s = 1.0
                    term = 1.0
                else:
                    term *= t / j
                    s += term
            return s

        def phi_curve():
            k = int(round(k_tr.get_value()))
            k = max(0, min(8, k))
            return axes.plot(lambda t: phi_k(k, t), x_range=[0, 1.5],
                             color=YELLOW, stroke_width=3)

        self.add(always_redraw(phi_curve))

        # Right column
        def k_now():
            return max(0, min(8, int(round(k_tr.get_value()))))

        def poly_str():
            k = k_now()
            parts = ["1"]
            for j in range(1, k + 1):
                if j == 1:
                    parts.append("t")
                else:
                    parts.append(rf"\tfrac{{t^{{{j}}}}}{{{j}!}}")
            return "+".join(parts)

        # We use a single Tex that rebuilds via updater (re-creation workaround: build/destroy)
        phi_lbl = Tex(r"$\varphi_0=1$", font_size=24, color=YELLOW)
        phi_lbl.to_edge(RIGHT, buff=0.3).shift(UP * 1.5)
        self.add(phi_lbl)

        def update_lbl(mob, dt):
            k = k_now()
            new = Tex(rf"$\varphi_{{{k}}}={poly_str()}$",
                      font_size=22, color=YELLOW)
            new.move_to(phi_lbl, aligned_edge=LEFT)
            phi_lbl.become(new)
            return phi_lbl
        phi_lbl.add_updater(update_lbl)

        def sup_error():
            k = k_now()
            ts = np.linspace(0, 1.5, 50)
            return float(max(abs(phi_k(k, t) - np.exp(t)) for t in ts))

        err_grp = VGroup(
            VGroup(Tex(r"$k=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"sup-error on $[0,1.5]$:", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=5,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"$\to 0$ as $k\to\infty$", color=GREEN, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.3).shift(DOWN * 1.0)
        err_grp[0][1].add_updater(lambda m: m.set_value(k_now()))
        err_grp[1][1].add_updater(lambda m: m.set_value(sup_error()))
        self.add(err_grp)

        for k in range(1, 9):
            self.play(k_tr.animate.set_value(float(k)),
                      run_time=0.7, rate_func=smooth)
            self.wait(0.25)
        self.wait(0.8)
