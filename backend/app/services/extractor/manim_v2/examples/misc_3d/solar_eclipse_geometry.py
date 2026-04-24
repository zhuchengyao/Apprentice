from manim import *
import numpy as np


class SolarEclipseGeometryExample(Scene):
    """
    Solar eclipse coincidence: the Moon's angular diameter ≈ the
    Sun's angular diameter because the Moon is 400× smaller but 400×
    closer. Visualize the shadow-cone geometry.

    SINGLE_FOCUS:
      Earth, Moon, Sun arranged; ValueTracker moon_offset_tr slides
      Moon along its orbit; always_redraw umbra cone (tangent lines
      from Sun edges past Moon) + Earth's intersection area.
    """

    def construct(self):
        title = Tex(r"Solar eclipse: angular sizes match $\approx 0.5^\circ$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Positions (scaled): Sun at x=-6, Moon slides around x=0, Earth at x=5
        sun_x = -6
        sun_r = 0.7
        moon_base_x = 0.5
        moon_r = 0.12
        earth_x = 5
        earth_r = 0.3

        moon_offset_tr = ValueTracker(0.0)

        def sun_dot():
            return Circle(radius=sun_r, color=YELLOW,
                            fill_opacity=0.9
                            ).move_to([sun_x, 0, 0])

        def moon_dot():
            off = moon_offset_tr.get_value()
            return Circle(radius=moon_r, color=GREY_B,
                            fill_opacity=1
                            ).move_to([moon_base_x, off, 0])

        def earth_dot():
            return Circle(radius=earth_r, color=BLUE,
                            fill_opacity=0.8
                            ).move_to([earth_x, 0, 0])

        def umbra_cone():
            """Draw the umbra cone from Sun top + Sun bottom tangent to Moon."""
            off = moon_offset_tr.get_value()
            moon_center = np.array([moon_base_x, off, 0])
            sun_top = np.array([sun_x, sun_r, 0])
            sun_bot = np.array([sun_x, -sun_r, 0])
            # Tangent lines from sun_top past moon touching its limb
            # Moon top tangent line from sun_top:
            # Simplify: draw line from sun_top to moon_center - up, extend to earth_x region
            # More accurate: straight lines from sun edges to Moon's opposite edge
            moon_top = moon_center + np.array([0, moon_r, 0])
            moon_bot = moon_center + np.array([0, -moon_r, 0])
            # Upper bounding ray: sun_top → moon_bot, extended
            def ray_to_x(p1, p2, x_target):
                dx = p2[0] - p1[0]
                if abs(dx) < 1e-6:
                    return p2
                t = (x_target - p1[0]) / dx
                return p1 + t * (p2 - p1)
            upper_end = ray_to_x(sun_top, moon_bot, earth_x + 2)
            lower_end = ray_to_x(sun_bot, moon_top, earth_x + 2)
            grp = VGroup()
            grp.add(Line(sun_top, upper_end, color=ORANGE,
                           stroke_width=2, stroke_opacity=0.55))
            grp.add(Line(sun_bot, lower_end, color=ORANGE,
                           stroke_width=2, stroke_opacity=0.55))
            # Fill the region between as a polygon
            shade = Polygon(sun_top, upper_end, lower_end, sun_bot,
                              color=ORANGE, fill_opacity=0.12,
                              stroke_width=0)
            grp.add(shade)
            return grp

        self.add(always_redraw(umbra_cone),
                  always_redraw(sun_dot),
                  always_redraw(moon_dot),
                  always_redraw(earth_dot))

        sun_lbl = Tex("Sun", color=YELLOW, font_size=20).move_to([sun_x, -1.3, 0])
        moon_lbl = Tex("Moon", color=GREY_B, font_size=16).move_to([moon_base_x, 0.5, 0])
        earth_lbl = Tex("Earth", color=BLUE, font_size=18).move_to([earth_x, -0.8, 0])
        self.play(Write(sun_lbl), Write(moon_lbl), Write(earth_lbl))

        def info():
            off = moon_offset_tr.get_value()
            # Moon covers sun when off ≈ 0
            coverage = 1.0 - min(1.0, abs(off) / 0.25)
            return VGroup(
                MathTex(rf"\text{{Moon offset}} = {off:+.3f}",
                         color=GREY_B, font_size=22),
                MathTex(rf"\text{{Sun coverage}} \approx {coverage:.2f}",
                         color=YELLOW, font_size=22),
                Tex(r"$R_S / d_S \approx R_M / d_M$",
                     color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        # Move Moon up/down
        self.play(moon_offset_tr.animate.set_value(0.6),
                   run_time=2, rate_func=smooth)
        self.play(moon_offset_tr.animate.set_value(-0.6),
                   run_time=3, rate_func=smooth)
        self.play(moon_offset_tr.animate.set_value(0.0),
                   run_time=2, rate_func=smooth)
        self.wait(0.5)
