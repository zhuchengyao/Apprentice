from manim import *
import numpy as np


class ParallaxMeasurementExample(Scene):
    """
    Parallax: as Earth orbits, a nearby star appears to shift against
    far background stars by an angle 2p; distance d = 1/p arcsec.

    SINGLE_FOCUS:
      Sun + Earth orbit. ValueTracker θ moves Earth around the orbit.
      A "nearby" yellow star sits to the upper right; faint background
      stars stay fixed. always_redraw line of sight from Earth to the
      star traces against the background; the apparent star position
      shifts left-right against the background as Earth orbits.
    """

    def construct(self):
        title = Tex(r"Parallax: $d = \dfrac{1}{p\,\text{arcsec}}\,\text{parsec}$",
                    font_size=28).to_edge(UP, buff=0.4)
        self.play(Write(title))

        sun = Dot([-3.4, -0.4, 0], color=YELLOW, radius=0.14)
        sun_lbl = Tex(r"Sun", color=YELLOW, font_size=20).next_to(sun, DOWN, buff=0.1)
        self.play(FadeIn(sun), Write(sun_lbl))

        orbit = Circle(radius=0.9, color=BLUE,
                       stroke_opacity=0.5).move_to(sun.get_center())
        self.play(Create(orbit))

        # Nearby star
        star = Dot([+2.5, +1.3, 0], color=WHITE, radius=0.12)
        star_lbl = Tex(r"nearby star", color=WHITE,
                       font_size=18).next_to(star, UP, buff=0.1)
        self.play(FadeIn(star), Write(star_lbl))

        # Background stars (fixed)
        np.random.seed(3)
        bg_stars = VGroup()
        for _ in range(40):
            p = np.array([np.random.uniform(3.0, 6.5),
                          np.random.uniform(-1.5, 3.5), 0])
            bg_stars.add(Dot(p, color=GREY_B, radius=0.04))
        self.play(FadeIn(bg_stars))

        # Earth on the orbit
        theta_tr = ValueTracker(0.0)

        def earth_pt():
            t = theta_tr.get_value()
            return sun.get_center() + 0.9 * np.array([np.cos(t), np.sin(t), 0])

        def earth_dot():
            return Dot(earth_pt(), color=BLUE, radius=0.10)

        def line_of_sight():
            return Line(earth_pt(), star.get_center(),
                        color=ORANGE, stroke_width=2)

        # The apparent (projected) position of the star against the background
        # Approximate: extend the line beyond the star to a fixed background plane
        def apparent_position():
            E = earth_pt()
            S = star.get_center()
            direction = S - E
            direction = direction / np.linalg.norm(direction)
            # Project to a vertical line at x = +5.0 (background screen)
            screen_x = 5.5
            t = (screen_x - S[0]) / direction[0]
            return Dot(S + direction * t, color=ORANGE, radius=0.08)

        self.add(always_redraw(earth_dot),
                 always_redraw(line_of_sight),
                 always_redraw(apparent_position))

        # RIGHT COLUMN
        rcol_x = +5.5

        def info_panel():
            t = theta_tr.get_value()
            return VGroup(
                MathTex(rf"\theta = {np.degrees(t):.0f}^\circ",
                        color=BLUE, font_size=22),
                Tex(r"orange dot $=$ apparent",
                    color=ORANGE, font_size=20),
                Tex(r"position against bg",
                    color=ORANGE, font_size=18),
                MathTex(r"d = 1/p\,\text{parsec}",
                        color=YELLOW, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([rcol_x, -2.0, 0])

        self.add(always_redraw(info_panel))

        # Sweep Earth around the orbit twice
        self.play(theta_tr.animate.set_value(4 * PI),
                  run_time=10, rate_func=linear)
        self.wait(0.6)
