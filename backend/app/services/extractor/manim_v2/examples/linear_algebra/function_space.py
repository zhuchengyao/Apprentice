from manim import *
import numpy as np


class FunctionSpaceExample(Scene):
    """
    Function space: polynomials up to degree 3 form a 4-dimensional
    vector space with basis {1, x, x², x³}. Any polynomial is a
    linear combination; coordinates are the coefficients.

    TWO_COLUMN:
      LEFT  — axes; always_redraw polynomial p(x) = a₀ + a₁x + a₂x²
              + a₃x³ with 4 coefficient ValueTrackers. 4 basis
              curves drawn faintly in background.
      RIGHT — coefficient vector (a₀, a₁, a₂, a₃) shown as 4 bars
              with ValueTrackers driving heights; live polynomial
              expression.
    """

    def construct(self):
        title = Tex(r"Function space: $\mathcal{P}_3 = \{\,a_0 + a_1 x + a_2 x^2 + a_3 x^3\,\}$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ax = Axes(x_range=[-2, 2, 1], y_range=[-3, 3, 1],
                   x_length=6.5, y_length=5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-2.8, -0.3, 0])
        self.play(Create(ax))

        # basis curves (faint)
        basis_colors = [BLUE, GREEN, RED, PURPLE]
        basis_fns = [lambda x: 1 + 0 * x,
                     lambda x: x,
                     lambda x: x ** 2 - 2,
                     lambda x: x ** 3 - 1]
        basis_curves = VGroup()
        for i, (f, c) in enumerate(zip(basis_fns, basis_colors)):
            bc = ax.plot(f, x_range=[-2, 2], color=c,
                           stroke_width=1.5, stroke_opacity=0.4)
            basis_curves.add(bc)
        self.play(Create(basis_curves))

        a0 = ValueTracker(0.0)
        a1 = ValueTracker(0.0)
        a2 = ValueTracker(0.0)
        a3 = ValueTracker(0.0)

        def poly(x):
            return (a0.get_value() + a1.get_value() * x
                    + a2.get_value() * x ** 2
                    + a3.get_value() * x ** 3)

        def p_curve():
            return ax.plot(poly, x_range=[-2, 2], color=YELLOW,
                            stroke_width=4)

        self.add(always_redraw(p_curve))

        # Right column: coefficient bars
        bars_base = np.array([3.5, -1.8, 0])
        bar_labels = [r"a_0", r"a_1", r"a_2", r"a_3"]
        bar_colors = basis_colors

        def bars():
            grp = VGroup()
            vals = [a0.get_value(), a1.get_value(),
                    a2.get_value(), a3.get_value()]
            for i, v in enumerate(vals):
                h = 0.7 * v
                bar = Rectangle(width=0.4, height=abs(h) + 0.001,
                                 color=bar_colors[i], fill_opacity=0.6,
                                 stroke_width=1.5)
                bar.move_to(bars_base + np.array([0.6 * i, h / 2, 0]))
                grp.add(bar)
                lbl = MathTex(bar_labels[i], font_size=22,
                                color=bar_colors[i]
                                ).move_to(bars_base
                                            + np.array([0.6 * i, -0.4, 0]))
                grp.add(lbl)
            return grp

        self.add(always_redraw(bars))

        def poly_expr():
            vals = [a0.get_value(), a1.get_value(),
                    a2.get_value(), a3.get_value()]
            terms = []
            for i, v in enumerate(vals):
                if abs(v) < 0.01:
                    continue
                if i == 0:
                    terms.append(rf"{v:+.2f}")
                elif i == 1:
                    terms.append(rf"{v:+.2f} x")
                else:
                    terms.append(rf"{v:+.2f} x^{i}")
            if not terms:
                expr = "p(x) = 0"
            else:
                expr = r"p(x) = " + " ".join(terms).lstrip("+")
            return MathTex(expr, color=YELLOW, font_size=22
                            ).move_to([3.5, 1.5, 0])

        self.add(always_redraw(poly_expr))

        # Tour through coefficient configurations
        configs = [
            (1, 0, 0, 0),    # constant
            (0, 1, 0, 0),    # linear
            (0, 0, 1, 0),    # quadratic
            (0, 0, 0, 0.5),  # cubic
            (1, 0.5, -0.5, 0.3),  # mixture
            (-1, 0, 1, 0),   # parabola shifted
        ]
        for (c0, c1, c2, c3) in configs:
            self.play(a0.animate.set_value(c0),
                       a1.animate.set_value(c1),
                       a2.animate.set_value(c2),
                       a3.animate.set_value(c3),
                       run_time=1.8, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.4)
