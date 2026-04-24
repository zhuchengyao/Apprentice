from manim import *
import numpy as np


class PAdicNestedBoxesExample(Scene):
    """
    p-adic distance: |x - y|_p = p^(-v_p(x-y)). Higher p-power
    common factor → smaller p-adic distance → nested deeper boxes.

    SINGLE_FOCUS:
      For p = 3, draw a sequence of nested boxes for an integer x:
        innermost = {x}
        next     = x mod 3 class
        next     = x mod 9 class
        next     = x mod 27 class
        outer    = x mod 81 class
      ValueTracker focus_idx steps highlights one of these classes
      at a time; the active class is YELLOW. A list of integers
      colored by their innermost-shared box shows clustering.
    """

    def construct(self):
        title = Tex(r"$3$-adic distance: nested boxes by shared $3^k$ residue",
                    font_size=24).to_edge(UP, buff=0.4)
        self.play(Write(title))

        x = 25  # reference integer (= 21 + 4 = …)
        # Set of nearby integers
        sample = list(range(0, 64))

        # Group integers by the largest k such that x ≡ y (mod 3^k)
        def shared_power(a, b):
            diff = abs(a - b)
            if diff == 0:
                return 6
            k = 0
            while diff % 3 == 0:
                diff //= 3
                k += 1
            return k

        # Color by shared power
        color_map = {0: BLUE_E, 1: BLUE_D, 2: GREEN, 3: YELLOW, 4: ORANGE,
                     5: RED, 6: WHITE}

        # Layout: number line of integers 0..63
        # Position each as a small dot, arranged in 2 rows
        anchor = np.array([-5.5, -1.0, 0])
        dots = VGroup()
        labels = VGroup()
        positions = {}
        for i, y in enumerate(sample):
            row = i // 32
            col = i % 32
            pos = anchor + np.array([col * 0.34, -row * 0.6, 0])
            positions[y] = pos
            k = shared_power(x, y)
            d = Dot(pos, color=color_map[k], radius=0.10)
            dots.add(d)
            if y % 8 == 0:
                lbl = Tex(rf"${y}$", color=GREY_B, font_size=14).next_to(
                    d, UP, buff=0.05)
                labels.add(lbl)
        self.play(FadeIn(dots), Write(labels))

        # Highlight the reference integer
        ref_circle = Circle(radius=0.18, color=WHITE,
                            stroke_width=3).move_to(positions[x])
        ref_lbl = MathTex(rf"x = {x}", color=WHITE, font_size=22).next_to(
            positions[x], UP, buff=0.6)
        self.play(Create(ref_circle), Write(ref_lbl))

        # Color legend
        legend = VGroup()
        for k in range(0, 6):
            row = VGroup(
                Dot(color=color_map[k], radius=0.10),
                MathTex(rf"k = {k}", color=color_map[k], font_size=18),
                MathTex(rf"|x - y|_3 = 3^{{-{k}}}", color=GREY_B, font_size=18),
            ).arrange(RIGHT, buff=0.15)
            legend.add(row)
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UR).shift(LEFT * 0.4 + DOWN * 0.5)
        self.play(Write(legend))

        principle = Tex(r"Higher $3^k$ shared factor $\to$ smaller $|x-y|_3$",
                        color=YELLOW, font_size=22).to_edge(DOWN, buff=0.4)
        self.play(Write(principle))
        self.wait(1.0)
