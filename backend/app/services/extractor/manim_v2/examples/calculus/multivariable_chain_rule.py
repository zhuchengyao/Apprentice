from manim import *
import numpy as np


class MultivariableChainRuleExample(Scene):
    """
    Chain rule on a 2-input function: df/dt = ∂_x f · x'(t) + ∂_y f · y'(t).

    Concrete example: x(t) = cos(t), y(t) = sin(t),
                      f(x, y) = x² + 3y² ⇒ f(t) = cos²t + 3sin²t.

    SINGLE_FOCUS computational graph: nodes for t, x, y, f, df/dt
    arranged left-to-right. ValueTracker t sweeps; the node values
    update live via always_redraw, edge labels show local derivatives,
    and the bottom panel computes df/dt two ways (closed form vs the
    chain-rule sum) — they agree numerically each frame.
    """

    def construct(self):
        title = Tex(r"Chain rule: $\dfrac{df}{dt} = \partial_x f \cdot x'(t) + \partial_y f \cdot y'(t)$",
                    font_size=28).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # Functions
        def x_of(t): return np.cos(t)
        def y_of(t): return np.sin(t)
        def xp(t): return -np.sin(t)
        def yp(t): return np.cos(t)
        def f_xy(x, y): return x ** 2 + 3 * y ** 2
        def fx(x, y): return 2 * x
        def fy(x, y): return 6 * y

        t_tracker = ValueTracker(0.0)

        def node(label_str, position, color):
            circle = Circle(radius=0.5, color=color, stroke_width=3).set_fill(color, opacity=0.25)
            circle.move_to(position)
            lbl = MathTex(label_str, font_size=24).move_to(position)
            return VGroup(circle, lbl)

        # Layout: t → (x, y) → f → df/dt
        pos_t = LEFT * 5.4 + DOWN * 0.4
        pos_x = LEFT * 2.3 + UP * 1.0
        pos_y = LEFT * 2.3 + DOWN * 1.8
        pos_f = RIGHT * 1.2 + DOWN * 0.4
        pos_dft = RIGHT * 4.8 + DOWN * 0.4

        node_t = node("t", pos_t, BLUE)
        node_x = node("x", pos_x, GREEN)
        node_y = node("y", pos_y, GREEN)
        node_f = node("f", pos_f, YELLOW)
        node_dft = node(r"\tfrac{df}{dt}", pos_dft, ORANGE)
        self.play(LaggedStart(*[FadeIn(n) for n in [node_t, node_x, node_y, node_f, node_dft]],
                              lag_ratio=0.15))

        # Edges
        e_tx = Arrow(node_t[0].get_right(), node_x[0].get_left(),
                     buff=0.05, color=GREY_B, stroke_width=3,
                     max_tip_length_to_length_ratio=0.10)
        e_ty = Arrow(node_t[0].get_right(), node_y[0].get_left(),
                     buff=0.05, color=GREY_B, stroke_width=3,
                     max_tip_length_to_length_ratio=0.10)
        e_xf = Arrow(node_x[0].get_right(), node_f[0].get_left(),
                     buff=0.05, color=GREY_B, stroke_width=3,
                     max_tip_length_to_length_ratio=0.10)
        e_yf = Arrow(node_y[0].get_right(), node_f[0].get_left(),
                     buff=0.05, color=GREY_B, stroke_width=3,
                     max_tip_length_to_length_ratio=0.10)
        e_fout = Arrow(node_f[0].get_right(), node_dft[0].get_left(),
                       buff=0.05, color=ORANGE, stroke_width=3,
                       max_tip_length_to_length_ratio=0.10)
        self.play(LaggedStart(*[GrowArrow(e) for e in [e_tx, e_ty, e_xf, e_yf, e_fout]],
                              lag_ratio=0.15))

        # Live edge labels
        def lbl_xprime():
            return MathTex(rf"x'(t) = {xp(t_tracker.get_value()):+.2f}",
                           color=GREY_B, font_size=20).next_to(e_tx, UP, buff=0.1)

        def lbl_yprime():
            return MathTex(rf"y'(t) = {yp(t_tracker.get_value()):+.2f}",
                           color=GREY_B, font_size=20).next_to(e_ty, DOWN, buff=0.1)

        def lbl_fx():
            return MathTex(rf"\partial_x f = {fx(x_of(t_tracker.get_value()), y_of(t_tracker.get_value())):+.2f}",
                           color=GREY_B, font_size=20).next_to(e_xf, UP, buff=0.1)

        def lbl_fy():
            return MathTex(rf"\partial_y f = {fy(x_of(t_tracker.get_value()), y_of(t_tracker.get_value())):+.2f}",
                           color=GREY_B, font_size=20).next_to(e_yf, DOWN, buff=0.1)

        # Live values inside nodes
        def t_val():
            return MathTex(rf"{t_tracker.get_value():.2f}",
                           color=BLUE, font_size=18).move_to(pos_t + DOWN * 0.85)

        def x_val():
            return MathTex(rf"{x_of(t_tracker.get_value()):+.2f}",
                           color=GREEN, font_size=18).move_to(pos_x + DOWN * 0.85)

        def y_val():
            return MathTex(rf"{y_of(t_tracker.get_value()):+.2f}",
                           color=GREEN, font_size=18).move_to(pos_y + DOWN * 0.85)

        def f_val():
            t = t_tracker.get_value()
            v = f_xy(x_of(t), y_of(t))
            return MathTex(rf"{v:.3f}",
                           color=YELLOW, font_size=18).move_to(pos_f + DOWN * 0.85)

        def dft_val():
            t = t_tracker.get_value()
            x_v, y_v = x_of(t), y_of(t)
            v = fx(x_v, y_v) * xp(t) + fy(x_v, y_v) * yp(t)
            return MathTex(rf"{v:+.3f}",
                           color=ORANGE, font_size=18).move_to(pos_dft + DOWN * 0.85)

        self.add(always_redraw(lbl_xprime), always_redraw(lbl_yprime),
                 always_redraw(lbl_fx), always_redraw(lbl_fy),
                 always_redraw(t_val), always_redraw(x_val),
                 always_redraw(y_val), always_redraw(f_val),
                 always_redraw(dft_val))

        # Bottom verification: chain-rule sum vs analytic derivative
        # f(t) = cos²t + 3sin²t  ⇒  df/dt = -2cos t·sin t + 6 sin t·cos t = 4 sin t·cos t = 2 sin(2t)
        def verify():
            t = t_tracker.get_value()
            x_v, y_v = x_of(t), y_of(t)
            chain = fx(x_v, y_v) * xp(t) + fy(x_v, y_v) * yp(t)
            analytic = 2 * np.sin(2 * t)
            return VGroup(
                MathTex(rf"\text{{chain-rule sum}} = {chain:+.4f}",
                        color=ORANGE, font_size=22),
                MathTex(rf"\text{{analytic }} 2\sin(2t) = {analytic:+.4f}",
                        color=GREEN, font_size=22),
            ).arrange(RIGHT, buff=0.6).to_edge(DOWN, buff=0.4)

        self.add(always_redraw(verify))

        # Sweep t through 0 → 2π
        self.play(t_tracker.animate.set_value(2 * PI),
                  run_time=8, rate_func=linear)
        self.wait(1.0)
