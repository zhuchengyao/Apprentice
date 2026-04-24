from manim import *
import numpy as np


class TriangleOfPowerExample(Scene):
    """
    The triangle-of-power notation unifies exponent, log, and root
    into one symbol with three corners filled in.

    SINGLE_FOCUS:
      Triangle with three corners labeled a (top-left), b (bottom),
      c (top-right). Any two filled → the third is derived.
      ValueTracker step_tr sequentially highlights the three derived
      forms (exp, root, log) via Transform between corner fill
      arrangements.
    """

    def construct(self):
        title = Tex(r"Triangle of power: $a\square = b$ depending on which corner is missing",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Triangle geometry
        A = np.array([-1.5, 1.2, 0])  # top-left corner (base/log arg)
        B = np.array([0.0, -1.8, 0])  # bottom corner (result)
        C = np.array([1.5, 1.2, 0])   # top-right corner (exponent)
        tri = Polygon(A, B, C, color=WHITE, stroke_width=3)
        self.play(Create(tri))

        def triangle_with(a_val, b_val, c_val, solved_corner, eq_text):
            g = VGroup()
            g.add(tri.copy())
            colors = {0: BLUE, 1: GREEN, 2: RED}
            positions = [A, B, C]
            vals = [a_val, b_val, c_val]
            for i in range(3):
                c = colors[i]
                v = vals[i]
                if i == solved_corner:
                    # Filled circle with value + "?" below to highlight
                    circ = Circle(radius=0.32, color=YELLOW,
                                    fill_opacity=0.8
                                    ).move_to(positions[i])
                    lbl = MathTex(rf"\mathbf{{{v}}}",
                                    color=BLACK, font_size=24
                                    ).move_to(positions[i])
                    g.add(circ, lbl)
                else:
                    circ = Circle(radius=0.28, color=c,
                                    fill_opacity=0.5, stroke_width=2
                                    ).move_to(positions[i])
                    lbl = MathTex(rf"{v}", color=WHITE,
                                    font_size=22
                                    ).move_to(positions[i])
                    g.add(circ, lbl)
            eq = MathTex(eq_text, color=YELLOW, font_size=26
                           ).to_edge(DOWN, buff=0.6)
            g.add(eq)
            return g

        # Example: a = 2, c = 3, b = 8
        e1 = triangle_with(2, 8, 3, solved_corner=1,
                            eq_text=r"\text{exponent: } b = a^c = 2^3 = 8")
        e2 = triangle_with(2, 8, 3, solved_corner=0,
                            eq_text=r"\text{root: } a = \sqrt[c]{b} = \sqrt[3]{8} = 2")
        e3 = triangle_with(2, 8, 3, solved_corner=2,
                            eq_text=r"\text{log: } c = \log_a b = \log_2 8 = 3")

        step_tr = ValueTracker(0)
        states = [e1, e2, e3]
        current = e1
        self.play(FadeIn(current))
        self.wait(1.0)

        for target in [1, 2]:
            self.play(Transform(current, states[target]), run_time=1.5)
            self.wait(1.0)

        note = Tex(r"Same triangle, three operations",
                    color=GREEN, font_size=22).next_to(title, DOWN, buff=0.3)
        self.play(Write(note))
        self.wait(0.5)
