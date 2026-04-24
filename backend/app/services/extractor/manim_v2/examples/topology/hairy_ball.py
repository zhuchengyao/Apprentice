from manim import *
import numpy as np


class HairyBallExample(ThreeDScene):
    """
    Hairy ball theorem: any continuous tangent vector field on S² has
    a zero. Two attempts to comb the sphere both fail.

    Sequence:
      Stage 1 — Sphere with "latitude flow" tangent field; vortex at
                each pole highlighted in RED.
      Stage 2 — Camera rotates to show the south-pole zero.
      Stage 3 — Different combing attempt (longitudinal); vortex now
                at equator (Möbius-like).
      Title overlay summarizes χ(S²) = 2 ≠ 0.
    """

    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-40 * DEGREES)
        title = Tex(r"Hairy ball: any continuous tangent field on $S^2$ has a zero",
                    font_size=22)
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(UP, buff=0.3)

        R = 1.4
        sphere = Sphere(radius=R, resolution=(20, 20)).set_fill(BLUE_D, opacity=0.5)
        self.play(Create(sphere))

        # Stage 1: latitude flow (all hairs point eastward in their tangent plane)
        def latitude_field():
            hairs = VGroup()
            for phi_deg in [25, 45, 65, 85, 95, 115, 135, 155]:
                phi = np.radians(phi_deg)
                for theta_deg in range(0, 360, 22):
                    theta = np.radians(theta_deg)
                    p = R * np.array([np.sin(phi) * np.cos(theta),
                                      np.sin(phi) * np.sin(theta),
                                      np.cos(phi)])
                    # Tangent vector in the eastward direction
                    tangent = 0.18 * np.array([-np.sin(theta), np.cos(theta), 0])
                    hairs.add(Line(p, p + tangent, color=YELLOW, stroke_width=2))
            return hairs

        hair_field = latitude_field()
        self.play(Create(hair_field), run_time=2)

        # Vortex markers at the two poles
        north = Dot3D(R * np.array([0, 0, 1.05]), color=RED, radius=0.10)
        south = Dot3D(R * np.array([0, 0, -1.05]), color=RED, radius=0.10)
        north_lbl_3d = Tex(r"\textbf{vortex}", color=RED, font_size=22)
        self.add_fixed_in_frame_mobjects(north_lbl_3d)
        north_lbl_3d.move_to([3.0, 2.0, 0])
        self.play(FadeIn(north), FadeIn(south), Write(north_lbl_3d))
        self.wait(0.6)

        # Camera rotation to show the south pole vortex
        self.move_camera(phi=110 * DEGREES, theta=-40 * DEGREES, run_time=2.5)
        self.wait(0.5)
        self.move_camera(phi=70 * DEGREES, theta=-40 * DEGREES, run_time=2.0)
        self.wait(0.4)

        # Stage 2: try longitudinal flow — vortex moves to a new place
        def longitudinal_field():
            hairs = VGroup()
            for phi_deg in [25, 45, 65, 85, 95, 115, 135, 155]:
                phi = np.radians(phi_deg)
                for theta_deg in range(0, 360, 22):
                    theta = np.radians(theta_deg)
                    p = R * np.array([np.sin(phi) * np.cos(theta),
                                      np.sin(phi) * np.sin(theta),
                                      np.cos(phi)])
                    # Tangent in the direction of increasing latitude (toward south)
                    tangent = 0.18 * np.array([
                        np.cos(phi) * np.cos(theta),
                        np.cos(phi) * np.sin(theta),
                        -np.sin(phi),
                    ])
                    hairs.add(Line(p, p + tangent, color=ORANGE, stroke_width=2))
            return hairs

        new_field = longitudinal_field()
        self.play(Transform(hair_field, new_field), run_time=2.5)

        attempt_lbl_3d = Tex(r"longitudinal: vortices at poles too",
                             color=ORANGE, font_size=20)
        self.add_fixed_in_frame_mobjects(attempt_lbl_3d)
        attempt_lbl_3d.next_to(north_lbl_3d, DOWN, buff=0.2)
        self.play(Write(attempt_lbl_3d))

        # Conclusion
        chi_lbl = Tex(r"$\chi(S^2) = 2 \neq 0\ \Rightarrow$ vortices forced",
                      color=GREEN, font_size=24)
        self.add_fixed_in_frame_mobjects(chi_lbl)
        chi_lbl.to_edge(DOWN, buff=0.4)
        self.play(Write(chi_lbl))
        self.wait(1.0)
