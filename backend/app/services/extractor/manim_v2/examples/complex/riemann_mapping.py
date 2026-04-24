from manim import *
import numpy as np


class RiemannMappingExample(Scene):
    """
    Riemann mapping theorem: every simply-connected proper subset of
    ℂ is conformally equivalent to the unit disk.

    COMPARISON:
      LEFT: upper-half plane H; RIGHT: unit disk 𝔻. Cayley map
      w = (z - i)/(z + i) provides the conformal equivalence.
      Grid curves map visibly.
    """

    def construct(self):
        title = Tex(r"Riemann mapping: simply-connected $\to$ unit disk",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        left = ComplexPlane(x_range=[-3, 3, 1], y_range=[0, 3, 1],
                              x_length=5, y_length=3.2,
                              background_line_style={"stroke_opacity": 0.25}
                              ).move_to([-3.5, 0.4, 0])
        right = ComplexPlane(x_range=[-1.3, 1.3, 0.5],
                               y_range=[-1.3, 1.3, 0.5],
                               x_length=4, y_length=4,
                               background_line_style={"stroke_opacity": 0.25}
                               ).move_to([3.5, -0.3, 0])
        self.play(Create(left), Create(right))

        unit_c = Circle(radius=right.c2p(1, 0)[0] - right.c2p(0, 0)[0],
                          color=YELLOW, stroke_width=2
                          ).move_to(right.c2p(0, 0))
        self.play(Create(unit_c))

        z_lbl = MathTex(r"H = \{z: \Im z > 0\}",
                         color=BLUE, font_size=18
                         ).next_to(left, UP, buff=0.1)
        w_lbl = MathTex(r"\mathbb D = \{|w| < 1\}",
                         color=YELLOW, font_size=18
                         ).next_to(right, UP, buff=0.1)
        self.play(Write(z_lbl), Write(w_lbl))

        def cayley(z):
            return (z - 1j) / (z + 1j)

        # Grid lines: horizontal y=const and vertical x=const
        colors_grid = [RED, GREEN, BLUE, ORANGE, PURPLE, TEAL]

        for i, y in enumerate([0.3, 0.8, 1.3, 2.0]):
            L_line = Line(left.c2p(-3, y), left.c2p(3, y),
                            color=colors_grid[i % 6], stroke_width=2)
            self.add(L_line)
            # Image: horizontal line in H maps to arc in disk
            pts = []
            for x in np.linspace(-3, 3, 60):
                w = cayley(x + 1j * y)
                pts.append(right.c2p(w.real, w.imag))
            m = VMobject(color=colors_grid[i % 6], stroke_width=2)
            m.set_points_as_corners(pts)
            self.add(m)

        for i, x in enumerate([-1.5, 0, 1.5]):
            L_line = Line(left.c2p(x, 0.02), left.c2p(x, 3),
                            color=colors_grid[(i + 4) % 6], stroke_width=2)
            self.add(L_line)
            pts = []
            for y in np.linspace(0.02, 3, 50):
                w = cayley(x + 1j * y)
                pts.append(right.c2p(w.real, w.imag))
            m = VMobject(color=colors_grid[(i + 4) % 6], stroke_width=2)
            m.set_points_as_corners(pts)
            self.add(m)

        # Moving point
        t_tr = ValueTracker(0)

        def z_dot():
            t = t_tr.get_value()
            x = 2 * np.sin(t)
            y = 1 + 0.7 * np.cos(t)
            return Dot(left.c2p(x, y), color=YELLOW, radius=0.12)

        def w_dot():
            t = t_tr.get_value()
            x = 2 * np.sin(t)
            y = 1 + 0.7 * np.cos(t)
            w = cayley(x + 1j * y)
            return Dot(right.c2p(w.real, w.imag),
                        color=YELLOW, radius=0.12)

        self.add(always_redraw(z_dot), always_redraw(w_dot))

        info = VGroup(
            MathTex(r"\text{Cayley: } w = \tfrac{z - i}{z + i}",
                     color=WHITE, font_size=22),
            Tex(r"conformal (angle-preserving)",
                 color=GREEN, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.25)
        self.play(Write(info))

        self.play(t_tr.animate.set_value(2 * PI),
                   run_time=6, rate_func=linear)
        self.wait(0.4)
