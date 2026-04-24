from manim import *
import numpy as np
from math import comb, factorial


class NChooseKFormulaExample(Scene):
    """
    Deriving C(n, k) = n! / (k!(n-k)!) by the orderings argument:
    pick k in order (n·(n-1)...(n-k+1) ways), then divide by the k!
    reorderings of the same subset.

    TWO_COLUMN:
      LEFT  — row of n dots; ordered pick animation: ValueTracker
              step_tr highlights k=3 dots in order with labels 1,
              2, 3 above, then Transform relabels them unordered.
      RIGHT — live derivation chain n! / ((n-k)! k!) step by step.
    """

    def construct(self):
        title = Tex(r"$\binom{n}{k} = \dfrac{n!}{k!\,(n-k)!}$ via orderings",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        n, k = 6, 3
        positions = [np.array([-4.5 + i * 1.1, 1.5, 0]) for i in range(n)]
        base_circles = VGroup()
        for i, p in enumerate(positions):
            c = Circle(radius=0.3, color=WHITE, stroke_width=2,
                        fill_opacity=0.1).move_to(p)
            lbl = MathTex(str(i + 1), font_size=22).move_to(p)
            base_circles.add(VGroup(c, lbl))
        self.play(FadeIn(base_circles))

        # Phase 1: ordered pick of (3, 1, 5) (= indices 2, 0, 4)
        pick_order = [2, 0, 4]
        order_labels = VGroup()
        for step, idx in enumerate(pick_order):
            self.play(
                base_circles[idx].animate.set_color(YELLOW),
                run_time=0.5,
            )
            ol = MathTex(str(step + 1), color=RED, font_size=24
                          ).next_to(positions[idx], UP, buff=0.2)
            order_labels.add(ol)
            self.play(Write(ol), run_time=0.4)
            self.wait(0.2)

        # Right column derivation, revealed step by step
        step_tr = ValueTracker(0)
        steps = VGroup(
            MathTex(r"\text{ordered picks: } n(n-1)\cdots(n-k+1)",
                     font_size=22, color=BLUE),
            MathTex(rf"= {n} \cdot {n-1} \cdot {n-2} = {n*(n-1)*(n-2)}",
                     font_size=22, color=BLUE),
            MathTex(r"= \dfrac{n!}{(n-k)!}",
                     font_size=22, color=BLUE),
            MathTex(r"\text{each subset counted } k! \text{ times}",
                     font_size=22, color=ORANGE),
            MathTex(rf"k! = {factorial(k)}",
                     font_size=22, color=ORANGE),
            MathTex(r"\binom{n}{k} = \dfrac{n!}{k!(n-k)!}",
                     font_size=26, color=GREEN),
            MathTex(rf"\binom{{{n}}}{{{k}}} = \dfrac{{{n*(n-1)*(n-2)}}}{{{factorial(k)}}} = {comb(n, k)}",
                     font_size=26, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.7, -0.5, 0])

        def revealed():
            t = int(round(step_tr.get_value()))
            g = VGroup()
            for i, s in enumerate(steps):
                if i < t:
                    g.add(s)
            return g

        self.add(always_redraw(revealed))

        for i in range(1, len(steps) + 1):
            self.play(step_tr.animate.set_value(i), run_time=0.8)
            self.wait(0.4)

        # Phase 2: show the k! = 6 orderings of the same {1, 3, 5}
        # transforming between them
        orderings = [
            [2, 0, 4], [2, 4, 0], [0, 2, 4],
            [0, 4, 2], [4, 2, 0], [4, 0, 2],
        ]

        note = Tex(r"These $3! = 6$ orderings produce the same subset $\{1, 3, 5\}$",
                    color=YELLOW, font_size=22).to_edge(DOWN, buff=0.35)
        self.play(Write(note))

        for o in orderings[1:]:
            anims = []
            new_order = VGroup()
            for step, idx in enumerate(o):
                new_lbl = MathTex(str(step + 1), color=RED, font_size=24
                                    ).next_to(positions[idx], UP, buff=0.2)
                new_order.add(new_lbl)
            self.play(Transform(order_labels, new_order),
                       run_time=0.7)
        self.wait(0.5)
