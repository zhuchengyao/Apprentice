from manim import *
import numpy as np


class GenusSurfaceGluingExample(Scene):
    """
    Classification of compact orientable surfaces: every one is a
    connect sum of g tori = sphere with g handles. Visualize by
    polygon-gluing representation: 4g-gon with edges
    a_1 b_1 a_1^(-1) b_1^(-1) ... a_g b_g a_g^(-1) b_g^(-1) identified.

    SINGLE_FOCUS: show 4g-gon for g=1 (torus: 4-gon) and g=2 (genus-2: 8-gon).
    ValueTracker g_tr toggles; always_redraw polygon with edge labels.
    """

    def construct(self):
        title = Tex(r"Genus $g$ surface $=$ identify edges of $4g$-gon",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        g_tr = ValueTracker(1.0)

        def g_now():
            return max(1, min(3, int(round(g_tr.get_value()))))

        def polygon():
            g = g_now()
            sides = 4 * g
            R = 2.5
            verts = [R * np.array([np.cos(2 * PI * k / sides + PI / 2),
                                     np.sin(2 * PI * k / sides + PI / 2),
                                     0]) for k in range(sides)]
            # Color edges: pattern a_i (RED), b_i (GREEN), a_i^(-1) (RED dashed), b_i^(-1) (GREEN dashed)
            # For each block of 4: [a_i, b_i, a_i^(-1), b_i^(-1)]
            lines = VGroup()
            lbls = VGroup()
            for k in range(sides):
                p1 = verts[k]
                p2 = verts[(k + 1) % sides]
                pos_in_block = k % 4
                block_idx = k // 4 + 1
                if pos_in_block == 0:  # a_i
                    col = RED
                    label = rf"$a_{{{block_idx}}}$"
                elif pos_in_block == 1:  # b_i
                    col = GREEN
                    label = rf"$b_{{{block_idx}}}$"
                elif pos_in_block == 2:  # a_i^-1
                    col = RED
                    label = rf"$a_{{{block_idx}}}^{{-1}}$"
                else:  # b_i^-1
                    col = GREEN
                    label = rf"$b_{{{block_idx}}}^{{-1}}$"

                # Arrow direction: a_i and b_i go "forward", inverses go "backward"
                if pos_in_block < 2:
                    arrow_start, arrow_end = p1, p2
                else:
                    arrow_start, arrow_end = p2, p1
                arrow = Arrow(arrow_start, arrow_end, color=col,
                                buff=0, stroke_width=3,
                                max_tip_length_to_length_ratio=0.12)
                lines.add(arrow)
                mid = (p1 + p2) / 2
                outward = mid / np.linalg.norm(mid)
                lbls.add(Tex(label, color=col, font_size=22).move_to(
                    mid + 0.35 * outward))
            return VGroup(lines, lbls)

        self.add(always_redraw(polygon))

        # Euler formula
        def euler_str():
            g = g_now()
            return rf"$\chi = 2-2g = 2-2\cdot {g} = {2 - 2 * g}$"

        info = VGroup(
            VGroup(Tex(r"genus $g=$", font_size=24),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=24).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"sides $=4g=$", font_size=22),
                   DecimalNumber(4, num_decimal_places=0,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            Tex(r"word: $a_1 b_1 a_1^{-1} b_1^{-1}\cdots$",
                font_size=22),
            Tex(euler_str(), color=GREEN, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(DR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(g_now()))
        info[1][1].add_updater(lambda m: m.set_value(4 * g_now()))

        def update_euler(mob, dt):
            new = Tex(euler_str(), color=GREEN, font_size=22).move_to(info[3])
            info[3].become(new)
            return info[3]
        info[3].add_updater(update_euler)
        self.add(info)

        for g in [2, 3, 1]:
            self.play(g_tr.animate.set_value(float(g)),
                      run_time=2.0, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.5)
