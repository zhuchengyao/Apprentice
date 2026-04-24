from manim import *
import numpy as np


class EulerFormulaAdditionInvariance(Scene):
    """Build up a planar graph edge-by-edge, watching V - E + F = 2 stay
    invariant.  Each new edge either (a) ends at an existing vertex —
    closing a cycle and adding a new face (E += 1, F += 1) or (b) ends at a
    brand-new vertex — extending a tree (V += 1, E += 1).  Either way the
    sum V - E + F doesn't change."""

    def construct(self):
        title = MathTex(
            r"V - E + F = 2\ \text{stays invariant}",
            font_size=32,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        positions = {
            1: np.array([-4, 1.0, 0]),
            2: np.array([-2, 2.0, 0]),
            3: np.array([-2, 0.0, 0]),
            4: np.array([0, 1.0, 0]),
            5: np.array([2, 2.0, 0]),
            6: np.array([2, 0.0, 0]),
        }

        vdots = {}
        for k, p in positions.items():
            d = Dot(p, radius=0.11, color=BLUE).set_z_index(5)
            vdots[k] = d

        V_val = Integer(0, font_size=30, color=BLUE)
        E_val = Integer(0, font_size=30, color=ORANGE)
        F_val = Integer(1, font_size=30, color=GREEN)
        sum_val = DecimalNumber(
            1.0, num_decimal_places=0, font_size=32, color=YELLOW,
        )
        panel = VGroup(
            VGroup(MathTex("V=", font_size=30), V_val).arrange(RIGHT, buff=0.1),
            VGroup(MathTex("E=", font_size=30), E_val).arrange(RIGHT, buff=0.1),
            VGroup(MathTex("F=", font_size=30), F_val).arrange(RIGHT, buff=0.1),
            VGroup(MathTex("V - E + F =", font_size=30),
                   sum_val).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        panel.to_edge(RIGHT, buff=0.4).shift(UP * 0.3)
        self.play(FadeIn(panel))

        def update_counts(V, E, F):
            V_val.set_value(V)
            E_val.set_value(E)
            F_val.set_value(F)
            sum_val.set_value(V - E + F)

        note = Tex("", font_size=26, color=YELLOW)
        note.to_edge(DOWN, buff=0.45)
        self.add(note)

        def set_note(new_text, color=YELLOW):
            new = Tex(new_text, font_size=26, color=color).move_to(note)
            self.play(Transform(note, new), run_time=0.35)

        V, E, F = 0, 0, 1

        self.play(FadeIn(vdots[1]))
        V += 1
        update_counts(V, E, F)
        set_note("New vertex 1: $V{+}1$, $F$ unchanged")

        for k in [2, 3, 4, 5, 6]:
            self.play(FadeIn(vdots[k]))
            V += 1
            update_counts(V, E, F)

        set_note("6 isolated vertices: $V=6, E=0, F=1$, total $= 7$")
        self.wait(0.5)

        tree_edges = [(1, 2), (1, 3), (3, 4), (4, 5), (4, 6)]
        cycle_edges = [(2, 4), (5, 6)]

        for a, b in tree_edges:
            line = Line(positions[a], positions[b],
                        color=WHITE, stroke_width=3)
            self.play(Create(line), run_time=0.4)
            E += 1
            update_counts(V, E, F)
            set_note(
                rf"new edge ({a},{b}): endpoint is new? $V$ grew earlier; now $E{{+}}1$, $F$ unchanged"
            )

        set_note("Tree built: $V-E+F = 6-5+1 = 2$", YELLOW)
        self.wait(0.5)

        for a, b in cycle_edges:
            line = Line(positions[a], positions[b],
                        color=PURPLE, stroke_width=3)
            self.play(Create(line), run_time=0.5)
            E += 1
            F += 1
            update_counts(V, E, F)
            set_note(
                rf"cycle edge ({a},{b}) closes a new face: $E{{+}}1$, $F{{+}}1$"
            )

        set_note(
            r"Always invariant: $V - E + F = 2$ — Euler's formula!", GREEN,
        )
        self.wait(1.5)
