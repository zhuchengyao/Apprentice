from manim import *
import numpy as np


class CouponCollectorExample(Scene):
    """
    Coupon collector: expected number of draws to collect all n
    distinct coupons = n·H_n ≈ n·ln(n). Simulate with n = 10.

    SINGLE_FOCUS:
      10 coupon slots; ValueTracker t_tr advances 1 draw at a time;
      always_redraw fills slots as they're first-seen; running count
      tracked vs expected n·H_n.
    """

    def construct(self):
        title = Tex(r"Coupon collector: $E[\text{draws}] = n H_n \approx n \ln n$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        n = 10
        rng = np.random.default_rng(19)
        # Simulate until all n are collected, keep a long draw list
        draws = []
        collected = set()
        H_n = sum(1 / k for k in range(1, n + 1))
        expected = n * H_n  # ≈ 29.3
        while len(collected) < n or len(draws) < 50:
            d = int(rng.integers(0, n))
            draws.append(d)
            collected.add(d)
            if len(draws) > 100:
                break

        # Slots
        slot_y = 1.5
        slot_w = 0.55
        x_start = -2.7
        slot_boxes = VGroup()
        for i in range(n):
            b = Rectangle(width=slot_w * 0.9, height=slot_w * 0.9,
                            color=WHITE, fill_opacity=0.1,
                            stroke_width=1.5)
            b.move_to([x_start + i * slot_w, slot_y, 0])
            slot_boxes.add(b)
            lbl = MathTex(rf"{i}", font_size=18, color=GREY_B
                            ).next_to(b, DOWN, buff=0.1)
            slot_boxes.add(lbl)
        self.play(FadeIn(slot_boxes))

        t_tr = ValueTracker(0)

        def filled_slots():
            t = int(round(t_tr.get_value()))
            t = max(0, min(t, len(draws)))
            seen = set(draws[:t])
            grp = VGroup()
            for i in range(n):
                if i in seen:
                    sq = Square(side_length=slot_w * 0.85,
                                  color=YELLOW, fill_opacity=0.75,
                                  stroke_width=1.5)
                    sq.move_to([x_start + i * slot_w, slot_y, 0])
                    grp.add(sq)
                    lbl_v = MathTex(rf"\checkmark",
                                      font_size=22, color=BLACK
                                      ).move_to(sq.get_center())
                    grp.add(lbl_v)
            return grp

        def current_draw():
            t = int(round(t_tr.get_value()))
            if t <= 0:
                return VGroup()
            d = draws[t - 1]
            return Circle(radius=slot_w * 0.55,
                            color=RED, stroke_width=3,
                            fill_opacity=0).move_to(
                [x_start + d * slot_w, slot_y, 0])

        self.add(always_redraw(filled_slots),
                  always_redraw(current_draw))

        # Progress bar: slots collected / n
        ax = Axes(x_range=[0, 60, 10], y_range=[0, n + 1, 2],
                   x_length=8, y_length=3, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([0, -1.7, 0])
        xl = Tex("draws", font_size=16).next_to(ax, DOWN, buff=0.1)
        yl = Tex("collected", font_size=16).next_to(ax, LEFT, buff=0.1)
        self.play(Create(ax), Write(xl), Write(yl))

        # Expected marker
        exp_line = DashedLine(ax.c2p(expected, 0),
                                ax.c2p(expected, n + 1),
                                color=GREEN, stroke_width=2)
        exp_lbl = MathTex(rf"E = {expected:.1f}",
                             color=GREEN, font_size=18
                             ).next_to(exp_line.get_top(), UP, buff=0.1)
        self.play(Create(exp_line), Write(exp_lbl))

        def progress_curve():
            t = int(round(t_tr.get_value()))
            t = max(1, min(t, len(draws)))
            pts = []
            seen = set()
            for k in range(t):
                seen.add(draws[k])
                pts.append(ax.c2p(k + 1, len(seen)))
            m = VMobject(color=YELLOW, stroke_width=3)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        self.add(always_redraw(progress_curve))

        def info():
            t = int(round(t_tr.get_value()))
            t = max(0, min(t, len(draws)))
            seen = set(draws[:t])
            return VGroup(
                MathTex(rf"\text{{draws}} = {t}", color=WHITE, font_size=20),
                MathTex(rf"\text{{collected}} = {len(seen)}/{n}",
                         color=YELLOW, font_size=20),
                MathTex(rf"E = n H_n = {expected:.2f}",
                         color=GREEN, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_corner(UR, buff=0.4)

        self.add(always_redraw(info))

        self.play(t_tr.animate.set_value(len(draws)),
                   run_time=8, rate_func=linear)
        self.wait(0.5)
