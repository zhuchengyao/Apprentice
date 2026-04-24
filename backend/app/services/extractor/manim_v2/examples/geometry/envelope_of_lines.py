from manim import *
import numpy as np


class EnvelopeOfLinesExample(Scene):
    """
    Envelope of a family of lines: the curve tangent to every member.
    Classic example: family of lines x cos t + y sin t = 1 has
    envelope = unit circle. Another: lines from (t, 0) to (0, 1-t)
    envelope is the parabola y = (1-x)² / 4... something like that.

    SINGLE_FOCUS:
      Plane with 30 lines x cos t + y sin t = 1 for t ∈ [0, 2π];
      envelope (unit circle) drawn over them.
    """

    def construct(self):
        title = Tex(r"Envelope of lines $x \cos t + y \sin t = 1$ is the unit circle",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                             x_length=7, y_length=7,
                             background_line_style={"stroke_opacity": 0.3}
                             ).move_to([-1, -0.3, 0])
        self.play(Create(plane))

        t_tr = ValueTracker(0)  # number of lines shown

        def line_family():
            n = int(round(t_tr.get_value()))
            n = max(0, min(n, 50))
            grp = VGroup()
            for i in range(n):
                t = 2 * PI * i / 50
                # Line: x cos t + y sin t = 1, i.e. (cos t, sin t) · (x, y) = 1
                # Normal direction (cos t, sin t); line passes through (cos t, sin t)
                # Parametrize the line: P + s * (-sin t, cos t)
                P = np.array([np.cos(t), np.sin(t)])
                d = np.array([-np.sin(t), np.cos(t)])
                # Extend for visibility
                s_max = 2.5
                start = plane.c2p(*(P - s_max * d))
                end = plane.c2p(*(P + s_max * d))
                grp.add(Line(start, end, color=BLUE,
                               stroke_width=1, stroke_opacity=0.55))
            return grp

        self.add(always_redraw(line_family))

        # Envelope: unit circle
        envelope_circle = Circle(radius=plane.c2p(1, 0)[0] - plane.c2p(0, 0)[0],
                                   color=YELLOW, stroke_width=4
                                   ).move_to(plane.c2p(0, 0))

        # Show envelope once many lines are drawn
        def envelope_reveal():
            n = int(round(t_tr.get_value()))
            if n >= 40:
                return envelope_circle
            return VGroup()

        self.add(always_redraw(envelope_reveal))

        def info():
            n = int(round(t_tr.get_value()))
            return VGroup(
                MathTex(rf"\text{{lines}} = {n}",
                         color=BLUE, font_size=22),
                Tex(r"each line tangent to unit circle",
                     color=YELLOW, font_size=20),
                MathTex(r"\text{envelope}: x^2 + y^2 = 1",
                         color=YELLOW, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(RIGHT, buff=0.3).shift(UP * 0.5)

        self.add(always_redraw(info))

        self.play(t_tr.animate.set_value(50),
                   run_time=6, rate_func=linear)
        self.wait(0.4)
