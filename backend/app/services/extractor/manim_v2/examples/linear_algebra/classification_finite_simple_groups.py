from manim import *
import numpy as np


class ClassificationFiniteSimpleGroups(Scene):
    """The classification of finite simple groups, one of the great
    achievements of 20th-century mathematics: every finite simple group
    is either a cyclic group of prime order, an alternating group A_n
    (n >= 5), a group of Lie type (16 infinite families), or one of
    exactly 26 sporadic groups — with the Monster M at the top."""

    def construct(self):
        title = Tex(
            r"Classification of finite simple groups",
            font_size=30,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        boxes = []

        def make_box(text, color, width=4.5, height=1.0):
            box = RoundedRectangle(
                corner_radius=0.15,
                width=width, height=height,
                color=color, stroke_width=3,
                fill_opacity=0.15,
            )
            lab = Tex(text, font_size=22, color=color).move_to(box)
            return VGroup(box, lab)

        cyclic = make_box(
            r"Cyclic groups $\mathbb{Z}_p$ of prime order\\"
            r"(infinitely many)", BLUE,
        )
        cyclic.move_to([-4.0, 1.5, 0])

        alt = make_box(
            r"Alternating groups $A_n$, $n \ge 5$\\"
            r"(infinitely many)", GREEN,
        )
        alt.move_to([0, 1.5, 0])

        lie = make_box(
            r"Groups of Lie type\\"
            r"(16 infinite families)", ORANGE,
        )
        lie.move_to([4.0, 1.5, 0])

        sporadic = make_box(
            r"26 sporadic groups\\(exceptional)", RED,
            width=5.5, height=1.0,
        )
        sporadic.move_to([-2.5, -0.3, 0])

        monster = make_box(
            r"Monster group $M$\\"
            r"$|M| \approx 8 \times 10^{53}$",
            YELLOW, width=5.2, height=1.1,
        )
        monster.move_to([3.0, -0.3, 0])

        self.play(FadeIn(cyclic))
        self.play(FadeIn(alt))
        self.play(FadeIn(lie))
        self.play(FadeIn(sporadic))
        self.play(FadeIn(monster))

        arrow = Arrow(
            sporadic.get_right(), monster.get_left(),
            buff=0.15, color=YELLOW, stroke_width=3,
            max_tip_length_to_length_ratio=0.15,
        )
        self.play(GrowArrow(arrow))

        monster_order = MathTex(
            r"|M| = 2^{46}\cdot 3^{20}\cdot 5^{9}\cdot 7^{6}\cdot 11^{2}"
            r"\cdot 13^{3}\cdot 17\cdot 19\cdot 23\cdot 29\cdot 31"
            r"\cdot 41\cdot 47\cdot 59\cdot 71",
            font_size=20, color=YELLOW,
        )
        monster_order.to_edge(DOWN, buff=0.7)
        self.play(Write(monster_order))

        moonshine = Tex(
            r"Monstrous moonshine: $M$ $\Leftrightarrow$ modular $j$-function — "
            r"the most surprising connection in 20th-c. math.",
            font_size=22, color=YELLOW,
        ).to_edge(DOWN, buff=0.2)
        self.play(FadeIn(moonshine))
        self.wait(1.5)
