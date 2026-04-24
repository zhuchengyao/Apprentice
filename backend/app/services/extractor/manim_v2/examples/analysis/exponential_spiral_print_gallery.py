from manim import *
import numpy as np


class ExponentialSpiralPrintGalleryExample(Scene):
    """
    Complex exponential maps a rectangular grid to a polar grid (from
    _2026/print_gallery/exponential): vertical lines → circles,
    horizontal lines → rays from origin. At the ground-level lines
    the effect is especially striking.

    SINGLE_FOCUS:
      Source grid + target spiral grid both visible; ValueTracker s_tr
      morphs between them via z ↦ (1-s)·z + s·e^z. Uses Transform-free
      approach with always_redraw re-generating grid curves.
    """

    def construct(self):
        title = Tex(r"Print gallery: $z \mapsto e^z$ warps grid to spiral",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = ComplexPlane(x_range=[-4, 4, 1], y_range=[-3, 3, 1],
                               x_length=11, y_length=6,
                               background_line_style={"stroke_opacity": 0.15}
                               ).move_to([0, -0.3, 0])
        self.play(Create(plane))

        s_tr = ValueTracker(0.0)

        def interp(z, s):
            # (1-s) z + s e^z, but scale e^z by 0.5 to keep it bounded
            return (1 - s) * z + s * 0.5 * np.exp(z)

        def grid_curves():
            s = s_tr.get_value()
            grp = VGroup()
            # Vertical lines x = const
            for xv in np.arange(-1.5, 1.51, 0.5):
                pts = []
                for yv in np.linspace(-2.5, 2.5, 80):
                    z = xv + 1j * yv
                    w = interp(z, s)
                    pts.append(plane.c2p(w.real, w.imag))
                m = VMobject(color=BLUE, stroke_width=1.5)
                m.set_points_as_corners(pts)
                grp.add(m)
            # Horizontal lines y = const
            for yv in np.arange(-2, 2.01, 0.5):
                pts = []
                for xv in np.linspace(-1.5, 1.5, 80):
                    z = xv + 1j * yv
                    w = interp(z, s)
                    pts.append(plane.c2p(w.real, w.imag))
                m = VMobject(color=ORANGE, stroke_width=1.5)
                m.set_points_as_corners(pts)
                grp.add(m)
            return grp

        self.add(always_redraw(grid_curves))

        def info():
            s = s_tr.get_value()
            return VGroup(
                MathTex(rf"s = {s:.2f}", color=YELLOW, font_size=24),
                MathTex(r"w = (1-s)z + \tfrac{s}{2} e^z",
                         color=GREEN, font_size=22),
                Tex(r"verticals $\to$ circles", color=BLUE, font_size=20),
                Tex(r"horizontals $\to$ rays", color=ORANGE, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.3).shift(DOWN * 1.8)

        self.add(always_redraw(info))

        self.play(s_tr.animate.set_value(1.0),
                   run_time=5, rate_func=smooth)
        self.wait(0.6)
        self.play(s_tr.animate.set_value(0.0),
                   run_time=3, rate_func=smooth)
        self.wait(0.4)
