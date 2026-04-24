from manim import *
import numpy as np


class EarthMorphTorusExample(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)

        sphere = Sphere(radius=1.2, resolution=(24, 24)).set_opacity(0.7).set_color(BLUE)
        self.play(Create(sphere))

        # Morph into torus by parametric transformation
        def torus(u, v):
            R, r = 1.4, 0.55
            return np.array([
                (R + r * np.cos(v)) * np.cos(u),
                (R + r * np.cos(v)) * np.sin(u),
                r * np.sin(v),
            ])

        torus_surface = Surface(
            torus,
            u_range=[0, TAU], v_range=[0, TAU],
            resolution=(24, 12),
            fill_opacity=0.7, checkerboard_colors=[TEAL_D, TEAL_E], stroke_width=0.3,
        )

        self.play(Transform(sphere, torus_surface), run_time=3)
        self.wait(0.3)

        caption = Text("Sphere and torus differ topologically — V−E+F = 2 vs 0",
                       font_size=22, color=YELLOW)
        self.add_fixed_in_frame_mobjects(caption)
        caption.to_edge(DOWN)
        self.play(Write(caption))
        self.wait(0.6)
