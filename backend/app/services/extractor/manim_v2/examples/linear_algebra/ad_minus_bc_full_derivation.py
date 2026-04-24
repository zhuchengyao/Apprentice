from manim import *
import numpy as np


class AdMinusBcFullDerivationExample(Scene):
    """
    Full derivation: decompose unit square transformed by [[a, b], [c, d]]
    into 4 triangles + 2 rectangles. Their areas sum to
    (a+b)(c+d) - ac - bd - 2bc = ad - bc.

    SINGLE_FOCUS: sketch the enclosing (a+b)×(c+d) rectangle and
    subtract out triangles and corner rects.
    """

    def construct(self):
        title = Tex(r"$\det=(a+b)(c+d)-ac-bd-2bc=ad-bc$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane_center = LEFT * 2 + DOWN * 0.3
        scale = 0.6

        a_v, b_v, c_v, d_v = 3.0, 1.5, 0.5, 2.0
        i_end = np.array([a_v, c_v])
        j_end = np.array([b_v, d_v])

        def to_screen(v):
            return np.array([v[0] * scale, v[1] * scale, 0]) + plane_center

        # The transformed parallelogram
        para = Polygon(to_screen(np.zeros(2)),
                        to_screen(i_end),
                        to_screen(i_end + j_end),
                        to_screen(j_end),
                        color=YELLOW, stroke_width=3,
                        fill_color=YELLOW, fill_opacity=0.4)

        # Enclosing rectangle of dimensions (a+b) × (c+d)
        rect_w = a_v + b_v
        rect_h = c_v + d_v
        bounding_rect = Polygon(to_screen(np.zeros(2)),
                                 to_screen(np.array([rect_w, 0])),
                                 to_screen(np.array([rect_w, rect_h])),
                                 to_screen(np.array([0, rect_h])),
                                 color=BLUE, stroke_width=2,
                                 fill_opacity=0.0)

        self.play(Create(bounding_rect))
        self.add(Tex(rf"$(a+b)(c+d)={rect_w:.1f}\cdot{rect_h:.1f}={rect_w * rect_h:.2f}$",
                      color=BLUE, font_size=22).to_edge(RIGHT).shift(UP * 2))

        # The 6 subtracted regions
        # 2 triangles of area ac/2 (bottom-left, top-right)
        tri1 = Polygon(to_screen(np.zeros(2)),
                        to_screen(np.array([a_v, 0])),
                        to_screen(i_end),
                        color=MAROON, fill_color=MAROON, fill_opacity=0.6,
                        stroke_width=0)
        tri2 = Polygon(to_screen(i_end + j_end),
                        to_screen(np.array([rect_w, rect_h])),
                        to_screen(np.array([b_v, rect_h])),
                        color=MAROON, fill_color=MAROON, fill_opacity=0.6,
                        stroke_width=0)

        # 2 triangles of area bd/2 (bottom-right, top-left)
        tri3 = Polygon(to_screen(i_end),
                        to_screen(np.array([rect_w, 0])),
                        to_screen(i_end + j_end),
                        color=TEAL, fill_color=TEAL, fill_opacity=0.6,
                        stroke_width=0)
        tri4 = Polygon(to_screen(np.zeros(2)),
                        to_screen(j_end),
                        to_screen(np.array([0, rect_h])),
                        color=TEAL, fill_color=TEAL, fill_opacity=0.6,
                        stroke_width=0)

        # 2 bc rectangles
        rect_bc1 = Polygon(to_screen(np.array([a_v, 0])),
                            to_screen(np.array([rect_w, 0])),
                            to_screen(np.array([rect_w, c_v])),
                            to_screen(i_end),
                            color=PINK, fill_color=PINK, fill_opacity=0.6,
                            stroke_width=0)
        rect_bc2 = Polygon(to_screen(np.array([0, d_v])),
                            to_screen(j_end),
                            to_screen(np.array([b_v, rect_h])),
                            to_screen(np.array([0, rect_h])),
                            color=PINK, fill_color=PINK, fill_opacity=0.6,
                            stroke_width=0)

        self.play(FadeIn(tri1), FadeIn(tri2))
        self.play(FadeIn(tri3), FadeIn(tri4))
        self.play(FadeIn(rect_bc1), FadeIn(rect_bc2))
        self.wait(0.5)
        self.play(Create(para))
        self.wait(0.5)

        calc_text = VGroup(
            Tex(rf"$(a+b)(c+d)={rect_w * rect_h:.2f}$", color=BLUE, font_size=22),
            Tex(rf"$-ac-ac={-a_v * c_v - a_v * c_v:.2f}$ (MAROON)", color=MAROON, font_size=22),
            Tex(rf"$-bd-bd={-b_v * d_v - b_v * d_v:.2f}$ (TEAL)", color=TEAL, font_size=22),
            Tex(rf"$-2bc={-2 * b_v * c_v:.2f}$ (PINK)", color=PINK, font_size=22),
            Tex(rf"$=ad-bc={a_v * d_v - b_v * c_v:.2f}$", color=YELLOW, font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.3).shift(DOWN * 0.2)

        for line in calc_text:
            self.play(Write(line), run_time=0.6)
            self.wait(0.3)
        self.wait(0.8)
