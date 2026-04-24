from manim import *
import numpy as np


class ConformalExpMapExample(Scene):
    """
    Conformal map z ↦ exp(z): strip morphs into an annulus.

    SINGLE_FOCUS layout: a single complex plane in the middle. A
    ValueTracker s ∈ [0, 1] interpolates a grid of vertical and
    horizontal segments from the rectangular strip
    {Re(z) ∈ [-1, 1], Im(z) ∈ [-π, π]} toward the image grid under
    z ↦ exp(z), where verticals become circles (|z|=eˣ) and
    horizontals become radial rays (arg z = y).

    Right of the plane: live equations showing the parametrization
    being interpolated, plus the conformal-map identity.
    """

    def construct(self):
        title = Tex(r"Conformal map $z \mapsto e^z$ sends a strip to an annulus",
                    font_size=30).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # ONE plane (instead of side-by-side). Centered.
        plane = ComplexPlane(
            x_range=[-3, 3, 1], y_range=[-3.2, 3.2, 1],
            x_length=6.5, y_length=6.0,
            background_line_style={"stroke_opacity": 0.25},
        ).move_to([-2.0, -0.2, 0])
        self.play(Create(plane))

        # Source grid: x ∈ [-1, 1] (5 verticals), y ∈ [-π+0.2, π-0.2] (7 horizontals)
        x_lines = np.linspace(-1, 1, 5)
        y_lines = np.linspace(-PI + 0.3, PI - 0.3, 7)

        s = ValueTracker(0.0)

        def interp(point: complex, s_val: float) -> complex:
            """Linearly interpolate from z to exp(z) by s."""
            return (1 - s_val) * point + s_val * np.exp(point)

        def vertical_lines():
            sv = s.get_value()
            grp = VGroup()
            for x in x_lines:
                # Sample many y values along this vertical to capture the curve
                pts = []
                for y in np.linspace(-PI + 0.05, PI - 0.05, 60):
                    z = complex(x, y)
                    w = interp(z, sv)
                    pts.append(plane.n2p(w))
                line = VMobject(color=BLUE, stroke_width=3)
                line.set_points_smoothly(pts)
                grp.add(line)
            return grp

        def horizontal_lines():
            sv = s.get_value()
            grp = VGroup()
            for y in y_lines:
                pts = []
                for x in np.linspace(-1, 1, 60):
                    z = complex(x, y)
                    w = interp(z, sv)
                    pts.append(plane.n2p(w))
                line = VMobject(color=GREEN, stroke_width=3)
                line.set_points_smoothly(pts)
                grp.add(line)
            return grp

        self.add(always_redraw(vertical_lines), always_redraw(horizontal_lines))

        # RIGHT COLUMN: live readouts and identities
        rcol_x = +4.4

        def info_panel():
            sv = s.get_value()
            return VGroup(
                Tex(rf"$s = {sv:.2f}$", color=WHITE, font_size=28),
                Tex(r"\textbf{interpolant:}", color=GREY_B, font_size=20),
                MathTex(r"w = (1-s)\,z + s\,e^z", color=YELLOW, font_size=24),
                Tex(r"\textbf{at }$s = 1$:", color=GREY_B, font_size=20),
                MathTex(r"|e^z| = e^{\mathrm{Re}(z)}", color=BLUE, font_size=22),
                MathTex(r"\arg(e^z) = \mathrm{Im}(z)", color=GREEN, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([rcol_x, +0.4, 0])

        self.add(always_redraw(info_panel))

        self.play(s.animate.set_value(1.0), run_time=5, rate_func=smooth)
        self.wait(0.6)
        self.play(s.animate.set_value(0.0), run_time=2.5, rate_func=smooth)
        self.wait(0.4)
        self.play(s.animate.set_value(1.0), run_time=2.5, rate_func=smooth)

        conclusion = Tex(r"Vertical strips $\to$ circles; horizontal lines $\to$ rays",
                         font_size=22, color=YELLOW).move_to([rcol_x, -3.0, 0])
        self.play(Write(conclusion))
        self.wait(1.0)
