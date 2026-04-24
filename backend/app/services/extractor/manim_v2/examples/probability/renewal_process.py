from manim import *
import numpy as np


class RenewalProcessExample(Scene):
    """
    Renewal process: arrivals at times T_1, T_2, ... with iid
    inter-arrival times X_i. Counting process N(t) = max{n: T_n ≤ t}.
    By LLN, N(t)/t → 1/E[X].

    SINGLE_FOCUS:
      Timeline with 30 precomputed Exp(1) inter-arrivals; ValueTracker
      t_tr advances; always_redraw arrival ticks and counting staircase.
    """

    def construct(self):
        title = Tex(r"Renewal process: $N(t)/t \to 1/E[X] = 1$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        rng = np.random.default_rng(13)
        N_ARRIVALS = 30
        inter_arrivals = rng.exponential(scale=1.0, size=N_ARRIVALS)
        arrivals = np.cumsum(inter_arrivals)

        T_MAX = 30.0

        ax = Axes(x_range=[0, T_MAX, 5], y_range=[0, 35, 5],
                   x_length=10, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([0, -0.5, 0])
        xl = MathTex(r"t", font_size=20).next_to(ax, DOWN, buff=0.1)
        yl = MathTex(r"N(t)", font_size=20).next_to(ax, LEFT, buff=0.1)
        self.play(Create(ax), Write(xl), Write(yl))

        # Reference line y = t (since 1/E[X] = 1)
        ref = DashedLine(ax.c2p(0, 0), ax.c2p(T_MAX, T_MAX),
                           color=GREEN, stroke_width=2)
        ref_lbl = MathTex(r"y = t/E[X]", color=GREEN, font_size=18
                            ).next_to(ax.c2p(T_MAX, T_MAX), UR, buff=0.1)
        self.play(Create(ref), Write(ref_lbl))

        t_tr = ValueTracker(0.0)

        def arrival_ticks():
            t_cur = t_tr.get_value()
            grp = VGroup()
            for i, ti in enumerate(arrivals):
                if ti > t_cur:
                    break
                if ti > T_MAX:
                    break
                tk = Line(ax.c2p(ti, 0) + UP * 0.1,
                            ax.c2p(ti, 0) + DOWN * 0.1,
                            color=YELLOW, stroke_width=2.5)
                grp.add(tk)
            return grp

        def counting_staircase():
            t_cur = t_tr.get_value()
            pts = [ax.c2p(0, 0)]
            count = 0
            for i, ti in enumerate(arrivals):
                if ti > t_cur or ti > T_MAX:
                    break
                pts.append(ax.c2p(ti, count))
                count += 1
                pts.append(ax.c2p(ti, count))
            # Final segment to t_cur
            if t_cur <= T_MAX:
                pts.append(ax.c2p(t_cur, count))
            m = VMobject(color=BLUE, stroke_width=3)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        def rider():
            t_cur = t_tr.get_value()
            count = sum(1 for ti in arrivals if ti <= t_cur)
            return Dot(ax.c2p(t_cur, count), color=RED, radius=0.11)

        self.add(always_redraw(counting_staircase),
                  always_redraw(arrival_ticks),
                  always_redraw(rider))

        def info():
            t_cur = t_tr.get_value()
            count = sum(1 for ti in arrivals if ti <= t_cur)
            rate = count / max(t_cur, 0.001)
            return VGroup(
                MathTex(rf"t = {t_cur:.2f}", color=WHITE, font_size=22),
                MathTex(rf"N(t) = {count}", color=BLUE, font_size=22),
                MathTex(rf"N(t)/t = {rate:.3f}", color=RED, font_size=22),
                MathTex(r"\to 1/E[X] = 1", color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        self.play(t_tr.animate.set_value(T_MAX),
                   run_time=9, rate_func=linear)
        self.wait(0.4)
