from manim import *
import numpy as np


class QuinticPolynomialRootsExample(Scene):
    """
    Roots of a quintic move continuously with coefficients (from
    _2022/quintic). Starting at z^5 = 1 (5 roots of unity on the
    circle) and ValueTracker s_tr interpolates coefficients toward
    z^5 + a·z + b = 0 for a specific (a, b); roots trace curves.

    SINGLE_FOCUS:
      ComplexPlane with 5 colored root markers; always_redraw
      rebuilds roots via numpy.roots(); persistent trails show how
      roots move as the coefficient parameter changes.
    """

    def construct(self):
        title = Tex(r"Roots of $z^5 + a z + b = 0$ as $(a, b)$ varies",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = ComplexPlane(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                               x_length=6, y_length=6,
                               background_line_style={"stroke_opacity": 0.25}
                               ).move_to([-2.5, -0.3, 0])
        self.play(Create(plane))

        # Initial: z^5 = 1, roots are 5th roots of unity.
        # Final: z^5 + a z + b = 0 with (a, b) = (2, -1)

        s_tr = ValueTracker(0.0)

        def current_poly():
            s = s_tr.get_value()
            # Coefficients of z^5 + 0 z^4 + 0 z^3 + 0 z^2 + s·a·z + (s·b - 1)
            # We want initial: z^5 - 1, final: z^5 + 2z - 1
            a_coef = 2.0 * s
            b_coef = -1.0 + s * (-1.0 - (-1.0))  # stays at -1
            # Coeff array high-to-low for numpy.roots
            return [1, 0, 0, 0, a_coef, b_coef]

        def root_dots():
            poly = current_poly()
            roots = np.roots(poly)
            grp = VGroup()
            colors = [RED, BLUE, GREEN, YELLOW, PURPLE]
            for i, r in enumerate(roots):
                grp.add(Dot(plane.c2p(float(r.real), float(r.imag)),
                              color=colors[i % len(colors)], radius=0.12))
            return grp

        # Trails of roots
        history = {i: [] for i in range(5)}

        def update_history():
            poly = current_poly()
            roots = np.roots(poly)
            # Sort by angle for consistent indexing
            angles = [np.angle(r) for r in roots]
            order = np.argsort(angles)
            for new_idx, old_idx in enumerate(order):
                history[new_idx].append(plane.c2p(
                    float(roots[old_idx].real),
                    float(roots[old_idx].imag)))

        # Dummy function for always_redraw trails
        def trails():
            grp = VGroup()
            colors = [RED, BLUE, GREEN, YELLOW, PURPLE]
            for i in range(5):
                if len(history[i]) < 2:
                    continue
                m = VMobject(color=colors[i], stroke_width=2,
                               stroke_opacity=0.6)
                m.set_points_as_corners(history[i])
                grp.add(m)
            return grp

        self.add(always_redraw(root_dots), always_redraw(trails))

        # Populate history as s changes - use updater
        def history_updater(mob):
            update_history()

        # Register a "phantom" mobject to trigger updates
        phantom = Mobject()
        phantom.add_updater(history_updater)
        self.add(phantom)

        # Legend
        legend = Tex(r"start: $z^5 = 1$ \quad\quad end: $z^5 + 2z - 1 = 0$",
                      color=WHITE, font_size=22).to_edge(DOWN, buff=0.25)
        self.play(Write(legend))

        def info():
            s = s_tr.get_value()
            poly = current_poly()
            roots = np.roots(poly)
            root_txts = []
            for r in roots:
                root_txts.append(f"{r.real:+.2f}{'+' if r.imag >= 0 else '-'}{abs(r.imag):.2f}i")
            return VGroup(
                MathTex(rf"s = {s:.2f}", color=YELLOW, font_size=22),
                MathTex(rf"p(z) = z^5 + {2 * s:.2f}\,z - 1",
                         color=WHITE, font_size=22),
                Tex(r"5 roots by Fundamental Thm of Algebra",
                     color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.8, 1.0, 0])

        self.add(always_redraw(info))

        self.play(s_tr.animate.set_value(1.0),
                   run_time=6, rate_func=smooth)
        self.wait(0.5)
