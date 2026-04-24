from manim import *
import numpy as np


class LinearPreservesEqualSpacingExample(Scene):
    """
    A linear map 2D→1D preserves equal spacing: if the input dots are
    evenly spaced along a line, the output dots on the number line
    are also evenly spaced (though the spacing scale may differ).

    Non-linear maps break this — spacing gets uneven.
    """

    def construct(self):
        title = Tex(r"Linear $\Leftrightarrow$ evenly-spaced $\to$ evenly-spaced",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-3, 3, 1], y_range=[-2, 2, 1],
                            x_length=5.5, y_length=4.5,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(LEFT * 3.0 + DOWN * 0.3)
        num_line = NumberLine(x_range=[-5, 5, 2], length=6,
                              include_numbers=True,
                              font_size=18).shift(RIGHT * 2.5 + DOWN * 0.3)
        self.play(Create(plane), Create(num_line))

        # Evenly-spaced dots along a line y=x/2+0.5
        dots_input = []
        for t in np.linspace(-2.2, 2.2, 9):
            p = np.array([t, t * 0.5 + 0.5])
            dots_input.append(p)

        colors = [interpolate_color(BLUE, PINK, i / 8) for i in range(9)]

        # Plane dots
        for p, col in zip(dots_input, colors):
            self.add(Dot(plane.c2p(p[0], p[1]), color=col, radius=0.09))

        # Stage: which map? Linear vs non-linear
        map_tr = ValueTracker(0.0)  # 0 = linear, 1 = non-linear

        def output_val(p):
            s = map_tr.get_value()
            # Linear: L(x, y) = x + y
            # Non-linear: N(x, y) = x² (introduces unequal spacing)
            lin = p[0] + p[1]
            nonlin = p[0] ** 2 - p[1] ** 2
            return (1 - s) * lin + s * nonlin

        def num_dots():
            grp = VGroup()
            for p, col in zip(dots_input, colors):
                val = output_val(p)
                val = max(-5, min(5, val))
                grp.add(Dot(num_line.n2p(val), color=col, radius=0.09))
            return grp

        self.add(always_redraw(num_dots))

        # Label
        def map_str():
            s = map_tr.get_value()
            if s < 0.05: return r"linear map $L(x, y)=x+y$"
            if s < 0.95: return r"morphing..."
            return r"non-linear $N(x, y)=x^2-y^2$ (spacing broken!)"

        lbl = Tex(map_str(), color=YELLOW, font_size=22).to_edge(DOWN, buff=0.4)
        self.add(lbl)
        def update_lbl(mob, dt):
            new = Tex(map_str(), color=YELLOW, font_size=22).move_to(lbl)
            lbl.become(new)
            return lbl
        lbl.add_updater(update_lbl)

        self.play(map_tr.animate.set_value(1.0), run_time=4, rate_func=smooth)
        self.wait(0.5)
        self.play(map_tr.animate.set_value(0.0), run_time=3, rate_func=smooth)
        self.wait(0.5)
