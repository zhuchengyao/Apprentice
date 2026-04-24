from manim import *
import numpy as np


class ArzelaAscoliExample(Scene):
    """
    Arzelà-Ascoli: a uniformly bounded, equicontinuous family on
    [a, b] has a uniformly convergent subsequence. Equicontinuous
    family: f_n(x) = sin(x + 1/n) — all share ω(δ) = δ.

    SINGLE_FOCUS:
      Axes with 8 equicontinuous functions f_n(x) = sin(x + 1/n);
      ValueTracker n_tr reveals them one at a time; they visibly
      converge uniformly to sin(x).
    """

    def construct(self):
        title = Tex(r"Arzelà-Ascoli: equicontinuous + bounded $\Rightarrow$ uniform convergent subseq.",
                    font_size=20).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ax = Axes(x_range=[0, 2 * PI + 0.1, PI / 2],
                   y_range=[-1.3, 1.3, 0.5],
                   x_length=9, y_length=4.5, tips=False,
                   axis_config={"font_size": 14}
                   ).move_to([0, -0.3, 0])
        self.play(Create(ax))

        # Limit function f(x) = sin(x)
        limit_curve = ax.plot(np.sin, x_range=[0, 2 * PI, 0.02],
                                color=GREY_B, stroke_width=2.5)
        limit_lbl = MathTex(r"f(x) = \sin(x)", color=GREY_B, font_size=20
                              ).next_to(ax.c2p(5.5, -0.5), DR, buff=0.1)
        self.play(Create(limit_curve), Write(limit_lbl))

        N_funcs = 8
        colors = [interpolate_color(BLUE, RED, i / (N_funcs - 1))
                  for i in range(N_funcs)]

        n_tr = ValueTracker(1)

        def fn_curves():
            n_cur = int(round(n_tr.get_value()))
            n_cur = max(1, min(n_cur, N_funcs))
            grp = VGroup()
            for i in range(n_cur):
                shift = 1 / (i + 1)
                m = ax.plot(lambda x: np.sin(x + shift),
                              x_range=[0, 2 * PI, 0.02],
                              color=colors[i], stroke_width=2,
                              stroke_opacity=0.75)
                grp.add(m)
            return grp

        self.add(always_redraw(fn_curves))

        def info():
            n = int(round(n_tr.get_value()))
            n = max(1, min(n, N_funcs))
            # Sup norm: max |sin(x + 1/n) - sin(x)| ≈ 1/n for small 1/n
            sup_norm = 2 * abs(np.sin(1 / (2 * n)))  # max over x
            return VGroup(
                MathTex(rf"n = {n}", color=YELLOW, font_size=24),
                MathTex(rf"f_n(x) = \sin(x + 1/n)",
                         color=YELLOW, font_size=22),
                MathTex(rf"\|f_n - f\|_\infty \approx {sup_norm:.4f}",
                         color=GREEN, font_size=20),
                Tex(r"equicontinuous + bounded $\Rightarrow$ uniform conv.",
                     color=GREEN, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for nv in range(2, N_funcs + 1):
            self.play(n_tr.animate.set_value(nv),
                       run_time=0.8, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.4)
