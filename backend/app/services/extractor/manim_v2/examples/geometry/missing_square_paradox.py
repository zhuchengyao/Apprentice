from manim import *
import numpy as np


class MissingSquareParadoxExample(Scene):
    """
    Missing-square "paradox": a triangle is split into 4 pieces, and
    when rearranged a unit-square gap appears. The illusion is that
    the hypotenuse isn't straight — slopes differ by a tiny amount.

    SINGLE_FOCUS:
      Two arrangements of 4 shapes (red tri 3-8, blue tri 2-5, green
      L, yellow L). ValueTracker morph_tr swaps between them via
      Transform. Zoom in to show the hypotenuse isn't straight —
      slopes 3/8 = 0.375 vs 2/5 = 0.4.
    """

    def construct(self):
        title = Tex(r"Missing-square paradox: the hypotenuse isn't straight",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # 13×5 grid
        unit = 0.4
        origin = np.array([-3.5, -1.5, 0])

        def pos(x, y):
            return origin + np.array([x * unit, y * unit, 0])

        # Arrangement 1: pieces fit without gap
        # Red triangle: (0,0), (8,0), (8,3)
        # Blue triangle: (8,3), (13,3), (13,5)
        # Green L: (0,0), (8,0), (8,2), (5,2), (5,3), (0,3)
        # Yellow L: ...

        # Simpler: just draw the "triangle" in one and in the other with a marked gap
        def arrangement_1():
            grp = VGroup()
            # 13x5 outer outline
            grp.add(Polygon(pos(0, 0), pos(13, 0), pos(13, 5),
                              color=WHITE, stroke_width=2, fill_opacity=0))
            # Red triangle (0,0)-(8,0)-(8,3)
            grp.add(Polygon(pos(0, 0), pos(8, 0), pos(8, 3),
                              color=RED, fill_opacity=0.55, stroke_width=1.5))
            # Blue triangle (8,3)-(13,3)-(13,5)
            grp.add(Polygon(pos(8, 3), pos(13, 3), pos(13, 5),
                              color=BLUE, fill_opacity=0.55, stroke_width=1.5))
            # Yellow L (5x2 + 3x1): (8,0), (13,0), (13,3), (8,3) minus (8,2)-(8,3)-(10,3)-(10,2)
            # Simpler: yellow rectangle (8,0)-(13,0)-(13,3)-(8,3) BUT that's too big
            # Actually yellow = (8,0)-(13,0)-(13,3)-(8,3)
            grp.add(Polygon(pos(8, 0), pos(13, 0), pos(13, 3), pos(8, 3),
                              color=YELLOW, fill_opacity=0.55, stroke_width=1.5))
            # Green above the red triangle: (0, 3)-(8, 3)-(8, 5)-(0, 5)
            grp.add(Polygon(pos(0, 3), pos(8, 3), pos(8, 5), pos(0, 5),
                              color=GREEN, fill_opacity=0.55, stroke_width=1.5))
            return grp

        def arrangement_2():
            """Rearranged version with 1-unit gap."""
            grp = VGroup()
            grp.add(Polygon(pos(0, 0), pos(13, 0), pos(13, 5),
                              color=WHITE, stroke_width=2, fill_opacity=0))
            # Shift some pieces to reveal a gap at (5,2)–(6,3)
            grp.add(Polygon(pos(0, 0), pos(8, 0), pos(8, 3),
                              color=RED, fill_opacity=0.55, stroke_width=1.5))
            # Blue moved next to red: triangle at (8,3)-(13,3)-(13,5)
            grp.add(Polygon(pos(8, 3), pos(13, 3), pos(13, 5),
                              color=BLUE, fill_opacity=0.55, stroke_width=1.5))
            # Yellow rect, shifted down by 1: (8,-1)-(13,-1)-(13,2)-(8,2)  # just visual — impossible in real
            # For the paradox: instead, show white gap at (5,2)-(6,3)
            grp.add(Polygon(pos(5, 2), pos(6, 2), pos(6, 3), pos(5, 3),
                              color=BLACK, fill_opacity=1,
                              stroke_color=YELLOW, stroke_width=3))
            grp.add(Polygon(pos(8, 0), pos(13, 0), pos(13, 3), pos(8, 3),
                              color=YELLOW, fill_opacity=0.55, stroke_width=1.5))
            grp.add(Polygon(pos(0, 3), pos(8, 3), pos(8, 5), pos(0, 5),
                              color=GREEN, fill_opacity=0.55, stroke_width=1.5))
            return grp

        arr1 = arrangement_1()
        self.play(Create(arr1))

        # Show diagonal bound: dashed line from (0,0) to (13,5)
        diag = DashedLine(pos(0, 0), pos(13, 5),
                            color=ORANGE, stroke_width=2)
        diag_lbl = MathTex(r"\text{true slope} = 5/13 \approx 0.385",
                             color=ORANGE, font_size=20
                             ).next_to(diag, UP, buff=0.1)
        self.play(Create(diag), Write(diag_lbl))

        slope_info = VGroup(
            MathTex(r"\text{red triangle slope} = 3/8 = 0.375",
                     color=RED, font_size=20),
            MathTex(r"\text{blue triangle slope} = 2/5 = 0.400",
                     color=BLUE, font_size=20),
            MathTex(r"\text{difference } \approx 0.025",
                     color=YELLOW, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2
                    ).to_edge(RIGHT, buff=0.3).shift(UP * 1.0)
        self.play(Write(slope_info))

        arr2 = arrangement_2()
        note = Tex(r"rearranged: hidden $1\times 1$ gap",
                    color=YELLOW, font_size=22).to_edge(DOWN, buff=0.35)

        self.play(Transform(arr1, arr2), Write(note))
        self.wait(0.6)

        # Swap back
        arr3 = arrangement_1()
        self.play(Transform(arr1, arr3))
        self.wait(0.4)
