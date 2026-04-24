from manim import *
import numpy as np


class DiscreteFourierTransformExample(Scene):
    """
    DFT from _2020/18S191/dft: an N-point time-domain signal decomposes
    into N complex frequency bins. Here N = 32 samples of a 3-sinusoid
    mixture; magnitude spectrum reveals the three peaks.

    TWO_COLUMN:
      LEFT  — time-domain stem plot of x[n] via always_redraw as
              ValueTracker n_samples_tr grows N from 4 → 32.
      RIGHT — magnitude spectrum |X[k]| computed each frame.
    """

    def construct(self):
        title = Tex(r"DFT: $X[k] = \sum_{n=0}^{N-1} x[n]\,e^{-2\pi i k n/N}$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        N = 32

        def x_signal(n):
            return (np.cos(2 * PI * 2 * n / N)
                    + 0.6 * np.cos(2 * PI * 5 * n / N)
                    + 0.4 * np.cos(2 * PI * 9 * n / N))

        # Precompute full signal + full DFT
        full_x = np.array([x_signal(n) for n in range(N)])
        full_X = np.fft.fft(full_x)

        ax_t = Axes(x_range=[0, N, 4], y_range=[-2.2, 2.2, 1],
                     x_length=6.5, y_length=3.0, tips=False,
                     axis_config={"font_size": 14, "include_numbers": True}
                     ).move_to([-3.3, 1.3, 0])
        ax_f = Axes(x_range=[0, N // 2 + 1, 4], y_range=[0, 18, 4],
                     x_length=6.5, y_length=3.0, tips=False,
                     axis_config={"font_size": 14, "include_numbers": True}
                     ).move_to([-3.3, -1.8, 0])
        t_lbl = MathTex(r"n", font_size=18).next_to(ax_t, DOWN, buff=0.08)
        y_lbl = MathTex(r"x[n]", font_size=18).next_to(ax_t, LEFT, buff=0.08)
        k_lbl = MathTex(r"k", font_size=18).next_to(ax_f, DOWN, buff=0.08)
        m_lbl = MathTex(r"|X[k]|", font_size=18).next_to(ax_f, LEFT, buff=0.08)
        self.play(Create(ax_t), Create(ax_f),
                   Write(t_lbl), Write(y_lbl),
                   Write(k_lbl), Write(m_lbl))

        n_samples_tr = ValueTracker(4)

        def stems():
            N_cur = int(round(n_samples_tr.get_value()))
            N_cur = max(1, min(N_cur, N))
            grp = VGroup()
            for i in range(N_cur):
                grp.add(Line(ax_t.c2p(i, 0),
                               ax_t.c2p(i, full_x[i]),
                               color=BLUE, stroke_width=2))
                grp.add(Dot(ax_t.c2p(i, full_x[i]),
                              color=BLUE, radius=0.05))
            return grp

        def spectrum():
            N_cur = int(round(n_samples_tr.get_value()))
            N_cur = max(1, min(N_cur, N))
            # DFT of first N_cur samples only (zero-padded to N)
            x_pad = np.zeros(N)
            x_pad[:N_cur] = full_x[:N_cur]
            X = np.fft.fft(x_pad)
            grp = VGroup()
            for k in range(N // 2 + 1):
                mag = abs(X[k])
                h_scene = ax_f.c2p(0, mag)[1] - ax_f.c2p(0, 0)[1]
                if h_scene < 0.005:
                    continue
                bar = Rectangle(width=0.25, height=h_scene,
                                 color=RED, fill_opacity=0.7,
                                 stroke_width=0.5)
                bar.move_to([ax_f.c2p(k, 0)[0],
                             ax_f.c2p(0, 0)[1] + h_scene / 2, 0])
                grp.add(bar)
            return grp

        self.add(always_redraw(stems), always_redraw(spectrum))

        def info():
            N_cur = int(round(n_samples_tr.get_value()))
            return VGroup(
                MathTex(rf"N = {N_cur}", color=YELLOW, font_size=24),
                Tex(r"peaks at $k = 2, 5, 9$",
                     color=RED, font_size=20),
                Tex(r"amplitudes $1, 0.6, 0.4$",
                     color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.3).shift(UP * 0.5)

        self.add(always_redraw(info))

        self.play(n_samples_tr.animate.set_value(N),
                   run_time=7, rate_func=linear)
        self.wait(0.5)
