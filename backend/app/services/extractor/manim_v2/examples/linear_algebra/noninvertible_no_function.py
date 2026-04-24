from manim import *
import numpy as np


class NoninvertibleNoFunctionExample(Scene):
    """
    When det A = 0, A squishes the plane onto a line. No function can
    un-squish (one output came from many inputs). Input vectors
    (x+2, x) for x=-4..4 ALL map to the same output vector.
    """

    def construct(self):
        title = Tex(r"$\det A=0$: no inverse (multiple inputs $\to$ same output)",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 5, 1], y_range=[-3, 3, 1],
                            x_length=9, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.1)
        self.play(Create(plane))

        A = np.array([[2.0, 1.0], [-2.0, -1.0]])  # det = 0

        stage_tr = ValueTracker(0.0)

        def M_of():
            t = stage_tr.get_value()
            return (1 - t) * np.eye(2) + t * A

        # Input vectors: (x+2, x) for x in [-4, 4] — all on same line
        input_vecs = []
        for x in np.arange(-4, 4.5, 0.5):
            input_vecs.append(np.array([x + 2, x]))

        def arrows():
            M = M_of()
            grp = VGroup()
            for i, v in enumerate(input_vecs):
                v_now = M @ v
                col = interpolate_color(PINK, YELLOW, i / len(input_vecs))
                grp.add(Arrow(plane.c2p(0, 0), plane.c2p(v_now[0], v_now[1]),
                               color=col, buff=0, stroke_width=3,
                               max_tip_length_to_length_ratio=0.15))
            return grp

        self.add(always_redraw(arrows))

        self.play(stage_tr.animate.set_value(1.0), run_time=3, rate_func=smooth)
        self.wait(0.5)

        # Annotation
        note = Tex(r"All these input vectors land on the SAME output vector $(4, 2)$",
                    color=RED, font_size=22).to_edge(DOWN, buff=0.3)
        note.add_background_rectangle(opacity=0.8)
        self.play(Write(note))
        self.wait(0.5)

        # Reverse to see inputs spread out
        self.play(stage_tr.animate.set_value(0.0), run_time=3, rate_func=smooth)
        self.wait(0.5)

        info = VGroup(
            Tex(r"$A=\begin{pmatrix}2&1\\-2&-1\end{pmatrix}$", font_size=22),
            Tex(r"$\det A=0$", color=RED, font_size=24),
            Tex(r"no function does this",
                color=RED, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.3)
        self.play(Write(info))
        self.wait(1.0)
