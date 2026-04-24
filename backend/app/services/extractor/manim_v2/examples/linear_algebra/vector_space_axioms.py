from manim import *


class VectorSpaceAxiomsExample(Scene):
    """
    The 8 vector space axioms define what counts as a "vector space."
    Anything satisfying them — 2D arrows, n-tuples, functions,
    polynomials, matrices — is a vector space.
    """

    def construct(self):
        title = Tex(r"8 axioms: what it takes to be a `vector space'",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axioms = VGroup(
            Tex(r"1. $\vec u+\vec v=\vec v+\vec u$ (commutativity)", font_size=22),
            Tex(r"2. $(\vec u+\vec v)+\vec w=\vec u+(\vec v+\vec w)$ (associativity)", font_size=22),
            Tex(r"3. $\exists\ \vec 0$: $\vec 0+\vec v=\vec v$", font_size=22),
            Tex(r"4. $\forall\vec v\exists-\vec v$: $\vec v+(-\vec v)=\vec 0$", font_size=22),
            Tex(r"5. $c(\vec u+\vec v)=c\vec u+c\vec v$ (distributive)", font_size=22),
            Tex(r"6. $(c+d)\vec v=c\vec v+d\vec v$", font_size=22),
            Tex(r"7. $(cd)\vec v=c(d\vec v)$", font_size=22),
            Tex(r"8. $1\cdot\vec v=\vec v$", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)

        for ax in axioms:
            self.play(Write(ax), run_time=0.35)
        self.wait(0.4)

        # Examples box on right
        examples = VGroup(
            Tex(r"Examples of vector spaces:", color=YELLOW, font_size=22),
            Tex(r"• geometric arrows $\mathbb{R}^n$", font_size=20),
            Tex(r"• tuples, matrices", font_size=20),
            Tex(r"• polynomials $P_n$", font_size=20),
            Tex(r"• continuous functions", font_size=20),
            Tex(r"• solutions to $\nabla^2 u=0$", font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.5)
        self.play(Write(examples))
        self.wait(1.0)
