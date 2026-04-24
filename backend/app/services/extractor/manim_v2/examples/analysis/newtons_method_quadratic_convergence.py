from manim import *
import numpy as np


class NewtonsMethodQuadraticConvergence(Scene):
    """Newton's method for finding a root of f(x).  At each step,
    x_{n+1} = x_n - f(x_n)/f'(x_n) — the tangent line at x_n crosses
    the x-axis at x_{n+1}.  Convergence is quadratic: |x_n - root|
    squared at each step.  Visualize 5 iterations on f(x) = x^3 - 2x - 5
    starting at x0 = 2.5 -> true root ~ 2.0946."""

    def construct(self):
        title = Tex(
            r"Newton's method: tangent $\to$ x-axis $\to$ iterate",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        def f(x):
            return x ** 3 - 2 * x - 5

        def fp(x):
            return 3 * x * x - 2

        axes = Axes(
            x_range=[1, 3, 0.5],
            y_range=[-3, 12, 3],
            x_length=7.5, y_length=5.0,
            tips=False,
            axis_config={"stroke_width": 1.5, "include_ticks": True},
        ).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        x_lab = MathTex("x", font_size=24).next_to(
            axes.x_axis.get_end(), DOWN, buff=0.1
        )
        y_lab = MathTex("f(x)", font_size=22).next_to(
            axes.y_axis.get_end(), LEFT, buff=0.1
        )
        curve = axes.plot(f, x_range=[1.2, 2.9, 0.01],
                          color=BLUE, stroke_width=3)
        self.play(Create(axes), FadeIn(x_lab), FadeIn(y_lab),
                  Create(curve))

        true_root = 2.094551482
        root_dot = Dot(axes.c2p(true_root, 0), radius=0.09,
                       color=GREEN).set_z_index(5)
        root_lab = MathTex(
            rf"x^* \approx {true_root:.4f}",
            font_size=22, color=GREEN,
        ).next_to(root_dot, DOWN, buff=0.15)
        self.play(FadeIn(root_dot), FadeIn(root_lab))

        x = 2.5
        history = [x]
        for _ in range(5):
            x = x - f(x) / fp(x)
            history.append(x)

        log = VGroup(
            Tex(r"iter\ \ $x_n$\ \ \ \ $|x_n - x^*|$",
                font_size=22, color=YELLOW),
        )
        y = 2.4
        log[0].move_to([3.2, y, 0])
        y -= 0.5
        error_history = []
        for i, xn in enumerate(history):
            err = abs(xn - true_root)
            error_history.append(err)
            row = MathTex(
                rf"{i}\ \ \ \ \ {xn:.6f}\ \ \ \ \ {err:.2e}",
                font_size=22,
            )
            row.move_to([3.2, y, 0])
            log.add(row)
            y -= 0.38

        self.play(FadeIn(log[0]))

        for i in range(len(history) - 1):
            xn = history[i]
            yn = f(xn)
            dot_on_curve = Dot(axes.c2p(xn, yn), radius=0.08,
                               color=RED).set_z_index(4)
            x_axis_dot = Dot(axes.c2p(xn, 0), radius=0.07,
                             color=YELLOW).set_z_index(4)
            vertical = DashedLine(
                axes.c2p(xn, 0), axes.c2p(xn, yn),
                color=GREY_B, stroke_width=2,
            )
            slope = fp(xn)
            x_next = history[i + 1]
            tangent = Line(
                axes.c2p(xn, yn),
                axes.c2p(x_next, 0),
                color=ORANGE, stroke_width=3,
            )
            next_dot = Dot(axes.c2p(x_next, 0), radius=0.07,
                           color=YELLOW).set_z_index(4)
            self.play(FadeIn(x_axis_dot), Create(vertical),
                      FadeIn(dot_on_curve), run_time=0.5)
            self.play(Create(tangent), FadeIn(next_dot),
                      run_time=0.6)
            self.play(FadeIn(log[i + 1]), run_time=0.3)

        quad_note = Tex(
            r"Quadratic convergence: each error is squared $\to$ double the correct digits per step.",
            font_size=22, color=YELLOW,
        ).to_edge(DOWN, buff=0.25)
        self.play(FadeIn(log[-1]))
        self.play(FadeIn(quad_note))
        self.wait(1.5)
