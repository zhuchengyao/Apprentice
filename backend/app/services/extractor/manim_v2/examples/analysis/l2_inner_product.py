from manim import *
import numpy as np


class L2InnerProductExample(Scene):
    """
    L²([0, π]) inner product ⟨f, g⟩ = ∫_0^π f(x) g(x) dx. Sines form
    orthogonal system: ⟨sin nx, sin mx⟩ = (π/2) δ_nm.

    TWO_COLUMN:
      LEFT  — two sine curves sin(nx) and sin(mx); ValueTracker n_tr
              and m_tr vary indices.
      RIGHT — product curve sin(nx) sin(mx); shaded area = integral.
    """

    def construct(self):
        title = Tex(r"Sine orthogonality: $\langle \sin nx, \sin mx \rangle = \tfrac{\pi}{2} \delta_{nm}$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ax_L = Axes(x_range=[0, PI, PI / 4], y_range=[-1.2, 1.2, 0.5],
                     x_length=6, y_length=2.8, tips=False,
                     axis_config={"font_size": 12}
                     ).move_to([-3.3, 1.5, 0])
        ax_R = Axes(x_range=[0, PI, PI / 4], y_range=[-1.2, 1.2, 0.5],
                     x_length=6, y_length=2.8, tips=False,
                     axis_config={"font_size": 12}
                     ).move_to([-3.3, -1.5, 0])
        self.play(Create(ax_L), Create(ax_R))

        n_tr = ValueTracker(2)
        m_tr = ValueTracker(3)

        def sin_nx():
            n = int(round(n_tr.get_value()))
            return ax_L.plot(lambda x: np.sin(n * x),
                              x_range=[0, PI, 0.01],
                              color=BLUE, stroke_width=3)

        def sin_mx():
            m = int(round(m_tr.get_value()))
            return ax_L.plot(lambda x: np.sin(m * x),
                              x_range=[0, PI, 0.01],
                              color=ORANGE, stroke_width=3)

        def product_curve():
            n = int(round(n_tr.get_value()))
            m = int(round(m_tr.get_value()))
            return ax_R.plot(lambda x: np.sin(n * x) * np.sin(m * x),
                              x_range=[0, PI, 0.01],
                              color=GREEN, stroke_width=3)

        def product_shade():
            n = int(round(n_tr.get_value()))
            m = int(round(m_tr.get_value()))
            pts = [ax_R.c2p(0, 0)]
            for x in np.linspace(0, PI, 80):
                pts.append(ax_R.c2p(x, np.sin(n * x) * np.sin(m * x)))
            pts.append(ax_R.c2p(PI, 0))
            return Polygon(*pts, color=GREEN, fill_opacity=0.35,
                             stroke_width=0)

        self.add(always_redraw(sin_nx), always_redraw(sin_mx),
                  always_redraw(product_shade), always_redraw(product_curve))

        def info():
            n = int(round(n_tr.get_value()))
            m = int(round(m_tr.get_value()))
            # Integral: analytically π/2 if n == m, else 0
            val = PI / 2 if n == m else 0
            return VGroup(
                MathTex(rf"n = {n},\ m = {m}",
                         color=YELLOW, font_size=22),
                MathTex(rf"\langle \sin nx, \sin mx \rangle = {val:.4f}",
                         color=GREEN, font_size=22),
                Tex(r"$\pi/2$ iff $n = m$, else $0$",
                     color=GREEN if n == m else RED, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(RIGHT, buff=0.3).shift(UP * 0.5)

        self.add(always_redraw(info))

        for (nv, mv) in [(2, 3), (3, 3), (4, 5), (5, 5), (2, 3)]:
            self.play(n_tr.animate.set_value(nv),
                       m_tr.animate.set_value(mv),
                       run_time=1.4, rate_func=smooth)
            self.wait(0.7)
        self.wait(0.4)
