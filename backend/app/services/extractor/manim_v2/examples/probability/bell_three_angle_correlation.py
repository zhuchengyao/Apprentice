from manim import *
import numpy as np


class BellThreeAngleCorrelation(Scene):
    """Bell's inequality in its clearest form.  Three polarizer angles
    A = 0°, B = 22.5°, C = 45° send entangled photon pairs through.
    Denote P(X ≠ Y) = probability two measurements disagree.
    Any local-hidden-variable theory obeys:
        P(A ≠ C) ≤ P(A ≠ B) + P(B ≠ C)   (Bell triangle inequality)
    Quantum mechanics predicts P(X ≠ Y) = sin²(θ_X − θ_Y), so:
        sin²(45°) = 0.5   vs   sin²(22.5°) + sin²(22.5°) ≈ 0.293.
    0.5 > 0.293 — the inequality is violated."""

    def construct(self):
        title = Tex(
            r"Bell inequality violation: three polarizer angles",
            font_size=30,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        def polarizer(x, angle_deg, label, color):
            box = Circle(radius=0.55, color=color, stroke_width=3,
                         fill_opacity=0.12)
            axis = Line(
                box.get_center() + rotate_vector(RIGHT * 0.5,
                                                 angle_deg * DEGREES),
                box.get_center() + rotate_vector(LEFT * 0.5,
                                                 angle_deg * DEGREES),
                color=color, stroke_width=5,
            )
            lab = VGroup(
                Tex(label, font_size=24, color=color),
                MathTex(rf"{angle_deg}^\circ", font_size=20, color=color),
            ).arrange(DOWN, buff=0.05).next_to(box, DOWN, buff=0.12)
            return VGroup(box, axis, lab).move_to([x, 1.3, 0])

        p_a = polarizer(-4, 0, "A", BLUE)
        p_b = polarizer(0, 22.5, "B", PURPLE)
        p_c = polarizer(4, 45, "C", GREEN)
        self.play(LaggedStart(FadeIn(p_a), FadeIn(p_b), FadeIn(p_c),
                              lag_ratio=0.2))

        def disagree_qm(dtheta_deg):
            return np.sin(np.deg2rad(dtheta_deg)) ** 2

        p_ab = disagree_qm(22.5)
        p_bc = disagree_qm(22.5)
        p_ac = disagree_qm(45.0)

        bell_rows = VGroup(
            MathTex(r"P(A\neq B) = \sin^2(22.5^\circ) \approx 0.146",
                    font_size=28, color=BLUE),
            MathTex(r"P(B\neq C) = \sin^2(22.5^\circ) \approx 0.146",
                    font_size=28, color=PURPLE),
            MathTex(r"P(A\neq C) = \sin^2(45^\circ) = 0.500",
                    font_size=30, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        bell_rows.to_edge(LEFT, buff=0.5).shift(DOWN * 0.5)
        self.play(FadeIn(bell_rows[0]))
        self.play(FadeIn(bell_rows[1]))
        self.play(FadeIn(bell_rows[2]))

        inequality = VGroup(
            MathTex(r"\text{LHV bound: }\quad P(A\neq C) \le P(A\neq B) + P(B\neq C)",
                    font_size=28),
            MathTex(
                rf"{p_ac:.3f}\ \not\le\ {p_ab:.3f} + {p_bc:.3f} = {p_ab+p_bc:.3f}",
                font_size=32, color=RED,
            ),
            MathTex(r"\Rightarrow\ \text{no local hidden variables}",
                    font_size=28, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        inequality.to_edge(RIGHT, buff=0.4).shift(DOWN * 0.5)
        self.play(FadeIn(inequality[0]))
        self.wait(0.3)
        self.play(Write(inequality[1]))
        box = SurroundingRectangle(inequality[1], color=RED,
                                   buff=0.15, stroke_width=3)
        self.play(Create(box))
        self.play(FadeIn(inequality[2]))
        self.wait(1.5)
