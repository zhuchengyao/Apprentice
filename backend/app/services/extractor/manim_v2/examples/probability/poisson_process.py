from manim import *
import numpy as np


class PoissonProcessExample(Scene):
    """
    Homogeneous Poisson process rate λ: inter-arrivals are iid
    Exp(λ), count N(t) in [0, t] is Poisson(λt).

    SINGLE_FOCUS:
      Timeline 0..20 with arrivals from Poisson(λ=1). ValueTracker
      t_tr advances; always_redraw arrival ticks + counting step
      function + shaded region; live mean = λt.
    """

    def construct(self):
        title = Tex(r"Poisson process: inter-arrivals $\sim \text{Exp}(\lambda)$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        T_MAX = 20.0
        lam = 1.0

        rng = np.random.default_rng(18)
        arrivals = []
        t = 0
        while True:
            dt = rng.exponential(scale=1 / lam)
            t += dt
            if t > T_MAX:
                break
            arrivals.append(t)

        ax = Axes(x_range=[0, T_MAX, 5], y_range=[0, 25, 5],
                   x_length=9, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-0.5, -0.3, 0])
        xl = MathTex(r"t", font_size=18).next_to(ax, DOWN, buff=0.1)
        yl = MathTex(r"N(t)", font_size=18).next_to(ax, LEFT, buff=0.1)
        self.play(Create(ax), Write(xl), Write(yl))

        # Reference line λt
        ref = DashedLine(ax.c2p(0, 0), ax.c2p(T_MAX, lam * T_MAX),
                           color=GREEN, stroke_width=2)
        ref_lbl = MathTex(r"E[N(t)] = \lambda t", color=GREEN, font_size=20
                            ).next_to(ref.get_end(), UR, buff=0.1)
        self.play(Create(ref), Write(ref_lbl))

        t_tr = ValueTracker(0.0)

        def tick_marks():
            t_cur = t_tr.get_value()
            grp = VGroup()
            for ti in arrivals:
                if ti > t_cur:
                    break
                grp.add(Line(ax.c2p(ti, 0) + UP * 0.15,
                               ax.c2p(ti, 0) + DOWN * 0.15,
                               color=YELLOW, stroke_width=2.5))
            return grp

        def step_fn():
            t_cur = t_tr.get_value()
            pts = [ax.c2p(0, 0)]
            count = 0
            for ti in arrivals:
                if ti > t_cur:
                    break
                pts.append(ax.c2p(ti, count))
                count += 1
                pts.append(ax.c2p(ti, count))
            pts.append(ax.c2p(t_cur, count))
            m = VMobject(color=BLUE, stroke_width=3)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        self.add(always_redraw(step_fn), always_redraw(tick_marks))

        def info():
            t_cur = t_tr.get_value()
            count = sum(1 for ti in arrivals if ti <= t_cur)
            return VGroup(
                MathTex(rf"t = {t_cur:.2f}", color=WHITE, font_size=22),
                MathTex(rf"N(t) = {count}", color=BLUE, font_size=22),
                MathTex(rf"\lambda t = {lam * t_cur:.2f}",
                         color=GREEN, font_size=22),
                MathTex(rf"|\text{{diff}}| = {abs(count - lam * t_cur):.2f}",
                         color=YELLOW, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        self.play(t_tr.animate.set_value(T_MAX),
                   run_time=8, rate_func=linear)
        self.wait(0.4)
