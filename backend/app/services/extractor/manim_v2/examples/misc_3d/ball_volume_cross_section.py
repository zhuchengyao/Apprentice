from manim import *
import numpy as np


class BallVolumeCrossSectionExample(ThreeDScene):
    """
    Ball volume via disk cross-sections:
       V = ∫_{-R}^{R} π (R² - z²) dz = 4/3 π R³

    3D scene:
      Transparent unit ball + a single highlighted disk slice at
      height z. ValueTracker z_tr sweeps z = -R → +R; the disk
      updates (always_redraw) with radius √(R² - z²). Fixed-frame
      panel shows the running Riemann sum approaching 4/3 π.
    """

    def construct(self):
        title = Tex(r"Ball volume via disks: $V = \int_{-R}^{R} \pi(R^2 - z^2)\,dz = \tfrac{4}{3}\pi R^3$",
                    font_size=22).to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        self.set_camera_orientation(phi=65 * DEGREES, theta=-35 * DEGREES)
        axes = ThreeDAxes(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                           z_range=[-2, 2, 1],
                           x_length=4, y_length=4, z_length=4)
        self.add(axes)

        R = 1.3

        # Transparent ball
        ball = Sphere(radius=R, resolution=(20, 20),
                        fill_opacity=0.15,
                        color=BLUE_D
                        ).move_to(axes.c2p(0, 0, 0))
        self.add(ball)

        z_tr = ValueTracker(-R + 0.02)

        def slice_disk():
            z = z_tr.get_value()
            r2 = max(R * R - z * z, 0)
            r = np.sqrt(r2)
            # Circle at height z
            return Circle(radius=r, color=YELLOW, fill_opacity=0.55,
                            stroke_width=2
                            ).move_to(axes.c2p(0, 0, z))

        self.add(always_redraw(slice_disk))

        # Thin "stack" of N_slices cross-sections stacked through the volume
        N_slices = 20

        def stack():
            grp = VGroup()
            z = z_tr.get_value()
            # Show all slices BETWEEN -R and z with opacity fading
            for zi in np.linspace(-R + 0.05, R - 0.05, N_slices):
                if zi > z:
                    continue
                r = np.sqrt(max(R * R - zi * zi, 0))
                c = Circle(radius=r, color=GREEN,
                            fill_opacity=0.15, stroke_width=1
                            ).move_to(axes.c2p(0, 0, zi))
                grp.add(c)
            return grp

        self.add(always_redraw(stack))

        def make_panel():
            z = z_tr.get_value()
            # Running Riemann integral from -R to z of π(R²-z²) dz
            lo = -R
            hi = max(z, lo)
            if hi <= lo:
                integral = 0.0
            else:
                # closed form: π (R²(z-lo) - (z³-lo³)/3)
                integral = PI * (R * R * (hi - lo) - (hi ** 3 - lo ** 3) / 3)
            full = 4 / 3 * PI * R ** 3
            return VGroup(
                MathTex(rf"z = {z:+.2f}", color=YELLOW, font_size=22),
                MathTex(rf"r(z) = \sqrt{{R^2 - z^2}} = {np.sqrt(max(R*R - z*z, 0)):.3f}",
                         color=YELLOW, font_size=20),
                MathTex(rf"\int_{{-R}}^{{z}} \pi r^2 dz = {integral:.3f}",
                         color=GREEN, font_size=22),
                MathTex(rf"V_{{\text{{full}}}} = \tfrac{{4}}{{3}}\pi R^3 = {full:.3f}",
                         color=BLUE, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(DR, buff=0.4)

        panel = make_panel()
        self.add_fixed_in_frame_mobjects(panel)

        self.begin_ambient_camera_rotation(rate=0.1)
        # Sweep z from -R to +R
        checkpoints = [-R * 0.5, 0, R * 0.5, R - 0.02]
        for cz in checkpoints:
            self.play(z_tr.animate.set_value(cz),
                       run_time=2, rate_func=smooth)
            new_panel = make_panel()
            self.add_fixed_in_frame_mobjects(new_panel)
            self.play(Transform(panel, new_panel), run_time=0.25)
            self.wait(0.35)
        self.stop_ambient_camera_rotation()
        self.wait(0.4)
