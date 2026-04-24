from manim import *
import numpy as np


class KeplerLawsExample(Scene):
    """
    Kepler's 2nd law: equal areas swept in equal times. Visualize
    with an elliptical orbit; time-steps at perihelion and aphelion
    trace sectors of equal area but different shape.

    SINGLE_FOCUS:
      Ellipse with Sun at focus F_1. ValueTracker t_tr advances a
      planet along the orbit at non-uniform angular speed (faster
      near perihelion). always_redraw planet + swept sector; after
      each fixed Δt shown in different colors.
    """

    def construct(self):
        title = Tex(r"Kepler 2: equal areas in equal times",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        a_ax, b_ax = 3.5, 2.2
        c = np.sqrt(a_ax * a_ax - b_ax * b_ax)

        ellipse_pts = [np.array([a_ax * np.cos(t), b_ax * np.sin(t), 0])
                        for t in np.linspace(0, 2 * PI, 200)]
        ellipse = VMobject(color=BLUE, stroke_width=3)
        ellipse.set_points_as_corners(ellipse_pts + [ellipse_pts[0]])
        self.play(Create(ellipse))

        F1 = np.array([c, 0, 0])  # Sun at right focus
        sun = Dot(F1, color=YELLOW, radius=0.2)
        sun_lbl = MathTex(r"\odot", color=YELLOW, font_size=20
                            ).next_to(sun, DOWN, buff=0.1)
        self.play(FadeIn(sun), Write(sun_lbl))

        # Planet position via Kepler-like time: use E-t parametrization
        # For simplicity, use true anomaly progressing via 1/r² law
        # Approximate with angular speed ω(θ) = ω_0 · (1 + e cos θ)² / (1-e²)^1.5
        e = c / a_ax
        # Mean anomaly grows uniformly; true anomaly inverted via Kepler's eq.
        # For visualization, use a precomputed table of positions at equal Δt.

        def orbit_position(M):
            """Given mean anomaly M (in [0, 2π]), return (x, y)."""
            # Solve Kepler's equation M = E - e sin E
            E = M
            for _ in range(5):
                E = M + e * np.sin(E)
            x_orb = a_ax * (np.cos(E) - e)
            y_orb = b_ax * np.sin(E)
            # Position relative to F1 = (c, 0):
            return np.array([x_orb, y_orb, 0])

        # The planet moves uniformly in M
        t_tr = ValueTracker(0.0)

        def planet():
            t = t_tr.get_value()
            M = 2 * PI * t
            p = orbit_position(M)
            return Dot(p, color=RED, radius=0.12)

        def orbit_trail():
            t = t_tr.get_value()
            pts = []
            N = max(10, int(200 * t))
            for ti in np.linspace(0, t, N):
                M = 2 * PI * ti
                pts.append(orbit_position(M))
            m = VMobject(color=ORANGE, stroke_width=2,
                           stroke_opacity=0.6)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        self.add(always_redraw(orbit_trail), always_redraw(planet))

        # Draw 4 sectors at equal time intervals (from t = 0, 0.25, 0.5, 0.75)
        sector_colors = [GREEN, YELLOW, PURPLE, PINK]
        dt = 0.08  # sector duration
        for i, t_start in enumerate([0.02, 0.3, 0.55, 0.8]):
            pts = [F1]
            for ti in np.linspace(t_start, t_start + dt, 20):
                M = 2 * PI * ti
                pts.append(orbit_position(M))
            pts.append(F1)
            sector = Polygon(*pts, color=sector_colors[i],
                               fill_opacity=0.5, stroke_width=1)
            self.add(sector)

        note = Tex(r"4 colored sectors = equal time, equal area",
                    color=WHITE, font_size=20).to_edge(DOWN, buff=0.25)
        self.play(Write(note))

        def info():
            t = t_tr.get_value()
            M = 2 * PI * t
            p = orbit_position(M)
            r = np.linalg.norm(p - F1)
            return VGroup(
                MathTex(rf"t/T = {t:.2f}", color=WHITE, font_size=22),
                MathTex(rf"r = {r:.2f}", color=RED, font_size=22),
                MathTex(r"dA/dt = \text{const}",
                         color=GREEN, font_size=22),
                MathTex(rf"e = {e:.3f}",
                         color=YELLOW, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.3).shift(UP * 0.5)

        self.add(always_redraw(info))

        self.play(t_tr.animate.set_value(1.0),
                   run_time=10, rate_func=linear)
        self.wait(0.5)
