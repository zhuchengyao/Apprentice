from manim import *
import numpy as np


class Diffusion2DHeatExample(Scene):
    """
    2D heat diffusion (from _2020/18S191/diffusion): a sharp hot
    spot spreads out over time. Visualized on a 25×15 cell grid
    with always_redraw heatmap colored by temperature.

    SINGLE_FOCUS:
      ValueTracker t_tr advances time; u(x, y, t) = exp(-(x²+y²)/
      (4αt + σ₀²)) / (4παt + σ₀²) — a Gaussian spreading kernel
      initial condition. Rebuilds heatmap each frame.
    """

    def construct(self):
        title = Tex(r"2D heat diffusion: Gaussian spreads as $\sigma^2 \sim 4\alpha t$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        cols, rows = 25, 15
        alpha = 0.2

        cell = 0.42
        origin = np.array([-cell * (cols - 1) / 2,
                             cell * (rows - 1) / 2 - 0.3, 0])

        # Sharp initial: sigma0 = 0.3
        sigma0_sq = 0.09

        t_tr = ValueTracker(0.0)

        def u_at(x, y, t):
            var = 4 * alpha * t + sigma0_sq
            return np.exp(-(x * x + y * y) / var) / var * sigma0_sq

        def heat_cells():
            t = t_tr.get_value()
            grp = VGroup()
            for r in range(rows):
                for c in range(cols):
                    # x in [-6, 6], y in [-3, 3]
                    x = (c - (cols - 1) / 2) * 0.5
                    y = ((rows - 1) / 2 - r) * 0.4
                    val = u_at(x, y, t)
                    intensity = min(1.0, val)
                    col = interpolate_color(BLUE_E, RED, intensity)
                    sq = Square(side_length=cell * 0.95,
                                  color=col, fill_opacity=0.85,
                                  stroke_width=0)
                    sq.move_to(origin + np.array([c * cell,
                                                       -r * cell, 0]))
                    grp.add(sq)
            return grp

        self.add(always_redraw(heat_cells))

        def info():
            t = t_tr.get_value()
            sigma = np.sqrt(4 * alpha * t + sigma0_sq)
            return VGroup(
                MathTex(rf"t = {t:.2f}", color=YELLOW, font_size=24),
                MathTex(rf"\sigma = \sqrt{{4\alpha t + \sigma_0^2}} = {sigma:.3f}",
                         color=GREEN, font_size=22),
                MathTex(rf"\alpha = {alpha}", color=WHITE, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        self.play(t_tr.animate.set_value(5),
                   run_time=8, rate_func=linear)
        self.wait(0.4)
