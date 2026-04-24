from manim import *
import numpy as np


class VolumeDerivativeEqualsSurfaceArea(Scene):
    """Beautiful calculus fact: d/dR(volume of a ball of radius R) equals
    the surface area of that ball.  Circle: A(R) = pi R^2, A'(R) = 2 pi R
    = circumference.  Sphere: V(R) = (4/3) pi R^3, V'(R) = 4 pi R^2 =
    surface area.  Visualize as a thin expanding shell dR — its volume
    ~ (surface area) * dR."""

    def construct(self):
        title = Tex(
            r"$\dfrac{d V}{d R}$ = surface area: the expanding-shell picture",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        r_tr = ValueTracker(1.0)
        dr = 0.07

        def get_inner():
            R = r_tr.get_value()
            return Circle(radius=R * 0.9, color=BLUE, stroke_width=2,
                          fill_opacity=0.25).move_to([-3.5, 0, 0])

        def get_shell():
            R = r_tr.get_value()
            outer = Circle(radius=(R + dr) * 0.9, color=YELLOW,
                           stroke_width=2).move_to([-3.5, 0, 0])
            inner = Circle(radius=R * 0.9, color=YELLOW,
                           stroke_width=2).move_to([-3.5, 0, 0])
            annulus = Difference(outer, inner,
                                 color=YELLOW, fill_opacity=0.7,
                                 stroke_width=0)
            return annulus

        inner = always_redraw(get_inner)
        shell = always_redraw(get_shell)
        self.play(FadeIn(inner))
        self.play(FadeIn(shell))

        for target_R in [1.4, 1.7, 2.1, 1.3, 1.9]:
            self.play(r_tr.animate.set_value(target_R), run_time=1.0)

        circle_math = VGroup(
            Tex(r"Circle:", font_size=24, color=BLUE),
            MathTex(r"A(R) = \pi R^2", font_size=26),
            MathTex(r"\frac{dA}{dR} = 2\pi R", font_size=26,
                    color=GREEN),
            Tex(r"= circumference", font_size=22, color=GREEN),
            MathTex(r"(2\pi R)\,dR \approx \Delta A",
                    font_size=24, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        circle_math.to_edge(RIGHT, buff=0.4).shift(UP * 1.3)

        for t in circle_math:
            self.play(FadeIn(t), run_time=0.4)

        sphere_math = VGroup(
            Tex(r"Sphere:", font_size=24, color=BLUE),
            MathTex(r"V(R) = \tfrac{4}{3}\pi R^3", font_size=26),
            MathTex(r"\frac{dV}{dR} = 4\pi R^2", font_size=26,
                    color=GREEN),
            Tex(r"= surface area", font_size=22, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        sphere_math.to_edge(RIGHT, buff=0.4).shift(DOWN * 1.6)

        for t in sphere_math:
            self.play(FadeIn(t), run_time=0.4)

        principle = Tex(
            r"Add a thin shell $dR$: new volume gained = (surface area) $\cdot$ $dR$",
            font_size=22, color=YELLOW,
        ).to_edge(DOWN, buff=0.25)
        self.play(FadeIn(principle))
        self.wait(1.5)
