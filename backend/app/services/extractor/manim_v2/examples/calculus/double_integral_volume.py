from manim import *
import numpy as np


class DoubleIntegralVolumeExample(ThreeDScene):
    """
    Double integral as volume under surface: ∫∫_D f(x, y) dA =
    volume under z = f(x, y) over region D. Illustrate with f(x, y)
    = x² + y² on [0, 1]².

    3D scene:
      Paraboloid surface over [0, 1]² + stack of tall rectangular
      prisms (Riemann sums); ValueTracker N_tr refines grid.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-40 * DEGREES)
        axes = ThreeDAxes(x_range=[0, 1.2, 0.25], y_range=[0, 1.2, 0.25],
                           z_range=[0, 2.5, 0.5],
                           x_length=4, y_length=4, z_length=3)
        self.add(axes)

        def f(x, y):
            return x ** 2 + y ** 2

        # True integral: ∫∫_[0,1]² (x²+y²) dx dy = 2/3
        true_vol = 2 / 3

        surface = Surface(lambda u, v: axes.c2p(u, v, f(u, v)),
                            u_range=[0, 1], v_range=[0, 1],
                            resolution=(15, 15),
                            fill_opacity=0.35,
                            checkerboard_colors=[GREEN, GREEN_E])
        self.add(surface)

        N_tr = ValueTracker(2)

        def riemann_prisms():
            N = int(round(N_tr.get_value()))
            N = max(2, min(N, 15))
            h = 1 / N
            grp = VGroup()
            for i in range(N):
                for j in range(N):
                    x_c = (i + 0.5) * h
                    y_c = (j + 0.5) * h
                    z = f(x_c, y_c)
                    # Draw prism as 4 bottom corners + top corners
                    p00 = axes.c2p(i * h, j * h, 0)
                    p10 = axes.c2p((i + 1) * h, j * h, 0)
                    p11 = axes.c2p((i + 1) * h, (j + 1) * h, 0)
                    p01 = axes.c2p(i * h, (j + 1) * h, 0)
                    p00t = axes.c2p(i * h, j * h, z)
                    p10t = axes.c2p((i + 1) * h, j * h, z)
                    p11t = axes.c2p((i + 1) * h, (j + 1) * h, z)
                    p01t = axes.c2p(i * h, (j + 1) * h, z)
                    # Top face
                    top_face = Polygon(p00t, p10t, p11t, p01t,
                                         color=YELLOW, fill_opacity=0.4,
                                         stroke_width=0.5)
                    grp.add(top_face)
            return grp

        self.add(always_redraw(riemann_prisms))

        title = Tex(r"Double integral $=$ volume under surface",
                    font_size=24).to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        def panel():
            N = int(round(N_tr.get_value()))
            h = 1 / N
            approx = sum(f((i + 0.5) * h, (j + 0.5) * h) * h * h
                          for i in range(N) for j in range(N))
            return VGroup(
                MathTex(rf"N = {N} \times {N}",
                         color=YELLOW, font_size=22),
                MathTex(rf"V_{{\text{{approx}}}} = {approx:.4f}",
                         color=YELLOW, font_size=20),
                MathTex(rf"\iint (x^2+y^2)\,dA = 2/3",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DR, buff=0.4)

        pnl = panel()
        self.add_fixed_in_frame_mobjects(pnl)

        self.begin_ambient_camera_rotation(rate=0.12)
        for nv in [4, 8, 12]:
            self.play(N_tr.animate.set_value(nv),
                       run_time=1.8, rate_func=smooth)
            new_pnl = panel()
            self.add_fixed_in_frame_mobjects(new_pnl)
            self.play(Transform(pnl, new_pnl), run_time=0.2)
            self.wait(0.5)
        self.stop_ambient_camera_rotation()
