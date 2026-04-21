from manim import *


class FollowingGraphCameraExample(MovingCameraScene):
    def construct(self):
        axes = Axes(
            x_range=[-1, 10, 1],
            y_range=[-1, 6, 1],
            x_length=9,
            y_length=5,
            tips=False,
        )
        graph = axes.plot(lambda x: 0.5 * x + 1.2, color=BLUE)
        self.play(Create(axes), Create(graph))

        dot = Dot(color=YELLOW).move_to(axes.c2p(0, 1.2))
        self.play(FadeIn(dot))

        # Camera frame follows the dot's x-coordinate.
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.scale(0.5).move_to(dot))
        self.play(
            dot.animate.move_to(axes.c2p(8, 5.2)),
            self.camera.frame.animate.move_to(axes.c2p(8, 5.2)),
            run_time=3,
        )
        self.play(Restore(self.camera.frame))
        self.wait(0.4)
