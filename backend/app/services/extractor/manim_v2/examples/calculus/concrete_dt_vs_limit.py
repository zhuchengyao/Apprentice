from manim import *
import numpy as np


class ConcreteDtVsLimitExample(Scene):
    """
    Concrete small dt ≠ taking the limit. For s(t) = t³, the formula
    ds/dt = 3t²+3tdt+dt²; in the limit dt→0 we get 3t². Show the
    algebra: using dt=0.01 gives approximate, but the exact formula
    is the limit.
    """

    def construct(self):
        title = Tex(r"Concrete small $dt$ vs the actual limit",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # s(t) = t^3, compute [s(t+dt) - s(t)] / dt
        derivation = VGroup(
            MathTex(r"\frac{s(t+dt)-s(t)}{dt}",
                      r"=",
                      r"\frac{(t+dt)^3-t^3}{dt}",
                      font_size=32),
            MathTex(r"=", r"\frac{3t^2\,dt + 3t\,dt^2 + dt^3}{dt}",
                      font_size=30),
            MathTex(r"=", r"3t^2 + 3t\,dt + dt^2",
                      font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).shift(UP * 0.7 + LEFT * 0.5)

        for line in derivation:
            self.play(Write(line), run_time=0.9)
            self.wait(0.2)
        self.wait(0.4)

        # Two interpretations
        concrete = Tex(r"with $dt=0.01, t=2$: $\approx 12 + 0.06 + 0.0001$",
                        color=ORANGE, font_size=22).shift(DOWN * 1.4)
        self.play(Write(concrete))
        self.wait(0.3)

        limit = Tex(r"$\lim_{dt\to 0}$: exactly $3t^2=12$ at $t=2$",
                     color=GREEN, font_size=24).shift(DOWN * 2.1)
        self.play(Write(limit))
        self.wait(0.3)

        self.play(Write(
            Tex(r"limit is cleaner than any concrete $dt$",
                 color=YELLOW, font_size=22).to_edge(DOWN, buff=0.3)
        ))
        self.wait(1.0)
