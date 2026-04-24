from manim import *
import numpy as np


class IdentityTheoremExample(Scene):
    """
    Identity theorem: if two holomorphic functions on connected D
    agree on a set with an accumulation point in D, they agree on
    all of D.

    SINGLE_FOCUS:
      Show two functions f(z) = sin(πz) and g(z) = 0 (both
      holomorphic) agreeing at z = 0, 1, 2, 3, ... — integer
      accumulation? No, integers have no finite accumulation.
      Instead: f(z) = 0 on ⟨1/n⟩_n → 0 accumulation at 0 ⇒ f ≡ 0.
      Illustrate with f(z) = z sin(π/z) vs 0.
    """

    def construct(self):
        title = Tex(r"Identity: $f, g$ holomorphic, agree on accumulating set $\Rightarrow f = g$",
                    font_size=20).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ax = Axes(x_range=[0, 1, 0.1], y_range=[-0.5, 1, 0.25],
                   x_length=9, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-0.5, -0.3, 0])
        self.play(Create(ax))

        # f(x) = x · sin(π/x) on (0, 1] — vanishes at x = 1/n
        f_curve = ax.plot(lambda x: x * np.sin(PI / x) if x > 1e-4 else 0,
                            x_range=[0.03, 1, 0.003],
                            color=BLUE, stroke_width=2.5)
        f_lbl = MathTex(r"f(z) = z \sin(\pi/z)",
                          color=BLUE, font_size=22
                          ).next_to(ax.c2p(0.7, 0.3), UR, buff=0.1)
        self.play(Create(f_curve), Write(f_lbl))

        # Zeros at z = 1/n
        n_tr = ValueTracker(1)

        def zero_dots():
            n = int(round(n_tr.get_value()))
            n = max(1, min(n, 20))
            grp = VGroup()
            for k in range(1, n + 1):
                x = 1 / k
                grp.add(Dot(ax.c2p(x, 0), color=RED, radius=0.08))
            return grp

        self.add(always_redraw(zero_dots))

        # Accumulation arrow at 0
        acc_arrow = Arrow(ax.c2p(0.3, -0.35), ax.c2p(0.02, -0.08),
                            color=YELLOW, buff=0, stroke_width=3,
                            max_tip_length_to_length_ratio=0.15)
        acc_lbl = Tex(r"accumulation at $0$",
                       color=YELLOW, font_size=18
                       ).next_to(acc_arrow, DOWN, buff=0.1)
        self.play(Create(acc_arrow), Write(acc_lbl))

        def info():
            n = int(round(n_tr.get_value()))
            n = max(1, min(n, 20))
            return VGroup(
                MathTex(rf"\text{{zeros shown}} = {n}",
                         color=RED, font_size=22),
                MathTex(r"f(1/n) = 0\ \forall n",
                         color=RED, font_size=20),
                Tex(r"zero set has accumulation at $z=0$",
                     color=YELLOW, font_size=18),
                Tex(r"but $f$ NOT holomorphic at 0 (essential sing.)",
                     color=ORANGE, font_size=16),
                Tex(r"so identity theorem doesn't force $f \equiv 0$",
                     color=GREEN, font_size=16),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        for nv in [3, 6, 10, 20]:
            self.play(n_tr.animate.set_value(nv),
                       run_time=1.0, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
