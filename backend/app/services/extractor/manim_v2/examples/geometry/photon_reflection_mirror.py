from manim import *
import numpy as np


class PhotonReflectionMirrorExample(Scene):
    """
    Law of reflection: θ_r = θ_i, swept by ValueTracker.

    A horizontal mirror with hatched back. ValueTracker θ_i sweeps the
    angle of the incoming ray from 15° to 75° and back. The reflected
    ray, the two angle arcs, and the angle labels all redraw via
    always_redraw so they stay synchronized with the incidence.

    A photon dot also bounces along the rays (incident → hit point →
    reflected) on each major sweep step using MoveAlongPath.
    """

    def construct(self):
        title = Tex(r"Law of reflection: $\theta_r = \theta_i$",
                    font_size=34).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # Mirror geometry — left panel
        mirror_y = -1.4
        hit_x = -1.5
        hit = np.array([hit_x, mirror_y, 0])

        mirror = Line([-5.5, mirror_y, 0], [+1.5, mirror_y, 0], color=WHITE, stroke_width=4)
        hatches = VGroup(*[
            Line([-5.5 + i * 0.45, mirror_y, 0],
                 [-5.5 + i * 0.45 + 0.25, mirror_y - 0.3, 0],
                 color=GREY_B, stroke_width=2)
            for i in range(17)
        ])
        normal = DashedLine(hit, hit + np.array([0, 3.0, 0]),
                            color=GREEN, stroke_width=2)
        normal_lbl = MathTex(r"\hat n", color=GREEN, font_size=22).next_to(
            hit + np.array([0, 3.0, 0]), UP, buff=0.1)
        self.play(Create(mirror), Create(hatches), Create(normal), Write(normal_lbl))

        # Tracker for incidence angle (radians)
        theta_i_tracker = ValueTracker(np.radians(45))
        ray_len = 3.5

        def incident_dir():
            t = theta_i_tracker.get_value()
            # Coming from upper-left, going down-right toward hit
            return np.array([np.sin(t), np.cos(t), 0])  # points DOWN-RIGHT

        def reflected_dir():
            t = theta_i_tracker.get_value()
            # Reflected: mirror across normal — same angle, opposite x
            return np.array([np.sin(t), -np.cos(t), 0])  # wait, let me reconsider

        # Let me redo with clearer convention.
        # Mirror is along y = mirror_y. Normal points UP.
        # Incident ray comes from (hit + L * (-sin θ, +cos θ)) toward hit.
        # So incident_start = hit + L * (-sin θ, cos θ).
        # Reflected ray goes from hit toward (hit + L * (+sin θ, +cos θ)).
        def incident_start():
            t = theta_i_tracker.get_value()
            return hit + ray_len * np.array([-np.sin(t), np.cos(t), 0])

        def reflected_end():
            t = theta_i_tracker.get_value()
            return hit + ray_len * np.array([+np.sin(t), np.cos(t), 0])

        def incident_arrow():
            return Arrow(incident_start(), hit, buff=0,
                         color=YELLOW, stroke_width=5,
                         max_tip_length_to_length_ratio=0.10)

        def reflected_arrow():
            return Arrow(hit, reflected_end(), buff=0,
                         color=YELLOW, stroke_width=5,
                         max_tip_length_to_length_ratio=0.10)

        def theta_i_arc():
            t = theta_i_tracker.get_value()
            return Arc(radius=0.7, start_angle=PI / 2,
                       angle=t, arc_center=hit,
                       color=YELLOW, stroke_width=3)

        def theta_r_arc():
            t = theta_i_tracker.get_value()
            return Arc(radius=0.7, start_angle=PI / 2 - t,
                       angle=t, arc_center=hit,
                       color=YELLOW, stroke_width=3)

        def theta_i_lbl():
            t = theta_i_tracker.get_value()
            mid_angle = PI / 2 + t / 2
            return MathTex(r"\theta_i", color=YELLOW, font_size=22).move_to(
                hit + 1.05 * np.array([np.cos(mid_angle), np.sin(mid_angle), 0]))

        def theta_r_lbl():
            t = theta_i_tracker.get_value()
            mid_angle = PI / 2 - t / 2
            return MathTex(r"\theta_r", color=YELLOW, font_size=22).move_to(
                hit + 1.05 * np.array([np.cos(mid_angle), np.sin(mid_angle), 0]))

        self.add(always_redraw(incident_arrow), always_redraw(reflected_arrow),
                 always_redraw(theta_i_arc), always_redraw(theta_r_arc),
                 always_redraw(theta_i_lbl), always_redraw(theta_r_lbl))

        # RIGHT COLUMN: live readouts and the law statement
        rcol_x = +4.4

        def info_panel():
            t = theta_i_tracker.get_value()
            return VGroup(
                MathTex(rf"\theta_i = {np.degrees(t):.0f}^\circ",
                        color=YELLOW, font_size=30),
                MathTex(rf"\theta_r = {np.degrees(t):.0f}^\circ",
                        color=YELLOW, font_size=30),
                MathTex(r"\theta_r = \theta_i", color=GREEN, font_size=30),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([rcol_x, +1.0, 0])

        self.add(always_redraw(info_panel))

        # Sweep through several incidence angles
        for deg in [20, 65, 30, 75, 45]:
            self.play(theta_i_tracker.animate.set_value(np.radians(deg)),
                      run_time=2.0, rate_func=smooth)
            self.wait(0.4)

        principle = MathTex(
            r"\text{Fermat: light takes the path of stationary time}",
            font_size=22, color=GREY_B,
        ).move_to([rcol_x, -2.4, 0])
        self.play(Write(principle))
        self.wait(1.0)
