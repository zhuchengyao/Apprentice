from manim import *


class SimilarityTransformMatrixExample(Scene):
    """M_Jenny = A^(-1) M A (similarity transform)."""

    def construct(self):
        title = Tex(r"Same transformation in Jenny's basis: $M_J=A^{-1}MA$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        nodes = [r"$\vec v_J$", r"$\vec v$", r"$M\vec v$", r"(M\vec v)_J"]
        node_mobs = [MathTex(n, font_size=36) for n in nodes]
        node_row = VGroup(*node_mobs).arrange(RIGHT, buff=1.5).shift(UP * 0.3)
        self.add(node_row)

        arrow_labels = [r"$A$ (to standard)", r"$M$", r"$A^{-1}$ (back to Jenny)"]
        arrows = VGroup()
        for i in range(3):
            arr = Arrow(node_mobs[i].get_right() + RIGHT * 0.1,
                         node_mobs[i + 1].get_left() + LEFT * 0.1,
                         color=YELLOW, buff=0.05, stroke_width=3)
            lbl = Tex(arrow_labels[i], font_size=18, color=YELLOW).next_to(arr, UP, buff=0.15)
            arrows.add(arr, lbl)
        self.play(Create(arrows))
        self.wait(0.5)

        compose_lbl = Tex(r"Compose: $M_J=A^{-1}MA$", color=GREEN, font_size=32).shift(DOWN * 1.0)
        brace = Brace(VGroup(node_mobs[0], node_mobs[-1]), DOWN, buff=0.3)
        self.play(GrowFromCenter(brace), Write(compose_lbl))
        self.wait(0.4)

        self.play(Write(
            Tex(r"e.g. $M=$ rotation; $M_J$ depends on Jenny's basis",
                 color=YELLOW, font_size=22).to_edge(DOWN, buff=0.5)
        ))
        self.wait(1.0)
