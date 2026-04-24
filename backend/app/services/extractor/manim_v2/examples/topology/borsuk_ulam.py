from manim import *
import numpy as np


class BorsukUlamExample(Scene):
    """
    Borsuk-Ulam in 1D version: f: S¹ → ℝ has antipodal points with f(p) = f(-p).

    SINGLE_FOCUS:
      Top: unit circle parametrized by θ ∈ [0, 2π]. ValueTracker θ moves
      a yellow point P(θ) and a red point P(θ+π) (its antipode).
      Bottom: graph of f(θ) = sin(2θ) + 0.5·cos(3θ); ValueTracker θ
      drives two always_redraw dots tracking f(θ) and f(θ+π). When the
      two values coincide (zero of g(θ) = f(θ) - f(θ+π)), markers
      flash GREEN.
    """

    def construct(self):
        title = Tex(r"Borsuk-Ulam ($n=1$): $\exists\, \theta$ with $f(\theta) = f(\theta + \pi)$",
                    font_size=24).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # TOP: unit circle (small)
        circle = Circle(radius=1.2, color=BLUE,
                        stroke_width=2).move_to([-3.2, +1.4, 0])
        self.play(Create(circle))

        # BOTTOM: f(θ) graph
        f = lambda t: np.sin(2 * t) + 0.5 * np.cos(3 * t)
        axes = Axes(
            x_range=[0, 2 * PI, PI / 2], y_range=[-1.6, 1.6, 0.5],
            x_length=8.0, y_length=2.8,
            axis_config={"include_tip": True, "include_numbers": False, "font_size": 16},
        ).move_to([+1.0, -1.6, 0])
        f_curve = axes.plot(f, x_range=[0, 2 * PI - 0.01, 0.05], color=BLUE)
        self.play(Create(axes), Create(f_curve))

        theta_tr = ValueTracker(0.5)

        # Circle: P and its antipode
        def P_pt():
            t = theta_tr.get_value()
            c = circle.get_center()
            return c + 1.2 * np.array([np.cos(t), np.sin(t), 0])

        def Q_pt():
            t = theta_tr.get_value() + PI
            c = circle.get_center()
            return c + 1.2 * np.array([np.cos(t), np.sin(t), 0])

        def p_dot():
            return Dot(P_pt(), color=YELLOW, radius=0.10)

        def q_dot():
            return Dot(Q_pt(), color=RED, radius=0.10)

        def chord():
            return Line(P_pt(), Q_pt(), color=GREY_B,
                        stroke_width=1.5, stroke_opacity=0.5)

        # Graph: dots at f(θ) and f(θ+π)
        def f_dot():
            t = theta_tr.get_value()
            return Dot(axes.c2p(t, f(t)), color=YELLOW, radius=0.10)

        def fp_dot():
            t = theta_tr.get_value() + PI
            t_wrapped = t % (2 * PI)
            return Dot(axes.c2p(t_wrapped, f(t)), color=RED, radius=0.10)

        # Connector showing |f(θ) - f(θ+π)|
        def gap_line():
            t = theta_tr.get_value()
            return Line(axes.c2p(t, f(t)),
                        axes.c2p(t, f(t + PI)),
                        color=ORANGE, stroke_width=3)

        self.add(always_redraw(p_dot), always_redraw(q_dot),
                 always_redraw(chord),
                 always_redraw(f_dot), always_redraw(fp_dot),
                 always_redraw(gap_line))

        # RIGHT COLUMN
        rcol_x = +5.4

        def info_panel():
            t = theta_tr.get_value()
            f1 = f(t)
            f2 = f(t + PI)
            gap = f1 - f2
            color_gap = GREEN if abs(gap) < 0.05 else WHITE
            return VGroup(
                MathTex(rf"\theta = {t:.3f}", color=YELLOW, font_size=22),
                MathTex(rf"f(\theta) = {f1:+.3f}", color=YELLOW, font_size=20),
                MathTex(rf"f(\theta+\pi) = {f2:+.3f}", color=RED, font_size=20),
                MathTex(rf"\text{{gap}} = {gap:+.3f}",
                        color=color_gap, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([rcol_x, +1.4, 0])

        self.add(always_redraw(info_panel))

        # Sweep θ — gap will hit 0 at multiple θ
        self.play(theta_tr.animate.set_value(2 * PI + 0.5),
                  run_time=8, rate_func=linear)
        self.wait(0.6)
