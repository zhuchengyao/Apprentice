from manim import *
import numpy as np


class ArgumentPrincipleExample(Scene):
    """
    Argument principle: (1/2πi) ∮_γ f'(z)/f(z) dz = Z - P, where Z
    is the number of zeros and P the number of poles of f inside γ.
    Equivalently, the image of γ under f winds around 0 (Z - P) times.

    COMPARISON:
      LEFT z-plane with contour γ; RIGHT w = f(z) image plane. For
      f(z) = (z - 0.5)(z + 0.3) (Z=2, P=0), image winds twice.
    """

    def construct(self):
        title = Tex(r"Argument principle: $\frac{1}{2\pi i}\oint \frac{f'}{f}\,dz = Z - P$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        left = ComplexPlane(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                              x_length=5, y_length=5,
                              background_line_style={"stroke_opacity": 0.25}
                              ).move_to([-3.5, -0.3, 0])
        right = ComplexPlane(x_range=[-4, 4, 1], y_range=[-4, 4, 1],
                               x_length=5, y_length=5,
                               background_line_style={"stroke_opacity": 0.25}
                               ).move_to([3.5, -0.3, 0])
        self.play(Create(left), Create(right))

        R = 1.5
        z_circ = Circle(radius=left.c2p(R, 0)[0] - left.c2p(0, 0)[0],
                          color=BLUE, stroke_width=3
                          ).move_to(left.c2p(0, 0))

        # Zeros of f at 0.5 and -0.3
        zeros = [0.5 + 0j, -0.3 + 0j]
        zero_dots = VGroup(
            Dot(left.c2p(zeros[0].real, zeros[0].imag),
                 color=RED, radius=0.1),
            Dot(left.c2p(zeros[1].real, zeros[1].imag),
                 color=RED, radius=0.1),
        )
        self.play(Create(z_circ), FadeIn(zero_dots))

        z_lbl = MathTex(r"z\text{-plane}", font_size=20
                         ).next_to(left, UP, buff=0.1)
        w_lbl = MathTex(r"w = (z-0.5)(z+0.3)",
                          color=YELLOW, font_size=18
                          ).next_to(right, UP, buff=0.1)
        self.play(Write(z_lbl), Write(w_lbl))

        # Origin on right plane
        right_origin = Dot(right.c2p(0, 0), color=YELLOW_E, radius=0.12)
        right_origin_lbl = MathTex(r"0", color=YELLOW_E, font_size=18
                                      ).next_to(right_origin, DR, buff=0.05)
        self.play(FadeIn(right_origin), Write(right_origin_lbl))

        theta_tr = ValueTracker(0.0)

        def z_dot():
            t = theta_tr.get_value()
            return Dot(left.c2p(R * np.cos(t), R * np.sin(t)),
                        color=BLUE, radius=0.1)

        def w_trail():
            t_cur = theta_tr.get_value()
            pts = []
            for t in np.linspace(0, t_cur, max(10, int(200 * t_cur / (2 * PI)))):
                z = R * np.exp(1j * t)
                w = (z - 0.5) * (z + 0.3)
                pts.append(right.c2p(w.real, w.imag))
            m = VMobject(color=YELLOW, stroke_width=3)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        def w_dot():
            t = theta_tr.get_value()
            z = R * np.exp(1j * t)
            w = (z - 0.5) * (z + 0.3)
            return Dot(right.c2p(w.real, w.imag),
                        color=RED, radius=0.11)

        self.add(always_redraw(z_dot), always_redraw(w_trail),
                  always_redraw(w_dot))

        def info():
            t = theta_tr.get_value()
            # Running winding approx
            winding_complete = t / (2 * PI) * 2  # expected 2 windings when t=2π
            return VGroup(
                MathTex(rf"\theta = {np.degrees(t):.0f}^\circ",
                         color=BLUE, font_size=22),
                MathTex(rf"\text{{windings so far}} \approx {winding_complete:.2f}",
                         color=YELLOW, font_size=22),
                MathTex(r"Z = 2 \text{ zeros, } P = 0",
                         color=RED, font_size=20),
                MathTex(r"\text{total winding} = Z - P = 2",
                         color=GREEN, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        self.play(theta_tr.animate.set_value(2 * PI),
                   run_time=7, rate_func=linear)
        self.wait(0.5)
