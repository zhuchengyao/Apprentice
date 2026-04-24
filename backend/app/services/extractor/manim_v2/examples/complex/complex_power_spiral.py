from manim import *
import numpy as np


class ComplexPowerSpiralExample(Scene):
    """
    Powers z^k of a complex number with |z| < 1 trace a logarithmic
    spiral inward to 0.

    TWO_COLUMN:
      LEFT  — ComplexPlane with the unit circle for reference, plus
              a moving dot at z^k (k continuous via ValueTracker).
              An always_redraw VMobject draws the partial spiral
              z^0, z^1, …, z^⌊k⌋ as a sequence of straight chords;
              the moving dot at z^k closes the curve smoothly.
      RIGHT — live readouts of z, |z|, arg(z), current k, |z^k|,
              arg(z^k), and the formula z^k = |z|^k · e^(ik·arg z).

    Two phases: |z|=0.88 (slow inward spiral) → switch to |z|=1.06
    (slow outward spiral); the trail forks visibly between the two
    regimes.
    """

    def construct(self):
        title = Tex(r"Powers $z^k$ trace a logarithmic spiral",
                    font_size=30).to_edge(UP, buff=0.4)
        self.play(Write(title))

        plane = ComplexPlane(
            x_range=[-2.4, 2.4, 1], y_range=[-2.4, 2.4, 1],
            x_length=5.6, y_length=5.6,
            background_line_style={"stroke_opacity": 0.3},
        ).move_to([-3.0, -0.4, 0])
        unit_circle = Circle(
            radius=plane.n2p(complex(1, 0))[0] - plane.n2p(0)[0],
            color=GREY_B, stroke_width=2, stroke_opacity=0.6,
        ).move_to(plane.n2p(0))
        self.play(Create(plane), Create(unit_circle))

        z_inner = 0.88 * np.exp(1j * PI / 8)  # inward
        z_outer = 1.06 * np.exp(1j * PI / 8)  # outward
        z_state = [z_inner]  # mutable list so closures can swap it

        k_tr = ValueTracker(0.0)

        def current_z():
            return z_state[0]

        def z_power(k):
            z = current_z()
            r = abs(z)
            ang = np.angle(z)
            return r ** k * np.exp(1j * ang * k)

        def spiral_path():
            k_max = k_tr.get_value()
            n_floor = int(np.floor(k_max))
            pts = [plane.n2p(z_power(k)) for k in range(n_floor + 1)]
            if k_max > n_floor:
                pts.append(plane.n2p(z_power(k_max)))
            path = VMobject(color=YELLOW, stroke_width=3)
            if len(pts) >= 2:
                path.set_points_as_corners(pts)
            else:
                path.set_points_as_corners([pts[0], pts[0]])
            return path

        def moving_dot():
            return Dot(plane.n2p(z_power(k_tr.get_value())),
                       color=YELLOW, radius=0.10)

        def integer_dots():
            k_max = k_tr.get_value()
            n_floor = int(np.floor(k_max))
            grp = VGroup()
            for k in range(n_floor + 1):
                grp.add(Dot(plane.n2p(z_power(k)),
                            color=ORANGE, radius=0.06))
            return grp

        self.add(always_redraw(spiral_path),
                 always_redraw(integer_dots),
                 always_redraw(moving_dot))

        # RIGHT COLUMN
        rcol_x = +3.4

        def info_panel():
            z = current_z()
            r = abs(z)
            ang = np.angle(z)
            k = k_tr.get_value()
            pk = z_power(k)
            return VGroup(
                MathTex(rf"|z| = {r:.3f}", color=YELLOW, font_size=22),
                MathTex(rf"\arg(z) = {np.degrees(ang):.0f}^\circ",
                        color=YELLOW, font_size=22),
                MathTex(rf"k = {k:.2f}", color=WHITE, font_size=24),
                MathTex(rf"|z^k| = |z|^k = {r ** k:.3f}",
                        color=BLUE, font_size=22),
                MathTex(rf"\arg(z^k) = k\,\arg(z) = {np.degrees(ang * k):.0f}^\circ",
                        color=BLUE, font_size=22),
                MathTex(rf"z^k = {pk.real:+.2f}{pk.imag:+.2f}\,i",
                        color=YELLOW, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([rcol_x, +0.6, 0])

        self.add(always_redraw(info_panel))

        # Phase 1: inward spiral
        self.play(k_tr.animate.set_value(25.0),
                  run_time=6, rate_func=linear)
        self.wait(0.6)

        # Reset for phase 2: outward
        z_state[0] = z_outer
        k_tr.set_value(0.0)
        # Trail will redraw automatically using new z

        outer_lbl = Tex(r"Now $|z| = 1.06 > 1$: spiral grows outward",
                        color=GREEN, font_size=22).move_to([rcol_x, -2.6, 0])
        self.play(Write(outer_lbl))
        self.play(k_tr.animate.set_value(20.0),
                  run_time=5, rate_func=linear)
        self.wait(1.0)
