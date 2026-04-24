from manim import *
import numpy as np


class PlanetsScaledExample(Scene):
    """
    Solar system planets to scale (from _2025/cosmic_distance/planets):
    radii and orbital distances differ by orders of magnitude. Shown
    on a log-scale distance axis with ValueTracker zoom_tr transitioning
    from a log view to a linear view that loses Mercury/Venus.

    SINGLE_FOCUS:
      Horizontal axis; 8 planets placed at their AU distance. In log
      mode all 8 visible; in linear mode inner planets collapse
      together. zoom_tr interpolates.
    """

    def construct(self):
        title = Tex(r"Scale of the solar system: log vs linear",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Distances in AU
        planets = [
            ("Mercury", 0.39, GREY_B),
            ("Venus",   0.72, ORANGE),
            ("Earth",   1.00, BLUE),
            ("Mars",    1.52, RED),
            ("Jupiter", 5.20, GOLD),
            ("Saturn",  9.58, YELLOW),
            ("Uranus",  19.2, TEAL),
            ("Neptune", 30.1, BLUE_D),
        ]

        # Build "log" and "linear" scene positions
        x_lo_log = -5.5
        x_hi_log = 5.5
        # log10(max) = log10(30.1) ≈ 1.48
        def log_pos(d):
            return x_lo_log + (np.log10(d) + 0.5) / 2.0 * (x_hi_log - x_lo_log)

        # Linear: x = lo + (d / 30.1) * (hi - lo)
        def lin_pos(d):
            return x_lo_log + d / 30.1 * (x_hi_log - x_lo_log)

        zoom_tr = ValueTracker(0.0)  # 0 = log, 1 = linear

        # Axis line
        axis = Line([x_lo_log, -0.5, 0], [x_hi_log, -0.5, 0],
                      color=WHITE, stroke_width=2)
        self.play(Create(axis))

        # Sun marker
        sun = Dot([x_lo_log, -0.5, 0], color=YELLOW, radius=0.18)
        sun_lbl = Tex(r"Sun", color=YELLOW, font_size=18
                       ).next_to(sun, DOWN, buff=0.15)
        self.play(FadeIn(sun), Write(sun_lbl))

        def planet_positions():
            z = zoom_tr.get_value()
            grp = VGroup()
            for (name, d, col) in planets:
                x_log = log_pos(d)
                x_lin = lin_pos(d)
                x = (1 - z) * x_log + z * x_lin
                dot = Dot([x, -0.5, 0], color=col, radius=0.12)
                lbl = Tex(name, font_size=14, color=col).next_to(
                    dot, UP, buff=0.15)
                dist_lbl = MathTex(rf"{d}\,\text{{AU}}", font_size=12,
                                     color=col).next_to(dot, DOWN, buff=0.15)
                grp.add(dot, lbl, dist_lbl)
            return grp

        self.add(always_redraw(planet_positions))

        def mode_lbl():
            z = zoom_tr.get_value()
            if z < 0.2:
                txt = "log scale — all 8 visible"
                col = GREEN
            elif z > 0.8:
                txt = "linear scale — inner planets collapse"
                col = RED
            else:
                txt = "interpolating..."
                col = YELLOW
            return Tex(txt, color=col, font_size=24
                        ).to_edge(DOWN, buff=0.5)

        self.add(always_redraw(mode_lbl))

        self.play(zoom_tr.animate.set_value(1.0),
                   run_time=4, rate_func=smooth)
        self.wait(1.0)
        self.play(zoom_tr.animate.set_value(0.0),
                   run_time=3, rate_func=smooth)
        self.wait(0.4)
