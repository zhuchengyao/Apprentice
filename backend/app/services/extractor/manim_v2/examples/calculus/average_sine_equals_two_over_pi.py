from manim import *
import numpy as np


class AverageSineEqualsTwoOverPiExample(Scene):
    """
    Average of sin over [0, π] = 2/π. Geometric: the average-height
    line at y=2/π has the same area under it as sin(x) does.
    """

    def construct(self):
        title = Tex(r"Average of $\sin x$ on $[0, \pi]$ = $\frac{2}{\pi}\approx 0.637$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[0, PI, PI / 4], y_range=[0, 1.2, 0.5],
                    x_length=9, y_length=4.5,
                    axis_config={"include_numbers": True, "font_size": 14}
                    ).shift(DOWN * 0.2)
        self.play(Create(axes))

        sin_curve = axes.plot(np.sin, x_range=[0, PI], color=BLUE, stroke_width=3)
        self.add(sin_curve)

        # Shade area under sin (which = 2)
        sin_fill = axes.get_area(sin_curve, x_range=[0, PI], color=BLUE, opacity=0.35)
        self.add(sin_fill)
        self.add(Tex(r"$\int_0^\pi\sin x\,dx=2$", color=BLUE, font_size=22).move_to(
            axes.c2p(PI / 2, 0.4)))

        # Average line
        avg_val = 2 / PI
        avg_curve = axes.plot(lambda x: avg_val, x_range=[0, PI],
                                color=GREEN, stroke_width=3)
        self.add(avg_curve)

        # Shade rectangle under avg line (which = π · 2/π = 2)
        rect = Polygon(axes.c2p(0, 0), axes.c2p(PI, 0),
                        axes.c2p(PI, avg_val), axes.c2p(0, avg_val),
                        color=GREEN, stroke_width=3,
                        fill_color=GREEN, fill_opacity=0.25)
        self.add(rect)
        self.add(Tex(rf"$y=2/\pi$, area $=\pi\cdot 2/\pi=2$",
                     color=GREEN, font_size=22).move_to(axes.c2p(PI / 2, 0.8)))

        # Annotation
        self.play(Write(
            Tex(r"both regions have area $2$: avg = total / length = $2/\pi$",
                 color=YELLOW, font_size=24).to_edge(DOWN, buff=0.4)
        ))
        self.wait(1.0)
