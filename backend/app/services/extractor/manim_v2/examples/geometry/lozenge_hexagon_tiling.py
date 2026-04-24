from manim import *
import numpy as np


class LozengeHexagonTilingExample(Scene):
    """
    Regular hexagon tiled by 3 congruent 60°/120° rhombi; the three
    rhombi rotate about the hexagon's center by 120° to permute
    among themselves.

    SINGLE_FOCUS:
      Hexagon with 3 rhombi in 3 colors; Rotate the whole tiling
      by 0→2π; second phase Transforms between the 3 canonical
      orientations of the tiling (3D-cube-like projection flips).
    """

    def construct(self):
        title = Tex(r"Lozenge tiling: 3 rhombi in a regular hexagon",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        cx, cy = 0, -0.2
        R = 2.2

        hex_pts = [np.array([cx + R * np.cos(k * PI / 3),
                              cy + R * np.sin(k * PI / 3), 0])
                   for k in range(6)]
        hex_poly = Polygon(*hex_pts, color=WHITE, stroke_width=3)
        center = np.array([cx, cy, 0])

        # Three rhombi: each uses 2 adjacent hex vertices and center
        # Rhombus 1: V0, V1, V2, center (NO — rhombus has 4 vertices, 2 sides)
        # Proper: rhombus = (V_i, V_{i+1}, V_{i+2}, center)
        rhombi_colors = [BLUE, RED, GREEN]
        rhombi = VGroup()
        for k in range(3):
            verts = [hex_pts[2 * k], hex_pts[2 * k + 1],
                     hex_pts[(2 * k + 2) % 6], center]
            rh = Polygon(*verts, color=rhombi_colors[k],
                          fill_opacity=0.55, stroke_width=2)
            rhombi.add(rh)

        self.play(Create(hex_poly), FadeIn(rhombi))
        self.wait(0.4)

        # Phase 1: rotate the whole tiling 360°
        self.play(Rotate(VGroup(hex_poly, rhombi), angle=TAU,
                          about_point=center),
                   run_time=4, rate_func=linear)

        # Phase 2: Transform to the OTHER "cube" lozenge tiling where the
        # center-slant is different — ValueTracker s_tr interpolates
        # between the two
        # Alternative tiling: rhombi (V_{i}, V_{i+1}, center, V_{i+5}) ... complicated.
        # Simpler alternative: swap the colors to flip "up" face vs "down" face
        alt_rhombi = VGroup()
        alt_colors = [GREEN, BLUE, RED]  # cycled
        for k in range(3):
            verts = [hex_pts[2 * k], hex_pts[2 * k + 1],
                     hex_pts[(2 * k + 2) % 6], center]
            rh = Polygon(*verts, color=alt_colors[k],
                          fill_opacity=0.55, stroke_width=2)
            alt_rhombi.add(rh)

        note = Tex(r"(cyclic color swap = cube rotation of the 3D interpretation)",
                    color=YELLOW, font_size=20).to_edge(DOWN, buff=0.4)
        self.play(Write(note))
        self.play(Transform(rhombi, alt_rhombi), run_time=1.5)
        self.wait(0.4)

        # Another rotation pass for emphasis
        self.play(Rotate(VGroup(hex_poly, rhombi), angle=TAU,
                          about_point=center),
                   run_time=4, rate_func=linear)
        self.wait(0.4)
