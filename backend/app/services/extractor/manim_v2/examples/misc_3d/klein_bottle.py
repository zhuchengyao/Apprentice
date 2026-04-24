from manim import *
import numpy as np


class KleinBottleExample(ThreeDScene):
    """
    Klein bottle: non-orientable closed surface in 4D, immersed in
    3D with self-intersection. Parametrize via figure-8 immersion;
    ValueTracker t_tr morphs a phase parameter that gradually unfolds
    the figure-8 cross-section.

    3D scene:
      Klein bottle as always_redraw Surface whose cross-section
      phase parameter depends on t_tr; ambient camera rotation.
    """

    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-40 * DEGREES)
        axes = ThreeDAxes(x_range=[-3, 3, 1], y_range=[-3, 3, 1],
                           z_range=[-2, 2, 1],
                           x_length=4, y_length=4, z_length=3)
        self.add(axes)

        R = 2.0
        r = 0.6

        t_tr = ValueTracker(1.0)

        def klein_surface():
            phase = t_tr.get_value()

            def klein_param(u, v):
                x = (R + r * np.cos(u / 2) * np.sin(v)
                       - phase * r * np.sin(u / 2) * np.sin(2 * v)) * np.cos(u)
                y = (R + r * np.cos(u / 2) * np.sin(v)
                       - phase * r * np.sin(u / 2) * np.sin(2 * v)) * np.sin(u)
                z = (r * np.sin(u / 2) * np.sin(v)
                      + phase * r * np.cos(u / 2) * np.sin(2 * v))
                return axes.c2p(x, y, z)

            return Surface(klein_param, u_range=[0, 2 * PI],
                             v_range=[0, 2 * PI],
                             resolution=(36, 24),
                             fill_opacity=0.6,
                             checkerboard_colors=[BLUE, PURPLE])

        self.add(always_redraw(klein_surface))

        title = Tex(r"Klein bottle: non-orientable, no boundary",
                    font_size=26).to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        info = VGroup(
            Tex(r"$\chi = 0$, non-orientable",
                 color=YELLOW, font_size=20),
            Tex(r"not embeddable in $\mathbb R^3$",
                 color=WHITE, font_size=18),
            Tex(r"figure-8 immersion shown",
                 color=WHITE, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DR, buff=0.4)
        self.add_fixed_in_frame_mobjects(info)

        self.begin_ambient_camera_rotation(rate=0.18)
        # Morph phase 1 → 0.3 → 1 to emphasize self-intersection forming
        self.play(t_tr.animate.set_value(0.3), run_time=3, rate_func=smooth)
        self.play(t_tr.animate.set_value(1.0), run_time=3, rate_func=smooth)
        self.wait(4)
        self.stop_ambient_camera_rotation()
