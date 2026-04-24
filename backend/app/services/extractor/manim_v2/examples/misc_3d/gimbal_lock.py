from manim import *
import numpy as np


class GimbalLockExample(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-50 * DEGREES)

        axes = ThreeDAxes(x_range=[-2, 2, 1], y_range=[-2, 2, 1], z_range=[-2, 2, 1])
        self.add(axes)

        outer = Circle(radius=1.8, color=RED, stroke_width=4)
        middle = Circle(radius=1.45, color=GREEN, stroke_width=4).rotate(PI / 2, axis=RIGHT)
        inner = Circle(radius=1.1, color=BLUE, stroke_width=4).rotate(PI / 2, axis=UP)

        rings = VGroup(outer, middle, inner)
        self.play(Create(outer), Create(middle), Create(inner))

        yaw = ValueTracker(0)
        pitch = ValueTracker(0)
        roll = ValueTracker(0)

        def update_ring(ring, axis, tracker_fn):
            def updater(r):
                r.become(ring.copy().rotate(tracker_fn(), axis=axis, about_point=ORIGIN))
            return updater

        # Reset copies for updating
        outer_template = outer.copy()
        middle_template = middle.copy()
        inner_template = inner.copy()

        def refresh(dummy=None):
            y = yaw.get_value()
            p = pitch.get_value()
            r = roll.get_value()
            new_outer = outer_template.copy().rotate(y, axis=OUT, about_point=ORIGIN)
            new_middle = middle_template.copy().rotate(y, axis=OUT, about_point=ORIGIN).rotate(p, axis=RIGHT, about_point=ORIGIN)
            new_inner = inner_template.copy().rotate(y, axis=OUT, about_point=ORIGIN).rotate(p, axis=RIGHT, about_point=ORIGIN).rotate(r, axis=UP, about_point=ORIGIN)
            outer.become(new_outer)
            middle.become(new_middle)
            inner.become(new_inner)

        dummy = Mobject()
        dummy.add_updater(refresh)
        self.add(dummy)

        self.play(yaw.animate.set_value(PI / 3), run_time=1.5)
        self.play(pitch.animate.set_value(PI / 2), run_time=1.5)  # align inner with outer
        self.play(roll.animate.set_value(PI / 2), run_time=1.5)
        dummy.clear_updaters()

        caption = Text("Pitch = 90°: roll and yaw axes coincide → gimbal lock",
                       font_size=22, color=YELLOW)
        self.add_fixed_in_frame_mobjects(caption)
        caption.to_edge(DOWN)
        self.play(Write(caption))
        self.wait(0.6)
