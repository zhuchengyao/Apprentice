from manim import *
import numpy as np


class MobiusTransformationExample(Scene):
    """
    Möbius transformation w = (az + b) / (cz + d): maps circles/lines
    to circles/lines. Visualize with the specific map z → 1/z which
    inverts through the unit circle and reflects across real axis
    (conjugates).

    COMPARISON:
      LEFT z-plane with colored test curves (grid + unit circle)
      RIGHT w-plane with the transformed curves; ValueTracker s_tr
      morphs from identity to w = 1/z.
    """

    def construct(self):
        title = Tex(r"Möbius: $w = 1/z$ inverts circles/lines to circles/lines",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        left = ComplexPlane(x_range=[-3, 3, 1], y_range=[-3, 3, 1],
                              x_length=5.2, y_length=5.2,
                              background_line_style={"stroke_opacity": 0.2}
                              ).move_to([-3.3, -0.3, 0])
        right = ComplexPlane(x_range=[-3, 3, 1], y_range=[-3, 3, 1],
                               x_length=5.2, y_length=5.2,
                               background_line_style={"stroke_opacity": 0.2}
                               ).move_to([3.3, -0.3, 0])
        self.play(Create(left), Create(right))

        z_lbl = MathTex(r"z\text{-plane}", font_size=20
                         ).next_to(left, UP, buff=0.1)
        w_lbl = MathTex(r"w = 1/z", color=YELLOW, font_size=20
                         ).next_to(right, UP, buff=0.1)
        self.play(Write(z_lbl), Write(w_lbl))

        # On LEFT: draw 3 circles of radius 0.5, 1, 2 (centered at origin)
        # + 2 vertical/horizontal lines
        def z_input_curves():
            grp = VGroup()
            # Circles
            for (r, col) in [(0.5, BLUE), (1.0, GREEN), (2.0, ORANGE)]:
                pts = [left.c2p(r * np.cos(t), r * np.sin(t))
                       for t in np.linspace(0, 2 * PI, 60)]
                m = VMobject(color=col, stroke_width=2)
                m.set_points_as_corners(pts + [pts[0]])
                grp.add(m)
            # Vertical line x = 1
            pts = [left.c2p(1, y) for y in np.linspace(-2.8, 2.8, 30)]
            m = VMobject(color=PURPLE, stroke_width=2)
            m.set_points_as_corners(pts)
            grp.add(m)
            # Horizontal line y = 1
            pts = [left.c2p(x, 1) for x in np.linspace(-2.8, 2.8, 30)]
            m = VMobject(color=RED, stroke_width=2)
            m.set_points_as_corners(pts)
            grp.add(m)
            return grp

        self.play(Create(z_input_curves()))

        s_tr = ValueTracker(0.0)

        def w_curves():
            s = s_tr.get_value()
            grp = VGroup()
            for (r, col) in [(0.5, BLUE), (1.0, GREEN), (2.0, ORANGE)]:
                pts_target = []
                pts_source = []
                for t in np.linspace(0, 2 * PI, 60):
                    z = r * np.exp(1j * t)
                    w = 1 / z if abs(z) > 1e-6 else z
                    pts_source.append(right.c2p(z.real, z.imag))
                    pts_target.append(right.c2p(w.real, w.imag))
                pts = [(1 - s) * np.array(a) + s * np.array(b)
                       for (a, b) in zip(pts_source, pts_target)]
                m = VMobject(color=col, stroke_width=2)
                m.set_points_as_corners(pts + [pts[0]])
                grp.add(m)
            # Vertical line x = 1
            pts_s = [right.c2p(1, y) for y in np.linspace(-2.8, 2.8, 40)]
            pts_t = []
            for y in np.linspace(-2.8, 2.8, 40):
                z = 1 + 1j * y
                w = 1 / z
                pts_t.append(right.c2p(w.real, w.imag))
            pts = [(1 - s) * np.array(a) + s * np.array(b)
                   for (a, b) in zip(pts_s, pts_t)]
            m = VMobject(color=PURPLE, stroke_width=2)
            m.set_points_as_corners(pts)
            grp.add(m)
            # Horizontal line y = 1
            pts_s = [right.c2p(x, 1) for x in np.linspace(-2.8, 2.8, 40)]
            pts_t = []
            for x in np.linspace(-2.8, 2.8, 40):
                z = x + 1j
                w = 1 / z
                pts_t.append(right.c2p(w.real, w.imag))
            pts = [(1 - s) * np.array(a) + s * np.array(b)
                   for (a, b) in zip(pts_s, pts_t)]
            m = VMobject(color=RED, stroke_width=2)
            m.set_points_as_corners(pts)
            grp.add(m)
            return grp

        self.add(always_redraw(w_curves))

        def info():
            s = s_tr.get_value()
            return VGroup(
                MathTex(rf"s = {s:.2f}", color=YELLOW, font_size=22),
                Tex(r"BLUE $r=0.5$ $\to r=2$",
                     color=BLUE, font_size=18),
                Tex(r"GREEN $r=1$ fixed",
                     color=GREEN, font_size=18),
                Tex(r"ORANGE $r=2$ $\to r=0.5$",
                     color=ORANGE, font_size=18),
                Tex(r"lines $\to$ circles through 0",
                     color=WHITE, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.13).to_edge(DOWN, buff=0.25)

        self.add(always_redraw(info))

        self.play(s_tr.animate.set_value(1.0),
                   run_time=5, rate_func=smooth)
        self.wait(0.6)
        self.play(s_tr.animate.set_value(0.0),
                   run_time=3, rate_func=smooth)
        self.wait(0.4)
