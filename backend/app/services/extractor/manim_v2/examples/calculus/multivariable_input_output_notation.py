from manim import *
import numpy as np


class MultivariableInputOutputNotation(Scene):
    """C(x_1, ..., x_n) feeds many inputs into a single scalar output;
    collapse to C(x, y) to visualize the two-input case."""

    def construct(self):
        title = Tex(
            r"A multi-input function yields one scalar output",
            font_size=26,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        func = MathTex(
            "C(", "x_1,", "x_2,", r"\dots,", "x_n", ")", "=",
            font_size=44,
        )
        func.shift(1.8 * LEFT)
        self.play(FadeIn(func))

        inputs = func[1:-2]
        inputs_brace = Brace(inputs, UP, buff=0.06)
        inputs_label = Tex(
            "Multiple inputs", font_size=26, color=YELLOW
        ).next_to(inputs_brace, UP, buff=0.06)
        self.play(GrowFromCenter(inputs_brace), Write(inputs_label))

        out = DecimalNumber(1.0, num_decimal_places=3, font_size=44)
        out.next_to(func, RIGHT, buff=0.18)
        t_tr = ValueTracker(0.0)
        out.add_updater(lambda m: m.set_value(1 + np.sin(t_tr.get_value())))
        self.add(out)

        out_brace = Brace(out, DOWN, buff=0.1)
        out_label = Tex(
            "Single output", font_size=26, color=GREEN
        ).next_to(out_brace, DOWN, buff=0.06)
        self.play(GrowFromCenter(out_brace), Write(out_label))

        self.play(t_tr.animate.set_value(3 * PI), run_time=5, rate_func=linear)

        alt_func = MathTex("C(", "x,", "y", ")", "=", font_size=44)
        alt_func.move_to(func, RIGHT)
        self.play(
            FadeOut(inputs_brace),
            FadeOut(inputs_label),
            ReplacementTransform(func, alt_func),
        )
        self.wait(0.3)
        self.play(t_tr.animate.set_value(5 * PI), run_time=3, rate_func=linear)
        out.clear_updaters()
        self.wait(0.8)
