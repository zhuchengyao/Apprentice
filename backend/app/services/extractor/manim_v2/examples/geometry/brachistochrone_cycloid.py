from manim import *
import numpy as np


class BrachistochroneCycloidExample(Scene):
    """
    Race between a cycloid path and a straight chord.

    Two beads start simultaneously at A=(0,0). One slides down a
    cycloid path; the other slides down a straight ramp. Both end
    at B = (πR, -2R), the bottom of the cycloid arch. Under gravity g
    on a frictionless track, the cycloid bead arrives FIRST — that's
    the brachistochrone property.

    ValueTracker τ ∈ [0, t_max] (real seconds) drives both beads via
    always_redraw. For each bead, position(τ) is computed from the
    physics: the cycloid bead's parameter satisfies θ(τ) = √(g/R)·τ,
    and the chord bead's position is found from constant-acceleration
    kinematics along the slope.
    """

    def construct(self):
        title = Tex(r"Brachistochrone: cycloid beats the straight ramp",
                    font_size=32).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # Physics setup
        R = 1.0
        g = 9.8
        # End point of the cycloid arch at the bottom
        x_B = PI * R
        y_B = -2 * R

        # Cycloid time to reach B (θ = π): t_cyc = π · √(R/g)
        t_cyc = PI * np.sqrt(R / g)

        # Chord (straight ramp) from A to B: length L, slope angle θ
        L = np.sqrt(x_B ** 2 + y_B ** 2)
        sin_theta = abs(y_B) / L
        # Acceleration along slope: a = g · sin θ.  L = ½ a t²  ⇒  t = √(2L/a)
        a_chord = g * sin_theta
        t_chord = np.sqrt(2 * L / a_chord)

        t_max = max(t_cyc, t_chord) + 0.05

        # SCALE: position the path so that it fits in the LEFT half of the frame.
        # World units map to plane via Axes.
        axes = Axes(
            x_range=[0, x_B + 0.4, 0.5], y_range=[y_B - 0.3, 0.4, 0.5],
            x_length=6.5, y_length=4.0,
            axis_config={"include_tip": False, "include_numbers": False},
        ).move_to([-2.4, -0.6, 0])
        self.play(Create(axes))

        # Cycloid path
        cycloid = ParametricFunction(
            lambda th: axes.c2p(R * (th - np.sin(th)), -R * (1 - np.cos(th))),
            t_range=[0, PI],
            color=YELLOW, stroke_width=4,
        )
        # Chord (straight line)
        chord = Line(axes.c2p(0, 0), axes.c2p(x_B, y_B),
                     color=BLUE, stroke_width=4)
        self.play(Create(cycloid), Create(chord))

        # Endpoint dots
        a_dot = Dot(axes.c2p(0, 0), color=GREEN, radius=0.10)
        b_dot = Dot(axes.c2p(x_B, y_B), color=RED, radius=0.10)
        a_lbl = Tex("$A$", color=GREEN, font_size=26).next_to(a_dot, UL, buff=0.05)
        b_lbl = Tex("$B$", color=RED, font_size=26).next_to(b_dot, DR, buff=0.05)
        self.play(FadeIn(a_dot), Write(a_lbl), FadeIn(b_dot), Write(b_lbl))

        # ValueTracker for actual time τ in seconds
        tau = ValueTracker(0.0)

        def cycloid_pos(t: float) -> np.ndarray:
            if t <= 0:
                return axes.c2p(0, 0)
            if t >= t_cyc:
                return axes.c2p(x_B, y_B)
            theta = np.sqrt(g / R) * t  # exact for the cycloid pendulum
            # Clamp θ to [0, π]
            theta = min(theta, PI)
            x = R * (theta - np.sin(theta))
            y = -R * (1 - np.cos(theta))
            return axes.c2p(x, y)

        def chord_pos(t: float) -> np.ndarray:
            if t <= 0:
                return axes.c2p(0, 0)
            if t >= t_chord:
                return axes.c2p(x_B, y_B)
            d = 0.5 * a_chord * t * t  # distance traveled along the slope
            frac = d / L
            return axes.c2p(frac * x_B, frac * y_B)

        def cycloid_bead():
            return Dot(cycloid_pos(tau.get_value()), color=YELLOW, radius=0.13)

        def chord_bead():
            return Dot(chord_pos(tau.get_value()), color=BLUE, radius=0.13)

        self.add(always_redraw(cycloid_bead), always_redraw(chord_bead))

        # RIGHT COLUMN: live time + arrival flags
        rcol_x = +4.0

        def info_panel():
            t = tau.get_value()
            cyc_done = t >= t_cyc
            chord_done = t >= t_chord
            return VGroup(
                Tex(rf"$\tau = {t:.2f}\,$s", color=WHITE, font_size=26),
                Tex(rf"cycloid finishes at $t_c = {t_cyc:.2f}\,$s",
                    color=YELLOW, font_size=22),
                Tex(rf"chord finishes at $t_l = {t_chord:.2f}\,$s",
                    color=BLUE, font_size=22),
                Tex(r"\textbf{cycloid wins!}" if cyc_done and not chord_done
                    else (r"chord catching up..." if cyc_done else r"both still falling"),
                    color=GREEN if (cyc_done and not chord_done) else GREY_B,
                    font_size=24),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([rcol_x, +1.0, 0])

        self.add(always_redraw(info_panel))

        # Race!
        self.play(tau.animate.set_value(t_max), run_time=4.5, rate_func=linear)
        self.wait(0.5)

        conclusion = Tex(
            r"Cycloid is the path of \emph{stationary time} (Bernoulli, 1696)",
            font_size=24, color=YELLOW,
        ).move_to([rcol_x, -2.6, 0])
        self.play(Write(conclusion))
        self.wait(1.0)
