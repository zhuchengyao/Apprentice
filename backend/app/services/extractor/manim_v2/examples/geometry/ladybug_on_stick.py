from manim import *
import numpy as np


class LadybugOnStickExample(Scene):
    def construct(self):
        title = Text("Ant-on-rubber-rope: bug reaches the end even if rope grows",
                     font_size=22).to_edge(UP)
        self.play(Write(title))

        # dp/dt = v / L(t),  L(t) = L0 + k*t.
        # Solution: p(t) = (v/k) * ln(1 + k*t/L0).  p=1 when t_end = (L0/k)(e^(k/v) - 1).
        L0 = 1.0
        k = 0.5
        v = 0.2
        t_end = (L0 / k) * (np.exp(k / v) - 1)  # ≈ 23.38 s

        screen_left, screen_right = -5.0, 5.0
        y = -0.3

        rope = Line([screen_left, y, 0], [screen_right, y, 0], color=BLUE, stroke_width=6)
        self.play(Create(rope))

        time_tracker = ValueTracker(0.0)

        def p_of_t(t):
            return (v / k) * np.log(1 + k * t / L0)

        bug = always_redraw(lambda: Dot(
            [screen_left + (screen_right - screen_left) * min(p_of_t(time_tracker.get_value()), 1.0),
             y, 0],
            color=RED, radius=0.15,
        ))
        self.add(bug)

        formula = MathTex(r"\frac{dp}{dt} = \frac{v}{L(t)},\;\; L(t) = L_0 + k t",
                          font_size=28, color=YELLOW).shift(UP * 1.3)
        self.play(Write(formula))

        readout = always_redraw(lambda: MathTex(
            rf"t = {time_tracker.get_value():.2f},\; "
            rf"L = {L0 + k * time_tracker.get_value():.2f},\; "
            rf"p = {min(p_of_t(time_tracker.get_value()), 1.0):.3f}",
            font_size=26,
        ).to_edge(DOWN).shift(UP * 0.4))
        self.add(readout)

        self.play(time_tracker.animate.set_value(t_end), run_time=6, rate_func=linear)
        self.wait(0.3)

        self.remove(readout)
        conclusion = Text(f"Reached end at t ≈ {t_end:.1f}s; rope length ≈ {L0 + k * t_end:.1f}",
                          font_size=22, color=GREEN).to_edge(DOWN)
        self.play(Write(conclusion))
        self.wait(0.6)
