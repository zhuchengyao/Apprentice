from manim import *
import numpy as np


class CauchyIntegralFormulaExample(Scene):
    """
    Cauchy integral formula: for f holomorphic on and inside γ,
        f(z_0) = 1/(2πi) ∮_γ f(z)/(z - z_0) dz
    Visualize via ∮_γ 1/(z - z_0) dz = 2πi for z_0 inside, 0 outside.

    SINGLE_FOCUS:
      ComplexPlane with a circle γ of radius 2 and a pole z_0 inside/
      outside. ValueTracker theta_tr parametrizes γ; always_redraw
      running complex-integral partial sum. Sum → 2πi (inside) or 0
      (outside).
    """

    def construct(self):
        title = Tex(r"Cauchy: $\oint_\gamma \frac{dz}{z - z_0} = 2\pi i$ ($z_0$ inside)",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = ComplexPlane(x_range=[-3, 3, 1], y_range=[-2.5, 2.5, 1],
                               x_length=7, y_length=5.5,
                               background_line_style={"stroke_opacity": 0.25}
                               ).move_to([-2, -0.3, 0])
        self.play(Create(plane))

        R = 2.0
        gamma_circle = Circle(radius=plane.c2p(R, 0)[0] - plane.c2p(0, 0)[0],
                                color=BLUE, stroke_width=3
                                ).move_to(plane.c2p(0, 0))
        self.play(Create(gamma_circle))

        z0_state = {"z": 0.8 + 0.4j}  # inside

        def z0_dot():
            z = z0_state["z"]
            return Dot(plane.c2p(z.real, z.imag), color=RED, radius=0.12)

        def z0_lbl():
            z = z0_state["z"]
            return MathTex(r"z_0", color=RED, font_size=22
                             ).next_to(
                plane.c2p(z.real, z.imag), UR, buff=0.05)

        self.add(always_redraw(z0_dot), always_redraw(z0_lbl))

        theta_tr = ValueTracker(0.0)

        def current_pt():
            t = theta_tr.get_value()
            return plane.c2p(R * np.cos(t), R * np.sin(t))

        def gamma_pt():
            return Dot(current_pt(), color=YELLOW, radius=0.11)

        def arc_trail():
            t = theta_tr.get_value()
            pts = []
            for ti in np.linspace(0, t, max(10, int(100 * t / (2 * PI)))):
                pts.append(plane.c2p(R * np.cos(ti), R * np.sin(ti)))
            m = VMobject(color=YELLOW, stroke_width=4)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        self.add(always_redraw(arc_trail), always_redraw(gamma_pt))

        # Integral running sum: I(t) = ∫_0^t iR e^{iτ}/(R e^{iτ} - z_0) dτ
        def integral_value(t):
            # Trapezoidal sum
            N = max(2, int(200 * t / (2 * PI)))
            taus = np.linspace(0.0001, t, N)
            dtau = t / N if N > 0 else 0.01
            z0 = z0_state["z"]
            total = 0 + 0j
            for tau in taus:
                z = R * np.exp(1j * tau)
                dz = 1j * R * np.exp(1j * tau)
                total += dz / (z - z0) * dtau
            return total

        def info():
            t = theta_tr.get_value()
            I = integral_value(t)
            z = z0_state["z"]
            inside = abs(z) < R
            return VGroup(
                MathTex(rf"\theta = {np.degrees(t):.0f}^\circ",
                         color=YELLOW, font_size=22),
                MathTex(rf"I(\theta) = {I.real:+.3f} {'+' if I.imag >= 0 else '-'} {abs(I.imag):.3f}\,i",
                         color=GREEN, font_size=20),
                MathTex(r"\text{expected: } 2\pi i \approx 6.283\,i"
                         if inside else r"\text{expected: } 0",
                         color=BLUE, font_size=20),
                Tex(r"inside" if inside else r"outside",
                     color=GREEN if inside else RED, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        self.play(theta_tr.animate.set_value(2 * PI),
                   run_time=5, rate_func=linear)
        self.wait(0.5)

        # Switch pole to outside
        new_pos = 2.8 + 0.3j
        z0_state["z"] = new_pos
        theta_tr.set_value(0.0001)
        self.play(theta_tr.animate.set_value(2 * PI),
                   run_time=5, rate_func=linear)
        self.wait(0.5)
