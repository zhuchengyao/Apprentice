from manim import *
import numpy as np


class ConvolutionBoxExample(Scene):
    """
    Box-with-box convolution: sliding one rectangular pulse past
    another produces a triangle.

    TWO_COLUMN:
      LEFT  — axes with f (BLUE box on [-1, 1]) and g_τ = g(τ - t)
              (ORANGE reflected sliding box); always_redraw shades
              the GREEN overlap region.
      RIGHT — axes with the output (f * g)(τ) = area of overlap;
              always_redraw builds the result as ValueTracker τ_tr
              sweeps -2 → 2. Result is a triangle of base 4, peak 2.
    """

    def construct(self):
        title = Tex(r"Convolution: $(f * g)(\tau) = \int f(t)\,g(\tau - t)\,dt$ (box $\ast$ box $=$ triangle)",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ax_in = Axes(x_range=[-2.5, 2.5, 1], y_range=[0, 1.3, 0.5],
                      x_length=6.4, y_length=2.6, tips=False,
                      axis_config={"font_size": 14, "include_numbers": True}
                      ).move_to([-3.2, 1.4, 0])
        ax_out = Axes(x_range=[-2.5, 2.5, 1], y_range=[0, 2.3, 1],
                       x_length=6.4, y_length=2.6, tips=False,
                       axis_config={"font_size": 14, "include_numbers": True}
                       ).move_to([-3.2, -1.8, 0])
        self.play(Create(ax_in), Create(ax_out))

        # f: box on [-1, 1] with height 1 (BLUE, static)
        f_box = Polygon(ax_in.c2p(-1, 0), ax_in.c2p(-1, 1),
                         ax_in.c2p(1, 1), ax_in.c2p(1, 0),
                         color=BLUE, fill_opacity=0.35)
        self.play(Create(f_box))

        tau_tr = ValueTracker(-2.0)

        def g_box():
            tau = tau_tr.get_value()
            return Polygon(ax_in.c2p(tau - 1, 0), ax_in.c2p(tau - 1, 1),
                            ax_in.c2p(tau + 1, 1), ax_in.c2p(tau + 1, 0),
                            color=ORANGE, fill_opacity=0.35)

        def overlap():
            tau = tau_tr.get_value()
            left = max(-1, tau - 1)
            right = min(1, tau + 1)
            if right <= left:
                return VGroup()
            return Polygon(ax_in.c2p(left, 0), ax_in.c2p(left, 1),
                            ax_in.c2p(right, 1), ax_in.c2p(right, 0),
                            color=GREEN, fill_opacity=0.55,
                            stroke_width=2)

        def out_trace():
            tau_cur = tau_tr.get_value()
            pts = []
            for t in np.linspace(-2.0, tau_cur, 80):
                left = max(-1, t - 1)
                right = min(1, t + 1)
                width = max(0, right - left)
                pts.append(ax_out.c2p(t, width))
            v = VMobject(color=GREEN, stroke_width=4)
            if len(pts) >= 2:
                v.set_points_as_corners(pts)
            return v

        def out_dot():
            tau = tau_tr.get_value()
            left = max(-1, tau - 1)
            right = min(1, tau + 1)
            width = max(0, right - left)
            return Dot(ax_out.c2p(tau, width), color=YELLOW, radius=0.09)

        self.add(always_redraw(g_box), always_redraw(overlap),
                  always_redraw(out_trace), always_redraw(out_dot))

        def info():
            tau = tau_tr.get_value()
            left = max(-1, tau - 1)
            right = min(1, tau + 1)
            width = max(0, right - left)
            return VGroup(
                MathTex(rf"\tau = {tau:+.2f}", color=WHITE, font_size=22),
                MathTex(rf"(f * g)(\tau) = {width:.3f}",
                         color=GREEN, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.8, 0.5, 0])

        self.add(always_redraw(info))

        self.play(tau_tr.animate.set_value(2.0),
                   run_time=8, rate_func=linear)
        self.wait(0.5)
