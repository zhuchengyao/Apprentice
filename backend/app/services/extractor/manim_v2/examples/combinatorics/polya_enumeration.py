from manim import *
import numpy as np


class PolyaEnumerationExample(Scene):
    """
    Pólya enumeration / Burnside refinement: count distinct
    3-colorings of a 4-bead necklace under C_4 rotations with
    cycle index Z(C_4) = (a_1^4 + a_2^2 + 2 a_4) / 4.

    Substituting a_i = k (number of colors) gives (k^4 + k^2 + 2k)/4
    colorings. For k=3: (81 + 9 + 6)/4 = 24.

    SINGLE_FOCUS:
      ValueTracker k_tr sweeps color count 1..4 via always_redraw;
      formula and count displayed.
    """

    def construct(self):
        title = Tex(r"Pólya: $Z(C_4) = \tfrac{1}{4}(a_1^4 + a_2^2 + 2 a_4)$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # 4-bead necklace
        n = 4
        center = np.array([-3, -0.3, 0])
        R = 1.0
        positions = [center + R * np.array([np.cos(2 * PI * i / n + PI / 4),
                                                np.sin(2 * PI * i / n + PI / 4), 0])
                     for i in range(n)]

        k_tr = ValueTracker(1)

        def beads():
            k = int(round(k_tr.get_value()))
            k = max(1, min(k, 4))
            colors = [RED, GREEN, BLUE, YELLOW][:k]
            grp = VGroup()
            # Color beads in some pattern: first bead picks color 0, etc.
            pattern_colors = [colors[i % k] for i in range(n)]
            for i, p in enumerate(positions):
                d = Circle(radius=0.25, color=pattern_colors[i],
                             fill_opacity=0.8, stroke_width=1.5
                             ).move_to(p)
                grp.add(d)
            # Ring connecting
            for i in range(n):
                grp.add(Line(positions[i], positions[(i + 1) % n],
                               color=GREY_B, stroke_width=1.5))
            return grp

        self.add(always_redraw(beads))

        def info():
            k = int(round(k_tr.get_value()))
            k = max(1, min(k, 4))
            count = (k ** 4 + k ** 2 + 2 * k) // 4
            return VGroup(
                MathTex(rf"k = {k}", color=YELLOW, font_size=24),
                MathTex(rf"k^4 = {k ** 4}", color=RED, font_size=20),
                MathTex(rf"k^2 = {k ** 2}", color=BLUE, font_size=20),
                MathTex(rf"2k = {2 * k}", color=GREEN, font_size=20),
                MathTex(rf"(k^4 + k^2 + 2k)/4 = {count}",
                         color=ORANGE, font_size=22),
                Tex(r"distinct necklaces", color=ORANGE, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for kv in [2, 3, 4, 1]:
            self.play(k_tr.animate.set_value(kv),
                       run_time=1.2, rate_func=smooth)
            self.wait(0.7)
        self.wait(0.4)
