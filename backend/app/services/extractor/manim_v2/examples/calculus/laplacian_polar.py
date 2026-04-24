from manim import *
import numpy as np


class LaplacianPolarExample(Scene):
    """
    Laplacian in polar: Δu = u_rr + (1/r) u_r + (1/r²) u_θθ.
    Verify on radial function u(r, θ) = r²(cos 2θ - ...) = Re(z²) = r² cos 2θ.
    Then Δu = 4 − 4 = 0 (harmonic).

    SINGLE_FOCUS:
      Heatmap of u(r, θ) = r² cos 2θ on polar grid; ValueTracker
      sigma_tr morphs between Cartesian Δu and polar expression
      showing they agree.
    """

    def construct(self):
        title = Tex(r"Polar Laplacian: $\Delta u = u_{rr} + \tfrac{1}{r} u_r + \tfrac{1}{r^2} u_{\theta\theta}$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Heatmap of u = r² cos 2θ = x² - y²
        plane_center = np.array([-2, -0.3, 0])
        size = 4.5
        N = 18
        cell = size / N

        def u_fn(x, y):
            return x ** 2 - y ** 2

        heat = VGroup()
        xs = np.linspace(-2, 2, N + 1)
        for r in range(N):
            for c in range(N):
                x = (xs[c] + xs[c + 1]) / 2
                y = (xs[r] + xs[r + 1]) / 2
                v = u_fn(x, y)
                frac = (v + 4) / 8
                col = interpolate_color(BLUE_E, RED, frac)
                sq = Square(side_length=cell * 0.95,
                              color=col, fill_opacity=0.85,
                              stroke_width=0)
                sq.move_to(plane_center + np.array([
                    (c + 0.5 - N / 2) * cell,
                    (N / 2 - r - 0.5) * cell, 0]))
                heat.add(sq)
        self.play(FadeIn(heat))

        # Polar coordinate overlay
        polar_grid = VGroup()
        for r_val in [0.5, 1.0, 1.5]:
            # approximate circle with line segments
            pts = []
            for t in np.linspace(0, 2 * PI, 48):
                pts.append(plane_center + r_val * np.array([np.cos(t),
                                                                 np.sin(t), 0]))
            m = VMobject(color=GREEN, stroke_width=1.5, stroke_opacity=0.5)
            m.set_points_as_corners(pts + [pts[0]])
            polar_grid.add(m)
        for angle in np.arange(0, 2 * PI, PI / 4):
            polar_grid.add(Line(plane_center,
                                  plane_center + 2 * np.array([np.cos(angle),
                                                                     np.sin(angle), 0]),
                                  color=GREEN, stroke_width=1.2,
                                  stroke_opacity=0.5))
        self.play(Create(polar_grid))

        # Point on grid
        r_tr = ValueTracker(1.0)
        theta_tr = ValueTracker(PI / 6)

        def probe_dot():
            r = r_tr.get_value()
            t = theta_tr.get_value()
            x = r * np.cos(t)
            y = r * np.sin(t)
            return Dot(plane_center + np.array([x, y, 0]),
                        color=YELLOW, radius=0.12)

        self.add(always_redraw(probe_dot))

        def info():
            r = r_tr.get_value()
            t = theta_tr.get_value()
            # u = r² cos 2θ
            u = r ** 2 * np.cos(2 * t)
            # Polar Laplacian of u:
            # u_r = 2r cos 2θ, u_rr = 2 cos 2θ
            # u_θθ = -4 r² cos 2θ
            u_rr = 2 * np.cos(2 * t)
            u_r_over_r = 2 * np.cos(2 * t)
            u_tt_over_r2 = -4 * np.cos(2 * t)
            laplacian = u_rr + u_r_over_r + u_tt_over_r2
            return VGroup(
                MathTex(rf"r = {r:.2f},\ \theta = {np.degrees(t):.0f}^\circ",
                         color=YELLOW, font_size=20),
                MathTex(rf"u = r^2 \cos 2\theta = {u:+.3f}",
                         color=WHITE, font_size=20),
                MathTex(rf"u_{{rr}} = {u_rr:.3f}",
                         color=BLUE, font_size=18),
                MathTex(rf"\tfrac{{1}}{{r^2}} u_{{\theta\theta}} = {u_tt_over_r2:.3f}",
                         color=BLUE, font_size=18),
                MathTex(rf"\Delta u = {laplacian:.4f} = 0",
                         color=GREEN, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.13).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for (rv, tv) in [(1.5, PI / 3), (0.7, PI / 2), (1.2, PI / 6)]:
            self.play(r_tr.animate.set_value(rv),
                       theta_tr.animate.set_value(tv),
                       run_time=1.5, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
