from manim import *
import numpy as np


class DirectionalDerivativeExample(Scene):
    """
    Directional derivative: D_u f = ∇f · u, maximized when u points
    along ∇f. Visualize by rotating u and tracking D_u f.

    SINGLE_FOCUS:
      Contour plot of f(x, y) = x² + 3y² at fixed point p. ValueTracker
      theta_tr rotates unit direction u; always_redraw u arrow,
      gradient arrow, and D_u f readout.
    """

    def construct(self):
        title = Tex(r"Directional derivative: $D_{\hat u} f = \nabla f \cdot \hat u$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-3, 3, 1], y_range=[-2, 2, 1],
                             x_length=8, y_length=5.5,
                             background_line_style={"stroke_opacity": 0.3}
                             ).move_to([-1, -0.3, 0])
        self.play(Create(plane))

        # Contours of f = x² + 3y²
        contours = VGroup()
        for level in [1, 3, 6, 10]:
            pts = []
            for a in np.linspace(0, 2 * PI, 100):
                # level = x²+3y², parametrize: x = √level cos a, y = √(level/3) sin a
                x = np.sqrt(level) * np.cos(a)
                y = np.sqrt(level / 3) * np.sin(a)
                pts.append(plane.c2p(x, y))
            m = VMobject(color=BLUE_D, stroke_width=1.5, stroke_opacity=0.55)
            m.set_points_as_corners(pts + [pts[0]])
            contours.add(m)
        self.play(Create(contours))

        p = np.array([1.5, 0.8])
        p_dot = Dot(plane.c2p(*p), color=RED, radius=0.12)
        p_lbl = MathTex(r"p", color=RED, font_size=22
                          ).next_to(p_dot, UR, buff=0.1)
        self.play(FadeIn(p_dot), Write(p_lbl))

        # Gradient at p: (2x, 6y) = (3, 4.8)
        grad = np.array([2 * p[0], 6 * p[1]])
        grad_arrow = Arrow(plane.c2p(*p),
                             plane.c2p(p[0] + 0.3 * grad[0],
                                          p[1] + 0.3 * grad[1]),
                             color=GREEN, buff=0, stroke_width=5,
                             max_tip_length_to_length_ratio=0.15)
        grad_lbl = MathTex(r"\nabla f", color=GREEN, font_size=20
                             ).next_to(grad_arrow.get_end(), UR, buff=0.1)
        self.play(Create(grad_arrow), Write(grad_lbl))

        theta_tr = ValueTracker(0.0)

        def u_arrow():
            t = theta_tr.get_value()
            u = np.array([np.cos(t), np.sin(t)])
            end = p + 0.8 * u
            return Arrow(plane.c2p(*p), plane.c2p(*end),
                          color=YELLOW, buff=0, stroke_width=5,
                          max_tip_length_to_length_ratio=0.2)

        self.add(always_redraw(u_arrow))

        def info():
            t = theta_tr.get_value()
            u = np.array([np.cos(t), np.sin(t)])
            D_u = np.dot(grad, u)
            D_max = np.linalg.norm(grad)
            return VGroup(
                MathTex(rf"\theta = {np.degrees(t):.0f}^\circ",
                         color=YELLOW, font_size=22),
                MathTex(rf"\nabla f = ({grad[0]:.1f}, {grad[1]:.1f})",
                         color=GREEN, font_size=18),
                MathTex(rf"D_{{\hat u}} f = {D_u:+.3f}",
                         color=YELLOW, font_size=22),
                MathTex(rf"\max = \|\nabla f\| = {D_max:.3f}",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        self.play(theta_tr.animate.set_value(2 * PI),
                   run_time=7, rate_func=linear)
        self.wait(0.4)
