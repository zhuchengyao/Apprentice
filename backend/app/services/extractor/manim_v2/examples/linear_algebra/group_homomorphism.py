from manim import *
import numpy as np


class GroupHomomorphismExample(Scene):
    """
    Concrete homomorphism log: (ℝ⁺, ·) → (ℝ, +).

    THREE_ROW layout:
      TOP    — number line for (ℝ⁺, ·) with two moving dots a, b and a
               third dot a·b at their product. Driven by ValueTrackers.
      MID    — number line for (ℝ, +) with three corresponding dots
               log(a), log(b), log(a)+log(b), placed by always_redraw.
      BOTTOM — verification log(a·b) = log(a) + log(b) shown live with
               numbers updated each frame.

    Two ValueTrackers a and b sweep through several (a, b) pairs. Watch
    the bottom-line dot for log(a) + log(b) sit exactly on log(a·b),
    confirming the structure-preservation axiom.
    """

    def construct(self):
        title = Tex(r"Homomorphism $\log: (\mathbb{R}^+, \cdot) \to (\mathbb{R}, +)$",
                    font_size=32).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # TOP number line: (ℝ⁺, ·) — log scale would be ideal but stick to linear
        # so multiplication is clear.
        nl_top = NumberLine(
            x_range=[0, 12, 2], length=10,
            include_numbers=True,
            decimal_number_config={"num_decimal_places": 0, "font_size": 22},
        ).move_to([0, +1.6, 0])
        top_lbl = Tex(r"$(\mathbb{R}^+, \cdot)$", color=BLUE,
                      font_size=28).next_to(nl_top, LEFT, buff=0.3)
        self.play(Create(nl_top), Write(top_lbl))

        # MID number line: (ℝ, +)
        nl_mid = NumberLine(
            x_range=[-2, 3, 1], length=10,
            include_numbers=True,
            decimal_number_config={"num_decimal_places": 0, "font_size": 22},
        ).move_to([0, -0.8, 0])
        mid_lbl = Tex(r"$(\mathbb{R}, +)$", color=GREEN,
                      font_size=28).next_to(nl_mid, LEFT, buff=0.3)
        self.play(Create(nl_mid), Write(mid_lbl))

        a_tr = ValueTracker(2.0)
        b_tr = ValueTracker(3.0)

        def a_dot():
            return Dot(nl_top.n2p(a_tr.get_value()), color=YELLOW, radius=0.10)

        def b_dot():
            return Dot(nl_top.n2p(b_tr.get_value()), color=ORANGE, radius=0.10)

        def ab_dot():
            return Dot(nl_top.n2p(a_tr.get_value() * b_tr.get_value()),
                       color=RED, radius=0.10)

        def log_a_dot():
            return Dot(nl_mid.n2p(np.log(a_tr.get_value())),
                       color=YELLOW, radius=0.10)

        def log_b_dot():
            return Dot(nl_mid.n2p(np.log(b_tr.get_value())),
                       color=ORANGE, radius=0.10)

        def log_ab_dot():
            v = np.log(a_tr.get_value()) + np.log(b_tr.get_value())
            return Dot(nl_mid.n2p(v), color=RED, radius=0.10)

        # Vertical drop arrows from a, b, ab on top to their log images on mid
        def drop_a():
            return DashedLine(
                a_dot().get_center(), log_a_dot().get_center(),
                color=YELLOW, stroke_width=2, stroke_opacity=0.5,
            )

        def drop_b():
            return DashedLine(
                b_dot().get_center(), log_b_dot().get_center(),
                color=ORANGE, stroke_width=2, stroke_opacity=0.5,
            )

        def drop_ab():
            return DashedLine(
                ab_dot().get_center(), log_ab_dot().get_center(),
                color=RED, stroke_width=2, stroke_opacity=0.5,
            )

        # Labels above each top dot showing its value
        def lbl_a():
            return MathTex(rf"a = {a_tr.get_value():.2f}",
                           color=YELLOW, font_size=22).next_to(
                a_dot(), UP, buff=0.1)

        def lbl_b():
            return MathTex(rf"b = {b_tr.get_value():.2f}",
                           color=ORANGE, font_size=22).next_to(
                b_dot(), UP, buff=0.1)

        def lbl_ab():
            return MathTex(rf"a\cdot b = {a_tr.get_value() * b_tr.get_value():.2f}",
                           color=RED, font_size=22).next_to(
                ab_dot(), UP, buff=0.1)

        self.add(always_redraw(a_dot), always_redraw(b_dot), always_redraw(ab_dot),
                 always_redraw(log_a_dot), always_redraw(log_b_dot), always_redraw(log_ab_dot),
                 always_redraw(drop_a), always_redraw(drop_b), always_redraw(drop_ab),
                 always_redraw(lbl_a), always_redraw(lbl_b), always_redraw(lbl_ab))

        # BOTTOM identity readout
        def identity_panel():
            a, b = a_tr.get_value(), b_tr.get_value()
            la, lb = np.log(a), np.log(b)
            return MathTex(
                rf"\log({a:.2f}\cdot{b:.2f}) = {np.log(a*b):.4f}"
                rf"\;=\;{la:.4f} + {lb:.4f} = \log({a:.2f}) + \log({b:.2f})",
                color=YELLOW, font_size=24,
            ).move_to([0, -2.7, 0])

        self.add(always_redraw(identity_panel))

        # Sweep through several (a, b) pairs
        for av, bv in [(4.0, 1.5), (1.5, 6.0), (3.0, 3.5),
                       (2.5, 4.0), (5.5, 1.8)]:
            self.play(a_tr.animate.set_value(av),
                      b_tr.animate.set_value(bv),
                      run_time=2.0, rate_func=smooth)
            self.wait(0.3)

        # Final identity at top
        rule = MathTex(
            r"\varphi(a \cdot b) = \varphi(a) + \varphi(b)",
            color=GREEN, font_size=32,
        ).next_to(title, DOWN, buff=0.3)
        self.play(Write(rule))
        self.wait(1.0)
