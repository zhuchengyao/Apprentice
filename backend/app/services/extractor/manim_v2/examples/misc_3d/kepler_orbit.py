from manim import *
import numpy as np


class KeplerOrbitExample(Scene):
    def construct(self):
        title = Text("Kepler's 2nd law: equal areas in equal time", font_size=28).to_edge(UP)
        self.play(Write(title))

        a, b = 3.2, 2.0
        c = np.sqrt(a**2 - b**2)
        orbit = Ellipse(width=2 * a, height=2 * b, color=BLUE).shift(0.3 * DOWN)
        sun = Dot(orbit.get_center() + LEFT * c, color=YELLOW, radius=0.14)
        sun_lbl = Text("Sun", font_size=22, color=YELLOW).next_to(sun, UP, buff=0.1)
        self.play(Create(orbit), FadeIn(sun), Write(sun_lbl))

        def pt(theta):
            return orbit.get_center() + np.array([a * np.cos(theta), b * np.sin(theta), 0])

        def wedge(theta_start, theta_end, color):
            n = 30
            pts = [sun.get_center()]
            for k in range(n + 1):
                t = theta_start + (theta_end - theta_start) * k / n
                pts.append(pt(t))
            p = Polygon(*pts, color=color, fill_opacity=0.45, stroke_width=2)
            return p

        # Near perihelion: small arc in angle, but large area due to proximity to sun
        # Near aphelion: large arc in angle, area equal
        w1 = wedge(-0.6, 0.6, RED)
        w2 = wedge(PI - 0.25, PI + 0.25, GREEN)
        self.play(FadeIn(w1), FadeIn(w2))

        planet = Dot(pt(-0.6), color=WHITE, radius=0.1)
        self.play(FadeIn(planet))
        self.play(MoveAlongPath(planet, Arc(radius=a, start_angle=0, angle=1.2).shift(orbit.get_center())),
                  run_time=2)
        self.wait(0.3)

        caption = MathTex(r"\frac{dA}{dt} = \text{const}", font_size=34, color=YELLOW).to_edge(DOWN)
        self.play(Write(caption))
        self.wait(0.6)
