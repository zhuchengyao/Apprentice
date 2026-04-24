from manim import *
import numpy as np


class InclusionExclusionExample(Scene):
    """
    Inclusion-exclusion for 3 sets:
      |A ∪ B ∪ C| = |A| + |B| + |C| - |AB| - |AC| - |BC| + |ABC|.
    Animated with 3 overlapping circles in a Venn diagram.

    SINGLE_FOCUS:
      3 circles; ValueTracker step_tr reveals the formula term by
      term with each region color coded. Count of elements (from a
      40-element test set) shown live.
    """

    def construct(self):
        title = Tex(r"Inclusion-exclusion: $|A \cup B \cup C| = \Sigma|A| - \Sigma|AB| + |ABC|$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Venn 3 circles
        cA_pos = np.array([-1.0, 0.6, 0])
        cB_pos = np.array([1.0, 0.6, 0])
        cC_pos = np.array([0.0, -1.0, 0])
        R = 1.5

        A = Circle(radius=R, color=BLUE, fill_opacity=0.3,
                     stroke_width=2).move_to(cA_pos)
        B = Circle(radius=R, color=RED, fill_opacity=0.3,
                     stroke_width=2).move_to(cB_pos)
        C = Circle(radius=R, color=GREEN, fill_opacity=0.3,
                     stroke_width=2).move_to(cC_pos)
        A_lbl = MathTex(r"A", color=BLUE, font_size=28
                          ).move_to(cA_pos + np.array([-1.0, 0.8, 0]))
        B_lbl = MathTex(r"B", color=RED, font_size=28
                          ).move_to(cB_pos + np.array([1.0, 0.8, 0]))
        C_lbl = MathTex(r"C", color=GREEN, font_size=28
                          ).move_to(cC_pos + np.array([0, -1.1, 0]))
        self.play(Create(A), Create(B), Create(C),
                   Write(A_lbl), Write(B_lbl), Write(C_lbl))

        # Hardcoded counts for illustration
        counts = {
            "A": 18, "B": 16, "C": 14,
            "AB": 6, "AC": 5, "BC": 4, "ABC": 2,
        }
        # |A∪B∪C| = 18+16+14 - 6-5-4 + 2 = 35
        # By inclusion-exclusion

        step_tr = ValueTracker(0)

        terms_text = [
            r"|A| + |B| + |C| = 48",
            r"- (|AB| + |AC| + |BC|) = -15",
            r"+ |ABC| = +2",
            r"|A \cup B \cup C| = 35",
        ]

        def formula():
            s = int(round(step_tr.get_value())) % (len(terms_text) + 1)
            grp = VGroup()
            for i, t in enumerate(terms_text):
                if i < s:
                    col = YELLOW if i == len(terms_text) - 1 else (WHITE if i != 3 else GREEN)
                    m = MathTex(t, color=col, font_size=22)
                    grp.add(m)
            grp.arrange(DOWN, aligned_edge=LEFT, buff=0.2
                          ).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)
            return grp

        self.add(always_redraw(formula))

        for s in range(1, len(terms_text) + 1):
            self.play(step_tr.animate.set_value(s),
                       run_time=0.9, rate_func=smooth)
            self.wait(1.0)
        self.wait(0.5)
