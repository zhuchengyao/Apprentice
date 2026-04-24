from manim import *


class DerivativeIsLinearOperatorExample(Scene):
    """
    Derivative is a linear operator:
       d/dx (f + g) = df/dx + dg/dx
       d/dx (c·f) = c · df/dx
    """

    def construct(self):
        title = Tex(r"Derivative is a linear operator",
                    font_size=30).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Additivity property
        add_prop = MathTex(r"\frac{d}{dx}(f+g)", r"=", r"\frac{df}{dx}+\frac{dg}{dx}",
                            font_size=40).shift(UP * 1.5)
        self.play(Write(add_prop))
        self.wait(0.5)

        # Scaling property
        scale_prop = MathTex(r"\frac{d}{dx}(c\cdot f)", r"=", r"c\cdot\frac{df}{dx}",
                              font_size=40).shift(UP * 0.2)
        self.play(Write(scale_prop))
        self.wait(0.5)

        # Definition
        defn = Tex(r"Two properties = `linearity'",
                    color=YELLOW, font_size=28).shift(DOWN * 0.8)
        self.play(Write(defn))
        self.wait(0.3)

        arrow = Arrow(defn.get_bottom() + DOWN * 0.1,
                       defn.get_bottom() + DOWN * 0.9, color=YELLOW)
        self.play(Create(arrow))

        conclusion = Tex(r"derivative $=$ linear `transformation' on function space",
                          color=GREEN, font_size=28).shift(DOWN * 2.3)
        self.play(Write(conclusion))
        self.wait(1.0)
