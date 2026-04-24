from manim import *
import numpy as np


def sierpinski_polys(depth, a, b, c):
    """Recursively build the Sierpinski triangles at given depth."""
    if depth == 0:
        return [Polygon(a, b, c, color=YELLOW, fill_opacity=0.7, stroke_width=0.5)]
    ab = (a + b) / 2
    bc = (b + c) / 2
    ca = (c + a) / 2
    return (
        sierpinski_polys(depth - 1, a, ab, ca)
        + sierpinski_polys(depth - 1, ab, b, bc)
        + sierpinski_polys(depth - 1, ca, bc, c)
    )


class SierpinskiTriangleExample(Scene):
    """
    Sierpinski iterates depth 0 → 6 with Transform morphs between
    successive depths. Right side tracks count and Hausdorff
    dimension log(3)/log(2) ≈ 1.585.

    SINGLE_FOCUS:
      Each depth's polygon set is built as a VGroup. ValueTracker
      depth_idx steps through 0..6; Transform morphs the displayed
      VGroup to the next. A live counter on the right shows the number
      of triangles 3^d and the total area (3/4)^d × A₀ — both shrinking
      visibly to a fractal limit.
    """

    def construct(self):
        title = Tex(r"Sierpinski triangle: $\dim_H = \dfrac{\log 3}{\log 2} \approx 1.585$",
                    font_size=26).to_edge(UP, buff=0.4)
        self.play(Write(title))

        a = np.array([-3.0, -1.8, 0])
        b = np.array([+3.0, -1.8, 0])
        c = np.array([0.0, +2.0, 0])

        # Anchor the triangle in the LEFT half
        offset = np.array([-1.6, 0, 0])
        a_o, b_o, c_o = a + offset, b + offset, c + offset

        depths = [0, 1, 2, 3, 4, 5, 6]
        groups = [VGroup(*sierpinski_polys(d, a_o, b_o, c_o)) for d in depths]

        current = groups[0].copy()
        self.add(current)

        depth_idx = ValueTracker(0)

        # RIGHT COLUMN
        rcol_x = +4.0

        def info_panel():
            i = int(round(depth_idx.get_value()))
            i = max(0, min(i, len(depths) - 1))
            d = depths[i]
            count = 3 ** d
            area_frac = (3 / 4) ** d
            return VGroup(
                MathTex(rf"\text{{depth}} = {d}", color=YELLOW, font_size=32),
                MathTex(rf"\#\text{{triangles}} = 3^{d} = {count}",
                        color=WHITE, font_size=24),
                MathTex(rf"\text{{area}} = (3/4)^{d} A_0",
                        color=WHITE, font_size=22),
                MathTex(rf"\approx {area_frac:.3f}\,A_0",
                        color=GREEN, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([rcol_x, +1.0, 0])

        self.add(always_redraw(info_panel))

        # Step through depths
        for i in range(1, len(depths)):
            new_grp = groups[i]
            self.play(Transform(current, new_grp),
                      depth_idx.animate.set_value(i),
                      run_time=1.2, rate_func=smooth)
            self.wait(0.3)

        limit_lbl = Tex(r"Area $\to 0$, perimeter $\to \infty$",
                        color=YELLOW, font_size=24).move_to([rcol_x, -2.0, 0])
        self.play(Write(limit_lbl))
        self.wait(1.0)
