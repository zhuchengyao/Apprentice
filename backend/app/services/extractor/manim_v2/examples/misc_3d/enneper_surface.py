from manim import *
import numpy as np


class EnneperSurfaceExample(ThreeDScene):
    """
    Enneper surface: classic self-intersecting minimal surface.
    Parametrization:
      x = u - u³/3 + u v²
      y = v - v³/3 + v u²
      z = u² - v²

    3D scene:
      Parametric surface drawn; ambient camera rotation;
      ValueTracker r_tr expands parameter domain showing more
      of the surface.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-40 * DEGREES)
        axes = ThreeDAxes(x_range=[-4, 4, 1], y_range=[-4, 4, 1],
                           z_range=[-4, 4, 1],
                           x_length=5, y_length=5, z_length=5)
        self.add(axes)

        r_tr = ValueTracker(0.3)

        def enneper():
            r = r_tr.get_value()

            def param(u, v):
                x = u - u ** 3 / 3 + u * v ** 2
                y = v - v ** 3 / 3 + v * u ** 2
                z = u ** 2 - v ** 2
                return axes.c2p(x, y, z)

            return Surface(param, u_range=[-r, r], v_range=[-r, r],
                             resolution=(25, 25),
                             fill_opacity=0.65,
                             checkerboard_colors=[BLUE_D, PURPLE])

        self.add(always_redraw(enneper))

        title = Tex(r"Enneper surface: minimal, self-intersecting",
                    font_size=24).to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        def panel():
            r = r_tr.get_value()
            return VGroup(
                MathTex(rf"u, v \in [-r, r],\ r = {r:.2f}",
                         color=YELLOW, font_size=22),
                Tex(r"minimal (mean curvature $= 0$)",
                     color=GREEN, font_size=20),
                Tex(r"self-intersects for $r \gtrsim 1.5$",
                     color=RED, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DR, buff=0.4)

        pnl = panel()
        self.add_fixed_in_frame_mobjects(pnl)

        self.begin_ambient_camera_rotation(rate=0.15)
        for rv in [0.8, 1.3, 1.8, 0.6]:
            self.play(r_tr.animate.set_value(rv),
                       run_time=1.8, rate_func=smooth)
            new_pnl = panel()
            self.add_fixed_in_frame_mobjects(new_pnl)
            self.play(Transform(pnl, new_pnl), run_time=0.2)
            self.wait(0.4)
        self.stop_ambient_camera_rotation()
