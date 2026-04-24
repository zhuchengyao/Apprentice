from manim import *
import numpy as np


class PendulumForceDecomposition(Scene):
    """Derive the pendulum equation of motion from gravity.  The gravity
    vector g-hat on the bob decomposes into a radial component (along the
    rod, absorbed by tension) and a tangential component -g*sin(theta)
    that produces acceleration.  So L*theta'' = -g*sin(theta), or
    theta'' = -(g/L)*sin(theta)."""

    def construct(self):
        title = Tex(
            r"Decomposing gravity gives $\ddot\theta = -\tfrac{g}{L}\sin\theta$",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        pivot = np.array([-2.5, 2.3, 0])
        pivot_dot = Dot(pivot, radius=0.08, color=WHITE)
        self.add(pivot_dot)

        L = 3.0
        theta = 0.75
        bob_pos = pivot + L * np.array([np.sin(theta), -np.cos(theta), 0])
        rod = Line(pivot, bob_pos, color=GREY_B, stroke_width=3)
        bob = Dot(bob_pos, radius=0.22, color=BLUE).set_z_index(4)
        self.play(Create(rod), FadeIn(bob))

        theta_arc = Arc(
            radius=0.6, angle=-theta, start_angle=-PI / 2,
            color=YELLOW, stroke_width=3,
        ).move_arc_center_to(pivot)
        theta_lab = MathTex(r"\theta", font_size=30, color=YELLOW).move_to(
            pivot + 0.9 * np.array([np.sin(theta / 2),
                                    -np.cos(theta / 2), 0])
        )
        self.play(Create(theta_arc), Write(theta_lab))

        g_end = bob_pos + np.array([0, -1.5, 0])
        g_vec = Arrow(bob_pos, g_end, buff=0, color=WHITE,
                      stroke_width=4,
                      max_tip_length_to_length_ratio=0.12)
        g_lab = MathTex(r"\vec g", font_size=28,
                        color=WHITE).next_to(g_vec, RIGHT, buff=0.1)
        self.play(GrowArrow(g_vec), Write(g_lab))

        radial_dir = (bob_pos - pivot) / np.linalg.norm(bob_pos - pivot)
        tangent_dir = np.array([-radial_dir[1], radial_dir[0], 0])
        g_val = 1.5
        radial_comp = g_val * np.cos(theta)
        tangent_comp = g_val * np.sin(theta)

        radial_end = bob_pos + radial_dir * radial_comp
        tangent_end = bob_pos - tangent_dir * tangent_comp

        radial_vec = Arrow(bob_pos, radial_end, buff=0, color=RED,
                           stroke_width=3,
                           max_tip_length_to_length_ratio=0.12)
        tangent_vec = Arrow(bob_pos, tangent_end, buff=0, color=GREEN,
                            stroke_width=4,
                            max_tip_length_to_length_ratio=0.12)
        rad_lab = MathTex(r"g\cos\theta", font_size=24,
                          color=RED).next_to(radial_vec, buff=0.05)
        tan_lab = MathTex(r"g\sin\theta", font_size=24,
                          color=GREEN).next_to(tangent_vec, buff=0.05)
        self.play(GrowArrow(radial_vec), Write(rad_lab))
        self.play(GrowArrow(tangent_vec), Write(tan_lab))

        dashed = DashedLine(radial_end, g_end, color=GREY_B,
                            stroke_width=1.5)
        dashed2 = DashedLine(tangent_end, g_end, color=GREY_B,
                             stroke_width=1.5)
        self.play(Create(dashed), Create(dashed2))

        derivation = VGroup(
            Tex(r"radial $\leftarrow$ absorbed by rod tension",
                font_size=22, color=RED),
            Tex(r"tangential $\to$ drives motion",
                font_size=22, color=GREEN),
            MathTex(r"m L \ddot\theta = -m g\sin\theta",
                    font_size=26),
            MathTex(r"\ddot\theta = -\tfrac{g}{L}\sin\theta",
                    font_size=28, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        derivation.to_edge(RIGHT, buff=0.4).shift(DOWN * 0.4)
        self.play(FadeIn(derivation[0]))
        self.play(FadeIn(derivation[1]))
        self.play(Write(derivation[2]))
        self.play(Write(derivation[3]))
        box = SurroundingRectangle(derivation[3], color=YELLOW,
                                   buff=0.15, stroke_width=3)
        self.play(Create(box))
        self.wait(1.3)
