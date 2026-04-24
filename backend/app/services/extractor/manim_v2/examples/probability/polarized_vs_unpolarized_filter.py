from manim import *
import numpy as np


class PolarizedVsUnpolarizedFilter(Scene):
    """Two fundamentally different situations, often confused.
    (a) UNpolarized light hits a filter at angle θ — exactly 1/2 passes,
        regardless of θ.
    (b) Polarized light (known axis) hits a filter at angle Δθ from its
        axis — fraction cos²(Δθ) passes.  This is Malus's law.
    Visualize both on one canvas for direct comparison."""

    def construct(self):
        title = Tex(
            r"Unpolarized vs polarized light through a filter",
            font_size=30,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        left_cap = Tex(
            r"Unpolarized $\to$ filter", font_size=26, color=BLUE,
        ).move_to([-3.3, 2.3, 0])
        right_cap = Tex(
            r"Polarized $\to$ filter", font_size=26, color=GREEN,
        ).move_to([3.3, 2.3, 0])
        self.play(Write(left_cap), Write(right_cap))

        def small_filter(pos, angle_deg, color):
            box = Circle(radius=0.55, color=color, stroke_width=3,
                         fill_opacity=0.15).move_to(pos)
            axis = Line(
                box.get_center() + rotate_vector(RIGHT * 0.5,
                                                 angle_deg * DEGREES),
                box.get_center() + rotate_vector(LEFT * 0.5,
                                                 angle_deg * DEGREES),
                color=color, stroke_width=5,
            )
            return VGroup(box, axis)

        unp_arrows = VGroup()
        rng = np.random.default_rng(4)
        origin_l = np.array([-5.2, 0.3, 0])
        for _ in range(9):
            ang = rng.uniform(0, 2 * np.pi)
            vec = rotate_vector(RIGHT * 0.4, ang)
            start = origin_l + np.array([
                0, rng.uniform(-0.6, 0.6), 0,
            ])
            unp_arrows.add(Arrow(
                start - vec * 0.5, start + vec * 0.5,
                buff=0, color=BLUE_B, stroke_width=2.5,
                max_tip_length_to_length_ratio=0.25,
            ))
        self.play(LaggedStart(*[GrowArrow(a) for a in unp_arrows],
                              lag_ratio=0.05))

        filter_l = small_filter([-3.5, 0.3, 0], 45, BLUE)
        self.play(FadeIn(filter_l))

        passed_l = VGroup()
        for _ in range(4):
            start = np.array([-3.0, rng.uniform(-0.3, 0.3) + 0.3, 0])
            vec = rotate_vector(RIGHT * 0.4, 45 * DEGREES)
            passed_l.add(Arrow(
                start - vec * 0.5, start + vec * 0.5,
                buff=0, color=BLUE, stroke_width=3,
                max_tip_length_to_length_ratio=0.25,
            ))
        self.play(LaggedStart(*[GrowArrow(a) for a in passed_l],
                              lag_ratio=0.1))

        left_stat = VGroup(
            MathTex(r"I_{\text{out}} = \tfrac{1}{2} I_0",
                    font_size=30, color=BLUE),
            Tex(r"(same for any filter angle)",
                font_size=20, color=BLUE),
        ).arrange(DOWN, buff=0.15).next_to(filter_l, DOWN, buff=0.3)
        self.play(Write(left_stat))

        pol_angle_deg = 0
        pol_vec = rotate_vector(
            RIGHT * 0.5, pol_angle_deg * DEGREES,
        )
        pol_arrows = VGroup()
        for i in range(6):
            start = np.array([2.0, 0.7 - i * 0.2, 0])
            pol_arrows.add(Arrow(
                start - pol_vec * 0.5, start + pol_vec * 0.5,
                buff=0, color=GREEN_B, stroke_width=3,
                max_tip_length_to_length_ratio=0.2,
            ))
        self.play(LaggedStart(*[GrowArrow(a) for a in pol_arrows],
                              lag_ratio=0.1))

        dtheta_tr = ValueTracker(30.0)

        def get_right_filter():
            ang = dtheta_tr.get_value()
            return small_filter([3.8, 0.3, 0], ang, GREEN)

        def get_right_out():
            ang = dtheta_tr.get_value()
            n = int(round(6 * np.cos(np.deg2rad(ang)) ** 2))
            out = VGroup()
            out_vec = rotate_vector(
                RIGHT * 0.4, ang * DEGREES,
            )
            for i in range(n):
                start = np.array([4.4, 0.6 - i * 0.25, 0])
                out.add(Arrow(
                    start - out_vec * 0.5, start + out_vec * 0.5,
                    buff=0, color=GREEN, stroke_width=3,
                    max_tip_length_to_length_ratio=0.25,
                ))
            return out

        def get_right_stat():
            ang = dtheta_tr.get_value()
            t = MathTex(
                rf"I_{{\text{{out}}}} = \cos^2({ang:.0f}^\circ)\, I_0"
                rf" \approx {np.cos(np.deg2rad(ang))**2:.2f}\, I_0",
                font_size=28, color=GREEN,
            )
            t.move_to([3.8, -1.5, 0])
            return t

        right_filter = always_redraw(get_right_filter)
        right_out = always_redraw(get_right_out)
        right_stat = always_redraw(get_right_stat)
        self.add(right_filter, right_out, right_stat)

        for ang in [0, 30, 60, 45, 90, 15]:
            self.play(dtheta_tr.animate.set_value(ang), run_time=1.2)
            self.wait(0.2)
        self.wait(1.3)
