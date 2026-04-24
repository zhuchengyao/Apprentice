from manim import *
import numpy as np


class BasketballProjectileExample(Scene):
    """
    Basketball projectile (from _2023/standup_maths/basketball): the
    minimum launch speed v_min for a given hoop distance d and
    height difference h comes from the envelope of parabolic
    trajectories.

    SINGLE_FOCUS:
      Launch point at (0, 2), hoop at (5, 3). ValueTracker θ_tr
      sweeps launch angle 20° → 80°. For each angle, initial speed
      is chosen so trajectory reaches the hoop; always_redraw
      trajectory parabola + hoop indicator. Speed is plotted
      inline and the minimum is marked.
    """

    def construct(self):
        title = Tex(r"Basketball projectile: launch angle $\to$ required speed",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Scene geometry
        launch = np.array([-4, -1, 0])
        hoop_scene = np.array([2.5, 0.5, 0])

        g_val = 9.81
        d = 5.0       # horizontal distance (world meters)
        h = 1.0       # vertical height diff

        # Given angle θ, required speed:
        #   h = d tan θ − g d²/(2 v² cos²θ)
        #   v² = g d² / (2 cos²θ (d tan θ − h))
        def speed_for(theta):
            num = g_val * d ** 2
            den = 2 * (np.cos(theta) ** 2) * (d * np.tan(theta) - h)
            if den <= 0:
                return 1e6
            return np.sqrt(num / den)

        # Map world (x, y) → scene
        def w2s(x, y):
            sx = launch[0] + x * 1.2
            sy = launch[1] + y * 1.0
            return np.array([sx, sy, 0])

        # Ground
        ground = Line(launch + LEFT * 0.5,
                        launch + RIGHT * 12,
                        color=GREY_B, stroke_width=2)
        # Launch dot + hoop
        launch_dot = Dot(launch, color=BLUE, radius=0.12)
        launch_lbl = Tex("launcher", color=BLUE,
                          font_size=18).next_to(launch_dot, DL, buff=0.05)

        hoop_x, hoop_y = d, h
        hoop_pos = w2s(hoop_x, hoop_y)
        hoop = Circle(radius=0.15, color=ORANGE, stroke_width=3,
                        fill_opacity=0).move_to(hoop_pos)
        hoop_lbl = Tex("hoop", color=ORANGE, font_size=18).next_to(
            hoop, UP, buff=0.1)

        self.play(Create(ground), FadeIn(launch_dot), Write(launch_lbl),
                   Create(hoop), Write(hoop_lbl))

        theta_tr = ValueTracker(30 * DEGREES)

        def trajectory():
            theta = theta_tr.get_value()
            v = speed_for(theta)
            if v > 60:
                return VMobject()
            pts = []
            t_final = d / (v * np.cos(theta))
            for t in np.linspace(0, t_final, 60):
                x = v * np.cos(theta) * t
                y = v * np.sin(theta) * t - 0.5 * g_val * t * t
                pts.append(w2s(x, y))
            m = VMobject(color=YELLOW, stroke_width=3)
            m.set_points_as_corners(pts)
            return m

        self.add(always_redraw(trajectory))

        def ball():
            theta = theta_tr.get_value()
            v = speed_for(theta)
            if v > 60:
                return Dot(launch, color=GREY_B, radius=0.08)
            # halfway-through point
            t_final = d / (v * np.cos(theta))
            t = t_final * 0.5
            x = v * np.cos(theta) * t
            y = v * np.sin(theta) * t - 0.5 * g_val * t * t
            return Dot(w2s(x, y), color=RED, radius=0.12)

        self.add(always_redraw(ball))

        # Speed vs angle plot on right
        ax_v = Axes(x_range=[20, 80, 15], y_range=[0, 20, 5],
                     x_length=4.5, y_length=3, tips=False,
                     axis_config={"font_size": 14, "include_numbers": True}
                     ).move_to([3.5, 1.2, 0])
        theta_deg_lbl = MathTex(r"\theta^\circ", font_size=18).next_to(ax_v, DOWN, buff=0.08)
        v_lbl = MathTex(r"v", font_size=18).next_to(ax_v, LEFT, buff=0.08)
        v_curve = ax_v.plot(lambda deg: min(speed_for(deg * DEGREES), 20),
                              x_range=[20, 80, 0.5], color=BLUE, stroke_width=2.5)
        self.play(Create(ax_v), Write(theta_deg_lbl), Write(v_lbl),
                   Create(v_curve))

        def v_rider():
            theta = theta_tr.get_value()
            deg = np.degrees(theta)
            v = min(speed_for(theta), 20)
            return Dot(ax_v.c2p(deg, v), color=YELLOW, radius=0.09)

        self.add(always_redraw(v_rider))

        def info():
            theta = theta_tr.get_value()
            v = speed_for(theta)
            return VGroup(
                MathTex(rf"\theta = {np.degrees(theta):.1f}^\circ",
                         color=YELLOW, font_size=22),
                MathTex(rf"v = {min(v, 99):.2f}\,\text{{m/s}}",
                         color=BLUE, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.5, -1.8, 0])

        self.add(always_redraw(info))

        # Tour angles — min v near 50°
        for deg in [25, 40, 50, 55, 70]:
            self.play(theta_tr.animate.set_value(deg * DEGREES),
                       run_time=1.5, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.4)
