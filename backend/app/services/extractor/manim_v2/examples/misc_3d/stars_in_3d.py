from manim import *
import numpy as np


class StarsIn3DExample(ThreeDScene):
    """
    Rotating star cluster in 3D — ValueTracker t_tr rotates the
    observer (camera) about the z-axis, and also 60 stars at
    random 3D positions. All star positions drawn via always_redraw.

    3D scene:
      60 stars placed randomly in a 4×4×4 cube; ValueTracker t_tr
      rotates them via a z-axis rotation matrix; size ∝ z-proximity
      to make perspective obvious.
    """

    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-30 * DEGREES)
        axes = ThreeDAxes(x_range=[-3, 3, 1], y_range=[-3, 3, 1],
                           z_range=[-3, 3, 1],
                           x_length=5, y_length=5, z_length=5)
        self.add(axes)

        rng = np.random.default_rng(5)
        N = 60
        positions = rng.uniform(-3.5, 3.5, (N, 3))
        brightness = rng.uniform(0.4, 1.0, N)

        t_tr = ValueTracker(0.0)

        def rotated(v, theta):
            c, s = np.cos(theta), np.sin(theta)
            return np.array([c * v[0] - s * v[1],
                             s * v[0] + c * v[1],
                             v[2]])

        def stars():
            t = t_tr.get_value()
            grp = VGroup()
            for i in range(N):
                p = rotated(positions[i], t)
                radius = 0.05 + 0.05 * brightness[i]
                color = interpolate_color(WHITE, YELLOW, brightness[i])
                grp.add(Dot3D(axes.c2p(*p),
                                color=color, radius=radius))
            return grp

        self.add(always_redraw(stars))

        title = Tex(r"Rotating 3D star field (parallax from observer motion)",
                    font_size=24).to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        def panel():
            t = t_tr.get_value()
            return VGroup(
                MathTex(rf"\theta = {np.degrees(t):.0f}^\circ",
                         color=YELLOW, font_size=22),
                MathTex(rf"N_\text{{stars}} = {N}",
                         color=WHITE, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)

        p = panel()
        p.to_corner(DR, buff=0.4)
        self.add_fixed_in_frame_mobjects(p)

        self.play(t_tr.animate.set_value(2 * PI),
                   run_time=8, rate_func=linear)
        new_p = panel()
        new_p.to_corner(DR, buff=0.4)
        self.add_fixed_in_frame_mobjects(new_p)
        self.play(Transform(p, new_p), run_time=0.2)
        self.wait(0.5)
