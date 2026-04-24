from manim import *
import numpy as np


class PolarizationMalusLawExample(Scene):
    """
    Malus's law (from _2025/grover/polarization): an ideal polarizer
    attenuates transmitted light by cos²(θ) where θ is the angle
    between the polarizer axis and the incident polarization axis.

    TWO_COLUMN:
      LEFT  — incident polarization arrow + polarizer axis + trans-
              mitted arrow; ValueTracker θ_tr rotates the polarizer.
      RIGHT — plot of I(θ) / I_0 = cos²θ with moving cursor; live
              intensity readout.
    """

    def construct(self):
        title = Tex(r"Malus's law: $I = I_0 \cos^2\theta$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # LEFT — polarizer visualization
        origin = np.array([-3.5, -0.3, 0])
        incident_axis = np.array([1, 0, 0])  # horizontal

        # Incident arrow
        incident = Arrow(origin - 1.5 * np.array([1, 0, 0]),
                           origin, color=BLUE, buff=0,
                           stroke_width=5,
                           max_tip_length_to_length_ratio=0.15)
        self.play(Create(incident))

        # Polarizer (disk with axis line)
        theta_tr = ValueTracker(0.0)

        def polarizer_disk():
            return Circle(radius=1.0, color=WHITE,
                            fill_opacity=0, stroke_width=3
                            ).move_to(origin + np.array([1.5, 0, 0]))

        def polarizer_axis():
            th = theta_tr.get_value()
            c = origin + np.array([1.5, 0, 0])
            v = 1.0 * np.array([np.cos(th), np.sin(th), 0])
            return Line(c - v, c + v, color=YELLOW, stroke_width=4)

        def transmitted():
            th = theta_tr.get_value()
            c = origin + np.array([1.5, 0, 0])
            amp = np.cos(th)
            tip = c + 1.5 * np.array([np.cos(th), np.sin(th), 0])
            # But transmitted arrow length ∝ |cos θ|
            end = c + 1.5 * abs(amp) * np.array([1, 0, 0])
            # Actually transmitted keeps forward-direction (x+) but amplitude cos θ
            # Better: simple amplitude scaling along +x
            return Arrow(c, c + (1.5 * amp + 0.01) * np.array([1, 0, 0]),
                          color=GREEN, buff=0,
                          stroke_width=5,
                          max_tip_length_to_length_ratio=0.2)

        self.add(always_redraw(polarizer_disk),
                  always_redraw(polarizer_axis),
                  always_redraw(transmitted))

        incident_lbl = Tex(r"incident",
                            color=BLUE, font_size=18
                            ).next_to(origin + np.array([-1, 0, 0]), UP, buff=0.2)
        axis_lbl = MathTex(r"\theta", color=YELLOW, font_size=22
                             ).move_to(origin + np.array([1.5, 1.3, 0]))
        self.play(Write(incident_lbl), Write(axis_lbl))

        # RIGHT — intensity curve
        ax = Axes(x_range=[0, 180, 45], y_range=[0, 1.1, 0.25],
                   x_length=5, y_length=3.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([3.3, 0.2, 0])
        xlbl = MathTex(r"\theta^\circ", font_size=20).next_to(ax, DOWN, buff=0.1)
        ylbl = MathTex(r"I/I_0", font_size=20).next_to(ax, LEFT, buff=0.1)
        self.play(Create(ax), Write(xlbl), Write(ylbl))

        cos2_curve = ax.plot(lambda deg: np.cos(deg * DEGREES) ** 2,
                               x_range=[0, 180, 1], color=GREEN, stroke_width=3)
        self.play(Create(cos2_curve))

        def rider():
            deg = np.degrees(theta_tr.get_value()) % 180
            val = np.cos(deg * DEGREES) ** 2
            return Dot(ax.c2p(deg, val), color=YELLOW, radius=0.09)

        self.add(always_redraw(rider))

        def info():
            th = theta_tr.get_value()
            I = np.cos(th) ** 2
            return VGroup(
                MathTex(rf"\theta = {np.degrees(th) % 180:.0f}^\circ",
                         color=YELLOW, font_size=22),
                MathTex(rf"I/I_0 = \cos^2\theta = {I:.3f}",
                         color=GREEN, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.3, -2.6, 0])

        self.add(always_redraw(info))

        for deg in [30, 60, 90, 45, 120, 0]:
            self.play(theta_tr.animate.set_value(deg * DEGREES),
                       run_time=1.5, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.4)
