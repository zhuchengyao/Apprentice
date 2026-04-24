from manim import *
import itertools


class FiveChooseThreeEnumeration(Scene):
    """Visualize C(5,3) = 10 by listing all 3-element subsets of {A,B,C,D,E}.
    Five people shown as labeled circles; each of the 10 subsets rendered
    as a miniature copy of the row with the chosen three highlighted
    YELLOW and the excluded two faded."""

    def construct(self):
        title = Tex(
            r"$\binom{5}{3} = 10$: every way to choose 3 from 5",
            font_size=30,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        people_labels = ["A", "B", "C", "D", "E"]

        def make_row(scale=1.0, highlight=None):
            row = VGroup()
            for i, lab in enumerate(people_labels):
                if highlight is not None and i in highlight:
                    c = Circle(radius=0.28, color=YELLOW,
                               fill_opacity=0.7, stroke_width=2)
                    t = Tex(lab, font_size=22, color=BLACK)
                else:
                    c = Circle(radius=0.28, color=GREY_B,
                               fill_opacity=0.15, stroke_width=2)
                    t = Tex(lab, font_size=22, color=GREY_B)
                t.move_to(c)
                grp = VGroup(c, t).shift(RIGHT * i * 0.65)
                row.add(grp)
            row.scale(scale)
            return row

        main_row = make_row(scale=1.0).move_to([0, 1.8, 0])
        self.play(LaggedStart(*[FadeIn(p) for p in main_row],
                              lag_ratio=0.1))

        subsets = list(itertools.combinations(range(5), 3))
        mini_rows = VGroup()
        positions = []
        cols = 5
        for idx, sub in enumerate(subsets):
            r = idx // cols
            c = idx % cols
            x = -5.2 + c * 2.6
            y = 0.1 - r * 1.5
            row = make_row(scale=0.55, highlight=set(sub)).move_to(
                [x, y, 0]
            )
            lab = Tex(
                "{" + ", ".join(people_labels[i] for i in sub) + "}",
                font_size=20, color=YELLOW,
            ).next_to(row, DOWN, buff=0.1)
            mini_rows.add(VGroup(row, lab))
            positions.append((x, y))

        self.play(LaggedStart(*[FadeIn(m) for m in mini_rows],
                              lag_ratio=0.1, run_time=3))

        formula = MathTex(
            r"\binom{5}{3} = \frac{5!}{3!\,2!} = \frac{120}{6 \cdot 2} = 10",
            font_size=30, color=YELLOW,
        )
        formula.to_edge(DOWN, buff=0.3)
        box = SurroundingRectangle(formula, color=YELLOW,
                                   buff=0.15, stroke_width=3)
        self.play(Write(formula), Create(box))
        self.wait(1.3)
