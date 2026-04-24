from manim import *
import numpy as np


class MVTForIntegralsExample(Scene):
    """
    Mean value theorem for integrals: if f continuous on [a, b], ∃ c ∈
    (a, b) with f(c) = (1/(b-a)) ∫_a^b f(x) dx — average value.

    SINGLE_FOCUS:
      Axes with f(x) = 1 + x + sin(x)² on [0, 3]; ValueTracker c_tr
      sweeps c; always_redraw f(c) rectangle vs actual ∫f dx area.
      Match when f(c) = average = (1/3) ∫_0^3 f dx.
    """

    def construct(self):
        title = Tex(r"MVT for integrals: $\exists\,c$ with $f(c) = \bar f$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        def f(x):
            return 1 + x + np.sin(x) ** 2

        a, b = 0.0, 3.0
        # Exact average via fine numerical integration
        xs_fine = np.linspace(a, b, 5000)
        avg = float(np.trapz(f(xs_fine), xs_fine)) / (b - a)

        ax = Axes(x_range=[0, 3, 0.5], y_range=[0, 5.5, 1],
                   x_length=8, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-1, -0.3, 0])
        self.play(Create(ax))

        curve = ax.plot(f, x_range=[a, b], color=BLUE, stroke_width=3)
        self.play(Create(curve))

        # Shade area under curve
        area_pts = [ax.c2p(a, 0)]
        for x in np.linspace(a, b, 60):
            area_pts.append(ax.c2p(x, f(x)))
        area_pts.append(ax.c2p(b, 0))
        area_poly = Polygon(*area_pts, color=BLUE, fill_opacity=0.25,
                              stroke_width=0)
        self.play(Create(area_poly))

        # Average rectangle (static reference)
        avg_rect = Rectangle(
            width=ax.c2p(b, 0)[0] - ax.c2p(a, 0)[0],
            height=ax.c2p(0, avg)[1] - ax.c2p(0, 0)[1],
            color=GREEN, fill_opacity=0.3, stroke_width=2
        ).move_to([(ax.c2p(a, 0)[0] + ax.c2p(b, 0)[0]) / 2,
                     (ax.c2p(0, 0)[1] + ax.c2p(0, avg)[1]) / 2, 0])
        avg_line = DashedLine(ax.c2p(a, avg), ax.c2p(b, avg),
                                color=GREEN, stroke_width=3)
        avg_lbl = MathTex(rf"\bar f = {avg:.3f}",
                            color=GREEN, font_size=20
                            ).next_to(avg_line.get_end(), RIGHT, buff=0.1)
        self.play(Create(avg_rect), Create(avg_line), Write(avg_lbl))

        c_tr = ValueTracker(0.5)

        def c_cursor():
            c = c_tr.get_value()
            return VGroup(
                DashedLine(ax.c2p(c, 0), ax.c2p(c, f(c)),
                            color=RED, stroke_width=2),
                Dot(ax.c2p(c, f(c)), color=RED, radius=0.12),
            )

        def c_marker():
            c = c_tr.get_value()
            return MathTex(r"c", color=RED, font_size=22
                             ).next_to(ax.c2p(c, 0), DOWN, buff=0.1)

        self.add(always_redraw(c_cursor), always_redraw(c_marker))

        def info():
            c = c_tr.get_value()
            fc = f(c)
            diff = abs(fc - avg)
            match = diff < 0.03
            return VGroup(
                MathTex(rf"c = {c:.3f}", color=RED, font_size=22),
                MathTex(rf"f(c) = {fc:.4f}", color=RED, font_size=22),
                MathTex(rf"\bar f = {avg:.4f}",
                         color=GREEN, font_size=22),
                MathTex(rf"|f(c) - \bar f| = {diff:.4f}",
                         color=YELLOW if not match else GREEN, font_size=20),
                Tex(r"match!" if match else r"keep sweeping",
                     color=GREEN if match else GREY_B, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.3).shift(DOWN * 1.2)

        self.add(always_redraw(info))

        self.play(c_tr.animate.set_value(2.8),
                   run_time=7, rate_func=linear)
        self.wait(0.4)
