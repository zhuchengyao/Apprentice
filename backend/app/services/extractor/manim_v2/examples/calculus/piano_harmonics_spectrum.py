from manim import *
import numpy as np


class PianoHarmonicsSpectrumExample(Scene):
    """
    A piano note decomposed into harmonics (from _2022/piano/
    fourier_animations): the perceived pitch at f_0 is actually a
    sum of harmonics at f_0, 2f_0, 3f_0 with decreasing amplitudes.

    TWO_COLUMN:
      LEFT  — time-domain sum y(t) = Σ A_k cos(2π k f_0 t) for
              k=1..5 with custom A_k; ValueTracker t_tr advances.
      RIGHT — spectrum plot: 5 stems at multiples of f_0 with
              heights A_k; static.
    """

    def construct(self):
        title = Tex(r"Piano note: harmonic spectrum and time signal",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        f_0 = 1.0  # base frequency (Hz, for visualization)
        amps = [1.0, 0.55, 0.35, 0.22, 0.12]

        ax_t = Axes(x_range=[0, 4, 1], y_range=[-2.5, 2.5, 1],
                     x_length=6.5, y_length=4, tips=False,
                     axis_config={"font_size": 14, "include_numbers": True}
                     ).move_to([-3.3, -0.3, 0])
        self.play(Create(ax_t))

        def y_full(t_val):
            return sum(A * np.cos(2 * PI * (k + 1) * f_0 * t_val)
                        for k, A in enumerate(amps))

        # Static full waveform
        full_curve = ax_t.plot(lambda t: y_full(t),
                                 x_range=[0, 4, 0.005],
                                 color=BLUE, stroke_width=3)
        self.play(Create(full_curve))

        t_tr = ValueTracker(0.0)

        def rider():
            t = t_tr.get_value()
            return Dot(ax_t.c2p(t, y_full(t)),
                        color=YELLOW, radius=0.1)

        self.add(always_redraw(rider))

        # Spectrum on right
        ax_spec = Axes(x_range=[0, 6, 1], y_range=[0, 1.2, 0.25],
                        x_length=5, y_length=3, tips=False,
                        axis_config={"font_size": 14, "include_numbers": True}
                        ).move_to([3.3, 1.4, 0])
        xl = MathTex(r"k f_0", font_size=18).next_to(ax_spec, DOWN, buff=0.1)
        yl = MathTex(r"A_k", font_size=18).next_to(ax_spec, LEFT, buff=0.1)
        self.play(Create(ax_spec), Write(xl), Write(yl))

        stems = VGroup()
        for k, A in enumerate(amps):
            stems.add(Line(ax_spec.c2p(k + 1, 0),
                             ax_spec.c2p(k + 1, A),
                             color=RED, stroke_width=4))
            stems.add(Dot(ax_spec.c2p(k + 1, A), color=RED, radius=0.08))
            stems.add(MathTex(rf"{A}", font_size=14, color=WHITE
                                ).next_to(ax_spec.c2p(k + 1, A),
                                            UP, buff=0.08))
        self.play(Create(stems))

        # Legend
        info = VGroup(
            Tex(r"time: $\sum_k A_k \cos(2\pi k f_0 t)$",
                 color=BLUE, font_size=22),
            Tex(r"spectrum: $A_k$ at $k f_0$",
                 color=RED, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.3, -1.8, 0])
        self.play(Write(info))

        self.play(t_tr.animate.set_value(4),
                   run_time=6, rate_func=linear)
        self.wait(0.4)
