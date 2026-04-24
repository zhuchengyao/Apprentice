from manim import *
import numpy as np


class ClacksPhaseCircleExample(Scene):
    """
    Phase-circle interpretation of block collisions (from _2019/
    clacks/solution2/position_phase_space): in coordinates
    (u, v) = (√M x₁, √m x₂), elastic-wall bounces become reflections,
    and block-block collisions are reflections across the line
    √M v = √m u — all trajectories are straight-line segments
    inside a wedge of angle θ = arctan(√(m/M)).

    SINGLE_FOCUS:
      The wedge inscribed in a circle; ValueTracker step_tr steps
      through reflections; each segment is drawn straight;
      total number of reflections ≈ π/θ ≈ π·10^k for M/m = 10^(2k).
    """

    def construct(self):
        title = Tex(r"Clacks: phase circle with wedge angle $\arctan\sqrt{m/M}$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        R = 3.0

        # For M/m = 100 → θ = arctan(1/10) ≈ 5.71°, giving ~31 clacks
        M_over_m = 100
        theta = np.arctan(1 / np.sqrt(M_over_m))

        # Circle
        circ = Circle(radius=R, color=WHITE, stroke_width=2
                       ).move_to([0, -0.2, 0])
        center = circ.get_center()

        # Wedge lines: horizontal (wall) and tilted (block-block)
        wall = Line(center,
                      center + R * np.array([1, 0, 0]),
                      color=BLUE, stroke_width=3)
        bb_line = Line(center,
                        center + R * np.array([np.cos(theta),
                                                   np.sin(theta), 0]),
                        color=RED, stroke_width=3)
        wall_lbl = Tex(r"wall", color=BLUE, font_size=18
                        ).next_to(wall.get_end(), DOWN, buff=0.15)
        bb_lbl = Tex(r"$\sqrt M v = \sqrt m u$", color=RED, font_size=18
                      ).next_to(bb_line.get_end(), UR, buff=0.1)

        self.play(Create(circ), Create(wall), Create(bb_line),
                   Write(wall_lbl), Write(bb_lbl))

        # Precompute chord segments: ball bounces between the two
        # wedge edges; angles advance by 2θ each reflection; stop
        # when angle exceeds π/2
        n_max = int(PI / theta) + 1

        def chord_endpoints(k):
            """Return the k-th chord's (start, end) on the unit circle."""
            # Start angle: -(2k-1)θ reflected; but easier: start at angle
            # -(k·θ) reflected off alternating edges.
            # We'll compute via direct bounce simulation.
            # Start: enter from top at some angle; first reflection at bb_line.
            pass  # (simplified below)

        # Simpler direct approach: build chords whose endpoints lie
        # on alternating wedge edges at progressing angles.
        chords = []
        # Ball starts on BB edge at angle θ from the wall. After one reflection
        # off the wall, its direction rotates by 2θ. The reflected-path chord
        # makes angles (kθ, (k+1)θ) with wall for k = 1, 2, ...
        # We draw chords connecting points on alternating edges:
        #   (wall at distance r_i) ↔ (BB edge at distance r_i')
        # For simplicity, draw all chords as radii of the unit circle
        # spaced 2θ apart — the "unfolded" representation.
        for i in range(n_max):
            angle = i * theta
            if angle > PI / 2:
                break
            chords.append((i, angle))

        step_tr = ValueTracker(0)

        def drawn_chords():
            k = int(round(step_tr.get_value()))
            k = max(0, min(k, len(chords)))
            grp = VGroup()
            # Place points on circle at alternating angles and connect
            for i in range(k):
                (idx, ang) = chords[i]
                p1 = center + R * np.array([np.cos(ang),
                                               np.sin(ang), 0])
                # Previous chord endpoint (reflected)
                ang_prev = chords[i - 1][1] if i > 0 else 0
                p0 = center + R * np.array([np.cos(ang_prev),
                                                np.sin(ang_prev), 0])
                grp.add(Line(p0, p1, color=YELLOW, stroke_width=2))
                grp.add(Dot(p1, color=YELLOW, radius=0.06))
            return grp

        self.add(always_redraw(drawn_chords))

        def info():
            k = int(round(step_tr.get_value()))
            return VGroup(
                MathTex(rf"M/m = {M_over_m}", color=WHITE, font_size=24),
                MathTex(rf"\theta = {np.degrees(theta):.2f}^\circ",
                         color=RED, font_size=22),
                MathTex(rf"\text{{reflections}} = {k}",
                         color=YELLOW, font_size=24),
                MathTex(rf"\lfloor \pi/\theta \rfloor = {int(PI/theta)}",
                         color=GREEN, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.3).shift(UP * 0.5)

        self.add(always_redraw(info))

        self.play(step_tr.animate.set_value(len(chords)),
                   run_time=5, rate_func=linear)
        self.wait(0.5)
