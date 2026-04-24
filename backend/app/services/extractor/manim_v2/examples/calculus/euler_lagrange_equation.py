from manim import *
import numpy as np


class EulerLagrangeEquationExample(Scene):
    """
    Euler-Lagrange: the curve y(x) between (0,0) and (1,1) that
    minimizes J[y] = ∫_0^1 √(1+y'^2) dx is the straight line.

    TWO_COLUMN:
      LEFT: axes with BLUE straight-line extremum; a GREEN candidate
      curve y_s(x) = x + s·sin(πx) with ValueTracker s_tr tours
      s ∈ {0.0, 0.4, -0.4, 0.8, -0.8, 0} via always_redraw.
      RIGHT: EL equation d/dx(∂L/∂y') - ∂L/∂y = 0 for L=√(1+y'²);
      derivation ⇒ y'' = 0 (line). Live J[y_s] numeric readout
      minimized at s=0.
    """

    def construct(self):
        title = Tex(r"Euler-Lagrange: minimize $J[y] = \int_0^1 \sqrt{1+y'^2}\,dx$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[0, 1.05, 0.25], y_range=[0, 1.8, 0.5],
                    x_length=5.2, y_length=4.0,
                    axis_config={"include_numbers": False}).shift(LEFT * 2.6 + DOWN * 0.3)
        self.play(Create(axes))

        # Straight-line extremum
        line_ext = axes.plot(lambda x: x, x_range=[0, 1], color=BLUE, stroke_width=5)
        line_lbl = Tex(r"$y=x$ (extremum)", color=BLUE, font_size=22).next_to(axes, DOWN, buff=0.2)
        self.play(Create(line_ext), Write(line_lbl))

        s_tr = ValueTracker(0.0)

        def candidate():
            s = s_tr.get_value()
            return axes.plot(lambda x: x + s * np.sin(PI * x),
                             x_range=[0, 1], color=GREEN, stroke_width=4)

        self.add(always_redraw(candidate))

        def J_value():
            s = s_tr.get_value()
            xs = np.linspace(0, 1, 200)
            yp = 1 + s * PI * np.cos(PI * xs)
            return float(np.trapezoid(np.sqrt(1 + yp ** 2), xs))

        # Right column: derivation + readouts
        eq1 = Tex(r"$L = \sqrt{1+y'^2}$", font_size=22)
        eq2 = Tex(r"$\dfrac{\partial L}{\partial y} = 0$", font_size=22)
        eq3 = Tex(r"$\dfrac{\partial L}{\partial y'} = \dfrac{y'}{\sqrt{1+y'^2}}$",
                  font_size=22)
        eq4 = Tex(r"$\dfrac{d}{dx}\dfrac{y'}{\sqrt{1+y'^2}} = 0 \Rightarrow y''=0$",
                  color=YELLOW, font_size=22)
        eq5 = Tex(r"$y(x)=x$ (unique line through $(0,0),(1,1)$)",
                  color=BLUE, font_size=22)
        derivation = VGroup(eq1, eq2, eq3, eq4, eq5).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        derivation.to_edge(RIGHT, buff=0.4).shift(UP * 0.9)

        for e in derivation:
            self.play(Write(e), run_time=0.5)

        s_lbl = VGroup(
            Tex(r"$y_s(x)=x+s\sin\pi x$", color=GREEN, font_size=22),
            VGroup(Tex(r"$s=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2, font_size=22).set_color(GREEN)
                   ).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$J[y_s]=$", font_size=22),
                   DecimalNumber(J_value(), num_decimal_places=4, font_size=22).set_color(YELLOW)
                   ).arrange(RIGHT, buff=0.1),
            Tex(r"min at $s=0$: $J=\sqrt{2}$", color=YELLOW, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.4).shift(DOWN * 1.7)

        s_lbl[1][1].add_updater(lambda m: m.set_value(s_tr.get_value()))
        s_lbl[2][1].add_updater(lambda m: m.set_value(J_value()))
        self.add(s_lbl)

        # Tour
        for sval in [0.4, -0.4, 0.8, -0.8, 0.0]:
            self.play(s_tr.animate.set_value(sval), run_time=1.4, rate_func=smooth)
            self.wait(0.2)

        self.wait(0.8)
