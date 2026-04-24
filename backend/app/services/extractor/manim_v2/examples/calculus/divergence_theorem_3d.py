from manim import *
import numpy as np


class DivergenceTheorem3DExample(ThreeDScene):
    """
    Divergence theorem (Gauss): ∫∫∫_V ∇·F dV = ∮∮_S F · n̂ dA.
    For F = (x, y, z) (div = 3) and V = unit ball: volume integral
    = 3 · (4π/3) = 4π; flux integral = 4π (surface integral of r·n̂).

    3D scene:
      Unit sphere + radial arrow field around it; ValueTracker t_tr
      reveals flux arrows progressively; always_redraw sphere
      surface.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-40 * DEGREES)
        axes = ThreeDAxes(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                           z_range=[-2, 2, 1],
                           x_length=4, y_length=4, z_length=4)
        self.add(axes)

        R = 1.0
        sphere = Sphere(radius=R, resolution=(18, 18),
                          fill_opacity=0.35,
                          color=BLUE_D).move_to(axes.c2p(0, 0, 0))
        self.add(sphere)

        t_tr = ValueTracker(0.0)

        def flux_arrows():
            t = t_tr.get_value()
            grp = VGroup()
            # Distribute arrows over sphere via fibonacci sphere
            N = 40
            phi_gold = PI * (3 - np.sqrt(5))
            revealed = int(t * N)
            for i in range(min(revealed, N)):
                y = 1 - 2 * (i / (N - 1)) if N > 1 else 0
                radius = np.sqrt(1 - y * y)
                theta = phi_gold * i
                x = np.cos(theta) * radius
                z = np.sin(theta) * radius
                p = np.array([x * R, y * R, z * R])
                # n̂ = p/R; F·n̂ = R (for F = (x, y, z))
                # Arrow along n̂
                start = axes.c2p(*p)
                end = axes.c2p(*(p * 1.5))
                grp.add(Line(start, end, color=YELLOW, stroke_width=3))
            return grp

        self.add(always_redraw(flux_arrows))

        title = Tex(r"Gauss: $\iiint \nabla\cdot\vec F\,dV = \oiint \vec F \cdot \hat n\,dA$",
                    font_size=22).to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        def panel():
            t = t_tr.get_value()
            n_rev = int(t * 40)
            return VGroup(
                MathTex(r"\vec F = (x, y, z)", color=YELLOW, font_size=22),
                MathTex(r"\nabla\cdot\vec F = 3", color=GREEN, font_size=22),
                MathTex(r"\iiint_V 3\,dV = 3 \cdot \tfrac{4\pi}{3} = 4\pi",
                         color=GREEN, font_size=20),
                MathTex(rf"\text{{flux arrows shown}} = {n_rev}/40",
                         color=YELLOW, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DR, buff=0.4)

        pnl = panel()
        self.add_fixed_in_frame_mobjects(pnl)

        self.begin_ambient_camera_rotation(rate=0.15)
        self.play(t_tr.animate.set_value(1.0), run_time=7, rate_func=linear)
        new_pnl = panel()
        self.add_fixed_in_frame_mobjects(new_pnl)
        self.play(Transform(pnl, new_pnl), run_time=0.2)
        self.stop_ambient_camera_rotation()
        self.wait(0.4)
