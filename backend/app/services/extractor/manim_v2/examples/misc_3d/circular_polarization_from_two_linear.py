from manim import *
import numpy as np


class CircularPolarizationFromTwoLinear(ThreeDScene):
    """Circularly polarized light is the sum of two linearly polarized
    waves 90° out of phase, oriented perpendicular to each other.
    Show E_y = A cos(kx - ωt), E_z = A sin(kx - ωt), and their vector sum
    (GREEN) whose tip traces a helix in space (or a circle at fixed x)."""

    def construct(self):
        self.set_camera_orientation(phi=72 * DEGREES, theta=-55 * DEGREES)
        axes = ThreeDAxes(
            x_range=[-1, 6, 1], y_range=[-1.5, 1.5, 1], z_range=[-1.5, 1.5, 1],
            x_length=8, y_length=3.2, z_length=3.2,
        )
        self.add(axes)

        title = Tex(
            r"Circular polarization = two linear waves $90^\circ$ out of phase",
            font_size=30,
        )
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(UP, buff=0.3)

        legend = VGroup(
            MathTex(r"E_y = A\cos(kx-\omega t)", font_size=24, color=BLUE),
            MathTex(r"E_z = A\sin(kx-\omega t)", font_size=24, color=YELLOW),
            MathTex(r"\vec E = E_y\,\hat y + E_z\,\hat z", font_size=24,
                    color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        self.add_fixed_in_frame_mobjects(legend)
        legend.to_corner(DL, buff=0.35)

        t_tr = ValueTracker(0.0)
        k = 1.6
        omega = 1.6
        A = 1.0
        xs = np.linspace(0, 5, 22)

        def make_vectors():
            t = t_tr.get_value()
            ey = VGroup()
            ez = VGroup()
            etot = VGroup()
            for x in xs:
                phase = k * x - omega * t
                yval = A * np.cos(phase)
                zval = A * np.sin(phase)
                ey.add(Arrow3D(
                    start=axes.c2p(x, 0, 0),
                    end=axes.c2p(x, yval, 0),
                    color=BLUE, thickness=0.01,
                    height=0.1, base_radius=0.035,
                ))
                ez.add(Arrow3D(
                    start=axes.c2p(x, 0, 0),
                    end=axes.c2p(x, 0, zval),
                    color=YELLOW, thickness=0.01,
                    height=0.1, base_radius=0.035,
                ))
                etot.add(Arrow3D(
                    start=axes.c2p(x, 0, 0),
                    end=axes.c2p(x, yval, zval),
                    color=GREEN, thickness=0.015,
                    height=0.14, base_radius=0.05,
                ))
            helix = ParametricFunction(
                lambda s: axes.c2p(
                    s,
                    A * np.cos(k * s - omega * t),
                    A * np.sin(k * s - omega * t),
                ),
                t_range=[0, 5, 0.02], color=GREEN, stroke_width=2.5,
            )
            return VGroup(ey, ez, etot, helix)

        wave = always_redraw(make_vectors)
        self.add(wave)

        self.play(t_tr.animate.set_value(2 * PI / omega),
                  run_time=4, rate_func=linear)
        self.play(t_tr.animate.set_value(4 * PI / omega),
                  run_time=4, rate_func=linear)
        self.wait(1.0)
