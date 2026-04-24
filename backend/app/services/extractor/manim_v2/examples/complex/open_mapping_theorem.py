from manim import *
import numpy as np


class OpenMappingTheoremExample(Scene):
    """
    Open mapping theorem: a non-constant holomorphic map sends open
    sets to open sets. Illustrate: small disk around z_0 maps under
    f(z) = z² + 1 to an open set around f(z_0) = z_0² + 1.

    COMPARISON:
      LEFT: small disk |z - z_0| < r; RIGHT: image f(disk), which is
      an open (approximately elliptical) region around f(z_0).
    """

    def construct(self):
        title = Tex(r"Open mapping: holomorphic $\Rightarrow$ open sets $\to$ open sets",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        left = ComplexPlane(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                              x_length=5, y_length=5,
                              background_line_style={"stroke_opacity": 0.25}
                              ).move_to([-3.5, -0.3, 0])
        right = ComplexPlane(x_range=[-3, 5, 1], y_range=[-3, 3, 1],
                               x_length=5, y_length=4,
                               background_line_style={"stroke_opacity": 0.25}
                               ).move_to([3.5, -0.3, 0])
        self.play(Create(left), Create(right))

        z_lbl = MathTex(r"z\text{-plane}", font_size=20
                         ).next_to(left, UP, buff=0.1)
        w_lbl = MathTex(r"f(z) = z^2 + 1", color=YELLOW, font_size=20
                          ).next_to(right, UP, buff=0.1)
        self.play(Write(z_lbl), Write(w_lbl))

        z_center_state = [1.0 + 0.5j]
        r_tr = ValueTracker(0.5)

        def z0_dot():
            z0 = z_center_state[0]
            return Dot(left.c2p(z0.real, z0.imag),
                        color=RED, radius=0.12)

        def source_disk():
            z0 = z_center_state[0]
            r = r_tr.get_value()
            return Circle(radius=(left.c2p(r, 0)[0] - left.c2p(0, 0)[0]),
                            color=BLUE, fill_opacity=0.4,
                            stroke_width=2
                            ).move_to(left.c2p(z0.real, z0.imag))

        def image_region():
            z0 = z_center_state[0]
            r = r_tr.get_value()
            # Sample boundary of disk
            pts = []
            for ang in np.linspace(0, 2 * PI, 80):
                z = z0 + r * np.exp(1j * ang)
                w = z ** 2 + 1
                pts.append(right.c2p(w.real, w.imag))
            m = VMobject(color=GREEN, fill_opacity=0.4, stroke_width=2)
            m.set_points_as_corners(pts + [pts[0]])
            return m

        def image_center():
            z0 = z_center_state[0]
            w0 = z0 ** 2 + 1
            return Dot(right.c2p(w0.real, w0.imag),
                        color=RED, radius=0.12)

        self.add(always_redraw(source_disk),
                  always_redraw(image_region),
                  always_redraw(z0_dot),
                  always_redraw(image_center))

        def info():
            z0 = z_center_state[0]
            r = r_tr.get_value()
            w0 = z0 ** 2 + 1
            return VGroup(
                MathTex(rf"z_0 = {z0.real:+.2f} {'+' if z0.imag >= 0 else '-'} {abs(z0.imag):.2f}i",
                         color=RED, font_size=20),
                MathTex(rf"r = {r:.2f}", color=BLUE, font_size=22),
                MathTex(rf"f(z_0) = {w0.real:+.2f} {'+' if w0.imag >= 0 else '-'} {abs(w0.imag):.2f}i",
                         color=GREEN, font_size=20),
                Tex(r"image of open disk = open region",
                     color=YELLOW, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        for rv in [0.8, 0.2, 0.5]:
            self.play(r_tr.animate.set_value(rv),
                       run_time=1.8, rate_func=smooth)
            self.wait(0.5)
        # Change z_0
        z_center_state[0] = 0.0 + 1.0j
        self.play(r_tr.animate.set_value(0.4), run_time=1.5)
        self.wait(0.5)
        self.play(r_tr.animate.set_value(0.8), run_time=1.5)
        self.wait(0.4)
