from manim import *
import numpy as np


class RieszRepresentationExample(Scene):
    """
    Riesz representation in L²: every bounded linear functional
    f: L²[0, 1] → ℝ is represented as f(u) = ∫ u(x) g(x) dx for
    unique g ∈ L²[0, 1].

    Example: f(u) = u(0.5). Representing function g is a Dirac-delta,
    not in L². But f(u) = ∫_0^{0.5} u dx has g(x) = 1_{[0, 0.5]}.

    TWO_COLUMN: LEFT axes with test function u (BLUE), representing
    function g (RED). RIGHT live ⟨u, g⟩ = f(u).
    """

    def construct(self):
        title = Tex(r"Riesz: $f(u)=\int u\,g\,dx$ for unique $g\in L^2$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[0, 1, 0.2], y_range=[-0.3, 1.5, 0.5],
                    x_length=6.0, y_length=4.0,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(LEFT * 2.2 + DOWN * 0.2)
        self.play(Create(axes))

        # Representing function g(x) = 1_[0, 0.5]
        g_fn_curve = VMobject().set_points_as_corners([
            axes.c2p(0, 1),
            axes.c2p(0.5, 1),
            axes.c2p(0.5, 0),
            axes.c2p(1, 0),
        ]).set_color(RED).set_stroke(width=4)
        self.add(g_fn_curve)
        self.add(Tex(r"$g(x)=\mathbf{1}_{[0, 0.5]}$", color=RED,
                     font_size=22).move_to(axes.c2p(0.3, 1.25)))

        # Test function u varying
        shape_tr = ValueTracker(0.0)

        def u_of(x):
            s = shape_tr.get_value()
            return float((1 - s) * (x + 0.2) + s * np.sin(3 * PI * x) * (1 + 0.5 * np.cos(2 * PI * x)))

        def u_curve():
            return axes.plot(u_of, x_range=[0, 1],
                             color=BLUE, stroke_width=3)

        self.add(always_redraw(u_curve))

        # Inner product computation
        def inner_prod():
            xs = np.linspace(0, 0.5, 200)
            vals = np.array([u_of(x) for x in xs])
            return float(np.trapezoid(vals, xs))

        # Shaded region where g=1 (overlap with u)
        def shaded_region():
            xs = np.linspace(0, 0.5, 40)
            top = [axes.c2p(x, u_of(x)) for x in xs]
            bot = [axes.c2p(x, 0) for x in xs]
            return Polygon(*top, *reversed(bot),
                            color=PURPLE, stroke_width=0,
                            fill_color=PURPLE, fill_opacity=0.4)

        self.add(always_redraw(shaded_region))

        info = VGroup(
            Tex(r"functional $f(u)=\int_0^{0.5} u\,dx$",
                color=RED, font_size=22),
            VGroup(Tex(r"$\langle u, g\rangle=\int u\,g\,dx=$",
                       font_size=22),
                   DecimalNumber(0.0, num_decimal_places=4,
                                 font_size=22).set_color(PURPLE)
                   ).arrange(RIGHT, buff=0.1),
            Tex(r"matches $f(u)$ by Riesz",
                color=GREEN, font_size=20),
            Tex(r"$g\in L^2[0,1]$: bounded functional has $L^2$ rep",
                color=GREY_B, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.2)
        info[1][1].add_updater(lambda m: m.set_value(inner_prod()))
        self.add(info)

        self.play(shape_tr.animate.set_value(1.0),
                  run_time=4, rate_func=smooth)
        self.wait(0.5)
        self.play(shape_tr.animate.set_value(0.5),
                  run_time=2, rate_func=smooth)
        self.wait(0.5)
