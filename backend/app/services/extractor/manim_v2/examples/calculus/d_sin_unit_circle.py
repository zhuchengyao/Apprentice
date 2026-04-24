from manim import *
import numpy as np


class DSinUnitCircleExample(Scene):
    """
    d(sin θ)/dθ = cos(θ) via unit circle.
    As θ increases by dθ, the point on the unit circle moves along
    an arc of length dθ (since radius=1). The y-coordinate change
    dy = sin(θ+dθ) - sin(θ) ≈ cos(θ) · dθ (tangent direction).
    So d(sin θ)/dθ = cos θ.
    """

    def construct(self):
        title = Tex(r"$\frac{d\sin\theta}{d\theta}=\cos\theta$ via unit circle",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-1.5, 1.5, 0.5], y_range=[-1.5, 1.5, 0.5],
                            x_length=4.5, y_length=4.5,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(LEFT * 3.3 + DOWN * 0.1)
        self.play(Create(plane))

        unit_c = Circle(radius=plane.x_length / (plane.x_range[1] - plane.x_range[0]),
                         color=BLUE, stroke_width=2).move_to(plane.n2p(0))
        self.add(unit_c)

        theta_tr = ValueTracker(PI / 4)

        def p_dot():
            t = theta_tr.get_value()
            return Dot(plane.n2p(complex(np.cos(t), np.sin(t))),
                        color=YELLOW, radius=0.1)

        def radial_line():
            t = theta_tr.get_value()
            return Line(plane.n2p(0), plane.n2p(complex(np.cos(t), np.sin(t))),
                         color=ORANGE, stroke_width=3)

        def sin_height():
            t = theta_tr.get_value()
            x_coord = np.cos(t)
            y_coord = np.sin(t)
            return Line(plane.n2p(complex(x_coord, 0)),
                         plane.n2p(complex(x_coord, y_coord)),
                         color=GREEN, stroke_width=4)

        # Tangent arrow direction at P
        def tangent_arrow():
            t = theta_tr.get_value()
            p = np.array([np.cos(t), np.sin(t)])
            tangent_dir = np.array([-np.sin(t), np.cos(t)])  # perpendicular to radial
            start = plane.n2p(complex(p[0], p[1]))
            end = plane.n2p(complex(p[0] + tangent_dir[0] * 0.3,
                                      p[1] + tangent_dir[1] * 0.3))
            return Arrow(start, end, color=RED, buff=0, stroke_width=3,
                          max_tip_length_to_length_ratio=0.2)

        self.add(always_redraw(p_dot), always_redraw(radial_line),
                 always_redraw(sin_height), always_redraw(tangent_arrow))

        # Right column: derivation
        info = VGroup(
            Tex(r"$\vec p=(\cos\theta, \sin\theta)$", color=YELLOW, font_size=22),
            Tex(r"tangent dir $=(-\sin\theta, \cos\theta)$",
                color=RED, font_size=22),
            Tex(r"arc length $=d\theta$ (radius 1)",
                color=GREY_B, font_size=22),
            Tex(r"$dy = \cos\theta\,d\theta$",
                color=GREEN, font_size=24),
            MathTex(r"\boxed{\frac{d\sin\theta}{d\theta}=\cos\theta}",
                     color=YELLOW, font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.3)
        self.play(Write(info))
        self.wait(0.4)

        self.play(theta_tr.animate.set_value(5 * PI / 6), run_time=4, rate_func=smooth)
        self.wait(0.5)
