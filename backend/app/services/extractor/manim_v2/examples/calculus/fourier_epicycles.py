from manim import *
import numpy as np


class FourierEpicyclesExample(Scene):
    """
    Fourier-series drawing as epicycles (from _2019/diffyq/part4/
    fourier_series_scenes): a target periodic curve f(t) is traced
    by a chain of N rotating vectors, each at frequency n, whose
    sum equals the partial Fourier sum.

    SINGLE_FOCUS:
      N = 12 epicycles drawing a square wave (odd-harmonic Fourier
      series). ValueTracker t_tr advances parameter; always_redraw
      chain of rotating vectors + persistent trail.
    """

    def construct(self):
        title = Tex(r"Fourier series = chain of rotating vectors",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        N = 12
        # Square-wave Fourier coefficients:
        #   f(t) = (4/π) Σ sin((2k-1)t)/(2k-1)
        # As complex exponentials e^(i(2k-1)t), coefficient = 2/(iπ(2k-1))
        coeffs = []
        for k in range(1, N + 1):
            if k % 2 == 1:
                amp = 4 / (PI * k) / 2  # halved for cleaner look
                coeffs.append((k, amp))
            # even k: skip (square wave has only odd harmonics)

        center = np.array([-2.5, -0.4, 0])
        t_tr = ValueTracker(0.0)

        def chain_vectors():
            t = t_tr.get_value()
            pos = center.copy()
            grp = VGroup()
            for (k, amp) in coeffs:
                angle = k * t
                tip = pos + amp * np.array([np.cos(angle),
                                                 np.sin(angle), 0])
                # Circle of radius amp at pos
                grp.add(Circle(radius=amp, color=GREY_B,
                                 stroke_width=1.2, stroke_opacity=0.5
                                 ).move_to(pos))
                grp.add(Arrow(pos, tip, color=YELLOW, buff=0,
                                stroke_width=2,
                                max_tip_length_to_length_ratio=0.12))
                pos = tip
            # Output dot
            grp.add(Dot(pos, color=RED, radius=0.1))
            return grp

        # Trail (precompute for the tip)
        trail_points = []

        def tip_pos(t):
            pos = center.copy()
            for (k, amp) in coeffs:
                angle = k * t
                pos = pos + amp * np.array([np.cos(angle),
                                                np.sin(angle), 0])
            return pos

        def trail():
            t = t_tr.get_value()
            pts = []
            N_samples = max(20, int(200 * t / (2 * PI)))
            for ti in np.linspace(0, t, N_samples):
                pts.append(tip_pos(ti))
            if len(pts) < 2:
                return VMobject()
            m = VMobject(color=RED, stroke_width=2.5)
            m.set_points_as_corners(pts)
            return m

        self.add(always_redraw(trail), always_redraw(chain_vectors))

        # Right-side reference: the target function
        ax = Axes(x_range=[0, 2 * PI + 0.1, PI / 2],
                   y_range=[-1.5, 1.5, 0.5],
                   x_length=5, y_length=3.5, tips=False,
                   axis_config={"font_size": 14}).move_to([3.3, 0.0, 0])

        target = ax.plot(
            lambda t: sum(4 / (PI * k) / 2 * np.sin(k * t)
                          for k in range(1, N + 1, 2)),
            x_range=[0, 2 * PI], color=BLUE, stroke_width=2.5)
        ax_lbl = Tex(r"target $f(t)$", color=BLUE,
                      font_size=20).next_to(ax, UP, buff=0.1)
        self.play(Create(ax), Create(target), Write(ax_lbl))

        def rider():
            t = t_tr.get_value()
            # Plot partial-sum value at t
            val = sum(4 / (PI * k) / 2 * np.sin(k * t)
                      for k in range(1, N + 1, 2))
            if t > 2 * PI:
                t = t - 2 * PI * int(t / (2 * PI))
            return Dot(ax.c2p(t, val), color=RED, radius=0.1)

        self.add(always_redraw(rider))

        self.play(t_tr.animate.set_value(2 * PI),
                   run_time=10, rate_func=linear)
        self.wait(0.5)
