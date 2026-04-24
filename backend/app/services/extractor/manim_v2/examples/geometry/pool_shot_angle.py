from manim import *
import numpy as np


class PoolShotAngleExample(Scene):
    """
    Pool-shot geometry (from _2023/standup_maths/pool): to sink the
    ball off one cushion, aim for the mirror image of the pocket
    reflected through the cushion. Straight line from cue ball to
    mirrored pocket = correct angle.

    SINGLE_FOCUS:
      Rectangular table with cue ball (BLUE), target pocket (YELLOW)
      at top-right corner. Bottom cushion is the reflector; mirrored
      pocket below the cushion (dashed). Straight line from cue to
      mirrored pocket intersects cushion at aim point. ValueTracker
      t_tr advances the ball along the path, bouncing at the cushion.
    """

    def construct(self):
        title = Tex(r"Pool: aim at the mirrored pocket",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Table
        table = Rectangle(width=10, height=5, color=GREEN,
                            fill_opacity=0.25, stroke_width=4
                            ).move_to([0, -0.3, 0])
        self.play(Create(table))

        # Cue ball
        cue = np.array([-3.5, 1.3, 0])  # upper-left area
        # Target pocket (top-right corner)
        target = np.array([5.0, 2.2, 0])
        # Bottom cushion at y = -2.8
        cushion_y = -2.8

        # Mirrored target (reflect target across cushion)
        mirror_target = np.array([target[0], 2 * cushion_y - target[1], 0])

        # Aim point on cushion (from cue to mirror_target, x at y=cushion_y)
        # Straight line: cue + s (mirror_target - cue); find s where y = cushion_y
        s_hit = (cushion_y - cue[1]) / (mirror_target[1] - cue[1])
        aim = cue + s_hit * (mirror_target - cue)

        # Draw cue, target, mirror_target
        cue_dot = Dot(cue, color=BLUE, radius=0.13)
        target_dot = Dot(target, color=YELLOW, radius=0.18)
        target_lbl = Tex("pocket", color=YELLOW, font_size=20
                          ).next_to(target_dot, UR, buff=0.05)

        mirror_dot = Dot(mirror_target, color=YELLOW_E, radius=0.13,
                           fill_opacity=0.4)
        mirror_lbl = Tex("mirrored pocket", color=YELLOW_E, font_size=18
                          ).next_to(mirror_dot, DL, buff=0.1)

        cushion_line = DashedLine([-6, cushion_y, 0], [6, cushion_y, 0],
                                    color=GREY_B, stroke_width=1.5)

        # Mirror-straight line (dashed)
        straight = DashedLine(cue, mirror_target,
                                color=ORANGE, stroke_width=2)

        self.play(FadeIn(cue_dot), FadeIn(target_dot),
                   Write(target_lbl), FadeIn(mirror_dot),
                   Write(mirror_lbl), Create(cushion_line))
        self.play(Create(straight))

        # Ball movement via ValueTracker
        t_tr = ValueTracker(0.0)

        def ball_pos(t):
            # Path: cue → aim → target, parameterized 0→1
            if t < 0.5:
                s = t / 0.5
                return cue + s * (aim - cue)
            else:
                s = (t - 0.5) / 0.5
                return aim + s * (target - aim)

        def ball():
            return Dot(ball_pos(t_tr.get_value()),
                        color=BLUE, radius=0.11)

        def path_trail():
            t = t_tr.get_value()
            pts = []
            for ti in np.linspace(0, t, 60):
                pts.append(ball_pos(ti))
            if len(pts) < 2:
                return VMobject()
            m = VMobject(color=BLUE, stroke_width=3)
            m.set_points_as_corners(pts)
            return m

        self.add(always_redraw(path_trail), always_redraw(ball))

        # Aim point marker
        aim_dot = Dot(aim, color=RED, radius=0.1)
        aim_lbl = Tex("aim", color=RED, font_size=18
                       ).next_to(aim_dot, DOWN, buff=0.1)
        self.play(FadeIn(aim_dot), Write(aim_lbl))

        info = VGroup(
            Tex(r"ORANGE: straight line cue $\to$ mirrored pocket",
                 color=ORANGE, font_size=18),
            Tex(r"BLUE: actual path of ball",
                 color=BLUE, font_size=18),
            Tex(r"cushion hit gives angle of incidence = reflection",
                 color=WHITE, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15
                    ).to_edge(DOWN, buff=0.2)
        self.play(Write(info))

        self.play(t_tr.animate.set_value(1.0),
                   run_time=4, rate_func=smooth)
        self.wait(0.5)
