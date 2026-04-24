from manim import *
import numpy as np


class GyroidTriplyPeriodicExample(ThreeDScene):
    """
    Gyroid: triply-periodic minimal surface defined implicitly by
    sin x cos y + sin y cos z + sin z cos x = 0.
    Approximate via sampling a thin 'slab' of 2D slice.

    3D scene:
      Z-slices of gyroid for varying z; always_redraw contour on xy
      plane as z sweeps. Demonstrates 3-periodicity.
    """

    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-35 * DEGREES)
        axes = ThreeDAxes(x_range=[-4, 4, 2], y_range=[-4, 4, 2],
                           z_range=[-2, 2, 1],
                           x_length=5, y_length=5, z_length=2.5)
        self.add(axes)

        z_tr = ValueTracker(0.0)

        def gyroid_slice():
            z = z_tr.get_value()
            # At fixed z, sample on 30×30 grid in [-π, π]²
            grp = VGroup()
            N = 25
            xs = np.linspace(-PI, PI, N + 1)
            for i in range(N):
                for j in range(N):
                    x = (xs[i] + xs[i + 1]) / 2
                    y = (xs[j] + xs[j + 1]) / 2
                    val = (np.sin(x) * np.cos(y)
                            + np.sin(y) * np.cos(z)
                            + np.sin(z) * np.cos(x))
                    intensity = np.tanh(val)  # map to [-1, 1]
                    col = interpolate_color(BLUE_E, RED, (intensity + 1) / 2)
                    # Map (x, y) ∈ [-π, π] to [-3, 3] scene coords via axes
                    sq = Square(side_length=0.22, color=col,
                                  fill_opacity=0.75, stroke_width=0)
                    sq.move_to(axes.c2p(x * 3 / PI, y * 3 / PI, z))
                    grp.add(sq)
            return grp

        self.add(always_redraw(gyroid_slice))

        title = Tex(r"Gyroid: $\sin x\cos y + \sin y\cos z + \sin z\cos x = 0$",
                    font_size=20).to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        def panel():
            z = z_tr.get_value()
            return VGroup(
                MathTex(rf"z = {z:.2f}", color=YELLOW, font_size=22),
                Tex(r"triply-periodic minimal surface",
                     color=GREEN, font_size=18),
                Tex(r"slice: RED / BLUE regions",
                     color=WHITE, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DR, buff=0.4)

        pnl = panel()
        self.add_fixed_in_frame_mobjects(pnl)

        self.begin_ambient_camera_rotation(rate=0.1)
        self.play(z_tr.animate.set_value(2 * PI),
                   run_time=8, rate_func=linear)
        self.stop_ambient_camera_rotation()
        self.wait(0.4)
