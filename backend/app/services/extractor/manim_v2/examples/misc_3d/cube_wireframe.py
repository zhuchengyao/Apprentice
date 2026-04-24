from manim import *
import numpy as np


class CubeWireframeExample(ThreeDScene):
    """
    Wireframe cube rotating about a space diagonal to exhibit
    3-fold symmetry.

    3D scene:
      Cube wireframe drawn from 8 vertices + 12 edges; ValueTracker
      phi_tr rotates the cube via always_redraw-like add_updater
      around the space diagonal (1, 1, 1); 3-fold symmetry: rotation
      by 2π/3 maps the cube to itself.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-30 * DEGREES)
        axes = ThreeDAxes(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                           z_range=[-2, 2, 1],
                           x_length=4, y_length=4, z_length=4)
        self.add(axes)

        # Cube vertices
        verts = [np.array([sx, sy, sz])
                 for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]
        edges = []
        for i in range(8):
            for j in range(i + 1, 8):
                diff = verts[i] - verts[j]
                if int(np.sum(np.abs(diff))) == 2:
                    edges.append((i, j))

        # Diagonal axis (1, 1, 1) normalized
        D = np.array([1, 1, 1]) / np.sqrt(3)

        def rot_about_D(v, theta):
            # Rodrigues formula
            k = D
            return (v * np.cos(theta)
                    + np.cross(k, v) * np.sin(theta)
                    + k * np.dot(k, v) * (1 - np.cos(theta)))

        phi_tr = ValueTracker(0.0)

        def cube_mob():
            t = phi_tr.get_value()
            rv = [rot_about_D(v, t) for v in verts]
            grp = VGroup()
            # edges
            for (i, j) in edges:
                grp.add(Line(axes.c2p(*rv[i]), axes.c2p(*rv[j]),
                               color=BLUE_D, stroke_width=3))
            # vertex dots
            for v in rv:
                grp.add(Dot3D(axes.c2p(*v), color=YELLOW, radius=0.07))
            return grp

        self.add(always_redraw(cube_mob))

        # Space diagonal line
        diag_line = Line(axes.c2p(*(-1.6 * D)), axes.c2p(*(1.6 * D)),
                          color=RED, stroke_width=3)
        self.add(diag_line)

        title = Tex(r"Cube: 3-fold symmetry about space diagonal $(1,1,1)$",
                    font_size=24).to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        def panel():
            t = phi_tr.get_value()
            mod = (t % (2 * PI / 3))
            in_sym = abs(mod) < 0.05 or abs(mod - 2 * PI / 3) < 0.05
            return VGroup(
                MathTex(rf"\theta = {np.degrees(t):.0f}^\circ",
                         color=YELLOW, font_size=24),
                MathTex(rf"120^\circ \mid \theta: {' yes' if in_sym else ' no'}",
                         color=GREEN if in_sym else GREY_B, font_size=22),
                Tex(r"order-3 rotation", color=WHITE, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)

        # Use update panel via phases
        p = panel()
        p.to_corner(DR, buff=0.4)
        self.add_fixed_in_frame_mobjects(p)

        # Rotate through 2π in phases to emphasize 3-fold symmetry
        for frac in [1/3, 2/3, 1.0]:
            target = 2 * PI * frac
            self.play(phi_tr.animate.set_value(target),
                       run_time=2.5, rate_func=linear)
            new_p = panel()
            new_p.to_corner(DR, buff=0.4)
            self.add_fixed_in_frame_mobjects(new_p)
            self.play(Transform(p, new_p), run_time=0.2)
            self.wait(0.6)

        self.wait(0.4)
