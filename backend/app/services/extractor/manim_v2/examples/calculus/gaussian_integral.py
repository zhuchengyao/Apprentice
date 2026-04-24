from manim import *
import numpy as np


class GaussianIntegralExample(Scene):
    """
    The √π trick: square the integral and switch to polar.

    THREE_ROW (with side annotations):
      LEFT panel — start with two stacked copies of the 1D Gaussian e^(-x²)
                   sitting on x-axes; their *product* fills a 2D plane with
                   the radially-symmetric e^(-(x²+y²)) heatmap.
      RIGHT side — a Cartesian rectangular grid on the heatmap morphs into
                   a polar (r, θ) grid via ValueTracker s ∈ [0, 1].
      Bottom    — algebraic chain I → I² → polar → π.

    Visual proof: the Cartesian region [-R, R]² and the disk of radius R
    are both shown; for large R the integral over the disk equals
    ∫₀^{2π}∫₀^∞ e^(-r²)·r dr dθ = π, so I² = π.
    """

    def construct(self):
        title = Tex(r"Compute $I = \int e^{-x^2}\,dx$ by squaring and going polar",
                    font_size=30).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # === LEFT PANEL: 2D heatmap of e^(-(x²+y²)) ===
        plane_anchor = np.array([-3.5, -0.4, 0])
        R = 2.2
        N = 18  # grid resolution

        s = ValueTracker(0.0)

        def heatmap_cells():
            """A grid of small rectangles colored by e^(-r²). At s=0 they sit
            in a Cartesian grid; at s=1 they're warped onto a polar grid.
            """
            cells = VGroup()
            sv = s.get_value()
            for i in range(N):
                for j in range(N):
                    # Cartesian position in [-R, R]²
                    xc = -R + (i + 0.5) * (2 * R / N)
                    yc = -R + (j + 0.5) * (2 * R / N)
                    # Polar position: r∈[0, R], θ∈[0, 2π]
                    r_target = (i + 0.5) * R / N
                    th_target = (j + 0.5) * (2 * PI) / N
                    px = r_target * np.cos(th_target)
                    py = r_target * np.sin(th_target)

                    # Interpolated position
                    cx = (1 - sv) * xc + sv * px
                    cy = (1 - sv) * yc + sv * py

                    # Color by e^(-r²) of the *physical* position
                    val = np.exp(-(cx ** 2 + cy ** 2))
                    color = interpolate_color(BLACK, YELLOW, val)
                    cell_w = 2 * R / N * 0.95
                    cell_h = 2 * R / N * 0.95
                    rect = Rectangle(width=cell_w, height=cell_h,
                                     fill_color=color, fill_opacity=0.85,
                                     stroke_width=0)
                    rect.move_to([cx + plane_anchor[0], cy + plane_anchor[1], 0])
                    cells.add(rect)
            return cells

        self.add(always_redraw(heatmap_cells))

        # === RIGHT COLUMN: equation chain ===
        rcol_x = +3.4
        eq1 = MathTex(r"I = \int_{-\infty}^{\infty} e^{-x^2}\, dx",
                      font_size=28, color=BLUE).move_to([rcol_x, +2.6, 0])
        eq2 = MathTex(r"I^2 = \int_{-\infty}^{\infty}\!\!\int_{-\infty}^{\infty}"
                      r" e^{-(x^2+y^2)}\, dx\, dy",
                      font_size=22, color=GREEN).move_to([rcol_x, +1.5, 0])
        eq3 = MathTex(r"= \int_0^{2\pi}\!\!\int_0^{\infty} e^{-r^2}\, r\, dr\, d\theta",
                      font_size=24, color=ORANGE).move_to([rcol_x, +0.4, 0])
        eq4 = MathTex(r"= 2\pi \cdot \tfrac{1}{2} = \pi",
                      font_size=28, color=ORANGE).move_to([rcol_x, -0.7, 0])
        eq5 = MathTex(r"I = \sqrt{\pi}",
                      font_size=44, color=YELLOW).move_to([rcol_x, -2.0, 0])

        self.play(Write(eq1))
        self.wait(0.5)
        self.play(Write(eq2))
        self.wait(0.6)

        # Now morph: Cartesian → polar
        self.play(Write(eq3), s.animate.set_value(1.0),
                  run_time=4.5, rate_func=smooth)
        self.wait(0.5)
        self.play(Write(eq4))
        self.play(Write(eq5))
        self.wait(1.0)
