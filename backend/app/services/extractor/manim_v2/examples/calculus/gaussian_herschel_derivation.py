from manim import *
import numpy as np


class GaussianHerschelDerivationExample(Scene):
    """
    Herschel's proof that radial symmetry + independence forces the
    Gaussian (from _2023/gauss_int/herschel):
        f(x) f(y) = g(r²) where r² = x² + y² ⇒ f must be exp(-α x²).

    SINGLE_FOCUS:
      Scatter of 2D dots sampled from an isotropic distribution;
      ValueTracker alpha_tr sweeps the exponent α of exp(-α(x²+y²));
      always_redraw radial contour rings + 2-term product curves
      on marginal axes. Demonstrates radial = product of 1-D Gaussians.
    """

    def construct(self):
        title = Tex(r"Herschel: radial + independent $\Rightarrow$ Gaussian",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-3, 3, 1], y_range=[-2.5, 2.5, 1],
                             x_length=6, y_length=5,
                             background_line_style={"stroke_opacity": 0.25}
                             ).move_to([-3, -0.3, 0])
        self.play(Create(plane))

        alpha_tr = ValueTracker(0.5)

        def rings():
            alpha = alpha_tr.get_value()
            grp = VGroup()
            for level in [0.8, 0.5, 0.25, 0.1]:
                # exp(-α r²) = level ⇒ r = √(-log(level)/α)
                r = np.sqrt(-np.log(level) / alpha)
                if r > 3:
                    continue
                pts = []
                for ang in np.linspace(0, 2 * PI, 80):
                    pts.append(plane.c2p(r * np.cos(ang),
                                           r * np.sin(ang)))
                m = VMobject(color=BLUE, stroke_width=2,
                               stroke_opacity=0.6)
                m.set_points_as_corners(pts + [pts[0]])
                grp.add(m)
            return grp

        self.add(always_redraw(rings))

        # Marginal axes on right
        ax_marg = Axes(x_range=[-3, 3, 1], y_range=[0, 1.2, 0.25],
                        x_length=5, y_length=2.5, tips=False,
                        axis_config={"font_size": 14}
                        ).move_to([3, 0.8, 0])
        lbl = MathTex(r"f(x) = e^{-\alpha x^2}", color=ORANGE, font_size=22
                        ).next_to(ax_marg, UP, buff=0.1)
        self.play(Create(ax_marg), Write(lbl))

        def marg_curve():
            a = alpha_tr.get_value()
            return ax_marg.plot(lambda x: np.exp(-a * x * x),
                                  x_range=[-3, 3, 0.02],
                                  color=ORANGE, stroke_width=3)

        self.add(always_redraw(marg_curve))

        def info():
            a = alpha_tr.get_value()
            return VGroup(
                MathTex(rf"\alpha = {a:.2f}", color=YELLOW, font_size=22),
                MathTex(r"f(x)f(y) = e^{-\alpha(x^2+y^2)}",
                         color=ORANGE, font_size=20),
                MathTex(r"= g(r^2)\text{ radial}",
                         color=BLUE, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.0, -2.2, 0])

        self.add(always_redraw(info))

        for av in [0.2, 0.8, 1.5, 0.5]:
            self.play(alpha_tr.animate.set_value(av),
                       run_time=1.6, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.4)
