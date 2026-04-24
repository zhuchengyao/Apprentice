from manim import *
import numpy as np


class CauchyConvergenceExample(Scene):
    """
    Cauchy / limit visualization for a_n = 1 + (-1)^n / n → L = 1.

    SINGLE_FOCUS:
      NumberLine shows the first 60 terms of a_n. ValueTracker
      eps_tr shrinks a YELLOW ε-band centered at L = 1; for each
      eps value the minimum index N = ⌈1/ε⌉ such that n > N ⇒ |a_n - L| < ε
      is shown live. As ε → 0, N → ∞ but all but finitely many
      terms still lie inside the shrinking band.
    """

    def construct(self):
        title = Tex(r"Cauchy: $\forall \varepsilon>0\ \exists N,\ n>N \Rightarrow |a_n - L| < \varepsilon$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        nl = NumberLine(x_range=[0, 2, 0.25], length=10,
                        include_numbers=True,
                        decimal_number_config={"num_decimal_places": 2,
                                                "font_size": 16}
                        ).move_to([0, -0.8, 0])
        self.play(Create(nl))

        L = 1.0
        N_max = 60

        def a(n):
            return L + (-1) ** n / n

        dots = VGroup()
        for n in range(1, N_max + 1):
            dots.add(Dot(nl.n2p(a(n)), color=BLUE,
                          radius=max(0.035, 0.11 - 0.0012 * n)))
        self.play(FadeIn(dots))

        L_lbl = MathTex(r"L = 1", color=YELLOW,
                         font_size=24).next_to(nl.n2p(L), UP, buff=0.5)
        self.play(Write(L_lbl))

        eps_tr = ValueTracker(0.4)

        def band():
            e = eps_tr.get_value()
            left = nl.n2p(L - e)
            right = nl.n2p(L + e)
            w = right[0] - left[0]
            return Rectangle(width=w, height=0.7, color=YELLOW,
                              fill_opacity=0.25, stroke_width=2
                              ).move_to(nl.n2p(L))

        self.add(always_redraw(band))

        def info():
            e = eps_tr.get_value()
            Nn = int(np.ceil(1 / e))
            return VGroup(
                MathTex(rf"\varepsilon = {e:.3f}", color=YELLOW, font_size=26),
                MathTex(rf"N = \lceil 1/\varepsilon \rceil = {Nn}",
                         color=GREEN, font_size=26),
                MathTex(r"a_n = 1 + \tfrac{(-1)^n}{n}",
                         color=WHITE, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.2, 2.0, 0])

        self.add(always_redraw(info))

        self.play(eps_tr.animate.set_value(0.05),
                   run_time=6, rate_func=linear)
        self.wait(0.5)
