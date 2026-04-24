from manim import *
import numpy as np


class QuaternionMultiplicationExample(Scene):
    """
    Quaternion multiplication (from _2018/quaternions): q = (w, x, y, z).
    Non-commutative: i·j = k but j·i = -k. Visualize the cyclic i→j→k
    multiplication rule on 4 basis quaternions.

    SINGLE_FOCUS:
      3 unit basis vectors i, j, k + 1 scalar 1 shown as 4 colored
      arrows; ValueTracker step_tr steps through products i·j = k,
      j·k = i, k·i = j and the reverse products (negatives).
    """

    def construct(self):
        title = Tex(r"Quaternions: $ij = k,\ ji = -k$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Triangle-diagram with 3 basis quats
        center = np.array([-2.5, -0.3, 0])
        r = 2.2
        i_pos = center + r * np.array([np.cos(PI / 2), np.sin(PI / 2), 0])
        j_pos = center + r * np.array([np.cos(PI + PI / 6),
                                           np.sin(PI + PI / 6), 0])
        k_pos = center + r * np.array([np.cos(-PI / 6),
                                           np.sin(-PI / 6), 0])

        i_dot = Dot(i_pos, color=RED, radius=0.14)
        j_dot = Dot(j_pos, color=GREEN, radius=0.14)
        k_dot = Dot(k_pos, color=BLUE, radius=0.14)

        i_lbl = MathTex(r"i", color=RED, font_size=36).next_to(i_dot, UP, buff=0.15)
        j_lbl = MathTex(r"j", color=GREEN, font_size=36).next_to(j_dot, DL, buff=0.15)
        k_lbl = MathTex(r"k", color=BLUE, font_size=36).next_to(k_dot, DR, buff=0.15)

        self.play(FadeIn(i_dot, j_dot, k_dot),
                   Write(i_lbl), Write(j_lbl), Write(k_lbl))

        step_tr = ValueTracker(0)
        products = [
            (r"ij", i_pos, j_pos, k_pos, r"ij = k", GREEN_A, False),
            (r"jk", j_pos, k_pos, i_pos, r"jk = i", YELLOW, False),
            (r"ki", k_pos, i_pos, j_pos, r"ki = j", ORANGE, False),
            (r"ji", j_pos, i_pos, k_pos, r"ji = -k", RED_A, True),
            (r"kj", k_pos, j_pos, i_pos, r"kj = -i", MAROON, True),
            (r"ik", i_pos, k_pos, j_pos, r"ik = -j", PINK, True),
        ]

        def active_arrow():
            s = int(round(step_tr.get_value())) % len(products)
            (_, start, mid, end, _, col, neg) = products[s]
            # Draw arrow start→mid (BLUE) and mid→end (YELLOW)
            grp = VGroup()
            grp.add(Arrow(start, mid, color=col, buff=0.25,
                            stroke_width=5,
                            max_tip_length_to_length_ratio=0.12))
            final_end = end
            if neg:
                # Point arrow AWAY from target (to signify negative)
                direction = (final_end - mid) / np.linalg.norm(final_end - mid)
                final_end = mid - 0.7 * direction * np.linalg.norm(final_end - mid)
            grp.add(Arrow(mid, final_end, color=col, buff=0.15,
                            stroke_width=5,
                            max_tip_length_to_length_ratio=0.12))
            return grp

        def eq_label():
            s = int(round(step_tr.get_value())) % len(products)
            return MathTex(products[s][4], color=YELLOW,
                             font_size=32).to_edge(RIGHT, buff=0.5).shift(UP * 1.5)

        self.add(always_redraw(active_arrow), always_redraw(eq_label))

        # Laws list on the right
        laws = VGroup(
            Tex(r"$i^2 = j^2 = k^2 = -1$", color=WHITE, font_size=22),
            Tex(r"$ijk = -1$", color=WHITE, font_size=22),
            Tex(r"cyclic: $ij = k, jk = i, ki = j$",
                 color=GREEN, font_size=22),
            Tex(r"reversed: $ji = -k$, etc.",
                 color=RED, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.5, -1.5, 0])
        self.play(Write(laws))

        for target in range(1, len(products) + 1):
            self.play(step_tr.animate.set_value(target),
                       run_time=1.1, rate_func=smooth)
            self.wait(0.6)
        self.wait(0.5)
