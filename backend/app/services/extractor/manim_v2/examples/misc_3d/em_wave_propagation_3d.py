from manim import *
import numpy as np


class EmWavePropagation3d(ThreeDScene):
    """A plane electromagnetic wave propagating along +x.  The E-field
    oscillates along y (BLUE), the B-field oscillates along z (YELLOW),
    both with the same phase.  Draw them as strips of arrows along the x
    axis.  ValueTracker t_tr advances time; always_redraw redraws the full
    wave at each frame."""

    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-55 * DEGREES)
        axes = ThreeDAxes(
            x_range=[-1, 7, 1], y_range=[-2, 2, 1], z_range=[-2, 2, 1],
            x_length=9, y_length=4, z_length=4,
        )
        x_lab = axes.get_x_axis_label(Tex("propagation", font_size=24))
        y_lab = axes.get_y_axis_label(Tex("E (blue)", font_size=22,
                                          color=BLUE))
        z_lab = axes.get_z_axis_label(Tex("B (yellow)", font_size=22,
                                          color=YELLOW))
        self.add(axes, x_lab, y_lab, z_lab)

        title = Tex(r"Electromagnetic wave: $\vec{E} \perp \vec{B}$, both $\perp$ propagation",
                    font_size=30)
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(UP, buff=0.3)

        t_tr = ValueTracker(0.0)

        k = 2.0
        omega = 2.0
        A = 1.3
        xs = np.linspace(0, 6, 26)

        def make_wave():
            t = t_tr.get_value()
            e_arrows = VGroup()
            b_arrows = VGroup()
            for x in xs:
                phase = k * x - omega * t
                E = A * np.sin(phase)
                B = A * np.sin(phase)
                e_arrows.add(Arrow3D(
                    start=axes.c2p(x, 0, 0),
                    end=axes.c2p(x, E, 0),
                    color=BLUE, thickness=0.012,
                    height=0.12, base_radius=0.04,
                ))
                b_arrows.add(Arrow3D(
                    start=axes.c2p(x, 0, 0),
                    end=axes.c2p(x, 0, B),
                    color=YELLOW, thickness=0.012,
                    height=0.12, base_radius=0.04,
                ))
            e_curve = ParametricFunction(
                lambda s: axes.c2p(s, A * np.sin(k * s - omega * t), 0),
                t_range=[0, 6, 0.05], color=BLUE, stroke_width=2.5,
            )
            b_curve = ParametricFunction(
                lambda s: axes.c2p(s, 0, A * np.sin(k * s - omega * t)),
                t_range=[0, 6, 0.05], color=YELLOW, stroke_width=2.5,
            )
            return VGroup(e_arrows, b_arrows, e_curve, b_curve)

        wave = always_redraw(make_wave)
        self.add(wave)
        self.play(t_tr.animate.set_value(2 * PI / omega),
                  run_time=4, rate_func=linear)
        self.play(t_tr.animate.set_value(4 * PI / omega),
                  run_time=4, rate_func=linear)
        self.wait(1.0)
