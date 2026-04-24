from manim import *
import numpy as np


class CompleteTheSquareVisualExample(Scene):
    """
    Geometric "completing the square": rectangle b·x slides under
    the x²-square via a parameter sweep.

    SINGLE_FOCUS animation:
      Stage 1 (t = 0.0): x²-square + b·x rectangle side by side.
      Stage 2 (t : 0 → 1): the b·x rectangle visibly splits into
        TWO half-strips of width b/2; one stays attached to the right
        of the x²-square, the other slides DOWN to attach beneath.
      Stage 3 (t = 1.0): a (b/2)² gap appears at bottom-right; we draw
        the (x + b/2)² big square outline that would close the figure
        if filled.

    ValueTracker t drives the slide.
    """

    def construct(self):
        title = Tex(r"Completing the square: $x^2 + bx = (x + \tfrac{b}{2})^2 - (\tfrac{b}{2})^2$",
                    font_size=26).to_edge(UP, buff=0.4)
        self.play(Write(title))

        x_side = 2.4
        b = 1.4
        half_b = b / 2

        # Anchor x²-square's bottom-left corner
        anchor = np.array([-2.5, -1.6, 0])

        x_sq = Square(side_length=x_side, color=BLUE, fill_opacity=0.55, stroke_width=2)
        x_sq.move_to(anchor + np.array([x_side / 2, x_side / 2, 0]))
        x_lbl = MathTex(r"x^2", color=WHITE, font_size=26).move_to(x_sq.get_center())
        self.play(FadeIn(x_sq), Write(x_lbl))

        # Two half-strips, each width half_b × x_side
        # Stage 1: both stacked together to the right of x_sq, forming a rectangle b × x_side
        t_tr = ValueTracker(0.0)

        def right_strip():
            # Stays glued to the right side of x_sq always (width half_b, height x_side)
            rect = Rectangle(width=half_b, height=x_side,
                             color=ORANGE, fill_opacity=0.55, stroke_width=2)
            rect.move_to(anchor + np.array([x_side + half_b / 2, x_side / 2, 0]))
            return rect

        def moving_strip():
            # At t=0, sits next to right_strip (forming the original b·x rectangle).
            # At t=1, has rotated 90° and moved underneath x_sq, becoming horizontal x_side × half_b.
            t = t_tr.get_value()
            # Interpolate: the strip's centroid moves from (x_side + 1.5*half_b, x_side/2) [vertical]
            #              to (x_side/2, -half_b/2) [horizontal under square]
            start_center = anchor + np.array([x_side + 1.5 * half_b, x_side / 2, 0])
            end_center = anchor + np.array([x_side / 2, -half_b / 2, 0])
            cx, cy, _ = (1 - t) * start_center + t * end_center

            # Width and height interpolate so the strip rotates from vertical to horizontal
            # At t=0: width=half_b, height=x_side
            # At t=1: width=x_side, height=half_b
            w = (1 - t) * half_b + t * x_side
            h = (1 - t) * x_side + t * half_b

            rect = Rectangle(width=w, height=h,
                             color=ORANGE, fill_opacity=0.55, stroke_width=2)
            rect.move_to([cx, cy, 0])
            return rect

        self.add(always_redraw(right_strip), always_redraw(moving_strip))

        # Stage 1 caption: x² + b·x
        caption1 = MathTex(r"x^2 + b x", color=YELLOW,
                           font_size=30).move_to([+3.5, +1.0, 0])
        self.play(Write(caption1))
        self.wait(0.5)

        # Sweep t from 0 to 1: the moving strip slides into place under x_sq
        self.play(t_tr.animate.set_value(1.0), run_time=2.5, rate_func=smooth)
        self.wait(0.5)

        # Stage 3: show the missing (b/2)² corner and the big square outline
        missing = Square(side_length=half_b, color=GREY_D, stroke_width=2,
                         fill_opacity=0.45)
        missing.move_to(anchor + np.array([x_side + half_b / 2, -half_b / 2, 0]))
        missing_lbl = MathTex(r"(\tfrac{b}{2})^2", color=GREY_B, font_size=20).move_to(
            missing.get_center())

        big_square = Square(side_length=x_side + half_b, color=YELLOW,
                            stroke_width=4, fill_opacity=0)
        # Aligned so its bottom-left is at anchor + (0, -half_b)
        big_anchor = anchor + np.array([(x_side + half_b) / 2,
                                        (x_side + half_b) / 2 - half_b, 0])
        big_square.move_to(big_anchor)

        big_lbl = MathTex(r"(x + \tfrac{b}{2})^2", color=YELLOW,
                          font_size=22).next_to(big_square, UP, buff=0.1)

        self.play(FadeIn(missing), Write(missing_lbl))
        self.play(Create(big_square), Write(big_lbl))

        formula = MathTex(
            r"x^2 + bx = (x + \tfrac{b}{2})^2 - (\tfrac{b}{2})^2",
            color=YELLOW, font_size=28,
        ).move_to([+3.5, -2.2, 0])
        self.play(Write(formula))
        self.wait(1.0)
