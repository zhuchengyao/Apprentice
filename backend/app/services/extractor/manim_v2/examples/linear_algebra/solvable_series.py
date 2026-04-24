from manim import *
import numpy as np


class SolvableSeriesExample(Scene):
    """
    Solvability by radicals ↔ the Galois group has a normal series
    with abelian quotients. S_4 is solvable via S_4 ⊃ A_4 ⊃ V_4 ⊃ {e};
    S_5 is NOT solvable because A_5 is simple (no nontrivial normal
    subgroup).

    COMPARISON:
      LEFT panel — S_4 chain visualized as nested circles, each step
                   labeled with its quotient order (also abelian);
                   ValueTracker step_tr reveals each level.
      RIGHT panel — S_5 chain stops: A_5 is simple; revealing the
                    obstruction.
    """

    def construct(self):
        title = Tex(r"Galois solvability: $S_4$ (solvable) vs $S_5$ (unsolvable)",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # LEFT: S_4 chain of nested circles
        left_center = np.array([-3.6, -0.3, 0])
        s4_chain = [
            ("S_4", 24, WHITE),
            ("A_4", 12, BLUE),
            ("V_4", 4, GREEN),
            (r"\{e\}", 1, YELLOW),
        ]
        s4_radii = [2.4, 1.8, 1.2, 0.4]
        s4_circles = VGroup()
        s4_labels = VGroup()
        for i, ((nm, ord_, col), r) in enumerate(zip(s4_chain, s4_radii)):
            c = Circle(radius=r, color=col, stroke_width=3,
                        fill_opacity=0.1).move_to(left_center)
            lbl = MathTex(nm, color=col, font_size=24
                           ).move_to(left_center
                                      + np.array([0, r - 0.25, 0]))
            s4_circles.add(c)
            s4_labels.add(lbl)

        s4_quotients = VGroup(
            MathTex(r"S_4/A_4 \cong \mathbb Z_2", font_size=20, color=BLUE),
            MathTex(r"A_4/V_4 \cong \mathbb Z_3", font_size=20, color=GREEN),
            MathTex(r"V_4/\{e\} \cong \mathbb Z_2 \times \mathbb Z_2",
                     font_size=20, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18
                    ).move_to(left_center + np.array([0, -3.0, 0]))

        # RIGHT: S_5 chain
        right_center = np.array([3.6, -0.3, 0])
        s5_chain = [
            ("S_5", 120, WHITE),
            ("A_5", 60, RED),
        ]
        s5_radii = [2.4, 1.8]
        s5_circles = VGroup()
        s5_labels = VGroup()
        for (nm, ord_, col), r in zip(s5_chain, s5_radii):
            c = Circle(radius=r, color=col, stroke_width=3,
                        fill_opacity=0.15).move_to(right_center)
            lbl = MathTex(nm, color=col, font_size=24
                           ).move_to(right_center
                                      + np.array([0, r - 0.25, 0]))
            s5_circles.add(c)
            s5_labels.add(lbl)

        s5_obstruction = VGroup(
            Tex(r"$A_5$ is simple:", color=RED, font_size=20),
            MathTex(r"\text{no nontrivial normal subgroup}",
                     color=RED, font_size=20),
            MathTex(r"\Rightarrow S_5 \text{ unsolvable}",
                     color=YELLOW, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15
                    ).move_to(right_center + np.array([0, -3.0, 0]))

        step_tr = ValueTracker(0)

        def s4_group():
            s = int(round(step_tr.get_value()))
            grp = VGroup()
            for i in range(min(s, len(s4_circles))):
                grp.add(s4_circles[i], s4_labels[i])
            for i in range(min(max(0, s - 1), len(s4_quotients))):
                grp.add(s4_quotients[i])
            return grp

        def s5_group():
            s = int(round(step_tr.get_value()))
            grp = VGroup()
            for i in range(min(s, len(s5_circles))):
                grp.add(s5_circles[i], s5_labels[i])
            if s >= 3:
                for m in s5_obstruction:
                    grp.add(m)
            return grp

        self.add(always_redraw(s4_group), always_redraw(s5_group))

        for target in [1, 2, 3, 4]:
            self.play(step_tr.animate.set_value(target),
                       run_time=1.0)
            self.wait(0.8)

        self.wait(0.6)
