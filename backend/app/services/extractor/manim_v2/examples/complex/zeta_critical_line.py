from manim import *
import numpy as np


class ZetaCriticalLineExample(Scene):
    """
    Plot ζ_N(s) = Σ_{k=1}^N k^(-s) for s = 1/2 + it on the complex plane,
    sweeping t.

    TWO_COLUMN:
      LEFT  — ComplexPlane with always_redraw partial-curve trace of
              ζ_N(1/2 + it) for t ∈ [0.1, T_now] and a moving dot at
              the head. ValueTracker T_now sweeps from 0.1 to 40.
      RIGHT — live readouts t (=T_now), |ζ_N|, arg(ζ_N), and the
              first nontrivial zero t ≈ 14.135 highlighted on a
              mini-axes |ζ_N(1/2+it)| vs t plot below — a tracking
              cursor follows.
    """

    def construct(self):
        title = Tex(r"$\zeta_N(s)$ on the critical line $s = \tfrac{1}{2} + it$ ($N = 80$)",
                    font_size=26).to_edge(UP, buff=0.4)
        self.play(Write(title))

        N = 80

        plane = ComplexPlane(
            x_range=[-2, 2.5, 1], y_range=[-2.5, 2.5, 1],
            x_length=5.6, y_length=5.6,
            background_line_style={"stroke_opacity": 0.3},
        ).move_to([-3.0, -0.4, 0])
        self.play(Create(plane))

        # Precompute partial zeta values along t
        ts = np.linspace(0.1, 40.0, 400)

        def zeta_N(t):
            return sum(1 / (k ** complex(0.5, t)) for k in range(1, N + 1))

        z_vals = [zeta_N(t) for t in ts]
        z_pts = [plane.n2p(z) for z in z_vals]

        T_tr = ValueTracker(0.1)

        def trace():
            T = T_tr.get_value()
            n_max = int((T - 0.1) / (40.0 - 0.1) * (len(ts) - 1))
            n_max = max(1, min(n_max, len(ts) - 1))
            curve = VMobject(color=YELLOW, stroke_width=2.5)
            curve.set_points_smoothly(z_pts[: n_max + 1])
            return curve

        def head_dot():
            T = T_tr.get_value()
            z = zeta_N(T)
            return Dot(plane.n2p(z), color=YELLOW, radius=0.10)

        # Mark origin with red dot to indicate "zero would land here"
        origin_dot = Dot(plane.n2p(0), color=RED, radius=0.06)
        self.add(origin_dot)
        self.add(always_redraw(trace), always_redraw(head_dot))

        # RIGHT COLUMN: |ζ_N| vs t plot + readouts
        rcol_x = +3.6

        def info_panel():
            T = T_tr.get_value()
            z = zeta_N(T)
            return VGroup(
                MathTex(rf"t = {T:.2f}", color=WHITE, font_size=24),
                MathTex(rf"|\zeta_N(\tfrac{{1}}{{2}}+it)| = {abs(z):.3f}",
                        color=YELLOW, font_size=22),
                MathTex(rf"\arg = {np.degrees(np.angle(z)):+.0f}^\circ",
                        color=YELLOW, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([rcol_x, +2.4, 0])

        self.add(always_redraw(info_panel))

        # Mini |ζ_N| vs t plot
        mini_axes = Axes(
            x_range=[0, 40, 10], y_range=[0, 3, 1],
            x_length=3.0, y_length=1.8,
            axis_config={"include_tip": False, "include_numbers": True, "font_size": 14},
        ).move_to([rcol_x, 0.2, 0])
        mag_curve = mini_axes.plot(
            lambda t: abs(zeta_N(t)),
            x_range=[0.5, 39.9, 0.4],
            color=YELLOW,
        )
        # Mark first nontrivial zero at t ≈ 14.135
        zero_marker = DashedLine(mini_axes.c2p(14.135, 0),
                                  mini_axes.c2p(14.135, 3),
                                  color=RED, stroke_width=2)
        zero_lbl = Tex(r"$t \approx 14.135$", color=RED,
                       font_size=18).next_to(mini_axes.c2p(14.135, 3), UP, buff=0.1)
        self.play(Create(mini_axes), Create(mag_curve),
                  Create(zero_marker), Write(zero_lbl))

        def cursor():
            T = T_tr.get_value()
            return Dot(mini_axes.c2p(T, abs(zeta_N(T))),
                       color=YELLOW, radius=0.07)

        self.add(always_redraw(cursor))

        rh_lbl = Tex(r"Riemann hypothesis: all $\zeta(s)=0$ have $\mathrm{Re}(s) = \tfrac{1}{2}$",
                     color=GREEN, font_size=20).move_to([rcol_x, -2.6, 0])
        self.play(Write(rh_lbl))

        self.play(T_tr.animate.set_value(40.0), run_time=10, rate_func=linear)
        self.wait(0.8)
