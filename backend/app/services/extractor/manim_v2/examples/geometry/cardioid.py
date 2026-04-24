from manim import *
import numpy as np


class CardioidExample(Scene):
    def construct(self):
        title = Text("Cardioid: locus of a point on a rolling circle", font_size=26).to_edge(UP)
        self.play(Write(title))

        R = 1.2
        fixed = Circle(radius=R, color=BLUE).shift(0.2 * DOWN)
        self.play(Create(fixed))

        t_tracker = ValueTracker(0.01)

        def rolling_circle():
            t = t_tracker.get_value()
            center_fixed = fixed.get_center()
            theta = t
            contact = center_fixed + R * np.array([np.cos(theta), np.sin(theta), 0])
            rolling_center = center_fixed + 2 * R * np.array([np.cos(theta), np.sin(theta), 0])
            c = Circle(radius=R, color=ORANGE)
            c.move_to(rolling_center)
            return c

        def traced_point():
            t = t_tracker.get_value()
            center_fixed = fixed.get_center()
            x = center_fixed[0] + 2 * R * np.cos(t) - R * np.cos(2 * t)
            y = center_fixed[1] + 2 * R * np.sin(t) - R * np.sin(2 * t)
            return Dot([x, y, 0], color=YELLOW, radius=0.09)

        rc = always_redraw(rolling_circle)
        tp = always_redraw(traced_point)
        self.add(rc, tp)

        # Manually create the cardioid path and draw it as tracker advances
        cardioid_path = ParametricFunction(
            lambda t: fixed.get_center() + np.array([
                2 * R * np.cos(t) - R * np.cos(2 * t),
                2 * R * np.sin(t) - R * np.sin(2 * t),
                0,
            ]),
            t_range=[0, TAU],
            color=YELLOW, stroke_width=3,
        )
        self.play(Create(cardioid_path), t_tracker.animate.set_value(TAU - 0.01), run_time=5)
        self.wait(0.3)

        formula = MathTex(r"r(\theta) = 2R(1 - \cos\theta)",
                          font_size=32, color=YELLOW).to_edge(DOWN)
        self.play(Write(formula))
        self.wait(0.6)
