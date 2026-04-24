from manim import *
import numpy as np


class ConformalDiskToHalfplaneExample(Scene):
    """
    Möbius map w = (z - i) / (z + i) sends the upper half-plane to
    the unit disk. Its inverse z = i(1 + w)/(1 - w) sends disk to
    UHP. Horizontal lines in UHP become circles through 1 on the
    disk boundary; circle arcs in UHP become arcs in the disk.

    COMPARISON:
      LEFT upper half-plane with horizontal/vertical grid lines;
      RIGHT unit disk with transformed curves.
    """

    def construct(self):
        title = Tex(r"Möbius disk $\leftrightarrow$ half-plane: $w = (z - i)/(z + i)$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        left = ComplexPlane(x_range=[-3, 3, 1], y_range=[0, 3, 1],
                              x_length=5, y_length=3.5,
                              background_line_style={"stroke_opacity": 0.25}
                              ).move_to([-3.5, 0, 0])
        right = ComplexPlane(x_range=[-1.5, 1.5, 0.5],
                               y_range=[-1.5, 1.5, 0.5],
                               x_length=4, y_length=4,
                               background_line_style={"stroke_opacity": 0.25}
                               ).move_to([3, 0, 0])
        self.play(Create(left), Create(right))

        # Unit circle on right
        unit_c = Circle(radius=right.c2p(1, 0)[0] - right.c2p(0, 0)[0],
                          color=YELLOW, stroke_width=3
                          ).move_to(right.c2p(0, 0))
        self.play(Create(unit_c))

        left_lbl = MathTex(r"z\text{-plane (UHP)}",
                             color=WHITE, font_size=20
                             ).next_to(left, UP, buff=0.1)
        right_lbl = MathTex(r"w = (z-i)/(z+i)",
                              color=YELLOW, font_size=20
                              ).next_to(right, UP, buff=0.1)
        self.play(Write(left_lbl), Write(right_lbl))

        def mob(z):
            return (z - 1j) / (z + 1j)

        # Draw horizontal lines y=0.5, 1, 1.5, 2
        # and their images (circles through 1 on disk)
        y_vals = [0.2, 0.5, 1.0, 1.5, 2.0]
        colors = [RED, ORANGE, GREEN, BLUE, PURPLE]

        for y, col in zip(y_vals, colors):
            # LEFT: horizontal line
            L_line = Line(left.c2p(-3, y), left.c2p(3, y),
                            color=col, stroke_width=2.5)
            self.add(L_line)
            # RIGHT: image — points along y=const map to a circle
            pts = []
            for xv in np.linspace(-3, 3, 120):
                w = mob(xv + 1j * y)
                pts.append(right.c2p(w.real, w.imag))
            R_curve = VMobject(color=col, stroke_width=2.5)
            R_curve.set_points_as_corners(pts)
            self.add(R_curve)

        # Vertical lines
        for x, col in zip([-1, 0, 1], [PINK, GOLD, TEAL]):
            L_line = Line(left.c2p(x, 0.01), left.c2p(x, 3),
                            color=col, stroke_width=2.5)
            self.add(L_line)
            pts = []
            for yv in np.linspace(0.02, 3, 80):
                w = mob(x + 1j * yv)
                pts.append(right.c2p(w.real, w.imag))
            R_curve = VMobject(color=col, stroke_width=2.5)
            R_curve.set_points_as_corners(pts)
            self.add(R_curve)

        # Moving point
        theta_tr = ValueTracker(0.0)

        def z_source():
            t = theta_tr.get_value()
            # Move around a square path in UHP
            # Simple: move along y=1 with x going -2 to 2 and back
            x = 2 * np.sin(t)
            y = 1.0 + 0.3 * np.cos(t)
            return x + 1j * y

        def z_dot():
            z = z_source()
            return Dot(left.c2p(z.real, z.imag),
                        color=YELLOW, radius=0.12)

        def w_dot():
            z = z_source()
            w = mob(z)
            return Dot(right.c2p(w.real, w.imag),
                        color=YELLOW, radius=0.12)

        self.add(always_redraw(z_dot), always_redraw(w_dot))

        info = VGroup(
            Tex(r"horizontal lines $\to$ circles through $w=1$",
                 color=WHITE, font_size=18),
            Tex(r"real axis $\to$ unit circle boundary",
                 color=YELLOW, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.3)
        self.play(Write(info))

        self.play(theta_tr.animate.set_value(4 * PI),
                   run_time=6, rate_func=linear)
        self.wait(0.4)
