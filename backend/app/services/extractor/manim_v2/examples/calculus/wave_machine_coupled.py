from manim import *
import numpy as np


class WaveMachineCoupledExample(Scene):
    """
    Coupled pendulum wave machine (from _2023/optics_puzzles/
    wave_machine): N pendulums of increasing length hanging in a row;
    as they swing, they produce a traveling "wave" of phase advance.

    SINGLE_FOCUS:
      20 pendulums side by side; each has angle θ_i(t) = A·cos(ω_i·t)
      with ω_i increasing linearly. ValueTracker t_tr advances time;
      always_redraw pendulum arms + bobs with colors shifting by
      phase. A snaking shape emerges.
    """

    def construct(self):
        title = Tex(r"Coupled pendulum wave machine",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        N = 20
        x_lo, x_hi = -5.5, 5.5
        bar_y = 2.8
        # Each pendulum length differs
        L_min = 1.4
        L_max = 3.5

        lengths = np.linspace(L_min, L_max, N)
        omegas = np.sqrt(9.81 / lengths) * 0.5  # slow down

        # Horizontal support bar
        support = Line([x_lo - 0.2, bar_y, 0], [x_hi + 0.2, bar_y, 0],
                         color=GREY_B, stroke_width=4)
        self.play(Create(support))

        hinge_xs = np.linspace(x_lo, x_hi, N)

        t_tr = ValueTracker(0.0)
        A = 0.4  # amplitude in radians

        def pendulums():
            t = t_tr.get_value()
            grp = VGroup()
            for i in range(N):
                theta = A * np.cos(omegas[i] * t)
                hinge = np.array([hinge_xs[i], bar_y, 0])
                bob = hinge + lengths[i] * np.array([np.sin(theta),
                                                         -np.cos(theta), 0])
                color = interpolate_color(BLUE, YELLOW, (i / (N - 1)))
                grp.add(Line(hinge, bob, color=GREY_B, stroke_width=2))
                grp.add(Dot(bob, color=color, radius=0.09))
            return grp

        self.add(always_redraw(pendulums))

        def info():
            t = t_tr.get_value()
            return VGroup(
                MathTex(rf"t = {t:.2f}\,s", color=YELLOW, font_size=22),
                MathTex(rf"N = {N}", color=WHITE, font_size=22),
                MathTex(r"\omega_i = \sqrt{g/L_i}",
                         color=GREEN, font_size=22),
                MathTex(rf"L \in [{L_min}, {L_max}]\,m",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        self.play(t_tr.animate.set_value(30),
                   run_time=10, rate_func=linear)
        self.wait(0.4)
