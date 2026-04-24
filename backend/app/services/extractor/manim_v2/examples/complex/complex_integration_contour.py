from manim import *
import numpy as np


class ComplexIntegrationContourExample(Scene):
    """
    Contour integral ∫_γ f(z) dz for f(z) = z² on two paths from
    -1-i to 1+i: straight line vs semicircle. Path-independence
    for holomorphic f implies both give the same value.

    COMPARISON:
      LEFT z-plane with both paths; ValueTracker s_tr traces both
      simultaneously with a rider dot on each.
      RIGHT running ∫ values for both paths; they converge to same
      number.
    """

    def construct(self):
        title = Tex(r"$\int_\gamma z^2\,dz$ is path-independent",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = ComplexPlane(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                               x_length=5.5, y_length=5.5,
                               background_line_style={"stroke_opacity": 0.25}
                               ).move_to([-3.5, -0.3, 0])
        self.play(Create(plane))

        z0 = -1 - 1j
        z1 = 1 + 1j

        z0_dot = Dot(plane.c2p(z0.real, z0.imag), color=GREEN, radius=0.12)
        z1_dot = Dot(plane.c2p(z1.real, z1.imag), color=RED, radius=0.12)
        self.play(FadeIn(z0_dot, z1_dot))

        # Path 1: straight line z(t) = (1-t) z0 + t z1
        def path1(t):
            return (1 - t) * z0 + t * z1

        # Path 2: semicircle through origin (upper half arc)
        def path2(t):
            # center = midpoint, radius = |z1 - z0|/2, angle from z0 to z1 going CCW
            center = (z0 + z1) / 2
            r = abs(z1 - z0) / 2
            ang_start = np.angle(z0 - center)
            # Semicircle: ang_start + t * PI (CCW)
            ang = ang_start + t * PI
            return center + r * np.exp(1j * ang)

        s_tr = ValueTracker(0.0)

        def path1_trail():
            s = s_tr.get_value()
            pts = [plane.c2p(path1(t).real, path1(t).imag)
                   for t in np.linspace(0, s, 50)]
            m = VMobject(color=BLUE, stroke_width=3)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        def path2_trail():
            s = s_tr.get_value()
            pts = [plane.c2p(path2(t).real, path2(t).imag)
                   for t in np.linspace(0, s, 50)]
            m = VMobject(color=PURPLE, stroke_width=3)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        def path1_dot():
            s = s_tr.get_value()
            p = path1(s)
            return Dot(plane.c2p(p.real, p.imag),
                        color=BLUE, radius=0.1)

        def path2_dot():
            s = s_tr.get_value()
            p = path2(s)
            return Dot(plane.c2p(p.real, p.imag),
                        color=PURPLE, radius=0.1)

        self.add(always_redraw(path1_trail), always_redraw(path2_trail),
                  always_redraw(path1_dot), always_redraw(path2_dot))

        # Integral values via numerical integration
        def integrate_along_path(path_fn, s_end):
            N = max(2, int(200 * s_end))
            ts = np.linspace(0, s_end, N)
            total = 0 + 0j
            for i in range(N - 1):
                z_a = path_fn(ts[i])
                z_b = path_fn(ts[i + 1])
                z_mid = (z_a + z_b) / 2
                dz = z_b - z_a
                total += z_mid ** 2 * dz
            return total

        # Analytic result: ∫_z0^z1 z² dz = (z1³ - z0³) / 3
        true_val = (z1 ** 3 - z0 ** 3) / 3

        def info():
            s = s_tr.get_value()
            I1 = integrate_along_path(path1, s)
            I2 = integrate_along_path(path2, s)
            return VGroup(
                MathTex(rf"s = {s:.2f}", color=WHITE, font_size=22),
                MathTex(rf"\int_{{\gamma_1}}: {I1.real:+.3f} {'+' if I1.imag >= 0 else '-'} {abs(I1.imag):.3f}i",
                         color=BLUE, font_size=20),
                MathTex(rf"\int_{{\gamma_2}}: {I2.real:+.3f} {'+' if I2.imag >= 0 else '-'} {abs(I2.imag):.3f}i",
                         color=PURPLE, font_size=20),
                MathTex(rf"\text{{exact}}: {true_val.real:+.3f} {'+' if true_val.imag >= 0 else '-'} {abs(true_val.imag):.3f}i",
                         color=YELLOW, font_size=20),
                Tex(r"match at $s=1$", color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        self.play(s_tr.animate.set_value(1.0),
                   run_time=6, rate_func=linear)
        self.wait(0.5)
