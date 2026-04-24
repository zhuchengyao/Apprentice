from manim import *
import numpy as np


class MarkovInequalityExample(Scene):
    """
    Markov's inequality: for X ≥ 0 and a > 0, P(X ≥ a) ≤ E[X]/a.

    TWO_COLUMN:
      LEFT  — histogram of 500 exponential(λ=1) samples + bound a;
              ValueTracker a_tr sweeps a.
      RIGHT — empirical P(X ≥ a) vs Markov bound 1/a.
    """

    def construct(self):
        title = Tex(r"Markov: $P(X \ge a) \le E[X]/a$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        rng = np.random.default_rng(5)
        N = 500
        samples = rng.exponential(scale=1.0, size=N)

        ax_L = Axes(x_range=[0, 6, 1], y_range=[0, 180, 40],
                     x_length=6.5, y_length=4, tips=False,
                     axis_config={"font_size": 14, "include_numbers": True}
                     ).move_to([-3.2, -0.3, 0])
        xl = MathTex(r"x", font_size=20).next_to(ax_L, DOWN, buff=0.1)
        self.play(Create(ax_L), Write(xl))

        # Static histogram
        bins = np.linspace(0, 6, 25)
        counts, _ = np.histogram(samples, bins=bins)
        bar_w = bins[1] - bins[0]
        hist_group = VGroup()
        for i, c in enumerate(counts):
            if c == 0:
                continue
            x_center = (bins[i] + bins[i + 1]) / 2
            h_scene = ax_L.c2p(0, c)[1] - ax_L.c2p(0, 0)[1]
            bar = Rectangle(
                width=(ax_L.c2p(bar_w, 0)[0] - ax_L.c2p(0, 0)[0]) * 0.95,
                height=h_scene, color=BLUE, fill_opacity=0.55,
                stroke_width=0.5)
            bar.move_to([ax_L.c2p(x_center, 0)[0],
                         ax_L.c2p(0, 0)[1] + h_scene / 2, 0])
            hist_group.add(bar)
        self.play(FadeIn(hist_group))

        a_tr = ValueTracker(1.5)

        def a_line():
            a = a_tr.get_value()
            return DashedLine(ax_L.c2p(a, 0), ax_L.c2p(a, 180),
                                color=RED, stroke_width=3)

        def tail_shade():
            a = a_tr.get_value()
            grp = VGroup()
            for i, c in enumerate(counts):
                x_center = (bins[i] + bins[i + 1]) / 2
                if x_center < a or c == 0:
                    continue
                h_scene = ax_L.c2p(0, c)[1] - ax_L.c2p(0, 0)[1]
                bar = Rectangle(
                    width=(ax_L.c2p(bar_w, 0)[0] - ax_L.c2p(0, 0)[0]) * 0.95,
                    height=h_scene, color=RED, fill_opacity=0.75,
                    stroke_width=0.5)
                bar.move_to([ax_L.c2p(x_center, 0)[0],
                             ax_L.c2p(0, 0)[1] + h_scene / 2, 0])
                grp.add(bar)
            return grp

        self.add(always_redraw(a_line), always_redraw(tail_shade))

        # RIGHT: P vs bound
        ax_R = Axes(x_range=[0.5, 5, 1], y_range=[0, 1.1, 0.25],
                     x_length=4, y_length=3, tips=False,
                     axis_config={"font_size": 12, "include_numbers": True}
                     ).move_to([3.3, 0.5, 0])
        self.play(Create(ax_R))

        # Bound curve E[X]/a = 1/a
        bound_curve = ax_R.plot(lambda a: min(1 / a, 1.1),
                                   x_range=[0.5, 5, 0.02],
                                   color=GREEN, stroke_width=3)
        self.play(Create(bound_curve))

        # Empirical rider
        def emp_dot():
            a = a_tr.get_value()
            emp = np.mean(samples >= a)
            return Dot(ax_R.c2p(a, emp), color=YELLOW, radius=0.1)

        self.add(always_redraw(emp_dot))

        def info():
            a = a_tr.get_value()
            emp = np.mean(samples >= a)
            bound = 1 / a
            return VGroup(
                MathTex(rf"a = {a:.2f}", color=RED, font_size=22),
                MathTex(r"E[X] = 1", color=WHITE, font_size=20),
                MathTex(rf"\hat P(X \ge a) = {emp:.3f}",
                         color=YELLOW, font_size=20),
                MathTex(rf"\text{{bound}} = E[X]/a = {bound:.3f}",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        for av in [0.5, 1.0, 2.0, 3.5, 1.5]:
            self.play(a_tr.animate.set_value(av),
                       run_time=1.4, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
