from manim import *
import numpy as np


class SpherePacking2DExample(Scene):
    """
    Best 2D sphere (circle) packing in the plane: hexagonal packing
    achieves density π/(2√3) ≈ 0.9069. Square packing is π/4 ≈ 0.7854.

    COMPARISON:
      LEFT panel — square lattice of circles; yellow unit cell;
                   density = π/4.
      RIGHT panel — hex lattice; yellow unit cell; density = π/(2√3).
      ValueTracker s_tr morphs the hex lattice from square-stagger
      (s=0) to actual hex-stagger (s=1) via always_redraw, and
      density label updates correspondingly.
    """

    def construct(self):
        title = Tex(r"2D sphere packing density: $\pi/4$ vs $\pi/(2\sqrt 3)$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # LEFT: square packing (static)
        sq_center = np.array([-3.5, -0.2, 0])
        r = 0.38
        grid = VGroup()
        for i in range(-2, 3):
            for j in range(-2, 3):
                c = Circle(radius=r, color=BLUE,
                            fill_opacity=0.4, stroke_width=1.5)
                c.move_to(sq_center + np.array([i * 2 * r, j * 2 * r, 0]))
                grid.add(c)
        self.play(FadeIn(grid))
        sq_cell = Square(side_length=2 * r, color=YELLOW,
                          stroke_width=3, fill_opacity=0
                          ).move_to(sq_center + np.array([r, r, 0]))
        self.play(Create(sq_cell))

        sq_lbl = MathTex(r"\rho_\square = \tfrac{\pi}{4} \approx 0.7854",
                          color=YELLOW, font_size=26
                          ).next_to(grid, DOWN, buff=0.5)
        self.play(Write(sq_lbl))

        # RIGHT: interpolated lattice via ValueTracker s_tr
        hex_center = np.array([3.5, -0.2, 0])
        s_tr = ValueTracker(0.0)

        def hex_grid():
            s = s_tr.get_value()
            grp = VGroup()
            for j in range(-2, 3):
                stagger = s * r  # hex shift for every other row
                for i in range(-3, 4):
                    x = i * 2 * r + (stagger if j % 2 else 0)
                    # For hex: rows squeeze closer too
                    y = j * 2 * r * (1 - s * (1 - np.sqrt(3) / 2))
                    c = Circle(radius=r, color=GREEN,
                                fill_opacity=0.4, stroke_width=1.5)
                    c.move_to(hex_center + np.array([x, y, 0]))
                    grp.add(c)
            return grp

        hex_g = always_redraw(hex_grid)
        self.add(hex_g)

        def hex_cell():
            s = s_tr.get_value()
            # rhombus: 60° angle when s=1
            dx = 2 * r
            dy = 2 * r * (1 - s * (1 - np.sqrt(3) / 2))
            shift = s * r
            O = hex_center
            p1 = O
            p2 = O + np.array([dx, 0, 0])
            p3 = O + np.array([dx + shift, dy, 0])
            p4 = O + np.array([shift, dy, 0])
            return Polygon(p1, p2, p3, p4, color=YELLOW,
                            stroke_width=3, fill_opacity=0)

        self.add(always_redraw(hex_cell))

        def hex_info():
            s = s_tr.get_value()
            if s < 0.01:
                txt = r"\rho = \tfrac{\pi}{4}"
                val = PI / 4
            else:
                area_rhomb = 2 * r * (2 * r * (1 - s * (1 - np.sqrt(3) / 2)))
                # only 1 circle area in a rhombus of 2 circles' contribution
                val = PI * r ** 2 / area_rhomb
                txt = rf"\rho = {val:.4f}"
            return MathTex(txt, color=YELLOW, font_size=26
                            ).move_to(hex_center + np.array([0, -2.5, 0]))

        self.add(always_redraw(hex_info))

        self.wait(0.5)
        self.play(s_tr.animate.set_value(1.0),
                   run_time=4, rate_func=smooth)

        final = MathTex(r"\rho_{\text{hex}} = \tfrac{\pi}{2\sqrt 3} \approx 0.9069",
                         color=GREEN, font_size=28
                         ).to_edge(DOWN, buff=0.4)
        self.play(Write(final))
        self.wait(0.5)
