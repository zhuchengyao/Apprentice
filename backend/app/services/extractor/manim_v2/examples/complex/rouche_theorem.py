from manim import *
import numpy as np


class RoucheTheoremExample(Scene):
    """
    Rouché's theorem: if |f(z)| > |g(z)| on contour γ, then f and
    f + g have the same number of zeros inside γ. Example:
    f(z) = z^5, g(z) = -3z² on |z|=2: |f|=32, |g|=12, so f+g has
    5 zeros inside.

    SINGLE_FOCUS:
      Contour |z|=2 + points on f(z), f(z)+g(z) as z walks around.
      Both wind 5 times around origin (same zero count).
    """

    def construct(self):
        title = Tex(r"Rouché: $|f| > |g|$ on $\gamma \Rightarrow \#$zeros$(f) = \#$zeros$(f+g)$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        left = ComplexPlane(x_range=[-3, 3, 1], y_range=[-3, 3, 1],
                              x_length=5, y_length=5,
                              background_line_style={"stroke_opacity": 0.25}
                              ).move_to([-3.5, -0.3, 0])
        right = ComplexPlane(x_range=[-40, 40, 20], y_range=[-40, 40, 20],
                               x_length=5, y_length=5,
                               background_line_style={"stroke_opacity": 0.25}
                               ).move_to([3.5, -0.3, 0])
        self.play(Create(left), Create(right))

        R = 2.0
        source_circle = Circle(radius=left.c2p(R, 0)[0] - left.c2p(0, 0)[0],
                                 color=BLUE, stroke_width=3
                                 ).move_to(left.c2p(0, 0))
        self.play(Create(source_circle))

        z_lbl = MathTex(r"|z| = 2", color=BLUE, font_size=22
                          ).next_to(left, UP, buff=0.1)
        w_lbl = MathTex(r"f(z) + g(z) = z^5 - 3z^2",
                          color=YELLOW, font_size=20
                          ).next_to(right, UP, buff=0.1)
        self.play(Write(z_lbl), Write(w_lbl))

        theta_tr = ValueTracker(0.0)

        def z_dot():
            t = theta_tr.get_value()
            return Dot(left.c2p(R * np.cos(t), R * np.sin(t)),
                        color=BLUE, radius=0.11)

        def f_trail():
            t_cur = theta_tr.get_value()
            pts = []
            for t in np.linspace(0, t_cur, max(20, int(300 * t_cur / (2 * PI)))):
                z = R * np.exp(1j * t)
                w = z ** 5
                # Clamp for visibility
                max_val = 35
                pts.append(right.c2p(np.clip(w.real, -max_val, max_val),
                                          np.clip(w.imag, -max_val, max_val)))
            m = VMobject(color=GREEN, stroke_width=2.5, stroke_opacity=0.7)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        def fg_trail():
            t_cur = theta_tr.get_value()
            pts = []
            for t in np.linspace(0, t_cur, max(20, int(300 * t_cur / (2 * PI)))):
                z = R * np.exp(1j * t)
                w = z ** 5 - 3 * z ** 2
                max_val = 35
                pts.append(right.c2p(np.clip(w.real, -max_val, max_val),
                                          np.clip(w.imag, -max_val, max_val)))
            m = VMobject(color=YELLOW, stroke_width=3)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        self.add(always_redraw(z_dot), always_redraw(f_trail),
                  always_redraw(fg_trail))

        # Origin on right plane
        origin_dot = Dot(right.c2p(0, 0), color=RED, radius=0.1)
        self.play(FadeIn(origin_dot))

        def info():
            t = theta_tr.get_value()
            winding = t / (2 * PI) * 5
            return VGroup(
                MathTex(rf"\theta = {np.degrees(t):.0f}^\circ",
                         color=BLUE, font_size=22),
                MathTex(rf"\text{{winds }} \approx {winding:.2f} \text{{ times}}",
                         color=YELLOW, font_size=20),
                Tex(r"GREEN: $z^5$; YELLOW: $z^5 - 3z^2$",
                     color=WHITE, font_size=16),
                MathTex(r"|z^5|=32 > |3z^2|=12 \text{ on } |z|=2",
                         color=GREEN, font_size=18),
                MathTex(r"5 \text{ zeros inside}",
                         color=YELLOW, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.13).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        self.play(theta_tr.animate.set_value(2 * PI),
                   run_time=7, rate_func=linear)
        self.wait(0.4)
