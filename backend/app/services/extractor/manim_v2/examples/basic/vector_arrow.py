from manim import *


class VectorArrowExample(Scene):
    def construct(self):
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            background_line_style={"stroke_opacity": 0.3},
        )
        origin = Dot(ORIGIN, color=WHITE)
        tip = np.array([2, 1, 0])
        arrow = Arrow(start=ORIGIN, end=tip, buff=0, color=YELLOW)
        label = MathTex(r"\vec{v} = (2, 1)").next_to(arrow.get_end(), UR, buff=0.1)

        self.play(Create(plane), FadeIn(origin))
        self.play(GrowArrow(arrow))
        self.play(Write(label))
        self.wait(0.6)
