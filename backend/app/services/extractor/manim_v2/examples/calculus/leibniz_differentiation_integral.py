from manim import *
import numpy as np


class LeibnizDifferentiationIntegralExample(Scene):
    """
    Leibniz rule for differentiating under the integral sign:
    d/dt [∫_0^t f(x, t) dx] = f(t, t) + ∫_0^t ∂f/∂t dx.

    TWO_COLUMN:
      LEFT  — axes of integrand f(x, t) = x² t at fixed t; shaded
              integral region; ValueTracker t_tr advances.
      RIGHT — I(t) = ∫_0^t x² t dx = t⁴/3; dI/dt shown.
    """

    def construct(self):
        title = Tex(r"Leibniz rule: $\tfrac{d}{dt} \int_0^t f(x, t)\,dx = f(t, t) + \int_0^t \partial_t f\,dx$",
                    font_size=20).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ax_L = Axes(x_range=[0, 2.5, 0.5], y_range=[0, 12, 2],
                     x_length=5, y_length=3.5, tips=False,
                     axis_config={"font_size": 12, "include_numbers": True}
                     ).move_to([-3.3, -0.3, 0])
        self.play(Create(ax_L))

        t_tr = ValueTracker(0.8)

        def integrand_curve():
            t = t_tr.get_value()
            return ax_L.plot(lambda x: x ** 2 * t,
                               x_range=[0, 2.5, 0.02],
                               color=BLUE, stroke_width=3)

        def integrand_shade():
            t = t_tr.get_value()
            pts = [ax_L.c2p(0, 0)]
            for x in np.linspace(0, t, 50):
                pts.append(ax_L.c2p(x, x ** 2 * t))
            pts.append(ax_L.c2p(t, 0))
            return Polygon(*pts, color=BLUE, fill_opacity=0.35,
                             stroke_width=0)

        def t_vertical():
            t = t_tr.get_value()
            return DashedLine(ax_L.c2p(t, 0), ax_L.c2p(t, 12),
                                color=YELLOW, stroke_width=2)

        self.add(always_redraw(integrand_shade),
                  always_redraw(integrand_curve),
                  always_redraw(t_vertical))

        # RIGHT: I(t) = t^4 / 3
        ax_R = Axes(x_range=[0, 2.5, 0.5], y_range=[0, 14, 3],
                     x_length=5, y_length=3.5, tips=False,
                     axis_config={"font_size": 12, "include_numbers": True}
                     ).move_to([3.3, -0.3, 0])
        self.play(Create(ax_R))

        I_curve = ax_R.plot(lambda t: t ** 4 / 3,
                              x_range=[0, 2.5, 0.01],
                              color=GREEN, stroke_width=3)
        I_lbl = MathTex(r"I(t) = t^4 / 3",
                          color=GREEN, font_size=20
                          ).next_to(ax_R.c2p(2.5, 5.2), UR, buff=0.1)
        self.play(Create(I_curve), Write(I_lbl))

        def I_rider():
            t = t_tr.get_value()
            return Dot(ax_R.c2p(t, t ** 4 / 3),
                        color=YELLOW, radius=0.1)

        self.add(always_redraw(I_rider))

        def info():
            t = t_tr.get_value()
            I = t ** 4 / 3
            dI_dt = 4 * t ** 3 / 3
            f_tt = t ** 2 * t  # t³
            partial_integral = t ** 3 / 3  # ∫_0^t x² dx = t³/3
            return VGroup(
                MathTex(rf"t = {t:.2f}", color=YELLOW, font_size=20),
                MathTex(rf"I(t) = {I:.3f}",
                         color=GREEN, font_size=20),
                MathTex(rf"f(t, t) = t^3 = {f_tt:.3f}",
                         color=BLUE, font_size=18),
                MathTex(rf"\int_0^t \partial_t f = \int_0^t x^2 = {partial_integral:.3f}",
                         color=ORANGE, font_size=17),
                MathTex(rf"\text{{sum}} = {f_tt + partial_integral:.3f} = dI/dt",
                         color=YELLOW, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        self.play(t_tr.animate.set_value(2.3),
                   run_time=6, rate_func=linear)
        self.wait(0.4)
