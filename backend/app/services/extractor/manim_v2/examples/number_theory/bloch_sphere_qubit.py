from manim import *
import numpy as np


class BlochSphereQubitExample(ThreeDScene):
    """
    Bloch sphere: a qubit state |ψ⟩ = cos(θ/2)|0⟩ + e^(iφ)sin(θ/2)|1⟩
    corresponds to a point on the unit sphere at polar angles (θ, φ).

    Adapted from _2025/grover/state_vectors.

    3D scene:
      Unit sphere + axes labeled |0⟩, |1⟩, |+⟩, |−⟩. ValueTrackers
      theta_tr and phi_tr position a state arrow from origin to the
      Bloch sphere surface; always_redraw. Tour: |0⟩ → |+⟩ → |+y⟩ →
      |1⟩ → |ψ⟩.
    """

    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)
        axes = ThreeDAxes(x_range=[-1.5, 1.5, 0.5],
                           y_range=[-1.5, 1.5, 0.5],
                           z_range=[-1.5, 1.5, 0.5],
                           x_length=3, y_length=3, z_length=3)
        self.add(axes)

        sphere = Sphere(radius=1.0, resolution=(16, 16),
                          fill_opacity=0.12,
                          color=BLUE_D).move_to(axes.c2p(0, 0, 0))
        self.add(sphere)

        # Basis-state markers
        zero = Dot3D(axes.c2p(0, 0, 1), color=GREEN, radius=0.08)
        one = Dot3D(axes.c2p(0, 0, -1), color=RED, radius=0.08)
        plus = Dot3D(axes.c2p(1, 0, 0), color=YELLOW, radius=0.08)
        minus = Dot3D(axes.c2p(-1, 0, 0), color=YELLOW, radius=0.08)
        plus_y = Dot3D(axes.c2p(0, 1, 0), color=ORANGE, radius=0.08)

        lbl_0 = MathTex(r"|0\rangle", color=GREEN, font_size=26)
        lbl_1 = MathTex(r"|1\rangle", color=RED, font_size=26)
        lbl_p = MathTex(r"|+\rangle", color=YELLOW, font_size=24)
        lbl_m = MathTex(r"|-\rangle", color=YELLOW, font_size=24)
        self.add_fixed_orientation_mobjects(lbl_0, lbl_1, lbl_p, lbl_m)
        lbl_0.next_to(axes.c2p(0, 0, 1), UP, buff=0.2)
        lbl_1.next_to(axes.c2p(0, 0, -1), DOWN, buff=0.2)
        lbl_p.next_to(axes.c2p(1, 0, 0), RIGHT, buff=0.2)
        lbl_m.next_to(axes.c2p(-1, 0, 0), LEFT, buff=0.2)
        self.add(zero, one, plus, minus, plus_y, lbl_0, lbl_1, lbl_p, lbl_m)

        theta_tr = ValueTracker(0.001)
        phi_tr = ValueTracker(0.0)

        def state_arrow():
            th = theta_tr.get_value()
            ph = phi_tr.get_value()
            x = np.sin(th) * np.cos(ph)
            y = np.sin(th) * np.sin(ph)
            z = np.cos(th)
            return Line(axes.c2p(0, 0, 0),
                          axes.c2p(x, y, z),
                          color=PURPLE, stroke_width=5)

        def state_dot():
            th = theta_tr.get_value()
            ph = phi_tr.get_value()
            x = np.sin(th) * np.cos(ph)
            y = np.sin(th) * np.sin(ph)
            z = np.cos(th)
            return Dot3D(axes.c2p(x, y, z),
                          color=PURPLE, radius=0.1)

        self.add(always_redraw(state_arrow), always_redraw(state_dot))

        title = Tex(r"Bloch sphere: $|\psi\rangle = \cos(\theta/2)|0\rangle + e^{i\phi}\sin(\theta/2)|1\rangle$",
                    font_size=22).to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        def panel():
            th = theta_tr.get_value()
            ph = phi_tr.get_value()
            alpha = np.cos(th / 2)
            beta_re = np.sin(th / 2) * np.cos(ph)
            beta_im = np.sin(th / 2) * np.sin(ph)
            return VGroup(
                MathTex(rf"\theta = {np.degrees(th):.0f}^\circ",
                         color=YELLOW, font_size=22),
                MathTex(rf"\phi = {np.degrees(ph):.0f}^\circ",
                         color=YELLOW, font_size=22),
                MathTex(rf"\alpha = {alpha:.3f}",
                         color=GREEN, font_size=22),
                MathTex(rf"\beta = {beta_re:+.3f} {'+' if beta_im >= 0 else '-'} {abs(beta_im):.3f}i",
                         color=RED, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DR, buff=0.4)

        p = panel()
        self.add_fixed_in_frame_mobjects(p)

        # Tour: |0⟩ → |+⟩ → |+y⟩ → |1⟩ → mid-general
        tour = [
            (PI / 2, 0),      # |+⟩
            (PI / 2, PI / 2), # |+y⟩
            (PI, 0),          # |1⟩
            (PI / 3, PI / 4), # general
        ]
        self.begin_ambient_camera_rotation(rate=0.1)
        for (th, ph) in tour:
            self.play(theta_tr.animate.set_value(th),
                       phi_tr.animate.set_value(ph),
                       run_time=1.7, rate_func=smooth)
            new_p = panel()
            self.add_fixed_in_frame_mobjects(new_p)
            self.play(Transform(p, new_p), run_time=0.2)
            self.wait(0.5)
        self.stop_ambient_camera_rotation()
        self.wait(0.4)
