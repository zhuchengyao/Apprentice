from manim import *
import numpy as np


class SpiralScrewExample(ThreeDScene):
    """
    Spiral / helicoidal ribbon: parametric surface along a helix
    r(t) = (cos t, sin t, pitch·t) with a small strip around it.

    3D scene:
      Helical ribbon built from 2 parallel helices; ValueTracker
      length_tr extends the ribbon; ambient camera rotation.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-35 * DEGREES)
        axes = ThreeDAxes(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                           z_range=[-2, 2, 1],
                           x_length=4, y_length=4, z_length=4)
        self.add(axes)

        pitch = 0.35
        R = 1.3
        width = 0.35  # ribbon half-width

        length_tr = ValueTracker(PI)

        def helix_ribbon():
            L = length_tr.get_value()

            def param(u, v):
                # u ∈ [0, L] (along helix), v ∈ [-1, 1] (across width)
                x = (R + v * width) * np.cos(u)
                y = (R + v * width) * np.sin(u)
                z = pitch * u
                return axes.c2p(x, y, z)

            return Surface(param, u_range=[0, L], v_range=[-1, 1],
                             resolution=(max(30, int(L * 5)), 5),
                             fill_opacity=0.75,
                             checkerboard_colors=[BLUE, PURPLE])

        self.add(always_redraw(helix_ribbon))

        title = Tex(r"Helical ribbon",
                    font_size=26).to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        def panel():
            L = length_tr.get_value()
            turns = L / (2 * PI)
            return VGroup(
                MathTex(rf"L = {L:.2f}\,\text{{rad}}",
                         color=YELLOW, font_size=22),
                MathTex(rf"\text{{turns}} = {turns:.2f}",
                         color=GREEN, font_size=22),
                MathTex(rf"\text{{pitch}} = {pitch}",
                         color=WHITE, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DR, buff=0.4)

        pnl = panel()
        self.add_fixed_in_frame_mobjects(pnl)

        self.begin_ambient_camera_rotation(rate=0.15)
        self.play(length_tr.animate.set_value(6 * PI),
                   run_time=8, rate_func=linear)
        new_pnl = panel()
        self.add_fixed_in_frame_mobjects(new_pnl)
        self.play(Transform(pnl, new_pnl), run_time=0.2)
        self.stop_ambient_camera_rotation()
