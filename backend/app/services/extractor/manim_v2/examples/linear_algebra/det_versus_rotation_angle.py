from manim import *
import numpy as np


class DetVersusRotationAngleExample(Scene):
    """
    Rotate î by angle θ while keeping ĵ fixed: the matrix becomes
    [[cos θ, 0], [sin θ, 1]] and its determinant is cos θ.

    TWO_COLUMN: LEFT plane showing the rotation; RIGHT plot of det
    as cos curve. Dots on both sides tied to shared ValueTracker.
    """

    def construct(self):
        title = Tex(r"Rotate $\hat\imath$: $\det = \cos\theta$ traces a cosine",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                            x_length=5.0, y_length=5.0,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(LEFT * 3.0 + DOWN * 0.2)
        self.play(Create(plane))

        theta_tr = ValueTracker(0.0)

        def M_of():
            t = theta_tr.get_value()
            return np.array([[np.cos(t), 0.0], [np.sin(t), 1.0]])

        def i_arrow():
            M = M_of()
            p = M @ np.array([1, 0])
            return Arrow(plane.c2p(0, 0), plane.c2p(p[0], p[1]),
                          color=GREEN, buff=0, stroke_width=5)

        def j_arrow():
            M = M_of()
            p = M @ np.array([0, 1])
            return Arrow(plane.c2p(0, 0), plane.c2p(p[0], p[1]),
                          color=RED, buff=0, stroke_width=5)

        def parallelogram():
            M = M_of()
            pts = [plane.c2p(*(M @ p)) for p in
                    [np.array([0, 0]), np.array([1, 0]),
                     np.array([1, 1]), np.array([0, 1])]]
            d = np.linalg.det(M)
            col = GREEN if d > 0.05 else (RED if d < -0.05 else GREY_D)
            return Polygon(*pts, color=col, stroke_width=2,
                            fill_color=col, fill_opacity=0.35)

        self.add(always_redraw(parallelogram),
                 always_redraw(i_arrow), always_redraw(j_arrow))

        # Right: det vs theta
        right_axes = Axes(x_range=[0, PI, PI / 4], y_range=[-1.1, 1.1, 0.5],
                          x_length=5.0, y_length=4.0,
                          axis_config={"include_numbers": True,
                                       "font_size": 16}
                          ).shift(RIGHT * 2.8 + DOWN * 0.3)
        self.play(Create(right_axes))

        det_curve = right_axes.plot(lambda t: np.cos(t), x_range=[0, PI],
                                      color=BLUE, stroke_width=3)
        self.add(det_curve)
        self.add(Tex(r"$\det(\theta)=\cos\theta$", color=BLUE, font_size=22).next_to(
            right_axes, UP, buff=0.1))

        def det_dot():
            t = theta_tr.get_value()
            return Dot(right_axes.c2p(t, np.cos(t)), color=YELLOW, radius=0.1)

        def det_trail():
            t = theta_tr.get_value()
            if t < 0.02:
                return VMobject()
            ts = np.linspace(0, t, 60)
            pts = [right_axes.c2p(s, np.cos(s)) for s in ts]
            return VMobject().set_points_as_corners(pts).set_color(YELLOW).set_stroke(width=4)

        self.add(always_redraw(det_dot), always_redraw(det_trail))

        info = VGroup(
            VGroup(Tex(r"$\theta=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\det=\cos\theta=$", font_size=22),
                   DecimalNumber(1.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"crosses 0 at $\theta=\pi/2$",
                color=GREY_B, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(theta_tr.get_value()))
        info[1][1].add_updater(lambda m: m.set_value(float(np.cos(theta_tr.get_value()))))
        self.add(info)

        self.play(theta_tr.animate.set_value(PI),
                  run_time=6, rate_func=linear)
        self.wait(0.8)
