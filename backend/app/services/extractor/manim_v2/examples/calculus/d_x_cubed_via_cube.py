from manim import *
import numpy as np


class DxCubedViaCubeExample(ThreeDScene):
    """
    Geometric derivation: d(x³)/dx = 3x².
    A cube of side x has volume x³. Nudge side by dx. New volume
    (x+dx)³ = x³ + 3x²·dx + 3x·dx² + dx³. The largest first-order
    contribution is 3 square slabs of dimensions x·x·dx = x²·dx,
    one on each of 3 faces. So dV ≈ 3x²·dx → dV/dx = 3x².
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=35 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.06)

        axes = ThreeDAxes(x_range=[-0.5, 3, 1], y_range=[-0.5, 3, 1], z_range=[-0.5, 3, 1],
                          x_length=4, y_length=4, z_length=4)
        self.add(axes)

        x = 1.5
        dx_tr = ValueTracker(0.35)

        def main_cube():
            return Cube(side_length=x, fill_color=BLUE,
                         fill_opacity=0.4, stroke_width=1.5).move_to(
                np.array([x / 2, x / 2, x / 2]))

        # 3 slab faces (one per axis direction)
        def slab_x():
            dx = dx_tr.get_value()
            return Prism(dimensions=[dx, x, x], fill_color=GREEN,
                          fill_opacity=0.7, stroke_width=1).move_to(
                np.array([x + dx / 2, x / 2, x / 2]))

        def slab_y():
            dx = dx_tr.get_value()
            return Prism(dimensions=[x, dx, x], fill_color=ORANGE,
                          fill_opacity=0.7, stroke_width=1).move_to(
                np.array([x / 2, x + dx / 2, x / 2]))

        def slab_z():
            dx = dx_tr.get_value()
            return Prism(dimensions=[x, x, dx], fill_color=YELLOW,
                          fill_opacity=0.7, stroke_width=1).move_to(
                np.array([x / 2, x / 2, x + dx / 2]))

        self.add(main_cube(), always_redraw(slab_x),
                 always_redraw(slab_y), always_redraw(slab_z))

        # Fixed frame info
        title = Tex(r"$\frac{d(x^3)}{dx}=3x^2$ via cube",
                    font_size=28)
        info = VGroup(
            Tex(r"3 slabs of $x\cdot x\cdot dx = x^2 dx$", font_size=22),
            Tex(r"$dV\approx 3x^2\,dx$", color=YELLOW, font_size=24),
            Tex(r"$\frac{dV}{dx}=3x^2$", color=GREEN, font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        self.add_fixed_in_frame_mobjects(title, info)
        title.to_edge(UP, buff=0.3)
        info.to_corner(UR, buff=0.3)

        # Shrink dx → 0 to show limit
        self.wait(0.8)
        self.play(dx_tr.animate.set_value(0.05), run_time=4, rate_func=smooth)
        self.wait(0.8)
        self.stop_ambient_camera_rotation()
