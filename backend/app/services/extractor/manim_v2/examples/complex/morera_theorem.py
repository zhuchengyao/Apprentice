from manim import *
import numpy as np


class MoreraTheoremExample(Scene):
    """
    Morera's theorem: if f is continuous on an open set D and
    ∮_γ f(z) dz = 0 for every closed loop γ in D, then f is
    holomorphic on D. Converse of Cauchy's theorem.

    SINGLE_FOCUS:
      Complex plane with f(z) = z² (holomorphic) and several test
      loops; ValueTracker loop_idx_tr cycles through 4 different
      loops; always_redraw ∮ f dz computing numerically (all → 0).
    """

    def construct(self):
        title = Tex(r"Morera: $\oint f\,dz = 0$ for all loops $\Rightarrow f$ holomorphic",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = ComplexPlane(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                               x_length=6, y_length=6,
                               background_line_style={"stroke_opacity": 0.25}
                               ).move_to([-2, -0.3, 0])
        self.play(Create(plane))

        def f(z):
            return z ** 2

        # 4 different test loops
        loops = [
            lambda t: np.exp(1j * t),  # unit circle
            lambda t: 1.2 * np.exp(1j * t) + 0.3 + 0.4j,  # shifted circle
            lambda t: 1.4 * (np.cos(t) + 1j * 0.6 * np.sin(t)),  # ellipse
            lambda t: 0.9 * (np.cos(t) + 1j * np.sin(t)) * (1 + 0.4 * np.cos(3 * t)),  # clover
        ]
        loop_names = ["circle", "shifted circle", "ellipse", "trefoil"]
        loop_colors = [BLUE, GREEN, ORANGE, PURPLE]

        loop_idx_tr = ValueTracker(0)

        def current_loop_curve():
            i = int(round(loop_idx_tr.get_value())) % len(loops)
            pts = [plane.c2p(loops[i](t).real, loops[i](t).imag)
                   for t in np.linspace(0, 2 * PI, 120)]
            m = VMobject(color=loop_colors[i], stroke_width=3)
            m.set_points_as_corners(pts + [pts[0]])
            return m

        self.add(always_redraw(current_loop_curve))

        def integral_value():
            i = int(round(loop_idx_tr.get_value())) % len(loops)
            # Numerical ∮ f(z) dz
            N = 200
            ts = np.linspace(0, 2 * PI, N + 1)
            total = 0 + 0j
            for k in range(N):
                z0 = loops[i](ts[k])
                z1 = loops[i](ts[k + 1])
                total += f(z0) * (z1 - z0)
            return total

        def info():
            i = int(round(loop_idx_tr.get_value())) % len(loops)
            val = integral_value()
            return VGroup(
                MathTex(r"f(z) = z^2", color=YELLOW, font_size=22),
                Tex(rf"loop: {loop_names[i]}",
                     color=loop_colors[i], font_size=22),
                MathTex(rf"\oint f\,dz \approx {val.real:+.3f} {'+' if val.imag >= 0 else '-'} {abs(val.imag):.3f}i",
                         color=GREEN, font_size=20),
                Tex(r"all loops give 0 $\Rightarrow z^2$ holomorphic",
                     color=GREEN, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for i in range(1, len(loops)):
            self.play(loop_idx_tr.animate.set_value(i),
                       run_time=1.3, rate_func=smooth)
            self.wait(0.8)
        self.wait(0.4)
