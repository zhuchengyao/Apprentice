from manim import *
import numpy as np


class HarmonicFunctionsExample(Scene):
    """
    Harmonic functions: u satisfying Laplace's equation Δu = 0.
    Equivalently, u is the real part of a holomorphic function.
    Example: u(x, y) = x² - y² = Re(z²).

    SINGLE_FOCUS:
      Heatmap of u(x, y) = x² - y² on 20×20 grid. ValueTracker
      t_tr rotates through harmonic examples Re(z²), Re(z³), Re(e^z).
    """

    def construct(self):
        title = Tex(r"Harmonic functions: $\Delta u = 0$, $u = \Re f$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane_center = np.array([-1.5, -0.3, 0])
        size = 4.5
        N = 20
        cell = size / N

        # State cycles through examples
        examples = [
            (lambda z: (z ** 2).real, "u = Re(z^2) = x^2 - y^2"),
            (lambda z: (z ** 3).real, "u = Re(z^3) = x^3 - 3xy^2"),
            (lambda z: np.real(np.exp(z)), "u = Re(e^z) = e^x \\cos y"),
        ]

        idx_tr = ValueTracker(0)

        def heatmap():
            i = int(round(idx_tr.get_value())) % len(examples)
            f, _ = examples[i]
            grp = VGroup()
            # Compute values on 20×20 grid over [-2, 2]²
            xs = np.linspace(-2, 2, N + 1)
            vals = np.zeros((N, N))
            for r in range(N):
                for c in range(N):
                    x = (xs[c] + xs[c + 1]) / 2
                    y = (xs[r] + xs[r + 1]) / 2  # inverted
                    vals[r, c] = f(x + 1j * y)
            # Normalize
            vmax = max(abs(vals.max()), abs(vals.min()))
            for r in range(N):
                for c in range(N):
                    v = vals[r, c]
                    frac = (v + vmax) / (2 * vmax + 1e-8)
                    col = interpolate_color(BLUE_E, RED, frac)
                    sq = Square(side_length=cell * 0.95,
                                  color=col, fill_opacity=0.85,
                                  stroke_width=0)
                    sq.move_to(plane_center + np.array([
                        (c + 0.5 - N / 2) * cell,
                        (N / 2 - r - 0.5) * cell, 0]))
                    grp.add(sq)
            return grp

        self.add(always_redraw(heatmap))

        def formula_label():
            i = int(round(idx_tr.get_value())) % len(examples)
            _, lbl = examples[i]
            return MathTex(lbl, color=YELLOW, font_size=24
                             ).to_edge(RIGHT, buff=0.3).shift(UP * 0.5)

        self.add(always_redraw(formula_label))

        info = VGroup(
            MathTex(r"\Delta u = \partial_{xx} u + \partial_{yy} u = 0",
                     color=WHITE, font_size=20),
            Tex(r"RED: positive, BLUE: negative",
                 color=WHITE, font_size=18),
            Tex(r"mean-value property at every point",
                 color=GREEN, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.3)
        self.play(Write(info))

        for i in range(1, len(examples)):
            self.play(idx_tr.animate.set_value(i),
                       run_time=1.3, rate_func=smooth)
            self.wait(1.0)
        self.wait(0.4)
