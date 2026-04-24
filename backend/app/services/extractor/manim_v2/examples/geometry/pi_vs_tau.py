from manim import *
import numpy as np


class PiVsTauExample(Scene):
    """
    Roll a circle along a number line and read off C / d  (=π)  vs  C / r  (=τ).

    SINGLE_FOCUS rolling demonstration:
      - A circle of radius R rolls along a horizontal axis.
      - ValueTracker θ ∈ [0, 2π] drives the rotation; the circle's
        bottom contact point traces out a horizontal segment of length
        R·θ along the axis (no slipping). After a full revolution
        θ=2π, the traced segment is exactly C = 2πR.
      - A red diameter and an orange radius rotate with the circle.
      - Two RIGHT-side stacked panels show what happens to the rolled-
        out length when divided by the diameter (gives π) vs the
        radius (gives τ).
    """

    def construct(self):
        title = Tex(r"$\pi$ vs $\tau$: roll a circle and divide $C$ by $d$ or $r$",
                    font_size=28).to_edge(UP, buff=0.4)
        self.play(Write(title))

        R = 1.0
        # The number line the circle rolls along
        nl = NumberLine(
            x_range=[-0.2, 7.5, 1], length=8.0, include_numbers=True,
            decimal_number_config={"num_decimal_places": 1, "font_size": 18},
        ).move_to([-1.7, -2.0, 0])
        nl_lbl = Tex(r"distance rolled $C = R\,\theta$",
                     color=GREY_B, font_size=20).next_to(nl, DOWN, buff=0.1)
        self.play(Create(nl), Write(nl_lbl))

        theta = ValueTracker(0.001)

        # Circle position: starts at left end of number line, moves right by R*θ
        x0 = nl.n2p(0)[0]
        y_center = nl.get_center()[1] + R  # circle sits on the line

        def circle_center():
            d = R * theta.get_value()
            return np.array([x0 + d, y_center, 0])

        def rolling_circle():
            return Circle(radius=R, color=BLUE, stroke_width=3).move_to(circle_center())

        def diameter_line():
            c = circle_center()
            ang = theta.get_value() + PI / 2  # rotate with the circle
            offset = R * np.array([np.cos(ang), np.sin(ang), 0])
            return Line(c - offset, c + offset, color=RED, stroke_width=4)

        def radius_line():
            c = circle_center()
            ang = -theta.get_value() + PI / 2  # the contact-tracking radius
            return Line(c, c + R * np.array([np.cos(ang), np.sin(ang), 0]),
                        color=ORANGE, stroke_width=4)

        def contact_dot():
            c = circle_center()
            return Dot([c[0], y_center - R, 0], color=YELLOW, radius=0.08)

        def rolled_segment():
            # Segment along number line from x0 to current contact
            d = R * theta.get_value()
            return Line(nl.n2p(0), nl.n2p(d), color=YELLOW, stroke_width=6)

        self.add(always_redraw(rolled_segment),
                 always_redraw(rolling_circle),
                 always_redraw(diameter_line),
                 always_redraw(radius_line),
                 always_redraw(contact_dot))

        # RIGHT COLUMN: live measurements
        rcol_x = +4.6

        def measurements():
            d = R * theta.get_value()
            return VGroup(
                MathTex(rf"R = {R:.1f}", color=ORANGE, font_size=22),
                MathTex(rf"d = 2R = {2*R:.1f}", color=RED, font_size=22),
                MathTex(rf"C = R\,\theta = {d:.4f}",
                        color=YELLOW, font_size=24),
                MathTex(rf"\frac{{C}}{{d}} = {d/(2*R):.4f}", color=BLUE, font_size=26),
                MathTex(rf"\frac{{C}}{{R}} = {d/R:.4f}", color=GREEN, font_size=26),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([rcol_x, +1.3, 0])

        self.add(always_redraw(measurements))

        # Roll one full revolution
        self.play(theta.animate.set_value(2 * PI),
                  run_time=8, rate_func=linear)
        self.wait(0.5)

        conclusion = VGroup(
            MathTex(r"\pi = \frac{C}{d} = 3.1415\ldots", color=BLUE, font_size=26),
            MathTex(r"\tau = \frac{C}{R} = 6.2831\ldots = 2\pi", color=GREEN, font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([rcol_x, -2.0, 0])
        self.play(Write(conclusion))
        self.wait(1.0)
