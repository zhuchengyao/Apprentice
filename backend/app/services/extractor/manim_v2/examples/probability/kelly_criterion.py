from manim import *
import numpy as np


class KellyCriterionExample(Scene):
    """
    Kelly criterion: optimal fraction f* to bet when payoff has
    probability p of winning b:1 odds is
        f* = p − (1 − p) / b  =  (bp − (1−p)) / b.

    SINGLE_FOCUS axes plot expected log-growth rate
        g(f) = p log(1 + bf) + (1 − p) log(1 − f)
    for p=0.55, b=1. Maximum at f* = 0.1. ValueTracker f_tr sweeps;
    always_redraw dot + vertical drop + live g(f). Phase 2 morphs p.
    """

    def construct(self):
        title = Tex(r"Kelly: $f^*=p-\tfrac{1-p}{b}$ maximizes $g(f)=p\log(1+bf)+(1-p)\log(1-f)$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[0, 1, 0.2], y_range=[-0.1, 0.05, 0.03],
                    x_length=8, y_length=4.5,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(DOWN * 0.3)
        self.play(Create(axes))

        p_tr = ValueTracker(0.55)
        b = 1.0

        def g(f, p):
            if f <= 0:
                return 0.0
            if f >= 1:
                return -5
            return p * np.log(1 + b * f) + (1 - p) * np.log(1 - f)

        def growth_curve():
            p = p_tr.get_value()
            return axes.plot(lambda ff: float(g(ff, p)),
                             x_range=[0.01, 0.95],
                             color=BLUE, stroke_width=3)

        self.add(always_redraw(growth_curve))

        def f_opt():
            p = p_tr.get_value()
            return max(0.0, p - (1 - p) / b)

        def opt_dot():
            p = p_tr.get_value()
            fstar = f_opt()
            return Dot(axes.c2p(fstar, g(fstar, p)),
                        color=RED, radius=0.12)

        def opt_dashed():
            fstar = f_opt()
            return DashedLine(axes.c2p(fstar, -0.1),
                              axes.c2p(fstar, 0.05),
                              color=RED, stroke_width=2)

        self.add(always_redraw(opt_dot), always_redraw(opt_dashed))

        # Sweeping probe
        f_tr = ValueTracker(0.0)

        def probe_dot():
            p = p_tr.get_value()
            f = f_tr.get_value()
            return Dot(axes.c2p(f, g(f, p)),
                        color=YELLOW, radius=0.1)

        self.add(always_redraw(probe_dot))

        # Info
        info = VGroup(
            VGroup(Tex(r"$p=$", font_size=22),
                   DecimalNumber(0.55, num_decimal_places=2,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$b=1$ (even odds)", font_size=22),
                    ).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$f=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$g(f)=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=4,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$f^*=$", font_size=22),
                   DecimalNumber(0.10, num_decimal_places=3,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(p_tr.get_value()))
        info[2][1].add_updater(lambda m: m.set_value(f_tr.get_value()))
        info[3][1].add_updater(lambda m: m.set_value(g(f_tr.get_value(), p_tr.get_value())))
        info[4][1].add_updater(lambda m: m.set_value(f_opt()))
        self.add(info)

        # Phase 1: sweep f with p fixed
        self.play(f_tr.animate.set_value(0.8),
                  run_time=4, rate_func=linear)
        self.play(f_tr.animate.set_value(f_opt()),
                  run_time=1.5, rate_func=smooth)
        self.wait(0.5)

        # Phase 2: morph p
        for pval in [0.7, 0.3, 0.85, 0.55]:
            self.play(p_tr.animate.set_value(pval),
                      run_time=1.8, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.5)
