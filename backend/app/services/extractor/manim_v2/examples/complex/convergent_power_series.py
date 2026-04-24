from manim import *
import numpy as np


class ConvergentPowerSeriesExample(Scene):
    """
    Radius of convergence: the series Σ z^n / n! converges for all
    z (R = ∞), but Σ z^n converges only for |z| < 1 (R = 1).

    COMPARISON:
      LEFT ComplexPlane showing |z| < R convergence disk for Σ z^n
      (R = 1, blue filled); RIGHT ComplexPlane for Σ z^n/n! (R = ∞,
      everywhere green). Moving test point shows where partial sums
      converge / diverge.
    """

    def construct(self):
        title = Tex(r"Radius of convergence: $\sum z^n$ (R=1) vs $\sum z^n/n!$ (R=$\infty$)",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        left = ComplexPlane(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                              x_length=5, y_length=5,
                              background_line_style={"stroke_opacity": 0.25}
                              ).move_to([-3.5, -0.3, 0])
        right = ComplexPlane(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                               x_length=5, y_length=5,
                               background_line_style={"stroke_opacity": 0.25}
                               ).move_to([3.5, -0.3, 0])
        self.play(Create(left), Create(right))

        # LEFT: geometric series — convergence disk R=1
        conv_disk_L = Circle(radius=left.c2p(1, 0)[0] - left.c2p(0, 0)[0],
                               color=BLUE, stroke_width=3,
                               fill_opacity=0.2).move_to(left.c2p(0, 0))
        self.play(Create(conv_disk_L))

        left_lbl = MathTex(r"\sum_{n=0}^\infty z^n,\ R=1",
                             color=BLUE, font_size=20
                             ).next_to(left, UP, buff=0.1)
        right_lbl = MathTex(r"\sum_{n=0}^\infty z^n/n!,\ R=\infty",
                              color=GREEN, font_size=20
                              ).next_to(right, UP, buff=0.1)
        self.play(Write(left_lbl), Write(right_lbl))

        # RIGHT: exponential — converges everywhere; fill plane GREEN
        conv_plane_R = Rectangle(
            width=right.c2p(2, 0)[0] - right.c2p(-2, 0)[0],
            height=right.c2p(0, 2)[1] - right.c2p(0, -2)[1],
            color=GREEN, stroke_width=2,
            fill_opacity=0.15
        ).move_to(right.c2p(0, 0))
        self.play(Create(conv_plane_R))

        # Moving test point: same z on both planes
        theta_tr = ValueTracker(0.0)
        r_tr = ValueTracker(0.5)

        def z_left():
            r = r_tr.get_value()
            t = theta_tr.get_value()
            return left.c2p(r * np.cos(t), r * np.sin(t))

        def z_right():
            r = r_tr.get_value()
            t = theta_tr.get_value()
            return right.c2p(r * np.cos(t), r * np.sin(t))

        def z_dot_L():
            r = r_tr.get_value()
            inside = r < 1
            return Dot(z_left(), color=YELLOW if inside else RED,
                        radius=0.12)

        def z_dot_R():
            return Dot(z_right(), color=YELLOW, radius=0.12)

        self.add(always_redraw(z_dot_L), always_redraw(z_dot_R))

        def info():
            r = r_tr.get_value()
            t = theta_tr.get_value()
            z = r * np.exp(1j * t)
            # Partial sums at N=50
            N = 50
            s1 = sum(z ** k for k in range(N + 1)) if r < 1 else float("inf")
            s2 = sum(z ** k / np.math.factorial(k) for k in range(N + 1))
            return VGroup(
                MathTex(rf"|z| = {r:.2f}", color=YELLOW, font_size=22),
                MathTex(rf"\sum z^n (N=50)",
                         color=BLUE, font_size=20),
                MathTex(rf"\ |\text{{diverges}}|" if r >= 1 else rf"\to 1/(1-z) = ({(1/(1-z)).real:.2f}, {(1/(1-z)).imag:.2f})",
                         color=BLUE if r < 1 else RED, font_size=18),
                MathTex(rf"\sum z^n/n!", color=GREEN, font_size=20),
                MathTex(rf"\ \to e^z = ({np.exp(z).real:.2f}, {np.exp(z).imag:.2f})",
                         color=GREEN, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        # Phase 1: rotate at r=0.5 (inside both)
        self.play(theta_tr.animate.set_value(2 * PI),
                   run_time=3, rate_func=linear)
        # Phase 2: increase r past 1
        self.play(r_tr.animate.set_value(1.8),
                   run_time=3, rate_func=smooth)
        # Phase 3: rotate at r=1.8 (outside LEFT, inside RIGHT)
        self.play(theta_tr.animate.set_value(4 * PI),
                   run_time=3, rate_func=linear)
        self.wait(0.4)
